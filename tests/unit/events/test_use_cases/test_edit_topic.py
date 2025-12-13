"""
Unit tests for edit_topic use case.
"""

import pytest
from model_bakery import baker

from events.models import Topic
from events.use_cases.edit_topic import edit_topic


@pytest.mark.django_db
class TestEditTopic:
    """Tests for edit_topic use case function."""

    def test_edit_topic_updates_topic(self) -> None:
        """Verify edit_topic updates topic fields."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make(
            "events.Topic",
            event=event,
            creator=user,
            title="Original Title",
            description="Original description",
        )
        original_slug = topic.slug

        dto = edit_topic(
            user=user,
            topic_slug=topic.slug,
            title="Updated Title",
            description="Updated description",
        )

        topic.refresh_from_db()
        assert topic.title == "Updated Title"
        assert topic.description == "Updated description"
        assert topic.slug == original_slug  # Slug should remain unchanged
        assert dto.title == "Updated Title"
        assert dto.description == "Updated description"

    def test_edit_topic_keeps_slug_immutable(self) -> None:
        """Verify edit_topic does not change slug even when title changes."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make(
            "events.Topic",
            event=event,
            creator=user,
            title="Original Title",
            slug="original-slug",
        )

        dto = edit_topic(
            user=user,
            topic_slug=topic.slug,
            title="Completely Different Title",
            description="",
        )

        topic.refresh_from_db()
        assert topic.slug == "original-slug"  # Slug unchanged
        assert dto.slug == "original-slug"

    def test_edit_topic_raises_when_topic_not_found(self) -> None:
        """Verify edit_topic raises DoesNotExist for invalid topic slug."""
        user = baker.make("accounts.User")

        with pytest.raises(Topic.DoesNotExist):
            edit_topic(
                user=user,
                topic_slug="non-existent-topic",
                title="Updated Title",
                description="",
            )

    def test_edit_topic_raises_when_not_owner(self) -> None:
        """Verify edit_topic raises PermissionError when user is not the creator."""
        event = baker.make("events.Event")
        creator = baker.make("accounts.User")
        other_user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=creator)

        with pytest.raises(PermissionError, match="not the creator"):
            edit_topic(
                user=other_user,
                topic_slug=topic.slug,
                title="Updated Title",
                description="",
            )

    def test_edit_topic_returns_dto_with_updated_fields(self) -> None:
        """Verify edit_topic returns DTO with updated fields."""
        event = baker.make("events.Event", slug="test-event", name="Test Event")
        user = baker.make("accounts.User", username="testuser")
        topic = baker.make(
            "events.Topic",
            event=event,
            creator=user,
            title="Original Title",
            description="Original description",
        )

        dto = edit_topic(
            user=user,
            topic_slug=topic.slug,
            title="Updated Title",
            description="Updated description",
        )

        assert dto.id == topic.id
        assert dto.slug == topic.slug
        assert dto.title == "Updated Title"
        assert dto.description == "Updated description"
        assert dto.event_slug == "test-event"
        assert dto.event_name == "Test Event"
