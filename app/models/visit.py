from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.url import URL


class Visit(BaseModel, table=True):
    """
    Visit model that represents a visit to a shortened URL.

    Inherits from BaseModel which provides common functionality:
    - ID, UUID, timestamps, active status, soft delete capabilities
    - Business logic is handled by appropriate services
    """

    url_id: int = Field(foreign_key="url.id")
    ip_address: Optional[str] = None
    url: Optional["URL"] = Relationship(back_populates="visits")
