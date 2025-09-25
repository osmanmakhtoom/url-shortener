from pydantic import BaseModel
from typing import Optional


class HealthCheck(BaseModel):
    status: str
    timestamp: str
    version: str
    environment: str
    database: str
    redis: str
    rabbitmq: Optional[str] = None
