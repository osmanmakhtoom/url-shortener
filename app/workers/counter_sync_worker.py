import asyncio
import logging

from app.core.db import get_session
from app.services import URLService
from app.services.base import BaseService

logger = logging.getLogger("CounterSyncWorker")

SYNC_INTERVAL = 0.8
MAX_RETRIES = 3
RETRY_DELAY = 5


class CounterSyncWorker(BaseService):
    def __init__(self, interval: float = SYNC_INTERVAL):
        super().__init__(session=None)
        self.interval = interval
        self.running = True
        self.retry_count = 0

    async def start(self) -> None:
        """Start the worker with proper Redis connection initialization."""
        try:
            # Ensure Redis connection is established before starting
            await self.ensure_redis_connection()
            logger.info(f"CounterSyncWorker started. Interval = {self.interval}s")

            while self.running:
                try:
                    await asyncio.sleep(self.interval)
                    await self.flush()
                    self.retry_count = 0  # Reset retry count on success
                except Exception as e:
                    self.retry_count += 1
                    logger.error(f"Worker error (attempt {self.retry_count}): {e}")

                    if self.retry_count >= MAX_RETRIES:
                        logger.error("Max retries exceeded. Stopping worker.")
                        self.running = False
                        break

                    await asyncio.sleep(RETRY_DELAY * self.retry_count)

        except Exception as e:
            logger.error(f"Failed to start CounterSyncWorker: {e}")
            self.running = False

    async def flush(self) -> None:
        """Flush visit counts from Redis to database."""
        try:
            # Ensure Redis connection is active before operations
            await self.ensure_redis_connection()

            keys = await self.redis.keys("visits:*")
            if not keys:
                logger.debug("No visit keys found to sync")
                return

            async with get_session() as session:
                us = URLService(session)
                successful_syncs = 0
                total_count = 0

                for key in keys:
                    try:
                        if not key.startswith("visits:"):
                            continue

                        short_code = key.split("visits:")[1]
                        count_str = await self.redis.get_and_delete(key)
                        count = int(count_str or 0)

                        if count <= 0:
                            continue

                        url = await us.get_by_code(short_code)
                        if not url:
                            logger.warning(f"URL not found for short_code: {short_code}")
                            continue

                        url.visit_count = (url.visit_count or 0) + count
                        session.add(url)
                        await us.commit_or_rollback()
                        successful_syncs += 1
                        total_count += count
                        logger.info(f"Synced {count} visits for {short_code}")

                    except Exception as e:
                        logger.error(f"Error syncing {key}: {e}")
                        await session.rollback()
                        continue  # Continue with other keys

                if successful_syncs > 0:
                    logger.info(
                        f"Sync completed. {successful_syncs}/{len(keys)} keys processed, {total_count} total visits"
                    )
                else:
                    logger.debug("No visits synced in this cycle")

        except Exception as e:
            logger.error(f"Flush error: {e}")
            raise  # Re-raise to trigger retry logic

    async def stop(self) -> None:
        """Graceful shutdown"""
        self.running = False
        if hasattr(self.redis, "close"):
            await self.redis.close()
        logger.info("CounterSyncWorker stopped")
