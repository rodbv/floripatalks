from events.dto.topic_dto import TopicDTO
from events.services.topic_service import get_topics_for_event as get_topics_for_event_service


def get_event_topics(event_slug: str, offset: int = 0, limit: int = 20) -> list[TopicDTO]:
    return get_topics_for_event_service(event_slug, offset, limit)
