"""
Unit tests for create_topic use case.
"""

import pytest
from model_bakery import baker

from events.models import Event, Topic
from events.use_cases.create_topic import create_topic


@pytest.mark.django_db
class TestCreateTopic:
    """Tests for create_topic use case function."""

    def test_create_topic_creates_topic(self) -> None:
        """Verify create_topic creates a topic with correct fields."""
        baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")

        dto = create_topic(
            user=user,
            title="Test Topic",
            description="Test description",
            event_slug="test-event",
        )

        assert dto.title == "Test Topic"
        assert dto.description == "Test description"
        assert dto.event_slug == "test-event"
        assert Topic.objects.filter(slug=dto.slug, creator=user).exists()

    def test_create_topic_generates_slug_from_title(self) -> None:
        """Verify create_topic generates slug from title."""
        baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")

        dto = create_topic(
            user=user,
            title="Advanced Django ORM",
            description="",
            event_slug="test-event",
        )

        assert dto.slug == "advanced-django-orm"
        topic = Topic.objects.get(slug=dto.slug)
        assert topic.title == "Advanced Django ORM"

    def test_create_topic_handles_duplicate_slugs(self) -> None:
        """Verify create_topic handles duplicate slugs by appending counter."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, slug="test-topic")

        dto = create_topic(
            user=user,
            title="Test Topic",
            description="",
            event_slug="test-event",
        )

        assert dto.slug in ["test-topic-1", "test-topic-2"]  # Counter appended
        topic = Topic.objects.get(slug=dto.slug)
        assert topic.title == "Test Topic"

    def test_create_topic_raises_when_event_not_found(self) -> None:
        """Verify create_topic raises DoesNotExist for invalid event slug."""
        user = baker.make("accounts.User")

        with pytest.raises(Event.DoesNotExist):
            create_topic(
                user=user,
                title="Test Topic",
                description="",
                event_slug="non-existent-event",
            )

    def test_create_topic_returns_dto_with_all_fields(self) -> None:
        """Verify create_topic returns DTO with all required fields."""
        baker.make("events.Event", slug="test-event", name="Test Event")
        user = baker.make("accounts.User", username="testuser")

        dto = create_topic(
            user=user,
            title="Test Topic",
            description="Test description",
            event_slug="test-event",
        )

        assert dto.id is not None
        assert dto.slug is not None
        assert dto.title == "Test Topic"
        assert dto.description == "Test description"
        assert dto.vote_count == 0
        assert dto.has_voted is False
        assert dto.creator_username == "testuser"
        assert dto.event_slug == "test-event"
        assert dto.event_name == "Test Event"
        assert dto.created_at is not None
