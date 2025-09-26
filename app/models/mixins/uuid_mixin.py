from uuid import UUID

import uuid6
from sqlmodel import Field, SQLModel, Uuid


class UUIDMixin(SQLModel, table=False):
    uuid: UUID = Field(
        sa_type=Uuid,
        default_factory=uuid6.uuid7,
        index=True,
        unique=True,
        nullable=False,
    )
