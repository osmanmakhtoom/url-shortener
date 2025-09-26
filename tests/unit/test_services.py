"""
Unit tests for service classes.
"""

import string

import pytest

from app.services.short_code_factory import (
    HexHashGenerator,
    RandomAlphaNumGenerator,
    ShortCodeFactory,
)


class TestShortCodeFactory:
    """Test short code factory functionality."""

    def test_create_random_generator(self):
        """Test creating random generator."""
        generator = ShortCodeFactory.create("random")
        assert isinstance(generator, RandomAlphaNumGenerator)

    def test_create_hex_generator(self):
        """Test creating hex generator."""
        generator = ShortCodeFactory.create("hex")
        assert isinstance(generator, HexHashGenerator)

    def test_create_default_generator(self):
        """Test creating default generator."""
        generator = ShortCodeFactory.create("unknown")
        assert isinstance(generator, RandomAlphaNumGenerator)

    def test_random_generator_generate(self):
        """Test random generator generate method."""
        generator = RandomAlphaNumGenerator()
        short_code = generator.generate()
        assert isinstance(short_code, str)
        assert len(short_code) == 6
        assert short_code.isalnum()

    def test_random_generator_custom_length(self):
        """Test random generator with custom length."""
        generator = RandomAlphaNumGenerator()
        short_code = generator.generate(length=8)
        assert isinstance(short_code, str)
        assert len(short_code) == 8
        assert short_code.isalnum()

    def test_hex_generator_generate(self):
        """Test hex generator generate method."""
        generator = HexHashGenerator()
        short_code = generator.generate()
        assert isinstance(short_code, str)
        assert len(short_code) == 6
        assert all(c in string.hexdigits for c in short_code)

    def test_hex_generator_custom_length(self):
        """Test hex generator with custom length."""
        generator = HexHashGenerator()
        short_code = generator.generate(length=10)
        assert isinstance(short_code, str)
        assert len(short_code) == 10
        assert all(c in string.hexdigits for c in short_code)

    def test_generate_multiple_codes(self):
        """Test generating multiple unique codes."""
        generator = RandomAlphaNumGenerator()
        codes = [generator.generate() for _ in range(10)]
        assert len(set(codes)) == 10
        for code in codes:
            assert len(code) == 6
            assert code.isalnum()


class TestBaseService:
    """Test base service functionality."""

    @pytest.mark.asyncio
    async def test_ensure_redis_connection_fallback(self):
        """Test ensure_redis_connection fallback path."""
        from unittest.mock import AsyncMock, MagicMock

        from app.services.base import BaseService

        service = BaseService()
        # Mock redis without ensure_connection method
        service.redis = MagicMock()
        service.redis.connect = AsyncMock()
        # Remove ensure_connection method to trigger fallback
        del service.redis.ensure_connection

        await service.ensure_redis_connection()
        service.redis.connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_commit_or_rollback_no_session(self):
        """Test commit_or_rollback with no session."""
        from app.services.base import BaseService

        service = BaseService(session=None)
        # Should return without error
        await service.commit_or_rollback()

    @pytest.mark.asyncio
    async def test_commit_or_rollback_rollback_failure(self):
        """Test commit_or_rollback with rollback failure."""
        from unittest.mock import AsyncMock

        from app.services.base import BaseService

        service = BaseService()
        mock_session = AsyncMock()
        mock_session.is_active = True
        mock_session.commit.side_effect = Exception("Commit failed")
        mock_session.rollback.side_effect = Exception("Rollback failed")
        service.session = mock_session

        with pytest.raises(Exception, match="Commit failed"):
            await service.commit_or_rollback()

    @pytest.mark.asyncio
    async def test_commit_or_rollback_inactive_session(self):
        """Test commit_or_rollback with inactive session."""
        from unittest.mock import AsyncMock

        from app.services.base import BaseService

        service = BaseService()
        mock_session = AsyncMock()
        mock_session.is_active = False
        mock_session.commit.side_effect = Exception("Commit failed")
        service.session = mock_session

        with pytest.raises(Exception, match="Commit failed"):
            await service.commit_or_rollback()

    @pytest.mark.asyncio
    async def test_cache_methods(self):
        """Test cache methods."""
        from unittest.mock import AsyncMock

        from app.services.base import BaseService

        service = BaseService()
        service.redis = AsyncMock()
        service.redis.get.return_value = "test_value"
        service.redis.set.return_value = True
        service.redis.incr.return_value = 1

        # Test cache_get
        result = await service.cache_get("test_key")
        assert result == "test_value"

        # Test cache_set
        result = await service.cache_set("test_key", "test_value", 3600)
        assert result is True

        # Test cache_incr
        result = await service.cache_incr("test_key")
        assert result == 1
