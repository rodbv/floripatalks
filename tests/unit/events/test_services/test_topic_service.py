"""
Unit tests for topic_service module.
"""

import pytest
from model_bakery import baker
from pytest_django.asserts import assertNumQueries

from events.dto.topic_dto import TopicDTO
from events.services.topic_service import get_topics_for_event


@pytest.mark.django_db
class TestGetTopicsForEvent:
    """Tests for get_topics_for_event function."""

    def test_get_topics_for_event_returns_list_of_dtos(self) -> None:
        """Verify get_topics_for_event returns a list of TopicDTO objects."""
        event = baker.make("events.Event", slug="test-event", name="Test Event")
        user = baker.make("accounts.User", username="testuser")
        baker.make("events.Topic", event=event, creator=user, title="Topic 1")
        baker.make("events.Topic", event=event, creator=user, title="Topic 2")

        dtos = get_topics_for_event("test-event")

        assert isinstance(dtos, list)
        assert len(dtos) == 2
        assert all(isinstance(dto, TopicDTO) for dto in dtos)

    def test_get_topics_for_event_returns_empty_list_for_no_topics(self) -> None:
        """Verify get_topics_for_event returns empty list when event has no topics."""
        baker.make("events.Event", slug="empty-event")

        dtos = get_topics_for_event("empty-event")

        assert dtos == []

    def test_get_topics_for_event_raises_for_invalid_slug(self) -> None:
        """Verify get_topics_for_event raises DoesNotExist for invalid event slug."""
        from events.models import Event

        with pytest.raises(Event.DoesNotExist):
            get_topics_for_event("non-existent-event")

    def test_get_topics_for_event_respects_offset_and_limit(self) -> None:
        """Verify get_topics_for_event respects offset and limit parameters."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, _quantity=25)

        # First page
        dtos = get_topics_for_event("test-event", offset=0, limit=20)
        assert len(dtos) == 20

        # Second page
        dtos = get_topics_for_event("test-event", offset=20, limit=20)
        assert len(dtos) == 5

        # Third page (empty)
        dtos = get_topics_for_event("test-event", offset=25, limit=20)
        assert len(dtos) == 0

    def test_get_topics_for_event_includes_all_dto_fields(self) -> None:
        """Verify get_topics_for_event populates all DTO fields correctly."""
        event = baker.make("events.Event", slug="test-event", name="Test Event")
        user = baker.make("accounts.User", username="testuser")
        topic = baker.make(
            "events.Topic",
            event=event,
            creator=user,
            title="Test Topic",
            description="Test description",
        )

        dtos = get_topics_for_event("test-event")

        assert len(dtos) == 1
        dto = dtos[0]
        assert dto.id == topic.id
        assert dto.slug == topic.slug
        assert dto.title == "Test Topic"
        assert dto.description == "Test description"
        assert dto.vote_count == 0  # Vote model doesn't exist yet
        assert dto.creator_username == "testuser"
        assert dto.event_slug == "test-event"
        assert dto.event_name == "Test Event"
        assert dto.created_at == topic.created_at

    def test_get_topics_for_event_no_n_plus_one_queries(self) -> None:
        """Verify get_topics_for_event doesn't cause N+1 queries."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, _quantity=10)

        with assertNumQueries(2):  # 1 for event, 1 for topics with select_related
            dtos = get_topics_for_event("test-event")

        assert len(dtos) == 10
        # Access DTO fields to ensure no additional queries
        for dto in dtos:
            _ = dto.event_name
            _ = dto.creator_username
