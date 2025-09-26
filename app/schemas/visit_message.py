from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class VisitMessage(BaseModel):
    short_code: str
    ip: Optional[str] = None
    timestamp: datetime
