"""
Base model classes for FloripaTalks.

All models should inherit from BaseModel or SoftDeleteModel to ensure
consistency across the application.
"""

import uuid6
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Abstract base model providing UUID v6 primary key and timestamps.

    All models should inherit from this class (or SoftDeleteModel) to ensure
    consistency across the application.
    """

    id = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class SoftDeleteManager(models.Manager):
    """
    Custom manager that filters out soft-deleted objects by default.

    Use `all_objects` to access all records including soft-deleted ones.
    """

    def get_queryset(self) -> models.QuerySet:
        """Return queryset excluding soft-deleted objects."""
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(BaseModel):
    """
    Abstract base model extending BaseModel with soft delete functionality.

    Models that need soft delete (e.g., Topic, Comment, PresenterSuggestion)
    should inherit from this class.
    """

    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Custom manager that filters is_deleted=False by default
    objects = SoftDeleteManager()
    # Default manager to access all objects including soft-deleted ones
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self) -> None:
        """Mark the object as deleted without actually deleting it."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self) -> None:
        """Restore a soft-deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])
