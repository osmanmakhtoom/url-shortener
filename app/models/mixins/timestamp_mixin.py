from sqlalchemy import event
from sqlmodel import SQLModel, Field
import datetime as dt
from datetime import datetime


class TimestampedMixin(SQLModel, table=False):
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)


def before_update_listener(mapper, connection, target):
    target.updated_at = datetime.now(dt.timezone.utc)


event.listen(TimestampedMixin, "before_update", before_update_listener)
