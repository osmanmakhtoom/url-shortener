"""
Unit tests for Pydantic schemas.
"""

from datetime import datetime

import pytest
from pydantic import BaseModel

from app.schemas.health_check import HealthCheck
from app.schemas.shorten_request import ShortenRequest
from app.schemas.shorten_response import ShortenResponse
from app.schemas.stats_response import StatsResponse
from app.schemas.visit_message import VisitMessage


class TestSchemas:
    """Test schemas for basic functionality."""

    def test_schemas_are_pydantic_models(self):
        """Test that schemas are Pydantic models."""
        assert issubclass(HealthCheck, BaseModel)
        assert issubclass(ShortenRequest, BaseModel)
        assert issubclass(ShortenResponse, BaseModel)
        assert issubclass(StatsResponse, BaseModel)
        assert issubclass(VisitMessage, BaseModel)

    def test_schemas_have_fields(self):
        """Test that schemas have expected fields."""
        # Test that schemas have model_fields (Pydantic v2)
        assert hasattr(ShortenRequest, "model_fields")
        assert hasattr(ShortenResponse, "model_fields")
        assert hasattr(StatsResponse, "model_fields")
        assert hasattr(VisitMessage, "model_fields")
        assert hasattr(HealthCheck, "model_fields")

        # Test that model_fields contain expected field names
        assert "url" in ShortenRequest.model_fields
        assert "short_code" in ShortenResponse.model_fields
        assert "short_url" in ShortenResponse.model_fields
        assert "original_url" in ShortenResponse.model_fields
        assert "created_at" in ShortenResponse.model_fields
        assert "short_code" in StatsResponse.model_fields
        assert "original_url" in StatsResponse.model_fields
        assert "visit_count" in StatsResponse.model_fields
        assert "created_at" in StatsResponse.model_fields
        assert "short_code" in VisitMessage.model_fields
        assert "ip" in VisitMessage.model_fields
        assert "timestamp" in VisitMessage.model_fields
        assert "status" in HealthCheck.model_fields

    def test_schemas_can_be_instantiated(self):
        """Test that schemas can be instantiated."""
        # Test ShortenRequest
        request = ShortenRequest(url="https://example.com")
        assert str(request.url) == "https://example.com/"

        # Test ShortenResponse
        response = ShortenResponse(
            short_code="abc123",
            original_url="https://example.com",
            created_at="2023-01-01T00:00:00Z",
        )
        assert response.short_code == "abc123"
        assert response.original_url == "https://example.com"
        assert response.created_at == "2023-01-01T00:00:00Z"

        # Test VisitMessage
        message = VisitMessage(
            short_code="abc123", ip="127.0.0.1", timestamp=datetime(2023, 1, 1, 0, 0, 0)
        )
        assert message.short_code == "abc123"
        assert message.ip == "127.0.0.1"
        assert message.timestamp == datetime(2023, 1, 1, 0, 0, 0)
