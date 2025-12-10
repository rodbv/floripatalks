"""
Django admin configuration for events app.
"""

from django.contrib import admin
from django.db.models import Count, QuerySet
from django.http import HttpRequest

from events.models import Event, Topic, Vote


class TopicInline(admin.TabularInline):
    """Inline admin for Topic model within Event admin."""

    model = Topic
    extra = 0
    fields = ["title", "slug", "creator", "is_deleted", "created_at"]
    readonly_fields = ["title", "slug", "creator", "is_deleted", "created_at"]
    can_delete = False
    show_change_link = True
    verbose_name = "Tópico"
    verbose_name_plural = "Tópicos"


class VoteInline(admin.TabularInline):
    """Inline admin for Vote model within Topic admin."""

    model = Vote
    extra = 0
    fields = ["user", "created_at"]
    readonly_fields = ["user", "created_at"]
    can_delete = True
    can_add = False
    can_change = False
    verbose_name = "Voto"
    verbose_name_plural = "Votos"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for Event model."""

    list_display = ["name", "slug", "topic_count", "created_at", "updated_at"]
    verbose_name = "Evento"
    verbose_name_plural = "Eventos"
    list_filter = ["created_at", "updated_at"]
    search_fields = ["name", "slug", "description"]
    readonly_fields = ["id", "created_at", "updated_at"]
    inlines = [TopicInline]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Event]:
        """Annotate queryset with topic count."""
        qs = super().get_queryset(request)
        return qs.annotate(_topic_count=Count("topics", distinct=True))

    @admin.display(
        description="Total de Tópicos",
        ordering="_topic_count",
    )
    def topic_count(self, obj: Event) -> int:
        """Display total topic count for the event."""
        return getattr(obj, "_topic_count", 0)

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

    list_display = ["title", "slug", "event", "creator", "vote_count", "is_deleted", "created_at"]
    verbose_name = "Tópico"
    verbose_name_plural = "Tópicos"
    list_filter = ["is_deleted", "created_at", "event"]
    search_fields = ["title", "slug", "description", "event__name", "creator__username"]
    readonly_fields = ["id", "created_at", "updated_at"]
    inlines = [VoteInline]
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
        """Use all_objects to access deleted records in admin and annotate vote count."""
        qs = self.model.all_objects.get_queryset()
        qs = qs.annotate(_vote_count=Count("votes", distinct=True))
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    @admin.display(
        description="Total de Votos",
        ordering="_vote_count",
    )
    def vote_count(self, obj: Topic) -> int:
        """Display total vote count for the topic."""
        return getattr(obj, "_vote_count", 0)
