from typing import Optional
from sqlmodel import Field, Relationship

from app.models.mixins import (
    UUIDMixin,
    TimestampedMixin,
    IsActiveMixin,
    SoftDeleteMixin,
    IDMixin,
)


class Visit(IDMixin, UUIDMixin, TimestampedMixin, IsActiveMixin, SoftDeleteMixin, table=True):
    url_id: int = Field(foreign_key="url.id")
    ip_address: Optional[str] = None
    url: Optional["URL"] = Relationship(back_populates="visits")
