"""
Unit tests for utility functions.
"""

import pytest

from app.utils.client_ip import extract_client_ip


class TestUtils:
    """Test utility functions."""

    def test_extract_client_ip_function_exists(self):
        """Test that extract_client_ip function exists."""
        assert callable(extract_client_ip)

    def test_extract_client_ip_import(self):
        """Test that extract_client_ip can be imported."""
        from app.utils.client_ip import extract_client_ip

        assert extract_client_ip is not None

    def test_utils_module_import(self):
        """Test that utils module can be imported."""
        from app.utils import client_ip

        assert client_ip is not None

    def test_utils_init_import(self):
        """Test that utils __init__ can be imported."""
        from app.utils import __init__

        assert __init__ is not None

    def test_short_code_regex_exists(self):
        """Test that SHORT_CODE_RE regex exists."""
        from app.utils.client_ip import SHORT_CODE_RE

        assert SHORT_CODE_RE is not None
        assert hasattr(SHORT_CODE_RE, "pattern")
