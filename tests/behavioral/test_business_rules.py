"""
Behavioral tests for business rules and domain logic.
"""

import pytest
from fastapi import status


class TestBusinessRules:
    """Test business rules and domain logic behaviors."""

    @pytest.mark.asyncio
    async def test_short_code_generation_rules(self, test_client):
        """Test business rules for short code generation."""
        # Test multiple URL creations to verify short code uniqueness
        short_codes = set()

        for i in range(10):
            response = await test_client.post(
                "/api/v1/shorten", json={"url": f"https://example{i}.com"}
            )
            assert response.status_code == status.HTTP_200_OK

            data = response.json()
            short_code = data["short_code"]

            # Business rule: Short codes should be alphanumeric
            assert short_code.isalnum()

            # Business rule: Short codes should be reasonable length
            assert 4 <= len(short_code) <= 10

            short_codes.add(short_code)

        # Business rule: All short codes should be unique
        assert len(short_codes) == 10

    @pytest.mark.asyncio
    async def test_url_validation_rules(self, test_client):
        """Test business rules for URL validation."""
        # Valid URLs should be accepted
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://subdomain.example.com",
            "https://example.com/path",
            "https://example.com/path?query=value",
            "https://example.com/path#fragment",
        ]

        for url in valid_urls:
            response = await test_client.post("/api/v1/shorten", json={"url": url})
            assert response.status_code == status.HTTP_200_OK

            data = response.json()
            assert "short_code" in data
            assert "original_url" in data

    @pytest.mark.asyncio
    async def test_response_format_rules(self, test_client):
        """Test business rules for response formats."""
        response = await test_client.post("/api/v1/shorten", json={"url": "https://example.com"})
        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        # Business rule: Response must contain required fields
        required_fields = ["short_code", "short_url", "original_url", "created_at"]
        for field in required_fields:
            assert field in data

        # Business rule: short_url should be properly formatted
        assert data["short_url"] == f"/{data['short_code']}"

        # Business rule: created_at should be valid ISO format
        created_at = data["created_at"]
        assert isinstance(created_at, str)
        assert "T" in created_at  # ISO format indicator

    @pytest.mark.asyncio
    async def test_error_handling_rules(self, test_client):
        """Test business rules for error handling."""
        # Business rule: Invalid URLs should return 422
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "javascript:alert('xss')",
            "",
        ]

        for invalid_url in invalid_urls:
            response = await test_client.post("/api/v1/shorten", json={"url": invalid_url})
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Business rule: Missing URL field should return 422
        response = await test_client.post("/api/v1/shorten", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Business rule: Non-existent short codes should return 404
        response = await test_client.get("/nonexistent123", follow_redirects=False)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = await test_client.get("/api/v1/stats/nonexistent123")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_data_consistency_rules(self, test_client):
        """Test business rules for data consistency."""
        # Create a short URL
        response = await test_client.post(
            "/api/v1/shorten", json={"url": "https://example.com/consistency-test"}
        )
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        short_code = data["short_code"]
        original_url = data["original_url"]

        # Business rule: Stats should be consistent with creation data
        stats_response = await test_client.get(f"/api/v1/stats/{short_code}")
        assert stats_response.status_code == status.HTTP_200_OK

        stats_data = stats_response.json()
        assert stats_data["short_code"] == short_code
        assert stats_data["original_url"] == original_url

        # Business rule: Visit count should be non-negative
        assert stats_data["visit_count"] >= 0

    @pytest.mark.asyncio
    async def test_performance_rules(self, test_client):
        """Test business rules for performance expectations."""
        import time

        # Business rule: URL creation should be fast
        start_time = time.time()
        response = await test_client.post(
            "/api/v1/shorten", json={"url": "https://example.com/performance-test"}
        )
        end_time = time.time()

        assert response.status_code == status.HTTP_200_OK
        assert (end_time - start_time) < 2.0  # Should complete within 2 seconds

        # Business rule: Stats retrieval should be fast
        data = response.json()
        short_code = data["short_code"]

        start_time = time.time()
        stats_response = await test_client.get(f"/api/v1/stats/{short_code}")
        end_time = time.time()

        assert stats_response.status_code == status.HTTP_200_OK
        assert (end_time - start_time) < 1.0  # Should complete within 1 second
