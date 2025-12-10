from typing import TYPE_CHECKING

from django.core.exceptions import FieldError
from django.db.models import Count, Exists, OuterRef

from events.dto.topic_dto import TopicDTO
from events.models import Event, Topic, Vote

if TYPE_CHECKING:
    from accounts.models import User


def get_user_avatar_url(user: "User | None") -> str | None:
    """
    Get user's avatar URL from social account if available.

    Returns None if no social account or avatar is available.

    Note: Assumes socialaccount_set is prefetched to avoid N+1 queries.
    """
    if not user or not hasattr(user, "socialaccount_set"):
        return None

    try:
        # Use all() to access prefetched data, then get first
        social_accounts = user.socialaccount_set.all()
        if social_accounts:
            return social_accounts[0].get_avatar_url()
    except Exception:
        pass

    return None


def get_user_display_name(user: "User | None") -> str:
    """
    Get user's display name, preferring first_name + last_name, falling back to username.
    """
    if not user:
        return ""

    if user.first_name or user.last_name:
        return f"{user.first_name or ''} {user.last_name or ''}".strip()

    return user.username or ""


def get_topics_for_event(
    event_slug: str, offset: int = 0, limit: int = 20, user: "User | None" = None
) -> list[TopicDTO]:
    event = Event.objects.get(slug=event_slug)

    # Check if user has voted on each topic
    has_voted_subquery = None
    if user and hasattr(user, "is_authenticated") and user.is_authenticated:
        has_voted_subquery = Exists(Vote.objects.filter(topic=OuterRef("pk"), user=user))

    try:
        topics_query = (
            Topic.objects.filter(event=event)
            .select_related("event", "creator")
            .prefetch_related("creator__socialaccount_set")
            .annotate(vote_count=Count("votes"))
        )

        if has_voted_subquery:
            topics_query = topics_query.annotate(has_voted=has_voted_subquery)

        topics = topics_query.order_by("-vote_count", "created_at")[offset : offset + limit]
    except FieldError:
        topics_query = (
            Topic.objects.filter(event=event)
            .select_related("event", "creator")
            .prefetch_related("creator__socialaccount_set")
        )

        if has_voted_subquery:
            topics_query = topics_query.annotate(has_voted=has_voted_subquery)

        topics = topics_query.order_by("created_at")[offset : offset + limit]
        for topic in topics:
            topic.vote_count = 0

    # Ensure we always return a list, even if topics is empty or None
    if not topics:
        return []

    return [
        TopicDTO(
            id=topic.id,
            slug=topic.slug,
            title=topic.title,
            description=topic.description,
            vote_count=getattr(topic, "vote_count", 0),
            has_voted=bool(getattr(topic, "has_voted", False)),
            creator_username=topic.creator.username,
            creator_display_name=get_user_display_name(topic.creator),
            creator_avatar_url=get_user_avatar_url(topic.creator),
            event_slug=topic.event.slug,
            event_name=topic.event.name,
            created_at=topic.created_at,
        )
        for topic in topics
    ]
