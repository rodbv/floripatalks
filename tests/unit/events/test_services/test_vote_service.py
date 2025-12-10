"""
Unit tests for vote_service module.
"""

import pytest
from model_bakery import baker

from events.models import Topic, Vote
from events.services.vote_service import get_user_vote_status, unvote_topic, vote_topic


@pytest.mark.django_db
class TestVoteTopic:
    """Tests for vote_topic function."""

    def test_vote_topic_creates_vote_record(self) -> None:
        """Verify vote_topic creates a Vote record."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)

        vote_topic(topic_slug=topic.slug, user=user)

        assert Vote.objects.filter(topic=topic, user=user).exists()

    def test_vote_topic_returns_true_when_vote_created(self) -> None:
        """Verify vote_topic returns True when vote is successfully created."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)

        result = vote_topic(topic_slug=topic.slug, user=user)

        assert result is True

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


@pytest.mark.django_db
class TestUnvoteTopic:
    """Tests for unvote_topic function."""

    def test_unvote_topic_deletes_vote_record(self) -> None:
        """Verify unvote_topic hard-deletes the Vote record."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)
        vote = baker.make("events.Vote", topic=topic, user=user)

        unvote_topic(topic_slug=topic.slug, user=user)

        assert not Vote.objects.filter(id=vote.id).exists()

    def test_unvote_topic_returns_true_when_vote_deleted(self) -> None:
        """Verify unvote_topic returns True when vote is successfully deleted."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)
        baker.make("events.Vote", topic=topic, user=user)

        result = unvote_topic(topic_slug=topic.slug, user=user)

        assert result is True

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


@pytest.mark.django_db
class TestGetUserVoteStatus:
    """Tests for get_user_vote_status function."""

    def test_get_user_vote_status_returns_true_when_user_voted(self) -> None:
        """Verify get_user_vote_status returns True when user has voted."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)
        baker.make("events.Vote", topic=topic, user=user)

        result = get_user_vote_status(topic_slug=topic.slug, user=user)

        assert result is True

    def test_get_user_vote_status_returns_false_when_user_not_voted(self) -> None:
        """Verify get_user_vote_status returns False when user hasn't voted."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)

        result = get_user_vote_status(topic_slug=topic.slug, user=user)

        assert result is False

    def test_get_user_vote_status_returns_false_for_anonymous_user(self) -> None:
        """Verify get_user_vote_status returns False for anonymous users."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)

        result = get_user_vote_status(topic_slug=topic.slug, user=None)

        assert result is False

    def test_get_user_vote_status_raises_when_topic_not_found(self) -> None:
        """Verify get_user_vote_status raises DoesNotExist for invalid topic slug."""
        user = baker.make("accounts.User")

        with pytest.raises(Topic.DoesNotExist):
            get_user_vote_status(topic_slug="non-existent-topic", user=user)
