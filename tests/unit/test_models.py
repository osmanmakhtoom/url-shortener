"""
Unit tests for models and mixins.
"""

from datetime import datetime

import pytest
from sqlmodel import SQLModel

from app.models.base import BaseModel
from app.models.mixins.timestamp_mixin import TimestampedMixin
from app.models.url import URL
from app.models.visit import Visit


class TestModels:
    """Test models for basic functionality."""

    def test_url_model_import(self):
        """Test that URL model can be imported."""
        assert URL is not None

    def test_visit_model_import(self):
        """Test that Visit model can be imported."""
        assert Visit is not None

    def test_base_model_import(self):
        """Test that BaseModel can be imported."""
        assert BaseModel is not None

    def test_models_have_table_attribute(self):
        """Test that models have table attribute."""
        assert hasattr(URL, "__tablename__")
        assert hasattr(Visit, "__tablename__")

    def test_models_have_fields(self):
        """Test that models have expected fields."""
        # URL model fields
        assert hasattr(URL, "id")
        assert hasattr(URL, "uuid")
        assert hasattr(URL, "original_url")
        assert hasattr(URL, "short_code")
        assert hasattr(URL, "created_at")
        assert hasattr(URL, "updated_at")
        assert hasattr(URL, "is_active")
        assert hasattr(URL, "deleted_at")

        # Visit model fields
        assert hasattr(Visit, "id")
        assert hasattr(Visit, "uuid")
        assert hasattr(Visit, "url_id")
        assert hasattr(Visit, "created_at")
        assert hasattr(Visit, "updated_at")
        assert hasattr(Visit, "is_active")
        assert hasattr(Visit, "deleted_at")

    def test_models_relationships(self):
        """Test that models have relationships."""
        # URL model relationships
        assert hasattr(URL, "visits")

        # Visit model relationships
        assert hasattr(Visit, "url")

    def test_models_are_sqlmodel_instances(self):
        """Test that models are SQLModel instances."""
        assert issubclass(URL, SQLModel)
        assert issubclass(Visit, SQLModel)

    def test_models_have_table_config(self):
        """Test that models have table configuration."""
        assert hasattr(URL, "__table__")
        assert hasattr(Visit, "__table__")


class TestTimestampMixin:
    """Test timestamp mixin functionality."""

    def test_timestamp_mixin_import(self):
        """Test that TimestampedMixin can be imported."""
        assert TimestampedMixin is not None

    def test_timestamp_mixin_instantiation(self):
        """Test that TimestampedMixin can be instantiated."""
        mixin = TimestampedMixin()
        assert mixin is not None
        assert hasattr(mixin, "created_at")
        assert hasattr(mixin, "updated_at")

    def test_timestamp_mixin_default_values(self):
        """Test that TimestampedMixin has default values."""
        mixin = TimestampedMixin()
        assert isinstance(mixin.created_at, datetime)
        assert isinstance(mixin.updated_at, datetime)

    def test_timestamp_mixin_custom_values(self):
        """Test that TimestampedMixin accepts custom values."""
        now = datetime.now()
        mixin = TimestampedMixin(created_at=now, updated_at=now)
        assert mixin.created_at == now
        assert mixin.updated_at == now

    def test_timestamp_mixin_inheritance(self):
        """Test that TimestampedMixin inherits from SQLModel."""
        assert issubclass(TimestampedMixin, SQLModel)


class TestMixins:
    """Test all mixins."""

    def test_id_mixin_import(self):
        """Test that IDMixin can be imported."""
        from app.models.mixins.id_mixin import IDMixin

        assert IDMixin is not None

    def test_is_active_mixin_import(self):
        """Test that IsActiveMixin can be imported."""
        from app.models.mixins.is_active_mixin import IsActiveMixin

        assert IsActiveMixin is not None

    def test_soft_delete_mixin_import(self):
        """Test that SoftDeleteMixin can be imported."""
        from app.models.mixins.soft_delete_mixin import SoftDeleteMixin

        assert SoftDeleteMixin is not None

    def test_uuid_mixin_import(self):
        """Test that UUIDMixin can be imported."""
        from app.models.mixins.uuid_mixin import UUIDMixin

        assert UUIDMixin is not None
