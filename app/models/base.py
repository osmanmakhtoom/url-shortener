"""
Base model class that combines all common mixins for convenience.
This follows service-oriented design by separating data structure from business logic.
"""

from app.models.mixins import (
    IDMixin,
    IsActiveMixin,
    SoftDeleteMixin,
    TimestampedMixin,
    UUIDMixin,
)


class BaseModel(IDMixin, UUIDMixin, TimestampedMixin, IsActiveMixin, SoftDeleteMixin):
    """
    Base model that combines all common mixins.

    This class provides the data structure but delegates business logic
    to appropriate services following service-oriented architecture.
    """

    pass
