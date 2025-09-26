import datetime

from fastapi import Depends, FastAPI
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import text

from app.api.v1.api import api_router
from app.core.cache import redis_client
from app.core.config import settings
from app.core.db import get_db_dependency
from app.core.queue import rabbitmq_client
from app.core.startup import lifespan, setup_logging
from app.schemas import HealthCheck

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", response_model=dict)
async def root() -> dict[str, str]:
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


@app.get("/health", response_model=HealthCheck)
async def health_check(session: AsyncSession = Depends(get_db_dependency)) -> HealthCheck:
    db_status = "disconnected"
    redis_status = "disconnected"
    rabbitmq_status = "disconnected"

    # --- DB health check ---
    try:
        await session.execute(text("SELECT 1"))
        db_status = "connected"
    except SQLAlchemyError as e:
        db_status = f"error: {str(e)}"

    # --- Redis health check ---
    try:
        await redis_client.connect()
        pong = await redis_client.ping()
        redis_status = "connected" if pong else "disconnected"
    except Exception as e:
        redis_status = f"error: {str(e)}"

    # --- RabbitMQ health check ---
    try:
        await rabbitmq_client.connect()
        if rabbitmq_client._connection and not rabbitmq_client._connection.is_closed:
            rabbitmq_status = "connected"
        else:
            rabbitmq_status = "disconnected"
    except Exception as e:
        rabbitmq_status = f"error: {str(e)}"

    # --- Overall status ---
    status = (
        "healthy"
        if db_status == "connected"
        and redis_status == "connected"
        and rabbitmq_status == "connected"
        else "degraded"
    )

    return HealthCheck(
        status=status,
        timestamp=datetime.datetime.now().isoformat(),
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        database=db_status,
        redis=redis_status,
        rabbitmq=rabbitmq_status,  # new field
    )
