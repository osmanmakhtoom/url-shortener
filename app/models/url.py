from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.visit import Visit


class URL(BaseModel, table=True):
    """
    URL model that represents a shortened URL.

    Inherits from BaseModel which provides common functionality:
    - ID, UUID, timestamps, active status, soft delete capabilities
    - Business logic is handled by appropriate services
    """

    original_url: str
    short_code: str = Field(index=True, unique=True, max_length=64)
    visit_count: int = Field(default=0)
    visits: List["Visit"] = Relationship(back_populates="url")
