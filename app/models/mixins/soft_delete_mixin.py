import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class SoftDeleteMixin(SQLModel, table=False):
    """
    Mixin that provides soft delete data structure.

    Business logic for soft delete operations is handled by SoftDeleteService
    following service-oriented architecture principles.
    """

    deleted_at: Optional[datetime.datetime] = Field(default=None, nullable=True)
