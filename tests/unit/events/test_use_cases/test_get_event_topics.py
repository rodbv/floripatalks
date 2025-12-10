"""
Unit tests for get_event_topics use case.
"""

import pytest
from model_bakery import baker

from events.dto.topic_dto import TopicDTO
from events.use_cases.get_event_topics import get_event_topics


@pytest.mark.django_db
class TestGetEventTopics:
    """Tests for get_event_topics use case function."""

    def test_get_event_topics_returns_list_of_dtos(self) -> None:
        """Verify get_event_topics returns a list of TopicDTO objects."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, title="Topic 1")
        baker.make("events.Topic", event=event, creator=user, title="Topic 2")

        dtos = get_event_topics("test-event")

        assert isinstance(dtos, list)
        assert len(dtos) == 2
        assert all(isinstance(dto, TopicDTO) for dto in dtos)

    def test_get_event_topics_calls_service_function(self) -> None:
        """Verify get_event_topics calls the service function correctly."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, _quantity=5)

        dtos = get_event_topics("test-event", offset=0, limit=3)

        assert len(dtos) == 3

    def test_get_event_topics_respects_pagination(self) -> None:
        """Verify get_event_topics respects offset and limit parameters."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, _quantity=10)

        dtos_page1 = get_event_topics("test-event", offset=0, limit=5)
        dtos_page2 = get_event_topics("test-event", offset=5, limit=5)

        assert len(dtos_page1) == 5
        assert len(dtos_page2) == 5
        # Verify different topics
        assert dtos_page1[0].id != dtos_page2[0].id
