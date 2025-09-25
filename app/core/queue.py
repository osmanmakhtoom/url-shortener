import asyncio
import logging
import aio_pika
import json
from typing import Optional, Callable, Awaitable, Any
from app.core.config import settings

logger = logging.getLogger("RabbitMQ Client")


class RabbitMQClient:
    def __init__(self, url: str = settings.RABBITMQ_URL):
        self._url = url
        self._connection: Optional[aio_pika.RobustConnection] = None
        self._channel: Optional[aio_pika.abc.AbstractChannel] = None

    async def connect(self, max_retries: int = 3, retry_delay: int = 5):
        """Connect to RabbitMQ with retry logic."""
        for attempt in range(max_retries):
            try:
                if not self._connection:
                    self._connection = await aio_pika.connect_robust(self._url, timeout=10)
                    self._channel = await self._connection.channel()
                    await self._channel.set_qos(prefetch_count=10)
                    logger.info("RabbitMQ connection established")
                return self._channel
            except Exception as e:
                logger.error(f"RabbitMQ connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (attempt + 1))
                else:
                    raise e

    async def close(self):
        """Close RabbitMQ connection."""
        if self._connection:
            await self._connection.close()
            self._connection = None
            self._channel = None

    async def publish(self, queue_name: str, message: dict):
        """Publish message to queue."""
        assert self._channel, "RabbitMQ channel not initialized. Call connect() first."
        body = json.dumps(message, default=str).encode()
        queue = await self._channel.declare_queue(queue_name, durable=True)
        await self._channel.default_exchange.publish(
            aio_pika.Message(body=body),
            routing_key=queue.name,
        )

    async def consume(self, queue_name: str, handler: Callable[[Any], Awaitable[None]]):
        """Consume messages from queue."""
        assert self._channel, "RabbitMQ channel not initialized. Call connect() first."
        queue = await self._channel.declare_queue(queue_name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        # Pass the raw message body to handler
                        await handler(message.body)
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")


rabbitmq_client = RabbitMQClient()
