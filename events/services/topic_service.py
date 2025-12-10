"""
Topic service for business logic related to topics.
"""

from events.dto.topic_dto import TopicDTO
from events.models import Event, Topic


class TopicService:
    """Service for topic-related business logic."""

    @staticmethod
    def get_topics_for_event(event_slug: str, offset: int = 0, limit: int = 20) -> list[TopicDTO]:
        event = Event.objects.get(slug=event_slug)
        topics = (
            Topic.objects.filter(event=event)
            .select_related("event", "creator")
            .order_by("-vote_count", "created_at")[offset : offset + limit]
        )

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
