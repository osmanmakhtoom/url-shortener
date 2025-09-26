"""
Generic Model Service that implements CRUD operations with service-oriented design.
This service combines multiple specialized services for comprehensive model management.
"""

from typing import Any, Generic, Optional, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.services.base import BaseService
from app.services.interfaces import CRUDServiceInterface
from app.services.soft_delete_service import SoftDeleteService
from app.services.timestamp_service import TimestampService

T = TypeVar("T")


class ModelService(BaseService, CRUDServiceInterface[T], Generic[T]):
    """
    Generic service that provides CRUD operations with service-oriented design.

    This service combines multiple specialized services:
    - SoftDeleteService for soft delete operations
    - TimestampService for timestamp management
    - BaseService for caching and session management
    """

    def __init__(self, session: AsyncSession, model_class: type[T]):
        super().__init__(session)
        self.model_class = model_class
        self.soft_delete_service = SoftDeleteService(session, model_class)
        self.timestamp_service = TimestampService(session, model_class)

    async def create(self, **kwargs: Any) -> T:
        """Create a new instance with proper timestamp handling."""
        instance = self.model_class(**kwargs)
        return await self.timestamp_service.save_with_timestamps(instance)

    async def get_by_id(self, record_id: int) -> Optional[T]:
        """Get instance by ID (only non-deleted records)."""
        return await self.soft_delete_service.get_by_id_not_deleted(record_id)

    async def get_by_uuid(self, uuid: str) -> Optional[T]:
        """Get instance by UUID (only non-deleted records)."""
        return await self.soft_delete_service.get_by_uuid_not_deleted(uuid)

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        """List all non-deleted records with pagination."""
        stmt = (
            select(self.model_class)
            .where(self.model_class.deleted_at.is_(None))  # type: ignore
            .offset(skip)
            .limit(limit)
            .order_by(self.model_class.created_at.desc())  # type: ignore
        )
        if self.session:
            result = await self.session.execute(stmt)
        else:
            return []
        return list(result.scalars().all())

    async def count(self) -> int:
        """Count all non-deleted records."""
        stmt = select(self.model_class).where(self.model_class.deleted_at.is_(None))  # type: ignore
        if self.session:
            result = await self.session.execute(stmt)
        else:
            return 0
        return len(result.scalars().all())

    async def exists(self, record_id: int) -> bool:
        """Check if a non-deleted record exists."""
        instance = await self.get_by_id(record_id)
        return instance is not None

    def validate_update_data(self, instance: T, **kwargs: Any) -> None:
        """Validate update data. Override in subclasses for business rules."""
        pass

    async def update(self, instance: T, **kwargs: Any) -> T:
        """Update instance with timestamp handling."""
        # Validate the update data
        self.validate_update_data(instance, **kwargs)

        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        self.timestamp_service.update_timestamp(instance)
        if self.session:
            self.session.add(instance)
            await self.commit_or_rollback()
            await self.session.refresh(instance)
        return instance

    async def delete(self, instance: T) -> T:
        """Soft delete an instance."""
        return await self.soft_delete_service.soft_delete(instance)

    async def restore(self, instance: T) -> T:
        """Restore a soft-deleted instance."""
        return await self.soft_delete_service.restore(instance)

    async def get_deleted(self) -> list[T]:
        """Get all soft-deleted records."""
        return await self.soft_delete_service.get_deleted()

    async def get_not_deleted(self) -> list[T]:
        """Get all non-deleted records."""
        return await self.soft_delete_service.get_not_deleted()
