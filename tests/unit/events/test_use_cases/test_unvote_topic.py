"""
Unit tests for unvote_topic use case.
"""

import pytest
from model_bakery import baker

from events.models import Topic, Vote
from events.use_cases.unvote_topic import unvote_topic


@pytest.mark.django_db
class TestUnvoteTopic:
    """Tests for unvote_topic use case function."""

    def test_unvote_topic_deletes_vote(self) -> None:
        """Verify unvote_topic hard-deletes the vote."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)
        vote = baker.make("events.Vote", topic=topic, user=user)

        result = unvote_topic(topic_slug=topic.slug, user=user)

        assert result is True
        assert not Vote.objects.filter(id=vote.id).exists()

    def test_unvote_topic_raises_when_topic_not_found(self) -> None:
        """Verify unvote_topic raises DoesNotExist for invalid topic slug."""
        user = baker.make("accounts.User")

        with pytest.raises(Topic.DoesNotExist):
            unvote_topic(topic_slug="non-existent-topic", user=user)

    def test_unvote_topic_returns_false_when_vote_not_found(self) -> None:
        """Verify unvote_topic returns False when user hasn't voted (no action, not an error)."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)

        result = unvote_topic(topic_slug=topic.slug, user=user)
        assert result is False  # Not voted, no action
