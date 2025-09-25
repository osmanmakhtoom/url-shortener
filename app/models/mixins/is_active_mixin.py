from sqlmodel import SQLModel, Field


class IsActiveMixin(SQLModel, table=False):
    is_active: bool = Field(default=True, nullable=False)
