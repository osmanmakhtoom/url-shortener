from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import redis_client


class BaseService:
    def __init__(self, session: Optional[AsyncSession] = None) -> None:
        self.session = session
        self.redis = redis_client

    async def ensure_redis_connection(self) -> None:
        """Ensure Redis connection is established before using it."""
        if hasattr(self.redis, "ensure_connection"):
            await self.redis.ensure_connection()
        else:
            # Fallback for older Redis client implementation
            await self.redis.connect()

    async def commit_or_rollback(self) -> None:
        """Commit session or rollback on error."""
        if not self.session:
            return
        try:
            await self.session.commit()
        except Exception as e:
            # Check if session is still valid before attempting rollback
            if self.session.is_active:
                try:
                    await self.session.rollback()
                except Exception:
                    # If rollback fails, the session is likely in an invalid state
                    # This can happen in concurrent scenarios - just log and continue
                    pass
            raise e

    async def cache_get(self, key: str) -> Optional[str]:
        await self.ensure_redis_connection()
        return await self.redis.get(key)

    async def cache_set(self, key: str, value: str, expire: int = 86400) -> bool:
        await self.ensure_redis_connection()
        return await self.redis.set(key, value, expire=expire)

    async def cache_incr(self, key: str) -> int:
        await self.ensure_redis_connection()
        return await self.redis.incr(key)
