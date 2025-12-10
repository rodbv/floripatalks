"""
Event models for FloripaTalks.
"""

from django.db import models

from core.models import BaseModel


class Event(BaseModel):
    """
    Represents a recurring event series (e.g., Python Floripa).

    Inherits from BaseModel for UUID v6 primary key and timestamps.
    """

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name
