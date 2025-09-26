from typing import Any, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import URL
from app.services import ShortCodeFactory
from app.services.model_service import ModelService


class URLService(ModelService[URL]):
    """
    URL Service that extends ModelService with URL-specific business logic.

    This service follows service-oriented architecture by:
    - Inheriting from ModelService for CRUD operations
    - Adding URL-specific methods for short code generation
    - Using dependency injection for the short code generator
    """

    def __init__(self, session: AsyncSession, generator_type: str = "random"):
        super().__init__(session, URL)
        self.generator = ShortCodeFactory.create(generator_type)

    def validate_update_data(self, instance: URL, **kwargs: Any) -> None:
        """Validate URL-specific update data."""
        if "visit_count" in kwargs:
            visit_count = kwargs["visit_count"]
            if visit_count < 0:
                raise ValueError("Visit count cannot be negative")

    async def create_short(self, original_url: str, max_attempts: int = 5) -> URL:
        """
        Create a shortened URL with unique short code generation.

        This method uses service-oriented design by:
        - Using the inherited create method for proper timestamp handling
        - Implementing retry logic for unique code generation
        - Using caching service for performance optimization
        - Validating input parameters
        """
        # Validate input
        if original_url is None:
            raise ValueError("URL cannot be None")

        original_url = str(original_url).strip()
        if not original_url:
            raise ValueError("URL cannot be empty")
        stmt = select(URL).where(
            URL.original_url == original_url,
            URL.deleted_at.is_(None),  # type: ignore # Only check non-deleted URLs
        )
        if self.session:
            result = await self.session.execute(stmt)
        else:
            raise RuntimeError("Database session not available")
        existing = result.scalars().first()
        if existing:
            return existing

        # Try generating unique short_code
        attempt, length = 0, 6
        while attempt < max_attempts:
            code = self.generator.generate(length=length)
            try:
                # Use the inherited create method for proper timestamp handling
                url = await self.create(original_url=original_url, short_code=code)

                # Cache short_code → original_url
                await self.cache_set(f"short:{code}", original_url)
                return url
            except IntegrityError:
                # In concurrent scenarios, the session might already be in an invalid state
                # Just continue to the next attempt without trying to rollback
                attempt += 1
                if attempt % 2 == 0:
                    length += 1

        raise Exception("Could not generate unique short code after max attempts")

    async def get_by_code(self, short_code: str) -> Optional[URL]:
        """
        Get URL by short code with caching optimization.

        This method uses service-oriented design by:
        - Using caching service for performance
        - Only returning non-deleted URLs
        - Implementing cache-aside pattern
        - Gracefully handling cache errors
        """
        try:
            cached = await self.cache_get(f"short:{short_code}")
            if cached:
                # Fetch from DB anyway to get a managed instance (but only non-deleted)
                stmt = select(URL).where(URL.short_code == short_code, URL.deleted_at.is_(None))  # type: ignore
                if self.session:
                    result = await self.session.execute(stmt)
                else:
                    return None
                url = result.scalars().first()

                # Validate that we got a proper URL object
                if url and not isinstance(url, URL):
                    return None

                return url
        except Exception:
            # Cache error - continue with database lookup
            pass

        try:
            stmt = select(URL).where(
                URL.short_code == short_code,
                URL.deleted_at.is_(None),  # type: ignore # Only return non-deleted URLs
            )
            if self.session:
                result = await self.session.execute(stmt)
            else:
                return None
            url = result.scalars().first()

            # Validate that we got a proper URL object
            if url and not isinstance(url, URL):
                return None

            if url:
                try:
                    await self.cache_set(f"short:{short_code}", url.original_url)
                except Exception:
                    # Cache error - ignore and continue
                    pass

            return url
        except Exception:
            # Database error - return None gracefully
            return None
