from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VisitMessage(BaseModel):
    short_code: str
    ip: Optional[str] = None
    timestamp: datetime
