"""
Unit tests for topic_service module.
"""

import pytest
from model_bakery import baker
from pytest_django.asserts import assertNumQueries

from events.dto.topic_dto import TopicDTO
from events.models import Event, Topic
from events.services.topic_service import create_topic as create_topic_service
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
        assert dto.vote_count == 0
        assert dto.has_voted is False
        assert dto.creator_username == "testuser"
        assert dto.creator_display_name == "testuser"  # Falls back to username
        assert dto.creator_avatar_url is None  # No social account in test
        assert dto.event_slug == "test-event"
        assert dto.event_name == "Test Event"
        assert dto.created_at == topic.created_at

    def test_get_topics_for_event_no_n_plus_one_queries(self) -> None:
        """Verify get_topics_for_event doesn't cause N+1 queries."""
        event = baker.make("events.Event", slug="test-event")
        # Create multiple different users to test N+1 prevention
        users = baker.make("accounts.User", _quantity=10)
        # Create topics with different creators to ensure prefetch works
        for user in users:
            baker.make("events.Topic", event=event, creator=user)

        with assertNumQueries(
            3
        ):  # 1 for event, 1 for topics with select_related, 1 for social accounts prefetch
            dtos = get_topics_for_event("test-event")

        assert len(dtos) == 10
        # Access DTO fields to ensure no additional queries
        for dto in dtos:
            _ = dto.event_name
            _ = dto.creator_username
            _ = dto.creator_display_name
            _ = dto.creator_avatar_url
            _ = dto.has_voted


@pytest.mark.django_db
class TestCreateTopicService:
    """Tests for create_topic service function."""

    def test_create_topic_creates_topic_with_slug(self) -> None:
        """Verify create_topic creates a topic with generated slug."""
        baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")

        dto = create_topic_service(
            user=user,
            title="Test Topic",
            description="Test description",
            event_slug="test-event",
        )

        assert dto.slug == "test-topic"
        topic = Topic.objects.get(slug=dto.slug)
        assert topic.title == "Test Topic"
        assert topic.description == "Test description"
        assert topic.creator == user
        assert topic.event.slug == "test-event"

    def test_create_topic_generates_unique_slug(self) -> None:
        """Verify create_topic generates unique slug when duplicate exists."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, slug="test-topic")

        dto = create_topic_service(
            user=user,
            title="Test Topic",
            description="",
            event_slug="test-event",
        )

        # Should append counter to make unique
        assert dto.slug.startswith("test-topic")
        assert dto.slug != "test-topic"
        topic = Topic.objects.get(slug=dto.slug)
        assert topic.title == "Test Topic"

    def test_create_topic_raises_when_event_not_found(self) -> None:
        """Verify create_topic raises DoesNotExist for invalid event slug."""
        user = baker.make("accounts.User")

        with pytest.raises(Event.DoesNotExist):
            create_topic_service(
                user=user,
                title="Test Topic",
                description="",
                event_slug="non-existent-event",
            )

    def test_create_topic_returns_dto(self) -> None:
        """Verify create_topic returns TopicDTO."""
        baker.make("events.Event", slug="test-event", name="Test Event")
        user = baker.make("accounts.User", username="testuser")

        dto = create_topic_service(
            user=user,
            title="Test Topic",
            description="Test description",
            event_slug="test-event",
        )

        assert isinstance(dto, TopicDTO)
        assert dto.title == "Test Topic"
        assert dto.description == "Test description"
        assert dto.creator_username == "testuser"
        assert dto.event_slug == "test-event"
        assert dto.event_name == "Test Event"


@pytest.mark.django_db
class TestSlugGenerationUniqueness:
    """Tests for slug generation uniqueness in topic service."""

    def test_slug_generation_handles_duplicates(self) -> None:
        """Verify slug generation handles duplicate slugs by appending counter."""
        baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")

        # Create first topic
        dto1 = create_topic_service(
            user=user,
            title="Test Topic",
            description="",
            event_slug="test-event",
        )
        assert dto1.slug == "test-topic"

        # Create second topic with same title
        dto2 = create_topic_service(
            user=user,
            title="Test Topic",
            description="",
            event_slug="test-event",
        )
        assert dto2.slug == "test-topic-1"

        # Create third topic with same title
        dto3 = create_topic_service(
            user=user,
            title="Test Topic",
            description="",
            event_slug="test-event",
        )
        assert dto3.slug == "test-topic-2"

    def test_slug_generation_handles_multiple_duplicates(self) -> None:
        """Verify slug generation handles multiple duplicates correctly."""
        baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")

        # Create multiple topics with same title
        slugs = []
        for _ in range(5):
            dto = create_topic_service(
                user=user,
                title="Duplicate Title",
                description="",
                event_slug="test-event",
            )
            slugs.append(dto.slug)

        # All slugs should be unique
        assert len(slugs) == len(set(slugs))
        # First should be base slug
        assert "duplicate-title" in slugs
        # Others should have counters
        assert any("-1" in slug for slug in slugs)
        assert any("-2" in slug for slug in slugs)

    def test_slug_generation_preserves_special_characters(self) -> None:
        """Verify slug generation handles special characters correctly."""
        baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")

        dto = create_topic_service(
            user=user,
            title="Advanced Django ORM & Best Practices!",
            description="",
            event_slug="test-event",
        )

        # Slug should be lowercase, spaces to hyphens, special chars removed
        assert "advanced" in dto.slug
        assert "django" in dto.slug
        assert "orm" in dto.slug
        assert "&" not in dto.slug
        assert "!" not in dto.slug
        assert " " not in dto.slug
