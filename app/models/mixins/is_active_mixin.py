from sqlmodel import Field, SQLModel


class IsActiveMixin(SQLModel, table=False):
    is_active: bool = Field(default=True, nullable=False)
