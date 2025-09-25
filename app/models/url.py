from typing import List
from sqlmodel import Field, Relationship

from app.models.mixins import (
    UUIDMixin,
    TimestampedMixin,
    IsActiveMixin,
    SoftDeleteMixin,
    IDMixin,
)


class URL(IDMixin, UUIDMixin, TimestampedMixin, IsActiveMixin, SoftDeleteMixin, table=True):
    original_url: str
    short_code: str = Field(index=True, unique=True, max_length=64)
    visit_count: int = Field(default=0)
    visits: List["Visit"] = Relationship(back_populates="url")
