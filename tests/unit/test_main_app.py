"""
Unit tests for main FastAPI application.
"""

import pytest
from fastapi import FastAPI


class TestMainApp:
    """Test main FastAPI application."""

    def test_main_app_import(self):
        """Test that main app can be imported."""
        from app.main import app

        assert app is not None
        assert isinstance(app, FastAPI)

    def test_main_app_title(self):
        """Test that main app has correct title."""
        from app.main import app

        assert app.title == "Shoraka URL-shortener API"

    def test_main_app_version(self):
        """Test that main app has version."""
        from app.main import app

        assert hasattr(app, "version")

    def test_main_app_routes(self):
        """Test that main app has routes."""
        from app.main import app

        assert len(app.routes) > 0

    def test_main_app_middleware(self):
        """Test that main app has middleware."""
        from app.main import app

        assert hasattr(app, "user_middleware")

    def test_main_app_openapi(self):
        """Test that main app has OpenAPI schema."""
        from app.main import app

        assert hasattr(app, "openapi")
        assert callable(app.openapi)


class TestAppImports:
    """Test app module imports."""

    def test_app_imports(self):
        """Test that app can be imported."""
        import app

        assert app is not None

    def test_app_main_import(self):
        """Test that app.main can be imported."""
        from app import main

        assert main is not None

    def test_app_core_import(self):
        """Test that app.core can be imported."""
        from app import core

        assert core is not None

    def test_app_models_import(self):
        """Test that app.models can be imported."""
        from app import models

        assert models is not None

    def test_app_services_import(self):
        """Test that app.services can be imported."""
        from app import services

        assert services is not None

    def test_app_schemas_import(self):
        """Test that app.schemas can be imported."""
        from app import schemas

        assert schemas is not None

    def test_app_api_import(self):
        """Test that app.api can be imported."""
        from app import api

        assert api is not None

    def test_app_utils_import(self):
        """Test that app.utils can be imported."""
        from app import utils

        assert utils is not None

    def test_app_decorators_import(self):
        """Test that app.decorators can be imported."""
        from app import decorators

        assert decorators is not None
