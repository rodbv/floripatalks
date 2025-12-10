from django.core.exceptions import FieldError
from django.db.models import Count

from events.dto.topic_dto import TopicDTO
from events.models import Event, Topic


def get_topics_for_event(event_slug: str, offset: int = 0, limit: int = 20) -> list[TopicDTO]:
    event = Event.objects.get(slug=event_slug)
    try:
        topics = (
            Topic.objects.filter(event=event)
            .select_related("event", "creator")
            .annotate(vote_count=Count("votes"))
            .order_by("-vote_count", "created_at")[offset : offset + limit]
        )
    except FieldError:
        topics = (
            Topic.objects.filter(event=event)
            .select_related("event", "creator")
            .order_by("created_at")[offset : offset + limit]
        )
        for topic in topics:
            topic.vote_count = 0

    return [
        TopicDTO(
            id=topic.id,
            slug=topic.slug,
            title=topic.title,
            description=topic.description,
            vote_count=topic.vote_count,
            creator_username=topic.creator.username,
            event_slug=topic.event.slug,
            event_name=topic.event.name,
            created_at=topic.created_at,
        )
        for topic in topics
    ]
