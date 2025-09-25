import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.cache import redis_client
from app.core.queue import RabbitMQClient
from app.core.config import settings
from app.main import app


TEST_DATABASE_URL = (
    settings.TEST_DATABASE_URL
    or "postgresql+psycopg://test_db_user:test_db_user_pass@postgres:5432/test_db"
)
engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
TestingSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="session")
def event_loop():
    """Ensure async tests share one event loop."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    """Recreate tables before running tests."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def test_client():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        yield client


@pytest_asyncio.fixture(scope="session", autouse=True)
async def redis_setup():
    await redis_client.connect()
    yield


@pytest_asyncio.fixture
async def rabbitmq_client_fixture():
    """Provide a fresh RabbitMQ client per test to avoid loop issues."""
    client = RabbitMQClient(settings.RABBITMQ_URL)
    await client.connect()
    yield client
    await client.close()
