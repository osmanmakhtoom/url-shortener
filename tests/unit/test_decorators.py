"""
Unit tests for decorators.
"""

import pytest

from app.decorators.log_visit import log_visit


class TestDecorators:
    """Test decorator functionality."""

    def test_log_visit_decorator_exists(self):
        """Test that log_visit decorator has expected attributes."""
        # Test that it's a decorator function
        assert hasattr(log_visit, "__call__")
        assert callable(log_visit)

    def test_log_visit_decorator_simple(self):
        """Test log_visit decorator simple functionality."""
        # Test that it's a decorator function
        assert callable(log_visit)

        # Test that it can be used as a decorator
        @log_visit
        def test_endpoint():
            return {"message": "test"}

        # Test that the decorated function still works
        assert callable(test_endpoint)

    def test_decorators_module_import(self):
        """Test that decorators module can be imported."""
        from app.decorators import log_visit

        assert log_visit is not None
