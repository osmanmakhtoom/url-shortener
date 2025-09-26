from datetime import datetime

from pydantic import BaseModel, HttpUrl


class StatsResponse(BaseModel):
    original_url: HttpUrl
    short_code: str
    visit_count: int
    created_at: datetime
