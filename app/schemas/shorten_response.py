from pydantic import BaseModel
from typing import Optional


class ShortenResponse(BaseModel):
    short_code: str
    short_url: Optional[str] = None
