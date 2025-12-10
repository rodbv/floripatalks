"""
Unit tests for vote_topic use case.
"""

import pytest
from model_bakery import baker

from events.models import Topic, Vote
from events.use_cases.vote_topic import vote_topic


@pytest.mark.django_db
class TestVoteTopic:
    """Tests for vote_topic use case function."""

    def test_vote_topic_creates_vote(self) -> None:
        """Verify vote_topic creates a vote for the user."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)

        result = vote_topic(topic_slug=topic.slug, user=user)

        assert result is True
        assert Vote.objects.filter(topic=topic, user=user).exists()

    def test_vote_topic_raises_when_topic_not_found(self) -> None:
        """Verify vote_topic raises DoesNotExist for invalid topic slug."""
        user = baker.make("accounts.User")

        with pytest.raises(Topic.DoesNotExist):
            vote_topic(topic_slug="non-existent-topic", user=user)

    def test_vote_topic_returns_false_for_duplicate_votes(self) -> None:
        """Verify vote_topic returns False for duplicate votes (no action, not an error)."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)

        result1 = vote_topic(topic_slug=topic.slug, user=user)
        assert result1 is True

        result2 = vote_topic(topic_slug=topic.slug, user=user)
        assert result2 is False  # Already voted, no action
