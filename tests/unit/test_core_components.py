"""
Unit tests for core components (config, cache, queue, db).
"""

import pytest

from app.core.config import settings


class TestConfig:
    """Test configuration settings."""

    def test_settings_validation(self):
        """Test that settings have required attributes."""
        assert hasattr(settings, "DATABASE_URL")
        assert hasattr(settings, "REDIS_URL")
        assert hasattr(settings, "RABBITMQ_URL")
        assert hasattr(settings, "ENVIRONMENT")
        assert hasattr(settings, "LOG_LEVEL")
        assert hasattr(settings, "LOG_FORMAT")

    def test_settings_properties(self):
        """Test that settings have correct property types."""
        assert isinstance(settings.is_development, bool)
        assert isinstance(settings.is_production, bool)

    def test_settings_version(self):
        """Test that settings have version."""
        assert hasattr(settings, "VERSION")
        assert isinstance(settings.VERSION, str)

    def test_settings_debug(self):
        """Test that settings have debug flag."""
        assert hasattr(settings, "DEBUG")
        assert isinstance(settings.DEBUG, bool)

    def test_settings_project_name(self):
        """Test that settings have project name."""
        assert hasattr(settings, "PROJECT_NAME")
        assert isinstance(settings.PROJECT_NAME, str)

    def test_settings_redis_settings(self):
        """Test that settings have Redis configuration."""
        assert hasattr(settings, "REDIS_URL")
        assert hasattr(settings, "REDIS_PASSWORD")
        assert hasattr(settings, "REDIS_DB")

    def test_settings_rabbitmq_settings(self):
        """Test that settings have RabbitMQ configuration."""
        assert hasattr(settings, "RABBITMQ_URL")

    def test_settings_logging_settings(self):
        """Test that settings have logging configuration."""
        assert hasattr(settings, "LOG_LEVEL")
        assert hasattr(settings, "LOG_FORMAT")

    def test_settings_environment_settings(self):
        """Test that settings have environment configuration."""
        assert hasattr(settings, "ENVIRONMENT")
        assert hasattr(settings, "DEBUG")


class TestCache:
    """Test cache functionality."""

    def test_redis_client_import(self):
        """Test that RedisClient can be imported."""
        from app.core.cache import RedisClient

        assert RedisClient is not None

    def test_redis_client_has_methods(self):
        """Test that RedisClient has expected methods."""
        from app.core.cache import RedisClient

        assert hasattr(RedisClient, "__init__")
        assert hasattr(RedisClient, "connect")
        assert hasattr(RedisClient, "close")
        assert hasattr(RedisClient, "get")
        assert hasattr(RedisClient, "set")
        assert hasattr(RedisClient, "delete")
        assert hasattr(RedisClient, "ping")

    def test_redis_client_instantiation(self):
        """Test that RedisClient can be instantiated."""
        from app.core.cache import RedisClient

        client = RedisClient("redis://localhost:6379")
        assert client is not None
        assert hasattr(client, "_url")
        assert client._url == "redis://localhost:6379"


class TestQueue:
    """Test queue functionality."""

    def test_rabbitmq_client_import(self):
        """Test that RabbitMQClient can be imported."""
        from app.core.queue import RabbitMQClient

        assert RabbitMQClient is not None

    def test_rabbitmq_client_has_methods(self):
        """Test that RabbitMQClient has expected methods."""
        from app.core.queue import RabbitMQClient

        assert hasattr(RabbitMQClient, "__init__")
        assert hasattr(RabbitMQClient, "connect")
        assert hasattr(RabbitMQClient, "close")
        assert hasattr(RabbitMQClient, "publish")
        assert hasattr(RabbitMQClient, "consume")

    def test_rabbitmq_client_instantiation(self):
        """Test that RabbitMQClient can be instantiated."""
        from app.core.queue import RabbitMQClient

        client = RabbitMQClient("amqp://localhost:5672")
        assert client is not None


class TestDatabase:
    """Test database functionality."""

    def test_db_module_import(self):
        """Test that db module can be imported."""
        from app.core import db

        assert db is not None

    def test_db_engine_exists(self):
        """Test that the engine object exists."""
        from app.core.db import engine

        assert engine is not None

    def test_db_init_db_exists(self):
        """Test that init_db function exists."""
        from app.core.db import init_db

        assert callable(init_db)

    def test_db_get_session_exists(self):
        """Test that get_session function exists."""
        from app.core.db import get_session

        assert callable(get_session)
