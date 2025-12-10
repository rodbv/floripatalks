"""
Django admin configuration for events app.
"""

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from events.models import Event, Topic


class TopicInline(admin.TabularInline):
    """Inline admin for Topic model within Event admin."""

    model = Topic
    extra = 0
    fields = ["title", "slug", "creator", "is_deleted", "created_at"]
    readonly_fields = ["slug", "created_at"]
    show_change_link = True
    verbose_name = "Tópico"
    verbose_name_plural = "Tópicos"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for Event model."""

    list_display = ["name", "slug", "created_at", "updated_at"]
    verbose_name = "Evento"
    verbose_name_plural = "Eventos"
    list_filter = ["created_at", "updated_at"]
    search_fields = ["name", "slug", "description"]
    readonly_fields = ["id", "created_at", "updated_at"]
    inlines = [TopicInline]
    fieldsets = (
        (
            "Informações Básicas",
            {
                "fields": ("name", "slug", "description"),
            },
        ),
        (
            "Metadados",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Admin interface for Topic model."""

    list_display = ["title", "slug", "event", "creator", "is_deleted", "created_at"]
    verbose_name = "Tópico"
    verbose_name_plural = "Tópicos"
    list_filter = ["is_deleted", "created_at", "event"]
    search_fields = ["title", "slug", "description", "event__name", "creator__username"]
    readonly_fields = ["id", "created_at", "updated_at"]
    fieldsets = (
        (
            "Informações Básicas",
            {
                "fields": ("event", "title", "slug", "description", "creator"),
            },
        ),
        (
            "Exclusão Lógica",
            {
                "fields": ("is_deleted", "deleted_at"),
            },
        ),
        (
            "Metadados",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Topic]:
        """Use all_objects to access deleted records in admin."""
        qs = self.model.all_objects.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
