"""
Service interfaces for better abstraction and dependency injection.
These interfaces define contracts that services must implement,
following service-oriented architecture principles.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, Protocol, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class SoftDeleteServiceInterface(Protocol[T]):
    """Interface for soft delete operations."""

    async def get_deleted(self) -> list[T]: ...
    async def get_not_deleted(self) -> list[T]: ...
    async def soft_delete(self, instance: T) -> T: ...
    async def restore(self, instance: T) -> T: ...
    async def get_by_id_not_deleted(self, record_id: int) -> T | None: ...
    async def get_by_uuid_not_deleted(self, uuid: str) -> T | None: ...


class TimestampServiceInterface(Protocol[T]):
    """Interface for timestamp operations."""

    def update_timestamp(self, instance: T) -> T: ...
    def set_created_timestamp(self, instance: T) -> T: ...
    async def save_with_timestamps(self, instance: T) -> T: ...


class ModelServiceInterface(ABC, Generic[T]):
    """Abstract base class for model services."""

    def __init__(self, session: Optional[AsyncSession], model_class: type[T]):
        self.session = session
        self.model_class = model_class

    @abstractmethod
    async def create(self, **kwargs: Any) -> T: ...

    @abstractmethod
    async def get_by_id(self, record_id: int) -> T | None: ...

    @abstractmethod
    async def get_by_uuid(self, uuid: str) -> T | None: ...

    @abstractmethod
    async def update(self, instance: T, **kwargs: Any) -> T: ...

    @abstractmethod
    async def delete(self, instance: T) -> T: ...


class CRUDServiceInterface(ModelServiceInterface[T]):
    """Interface for CRUD operations with additional query methods."""

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> list[T]: ...

    @abstractmethod
    async def count(self) -> int: ...

    @abstractmethod
    async def exists(self, record_id: int) -> bool: ...
