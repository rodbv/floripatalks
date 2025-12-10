"""
Use case for retrieving event topics.
"""

from typing import TYPE_CHECKING

from events.dto.topic_dto import TopicDTO
from events.services.topic_service import get_topics_for_event as get_topics_for_event_service

if TYPE_CHECKING:
    from accounts.models import User


def get_event_topics(
    event_slug: str, offset: int = 0, limit: int = 20, user: "User | None" = None
) -> list[TopicDTO]:
    return get_topics_for_event_service(event_slug, offset, limit, user=user)
