import asyncio
import json
import logging
from typing import Any, Optional

from app.core.db import get_session
from app.core.queue import rabbitmq_client
from app.models import Visit
from app.schemas.visit_message import VisitMessage
from app.services import URLService

logger = logging.getLogger("VisitWorker")

BATCH_SIZE = 200
BATCH_INTERVAL = 0.8
MAX_BUFFER_SIZE = 1000


class VisitWorker:
    def __init__(self) -> None:
        self.rabbitmq = rabbitmq_client
        self.buffer: list[VisitMessage] = []
        self._flush_task: Optional[Any] = None
        self._consuming = True

    async def start(self) -> None:
        """Start the worker with connection retry logic."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await self.rabbitmq.connect()
                logger.info("VisitWorker started. Listening for visit logs...")

                self._flush_task = asyncio.create_task(self._periodic_flush())
                await self.rabbitmq.consume("visits", self._handle_message)
                break  # Success
            except Exception as e:
                logger.error(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(5 * (attempt + 1))
                else:
                    logger.error("Max connection retries exceeded")
                    raise

    async def _handle_message(self, message_body: bytes) -> None:
        """Handle incoming messages using Pydantic schema."""
        try:
            payload = json.loads(message_body.decode("utf-8"))
            msg = VisitMessage.model_validate(payload)  # ✅ validate & convert

            if len(self.buffer) >= MAX_BUFFER_SIZE:
                logger.warning("Buffer full, forcing flush")
                await self.flush()

            self.buffer.append(msg)
            if len(self.buffer) >= BATCH_SIZE:
                await self.flush()

        except json.JSONDecodeError as e:
            logger.error(
                f"JSON decode error: {e}, raw={message_body.decode('utf-8', errors='replace')}"
            )
        except Exception as e:
            logger.error(
                f"Error handling message: {e}, raw={message_body.decode('utf-8', errors='replace')}"
            )

    async def _periodic_flush(self) -> None:
        """Periodic flush with error handling."""
        while self._consuming:
            try:
                await asyncio.sleep(BATCH_INTERVAL)
                if self.buffer:
                    await self.flush()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Periodic flush error: {e}")

    async def flush(self) -> None:
        """Flush buffer to database with transaction handling."""
        if not self.buffer:
            return

        buffer_copy = self.buffer.copy()
        self.buffer.clear()

        try:
            async with get_session() as session:
                us = URLService(session)
                visits = []
                processed_count, errors = 0, 0

                for msg in buffer_copy:
                    try:
                        if not isinstance(msg, VisitMessage):
                            logger.error(f"Invalid buffer item: {msg}")
                            errors += 1
                            continue

                        url = await us.get_by_code(msg.short_code)
                        if not url:
                            logger.warning(f"URL not found for short_code: {msg.short_code}")
                            errors += 1
                            continue

                        visit = Visit(
                            url_id=url.id,
                            ip_address=msg.ip,
                            visited_at=msg.timestamp,  # already a datetime
                        )
                        visits.append(visit)
                        processed_count += 1

                    except Exception as e:
                        logger.error(f"Error processing visit record: {e}, msg={msg}")
                        errors += 1
                        continue

                if visits:
                    try:
                        session.add_all(visits)
                        await session.commit()
                        logger.info(
                            f"Flushed {len(visits)} visits to DB "
                            f"(processed {processed_count}/{len(buffer_copy)}, errors: {errors})"
                        )
                    except Exception as e:
                        await session.rollback()
                        logger.error(f"Database commit error: {e}")
                        self.buffer.extend(buffer_copy)  # retry
                else:
                    logger.warning(
                        f"No valid visits to flush (errors: {errors}/{len(buffer_copy)})"
                    )

        except Exception as e:
            logger.error(f"Flush error: {e}")
            self.buffer.extend(buffer_copy)

    async def stop(self) -> None:
        """Graceful shutdown."""
        self._consuming = False
        if self._flush_task:
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass

        if self.buffer:
            await self.flush()

        await self.rabbitmq.close()
        logger.info("VisitWorker stopped")
