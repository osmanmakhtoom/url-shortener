import functools
from typing import Any, Callable, Optional

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import VisitService


def log_visit(short_code_param: str = "short_code") -> Callable:
    """
    Decorator for endpoints that need visit logging.
    Uses VisitService (Redis + RabbitMQ) instead of direct clients.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            request: Optional[Request] = kwargs.get("request")
            short_code: Optional[str] = kwargs.get(short_code_param)
            session: Optional[AsyncSession] = kwargs.get("session")

            if short_code and session:
                service = VisitService(session)
                await service.log_visit(short_code=short_code, request=request)

            return await func(*args, **kwargs)

        return wrapper

    return decorator
