from fastapi import Request
from datetime import datetime, timezone
from app.core.queue import rabbitmq_client
from app.services.base import BaseService
from app.schemas import VisitMessage
from app.utils import extract_client_ip


class VisitService(BaseService):
    """Handles logging visits via Redis + RabbitMQ."""

    def __init__(self, queue_name: str = "visits"):
        super().__init__(session=None)
        self.queue_name = queue_name

    async def log_visit(self, short_code: str, request: Request | None = None):
        await self.cache_incr(f"visits:{short_code}")

        msg = VisitMessage(
            short_code=short_code,
            ip=extract_client_ip(request) if request else None,
            timestamp=datetime.now(timezone.utc),
        )

        await rabbitmq_client.connect()
        await rabbitmq_client.publish(self.queue_name, msg.model_dump())
