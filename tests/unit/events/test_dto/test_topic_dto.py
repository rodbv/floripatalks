"""
Unit tests for TopicDTO with N+1 query prevention verification.
"""

import pytest
from model_bakery import baker
from pytest_django.asserts import assertNumQueries

from events.dto.topic_dto import TopicDTO
from events.services.topic_service import get_topics_for_event


@pytest.mark.django_db
class TestTopicDTO:
    """Tests for TopicDTO dataclass."""

    def test_topic_dto_has_all_required_fields(self) -> None:
        """Verify TopicDTO has all required fields."""
        event = baker.make("events.Event", slug="test-event", name="Test Event")
        user = baker.make("accounts.User", username="testuser")
        topic = baker.make(
            "events.Topic",
            event=event,
            creator=user,
            slug="test-topic",
            title="Test Topic",
            description="Test description",
        )

        dto = TopicDTO(
            id=topic.id,
            slug=topic.slug,
            title=topic.title,
            description=topic.description,
            vote_count=0,
            creator_username=user.username,
            event_slug=event.slug,
            event_name=event.name,
            created_at=topic.created_at,
        )

        assert dto.id == topic.id
        assert dto.slug == "test-topic"
        assert dto.title == "Test Topic"
        assert dto.description == "Test description"
        assert dto.vote_count == 0
        assert dto.creator_username == "testuser"
        assert dto.event_slug == "test-event"
        assert dto.event_name == "Test Event"
        assert dto.created_at == topic.created_at

    def test_topic_dto_description_can_be_none(self) -> None:
        """Verify TopicDTO handles None description."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user, description=None)

        dto = TopicDTO(
            id=topic.id,
            slug=topic.slug,
            title=topic.title,
            description=None,
            vote_count=0,
            creator_username=user.username,
            event_slug=event.slug,
            event_name=event.name,
            created_at=topic.created_at,
        )

        assert dto.description is None


@pytest.mark.django_db
class TestGetTopicsForEventNPlusOnePrevention:
    """Tests to verify N+1 query prevention in get_topics_for_event."""

    def test_get_topics_for_event_single_topic_no_n_plus_one(self) -> None:
        """Verify get_topics_for_event doesn't cause N+1 queries for single topic."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user)

        with assertNumQueries(2):  # 1 for event, 1 for topics with select_related
            dtos = get_topics_for_event("test-event")

        assert len(dtos) == 1
        assert isinstance(dtos[0], TopicDTO)
        assert dtos[0].event_slug == "test-event"
        assert dtos[0].creator_username == user.username

    def test_get_topics_for_event_multiple_topics_no_n_plus_one(self) -> None:
        """Verify get_topics_for_event doesn't cause N+1 queries for multiple topics."""
        event = baker.make("events.Event", slug="test-event")
        user1 = baker.make("accounts.User")
        user2 = baker.make("accounts.User")
        user3 = baker.make("accounts.User")

        baker.make("events.Topic", event=event, creator=user1, _quantity=3)
        baker.make("events.Topic", event=event, creator=user2, _quantity=2)
        baker.make("events.Topic", event=event, creator=user3, _quantity=1)

        with assertNumQueries(2):  # 1 for event, 1 for topics with select_related
            dtos = get_topics_for_event("test-event")

        assert len(dtos) == 6
        for dto in dtos:
            assert isinstance(dto, TopicDTO)
            assert dto.event_slug == "test-event"

    def test_get_topics_for_event_without_votes_returns_zero_count(self) -> None:
        """Verify get_topics_for_event returns vote_count=0 when Vote model doesn't exist yet."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, _quantity=2)

        with assertNumQueries(2):  # 1 for event, 1 for topics with select_related
            dtos = get_topics_for_event("test-event")

        assert len(dtos) >= 2
        for dto in dtos:
            assert isinstance(dto, TopicDTO)
            assert isinstance(dto.vote_count, int)
            assert dto.vote_count == 0  # Vote model doesn't exist yet

    def test_get_topics_for_event_empty_list_no_n_plus_one(self) -> None:
        """Verify get_topics_for_event handles empty event without N+1 queries."""
        baker.make("events.Event", slug="empty-event")

        with assertNumQueries(2):  # 1 for event, 1 for topics query (empty result)
            dtos = get_topics_for_event("empty-event")

        assert len(dtos) == 0
        assert dtos == []

    def test_get_topics_for_event_pagination_no_n_plus_one(self) -> None:
        """Verify get_topics_for_event pagination doesn't cause N+1 queries."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, _quantity=25)

        with assertNumQueries(2):  # 1 for event, 1 for topics with limit
            dtos = get_topics_for_event("test-event", offset=0, limit=20)

        assert len(dtos) == 20

        with assertNumQueries(2):  # 1 for event, 1 for topics with offset/limit
            dtos = get_topics_for_event("test-event", offset=20, limit=20)

        assert len(dtos) == 5

    def test_get_topics_for_event_accesses_related_data_without_queries(self) -> None:
        """Verify accessing related data in DTOs doesn't trigger additional queries."""
        event = baker.make("events.Event", slug="test-event", name="Test Event Name")
        user = baker.make("accounts.User", username="creator")
        baker.make("events.Topic", event=event, creator=user, title="Test Topic")

        with assertNumQueries(2):  # Only the initial queries (1 for event, 1 for topics)
            dtos = get_topics_for_event("test-event")
            dto = dtos[0]

            # Accessing DTO fields should not trigger additional queries
            assert dto.event_slug == "test-event"
            assert dto.event_name == "Test Event Name"
            assert dto.creator_username == "creator"
            assert dto.title == "Test Topic"
