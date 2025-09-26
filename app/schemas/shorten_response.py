from typing import Optional

from pydantic import BaseModel


class ShortenResponse(BaseModel):
    short_code: str
    original_url: str
    short_url: Optional[str] = None
    created_at: str
