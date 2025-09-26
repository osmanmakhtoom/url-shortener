from datetime import datetime
from typing import Any

from sqlalchemy import event
from sqlmodel import Field, SQLModel


class TimestampedMixin(SQLModel, table=False):
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)


def before_update_listener(mapper: Any, connection: Any, target: Any) -> None:
    target.updated_at = datetime.now()


event.listen(TimestampedMixin, "before_update", before_update_listener)
