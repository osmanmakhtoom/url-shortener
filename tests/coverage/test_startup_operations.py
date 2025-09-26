"""
Coverage tests for startup operations.
"""

import logging
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.startup import lifespan, setup_logging


class TestStartupOperations:
    """Test startup operations for coverage."""

    @pytest.mark.asyncio
    async def test_lifespan_success(self):
        """Test successful lifespan context manager."""
        mock_app = MagicMock()
        with patch("app.core.startup.init_db") as mock_init_db:
            mock_init_db.return_value = None
            async with lifespan(mock_app):
                pass
            mock_init_db.assert_called_once()

    @pytest.mark.asyncio
    async def test_lifespan_db_error(self):
        """Test lifespan with database initialization error."""
        mock_app = MagicMock()
        with patch("app.core.startup.init_db") as mock_init_db:
            mock_init_db.side_effect = Exception("Database initialization error")
            with pytest.raises(Exception, match="Database initialization error"):
                async with lifespan(mock_app):
                    pass
            mock_init_db.assert_called_once()

    @pytest.mark.asyncio
    async def test_lifespan_development_mode(self):
        """Test lifespan in development mode."""
        mock_app = MagicMock()
        with (
            patch("app.core.startup.settings") as mock_settings,
            patch("app.core.startup.init_db") as mock_init_db,
        ):
            mock_settings.is_development = True
            mock_init_db.return_value = None
            async with lifespan(mock_app):
                pass
            mock_init_db.assert_called_once()

    @pytest.mark.asyncio
    async def test_lifespan_production_mode(self):
        """Test lifespan in production mode."""
        mock_app = MagicMock()
        with (
            patch("app.core.startup.settings") as mock_settings,
            patch("app.core.startup.init_db") as mock_init_db,
        ):
            mock_settings.is_development = False
            async with lifespan(mock_app):
                pass
            mock_init_db.assert_not_called()

    def test_setup_logging(self):
        """Test setup_logging function."""
        with (
            patch("app.core.startup.logging.basicConfig") as mock_basic_config,
            patch("app.core.startup.settings") as mock_settings,
        ):
            mock_settings.LOG_LEVEL = "INFO"
            mock_settings.LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            setup_logging()
            mock_basic_config.assert_called_once_with(
                level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
