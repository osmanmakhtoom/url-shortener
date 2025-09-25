import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.db import init_db
from app.core.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up application...")

    if settings.is_development:
        logger.info("Creating database tables...")
        try:
            await init_db()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise

    yield

    # Shutdown
    logger.info("Shutting down application...")


def setup_logging():
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=settings.LOG_FORMAT,
    )
