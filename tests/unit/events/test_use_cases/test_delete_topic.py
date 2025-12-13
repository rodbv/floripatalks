"""
Unit tests for delete_topic use case.
"""

import pytest
from model_bakery import baker

from events.models import Topic
from events.use_cases.delete_topic import delete_topic


@pytest.mark.django_db
class TestDeleteTopic:
    """Tests for delete_topic use case function."""

    def test_delete_topic_soft_deletes_topic(self) -> None:
        """Verify delete_topic sets is_deleted=True (soft delete)."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user, is_deleted=False)

        delete_topic(user=user, topic_slug=topic.slug)

        topic.refresh_from_db()
        assert topic.is_deleted is True
        # Topic should not appear in regular queryset
        assert not Topic.objects.filter(id=topic.id).exists()
        # Topic should appear in all_objects queryset
        assert Topic.all_objects.filter(id=topic.id).exists()

    def test_delete_topic_raises_when_topic_not_found(self) -> None:
        """Verify delete_topic raises DoesNotExist for invalid topic slug."""
        user = baker.make("accounts.User")

        with pytest.raises(Topic.DoesNotExist):
            delete_topic(user=user, topic_slug="non-existent-topic")

    def test_delete_topic_raises_when_not_owner(self) -> None:
        """Verify delete_topic raises PermissionError when user is not the creator."""
        event = baker.make("events.Event")
        creator = baker.make("accounts.User")
        other_user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=creator)

        with pytest.raises(PermissionError, match="not the creator"):
            delete_topic(user=other_user, topic_slug=topic.slug)

    def test_delete_topic_does_not_hard_delete(self) -> None:
        """Verify delete_topic does not permanently delete the record."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)

        delete_topic(user=user, topic_slug=topic.slug)

        # Record should still exist in database
        assert Topic.all_objects.filter(id=topic.id).exists()
        # But should be marked as deleted
        topic.refresh_from_db()
        assert topic.is_deleted is True
