# app/core/redis.py
import asyncio
from redis import asyncio as aioredis
from typing import Optional, List, Any
import logging
from app.core.config import settings

logger = logging.getLogger("RedisClient")


class RedisClient:
    def __init__(
        self,
        url: str,
        decode_responses: bool = True,
        connect_timeout: int = 5,
        socket_timeout: int = 5,
        retry_attempts: int = 3,
        retry_delay: int = 1,
    ):
        self._url = url
        self._decode_responses = decode_responses
        self._connect_timeout = connect_timeout
        self._socket_timeout = socket_timeout
        self._retry_attempts = retry_attempts
        self._retry_delay = retry_delay
        self._client: Optional[aioredis.Redis] = None
        self._connection_pool: Optional[aioredis.ConnectionPool] = None
        self._is_connected = False

    async def ensure_connection(self):
        """Ensure Redis connection is established."""
        if not self._is_connected or not self._client:
            await self.connect()

    async def connect(self):
        """Initialize Redis connection with retry logic."""
        for attempt in range(self._retry_attempts):
            try:
                if not self._client:
                    self._connection_pool = aioredis.ConnectionPool.from_url(
                        self._url,
                        decode_responses=self._decode_responses,
                        socket_connect_timeout=self._connect_timeout,
                        socket_timeout=self._socket_timeout,
                        max_connections=10,
                        retry_on_timeout=True,
                    )
                    self._client = aioredis.Redis(connection_pool=self._connection_pool)
                    await self._client.ping()  # Test connection
                    self._is_connected = True
                    logger.info("Redis connection established")
                    return self._client
            except Exception as e:
                logger.warning(f"Redis connection attempt {attempt + 1} failed: {e}")
                if attempt < self._retry_attempts - 1:
                    await asyncio.sleep(self._retry_delay * (attempt + 1))
                else:
                    self._is_connected = False
                    raise e

    async def close(self):
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            self._client = None
        if self._connection_pool:
            await self._connection_pool.disconnect()
            self._connection_pool = None
        self._is_connected = False

    async def get_and_delete(self, key: str) -> str:
        """Atomically get and delete a key with error handling."""
        await self.ensure_connection()
        for attempt in range(self._retry_attempts):
            try:
                script = """
                local val = redis.call('GET', KEYS[1])
                if val then
                    redis.call('DEL', KEYS[1])
                    return val
                end
                return 0
                """
                return await self._client.eval(script, 1, key)
            except Exception as e:
                logger.warning(f"get_and_delete attempt {attempt + 1} failed: {e}")
                if attempt < self._retry_attempts - 1:
                    await asyncio.sleep(self._retry_delay)
                else:
                    return "0"

    async def keys(self, pattern: str) -> List[str]:
        """Get keys matching pattern with retry logic."""
        await self.ensure_connection()
        for attempt in range(self._retry_attempts):
            try:
                return await self._client.keys(pattern)
            except Exception as e:
                logger.warning(f"keys attempt {attempt + 1} failed: {e}")
                if attempt < self._retry_attempts - 1:
                    await asyncio.sleep(self._retry_delay)
                else:
                    return []

    # Add ensure_connection to all other methods...
    async def get(self, key: str) -> Optional[str]:
        await self.ensure_connection()
        for attempt in range(self._retry_attempts):
            try:
                return await self._client.get(key)
            except Exception as e:
                logger.warning(f"get attempt {attempt + 1} failed: {e}")
                if attempt < self._retry_attempts - 1:
                    await asyncio.sleep(self._retry_delay)
                else:
                    return None

    async def set(self, key: str, value: str, expire: int = 3600) -> bool:
        await self.ensure_connection()
        for attempt in range(self._retry_attempts):
            try:
                return await self._client.set(key, value, ex=expire)
            except Exception as e:
                logger.warning(f"set attempt {attempt + 1} failed: {e}")
                if attempt < self._retry_attempts - 1:
                    await asyncio.sleep(self._retry_delay)
                else:
                    return False

    async def incr(self, key: str, amount: int = 1) -> int:
        await self.ensure_connection()
        for attempt in range(self._retry_attempts):
            try:
                return await self._client.incrby(key, amount)
            except Exception as e:
                logger.warning(f"incr attempt {attempt + 1} failed: {e}")
                if attempt < self._retry_attempts - 1:
                    await asyncio.sleep(self._retry_delay)
                else:
                    return 0

    async def delete(self, key: str) -> bool:
        """Delete key with retry logic."""
        for attempt in range(self._retry_attempts):
            try:
                result = await self._client.delete(key)
                return result > 0
            except Exception as e:
                logger.warning(f"delete attempt {attempt + 1} failed: {e}")
                if attempt < self._retry_attempts - 1:
                    await asyncio.sleep(self._retry_delay)
                else:
                    return False

    async def ping(self) -> bool:
        """Ping Redis server with retry logic."""
        for attempt in range(self._retry_attempts):
            try:
                return await self._client.ping()
            except Exception as e:
                logger.warning(f"ping attempt {attempt + 1} failed: {e}")
                if attempt < self._retry_attempts - 1:
                    await asyncio.sleep(self._retry_delay)
                else:
                    return False

    async def client(self) -> aioredis.Redis:
        return self._client


redis_client = RedisClient(settings.REDIS_URL)
