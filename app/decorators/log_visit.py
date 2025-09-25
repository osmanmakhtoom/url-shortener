import functools
from fastapi import Request
from app.services import VisitService


def log_visit(short_code_param: str = "short_code"):
    """
    Decorator for endpoints that need visit logging.
    Uses VisitService (Redis + RabbitMQ) instead of direct clients.
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            short_code = kwargs.get(short_code_param)

            if short_code:
                service = VisitService()
                await service.log_visit(short_code=short_code, request=request)

            return await func(*args, **kwargs)

        return wrapper

    return decorator
