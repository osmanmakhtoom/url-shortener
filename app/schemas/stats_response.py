from pydantic import BaseModel, HttpUrl
from datetime import datetime


class StatsResponse(BaseModel):
    original_url: HttpUrl
    short_code: str
    visits: int
    created_at: datetime
