"""
Event models for FloripaTalks.
"""

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from core.models import BaseModel, SoftDeleteModel


class Event(BaseModel):
    """
    Represents a recurring event series (e.g., Python Floripa).

    Inherits from BaseModel for UUID v6 primary key and timestamps.
    """

    name = models.CharField("Nome", max_length=200)
    slug = models.SlugField("Slug", unique=True, max_length=100)
    description = models.TextField("Descrição", blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self) -> str:
        return self.name


class Topic(SoftDeleteModel):
    """
    Represents a suggested talk topic for an event.

    Inherits from SoftDeleteModel for UUID v6 primary key, timestamps, and soft delete.
    """

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="topics", verbose_name="Evento"
    )
    slug = models.SlugField("Slug", unique=True, max_length=200)
    title = models.CharField("Título", max_length=200)
    description = models.TextField("Descrição", max_length=2000, blank=True, null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_topics",
        verbose_name="Criador",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Tópico"
        verbose_name_plural = "Tópicos"
        indexes = [
            models.Index(fields=["event", "is_deleted", "created_at"]),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args: object, **kwargs: object) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
            base_slug = self.slug
            counter = 1
            while Topic.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
