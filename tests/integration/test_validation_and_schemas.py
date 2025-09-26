"""
Integration tests for validation and schema behavior.
"""

import pytest
from fastapi import status


class TestValidationAndSchemas:
    """Test validation and schema behavior."""

    @pytest.mark.asyncio
    async def test_url_validation(self, test_client):
        """Test URL validation in schemas."""
        # Valid URLs
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://subdomain.example.com",
            "https://example.com/path",
            "https://example.com/path?query=value",
        ]

        for url in valid_urls:
            response = await test_client.post("/api/v1/shorten", json={"url": url})
            assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_invalid_url_validation(self, test_client):
        """Test invalid URL validation."""
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "javascript:alert('xss')",
            "",
            "example.com",  # Missing protocol
        ]

        for url in invalid_urls:
            response = await test_client.post("/api/v1/shorten", json={"url": url})
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_schema_field_validation(self, test_client):
        """Test schema field validation."""
        # Missing required fields
        response = await test_client.post("/api/v1/shorten", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Extra fields (should be ignored)
        response = await test_client.post(
            "/api/v1/shorten",
            json={"url": "https://example.com", "extra_field": "should_be_ignored"},
        )
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_response_schema_structure(self, test_client):
        """Test response schema structure."""
        response = await test_client.post("/api/v1/shorten", json={"url": "https://example.com"})
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        required_fields = ["short_code", "short_url", "original_url", "created_at"]
        for field in required_fields:
            assert field in data

    @pytest.mark.asyncio
    async def test_stats_response_schema(self, test_client):
        """Test stats response schema structure."""
        # Create a short URL first
        create_response = await test_client.post(
            "/api/v1/shorten", json={"url": "https://example.com"}
        )
        assert create_response.status_code == status.HTTP_200_OK
        short_code = create_response.json()["short_code"]

        # Get stats
        stats_response = await test_client.get(f"/api/v1/stats/{short_code}")
        assert stats_response.status_code == status.HTTP_200_OK

        data = stats_response.json()
        required_fields = ["short_code", "original_url", "visit_count", "created_at"]
        for field in required_fields:
            assert field in data

    @pytest.mark.asyncio
    async def test_health_check_schema(self, test_client):
        """Test health check response schema."""
        response = await test_client.get("/health")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_url_normalization_behavior(self, test_client):
        """Test URL normalization behavior in responses."""
        test_cases = [
            ("https://example.com", "https://example.com/"),
            ("https://example.com/", "https://example.com/"),
            ("https://example.com/path", "https://example.com/path"),
        ]

        for input_url, expected_normalized in test_cases:
            response = await test_client.post("/api/v1/shorten", json={"url": input_url})
            assert response.status_code == status.HTTP_200_OK

            data = response.json()
            assert data["original_url"] == expected_normalized

    @pytest.mark.asyncio
    async def test_short_code_format(self, test_client):
        """Test short code format validation."""
        response = await test_client.post("/api/v1/shorten", json={"url": "https://example.com"})
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        short_code = data["short_code"]

        # Short code should be alphanumeric and reasonable length
        assert short_code.isalnum()
        assert 4 <= len(short_code) <= 10

    @pytest.mark.asyncio
    async def test_created_at_format(self, test_client):
        """Test created_at timestamp format."""
        response = await test_client.post("/api/v1/shorten", json={"url": "https://example.com"})
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        created_at = data["created_at"]

        # Should be a valid ISO format timestamp
        assert isinstance(created_at, str)
        assert "T" in created_at  # ISO format indicator
