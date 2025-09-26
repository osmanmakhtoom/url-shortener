"""
Soft Delete Service - handles soft deletion business logic.
This service is responsible for all soft delete operations, following
service-oriented architecture principles.
"""

import datetime
from typing import Any, Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.services.base import BaseService

T = TypeVar("T")


class SoftDeleteService(BaseService, Generic[T]):
    """Service for handling soft delete operations on models with SoftDeleteMixin."""

    def __init__(self, session: AsyncSession, model_class: type[T]):
        super().__init__(session)
        self.model_class = model_class

    async def get_deleted(self) -> list[T]:
        """Get all soft-deleted records."""
        stmt = select(self.model_class).where(self.model_class.deleted_at.is_not(None))  # type: ignore
        if self.session:
            result = await self.session.execute(stmt)
        else:
            return []
        return list(result.scalars().all())

    async def get_not_deleted(self) -> list[T]:
        """Get all non-deleted records."""
        stmt = select(self.model_class).where(self.model_class.deleted_at.is_(None))  # type: ignore
        if self.session:
            result = await self.session.execute(stmt)
        else:
            return []
        return list(result.scalars().all())

    async def soft_delete(self, instance: T) -> T:
        """Soft delete a record by setting deleted_at timestamp."""
        instance.deleted_at = datetime.datetime.now()  # type: ignore
        if self.session:
            self.session.add(instance)
            await self.commit_or_rollback()
            await self.session.refresh(instance)
        return instance

    async def restore(self, instance: T) -> T:
        """Restore a soft-deleted record by clearing deleted_at."""
        instance.deleted_at = None  # type: ignore
        if self.session:
            self.session.add(instance)
            await self.commit_or_rollback()
            await self.session.refresh(instance)
        return instance

    async def get_by_id_not_deleted(self, record_id: int) -> T | None:
        """Get a non-deleted record by ID."""
        stmt = select(self.model_class).where(
            self.model_class.id == record_id,  # type: ignore
            self.model_class.deleted_at.is_(None),  # type: ignore
        )
        if self.session:
            result = await self.session.execute(stmt)
        else:
            return None
        return result.scalars().first()

    async def get_by_uuid_not_deleted(self, uuid: str) -> T | None:
        """Get a non-deleted record by UUID."""
        stmt = select(self.model_class).where(
            self.model_class.uuid == uuid,  # type: ignore
            self.model_class.deleted_at.is_(None),  # type: ignore
        )
        if self.session:
            result = await self.session.execute(stmt)
        else:
            return None
        return result.scalars().first()
