from datetime import datetime, timezone
from typing import Optional

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.queue import rabbitmq_client
from app.models import URL, Visit
from app.schemas import VisitMessage
from app.services.model_service import ModelService
from app.utils import extract_client_ip


class VisitService(ModelService[Visit]):
    """
    Visit Service that extends ModelService with visit-specific business logic.

    This service follows service-oriented architecture by:
    - Inheriting from ModelService for CRUD operations
    - Adding visit-specific methods for logging and statistics
    - Using message queue for asynchronous processing
    """

    def __init__(self, session: AsyncSession, queue_name: str = "visits"):
        super().__init__(session, Visit)
        self.queue_name = queue_name

    async def log_visit(self, short_code: str, request: Request | None = None) -> None:
        """
        Log a visit asynchronously using message queue.

        This method uses service-oriented design by:
        - Using caching service for immediate counter updates
        - Using message queue for asynchronous persistence
        - Separating concerns between immediate response and data persistence
        """
        await self.cache_incr(f"visits:{short_code}")

        msg = VisitMessage(
            short_code=short_code,
            ip=extract_client_ip(request) if request else None,
            timestamp=datetime.now(),
        )

        # Handle RabbitMQ operations gracefully
        try:
            await rabbitmq_client.connect()
            await rabbitmq_client.publish(self.queue_name, msg.model_dump())
        except Exception as e:
            # Log the error but don't fail the visit logging
            # In production, you might want to log this to a proper logging system
            print(f"Warning: Failed to publish visit message to RabbitMQ: {e}")
            # Continue execution - the cache increment above still works

    async def create_visit_record(self, url: URL, ip_address: Optional[str] = None) -> Visit:
        """
        Create a visit record in the database.

        This method uses the inherited create method for proper timestamp handling
        and follows service-oriented design principles.
        """
        return await self.create(url_id=url.id, ip_address=ip_address)

    async def get_visits_for_url(self, url_id: int) -> list[Visit]:
        """Get all visits for a specific URL (only non-deleted records)."""
        from sqlmodel import select

        stmt = (
            select(Visit)
            .where(Visit.url_id == url_id, Visit.deleted_at.is_(None))  # type: ignore
            .order_by(Visit.created_at.desc())  # type: ignore
        )

        if self.session:
            result = await self.session.execute(stmt)
        else:
            return []
        return list(result.scalars().all())
