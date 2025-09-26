"""
Timestamp Service - handles timestamp management business logic.
This service is responsible for managing created_at and updated_at timestamps
following service-oriented architecture principles.
"""

import datetime
from typing import Any, Generic, TypeVar

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import BaseService

T = TypeVar("T")


class TimestampService(BaseService, Generic[T]):
    """Service for handling timestamp operations on models with TimestampedMixin."""

    def __init__(self, session: AsyncSession, model_class: type[T]):
        super().__init__(session)
        self.model_class = model_class
        self._setup_event_listeners()

    def _setup_event_listeners(self) -> None:
        """Setup SQLAlchemy event listeners for automatic timestamp updates."""

        @event.listens_for(self.model_class, "before_update")
        def before_update_listener(mapper: Any, connection: Any, target: Any) -> None:
            target.updated_at = datetime.datetime.now()

        @event.listens_for(self.model_class, "before_insert")
        def before_insert_listener(mapper: Any, connection: Any, target: Any) -> None:
            now = datetime.datetime.now()
            if target.created_at is None:
                target.created_at = now
            if target.updated_at is None:
                target.updated_at = now

    def update_timestamp(self, instance: T) -> T:
        """Manually update the updated_at timestamp."""
        instance.updated_at = datetime.datetime.now()  # type: ignore
        return instance

    def set_created_timestamp(self, instance: T) -> T:
        """Set the created_at timestamp (usually called during creation)."""
        if instance.created_at is None:  # type: ignore
            instance.created_at = datetime.datetime.now()  # type: ignore
        return instance

    async def save_with_timestamps(self, instance: T) -> T:
        """Save instance with proper timestamp handling."""
        self.set_created_timestamp(instance)
        self.update_timestamp(instance)

        if self.session:
            self.session.add(instance)
            await self.commit_or_rollback()
            await self.session.refresh(instance)
        return instance
