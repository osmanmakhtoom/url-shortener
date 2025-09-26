"""
Coverage tests for API module.
"""

import pytest


class TestAPIModule:
    """Test API module for coverage."""

    def test_api_module_import(self):
        """Test that api module can be imported."""
        from app.api.v1 import api

        assert api is not None

    def test_api_router_exists(self):
        """Test that the api_router object exists."""
        from app.api.v1.api import api_router

        assert api_router is not None
