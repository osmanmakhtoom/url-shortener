from typing import Optional
from sqlmodel import SQLModel, Field


class IDMixin(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
