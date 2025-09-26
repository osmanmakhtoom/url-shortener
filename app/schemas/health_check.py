from typing import Optional

from pydantic import BaseModel


class HealthCheck(BaseModel):
    status: str
    timestamp: str
    version: str
    environment: str
    database: str
    redis: str
    rabbitmq: Optional[str] = None
