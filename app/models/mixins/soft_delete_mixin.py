import datetime
from typing import Optional, Any

from sqlmodel import SQLModel, Field, select


class SoftDeleteMixin(SQLModel, table=False):
    deleted_at: Optional[datetime.datetime] = Field(default=None, nullable=True)

    @classmethod
    def get_deleted(cls, db) -> Any:
        stmt = select(cls).where(cls.deleted_at is not None)
        return list(db.scalars(stmt))

    @classmethod
    def get_not_deleted(cls, db) -> Any:
        stmt = select(cls).where(cls.deleted_at is None)
        return list(db.scalars(stmt))

    def soft_delete(self, db):
        self.deleted_at = datetime.datetime.now(datetime.UTC)
        db.add(self)
        db.commit()
        db.refresh(self)

    def restore(self, db):
        self.deleted_at = None
        db.add(self)
        db.commit()
        db.refresh(self)
