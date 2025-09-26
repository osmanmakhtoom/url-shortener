import os
from typing import Any, List, Optional

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = Field(
        ..., description="Database connection URL - REQUIRED from environment"
    )
    TEST_DATABASE_URL: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/test_db",
        description="Test database connection URL - REQUIRED from environment",
    )

    # Redis
    REDIS_URL: str = Field(..., description="Redis connection URL - REQUIRED from environment")
    REDIS_HOST: str = Field(default="localhost", description="Redis host")
    REDIS_PORT: int = Field(default=6379, description="Redis port")
    REDIS_DB: int = Field(default=0, description="Redis database number")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis password")

    # RabbitMQ
    RABBITMQ_URL: str = Field(
        ..., description="RabbitMQ connection URL - REQUIRED from environment"
    )
    RABBITMQ_HOST: str = Field(default="localhost", description="RabbitMQ Host")
    RABBITMQ_PORT: int = Field(default=5672, description="RabbitMQ Port")
    RABBITMQ_USER: str = Field(default="guest", description="RabbitMQ Username")
    RABBITMQ_PASS: str = Field(default="guest", description="RabbitMQ Password")

    # API
    API_V1_STR: str = Field(default="/api/v1", description="API v1 prefix")
    PROJECT_NAME: str = Field(default="Shoraka URL-shortener API", description="Project name")
    VERSION: str = Field(default="1.0.0", description="API version")
    DESCRIPTION: str = Field(default="A URL-shortener API", description="API description")

    # Env
    ENVIRONMENT: str = Field(
        default="development", description="Environment (development/staging/production)"
    )
    DEBUG: bool = Field(default=True, description="Debug mode")

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Rate limit requests per minute")
    RATE_LIMIT_WINDOW: int = Field(default=60, description="Rate limit window in seconds")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Log format"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

    @field_validator("DATABASE_URL", "REDIS_URL", "RABBITMQ_URL")
    @classmethod
    def validate_required(cls, v: str, field: Any) -> str:
        if not v:
            raise ValueError(f"{field.name} is required")
        return v

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    @property
    def database_url_sync(self) -> str:
        return self.DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg")

    @property
    def redis_config(self) -> dict:
        config = {
            "host": self.REDIS_HOST,
            "port": self.REDIS_PORT,
            "db": self.REDIS_DB,
        }
        if self.REDIS_PASSWORD:
            config["password"] = self.REDIS_PASSWORD
        return config


# Load settings with fallback values for development
settings = Settings(
    DATABASE_URL=os.getenv(
        "DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/shortener"
    ),
    REDIS_URL=os.getenv("REDIS_URL", "redis://localhost:6379"),
    RABBITMQ_URL=os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672"),
)
