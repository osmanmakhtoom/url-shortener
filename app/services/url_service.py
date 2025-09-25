from typing import Optional
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import URL
from app.services import ShortCodeFactory
from app.services.base import BaseService


class URLService(BaseService):
    def __init__(self, session: AsyncSession, generator_type: str = "random"):
        super().__init__(session)
        self.generator = ShortCodeFactory.create(generator_type)

    async def create_short(self, original_url: str, max_attempts: int = 5) -> URL:
        # Check if URL already exists
        original_url = str(original_url).strip()
        stmt = select(URL).where(URL.original_url == original_url)
        result = await self.session.execute(stmt)
        existing = result.scalars().first()
        if existing:
            return existing

        # Try generating unique short_code
        attempt, length = 0, 6
        while attempt < max_attempts:
            code = self.generator.generate(length=length)
            url = URL(original_url=original_url, short_code=code)
            try:
                self.session.add(url)
                await self.commit_or_rollback()
                await self.session.refresh(url)

                # Cache short_code → original_url
                await self.cache_set(f"short:{code}", original_url)
                return url
            except IntegrityError:
                await self.session.rollback()
                attempt += 1
                if attempt % 2 == 0:
                    length += 1

        raise Exception("Could not generate unique short code after max attempts")

    async def get_by_code(self, short_code: str) -> Optional[URL]:
        cached = await self.cache_get(f"short:{short_code}")
        if cached:
            # Fetch from DB anyway to get a managed instance
            stmt = select(URL).where(URL.short_code == short_code)
            result = await self.session.execute(stmt)
            return result.scalars().first()

        stmt = select(URL).where(URL.short_code == short_code)
        result = await self.session.execute(stmt)
        url = result.scalars().first()

        if url:
            await self.cache_set(f"short:{short_code}", url.original_url)

        return url
