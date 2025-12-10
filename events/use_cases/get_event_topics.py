from events.dto.topic_dto import TopicDTO
from events.services import topic_service


def get_event_topics(event_slug: str, offset: int = 0, limit: int = 20) -> list[TopicDTO]:
    return topic_service.get_topics_for_event(event_slug, offset, limit)
