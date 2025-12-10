"""
Unit tests for topic_service vote status functionality.
"""

import pytest
from model_bakery import baker

from events.services.topic_service import get_topics_for_event


@pytest.mark.django_db
class TestGetTopicsForEventVoteStatus:
    """Tests for get_topics_for_event vote status functionality."""

    def test_get_topics_for_event_includes_vote_status_for_authenticated_user(
        self,
    ) -> None:
        """Verify get_topics_for_event includes has_voted field for authenticated user."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user)

        dtos = get_topics_for_event("test-event", user=user)

        assert len(dtos) == 1
        assert dtos[0].has_voted is False

    def test_get_topics_for_event_shows_voted_status_when_user_voted(
        self,
    ) -> None:
        """Verify get_topics_for_event shows has_voted=True when user has voted."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)
        baker.make("events.Vote", topic=topic, user=user)

        dtos = get_topics_for_event("test-event", user=user)

        assert len(dtos) == 1
        assert dtos[0].has_voted is True

    def test_get_topics_for_event_returns_false_for_anonymous_user(
        self,
    ) -> None:
        """Verify get_topics_for_event returns has_voted=False for anonymous users."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user)

        dtos = get_topics_for_event("test-event", user=None)

        assert len(dtos) == 1
        assert dtos[0].has_voted is False

    def test_get_topics_for_event_shows_correct_vote_status_per_user(
        self,
    ) -> None:
        """Verify get_topics_for_event shows correct vote status for each user."""
        event = baker.make("events.Event", slug="test-event")
        user1 = baker.make("accounts.User", username="user1")
        user2 = baker.make("accounts.User", username="user2")
        topic = baker.make("events.Topic", event=event, creator=user1)
        baker.make("events.Vote", topic=topic, user=user1)

        # User1 has voted
        dtos_user1 = get_topics_for_event("test-event", user=user1)
        assert dtos_user1[0].has_voted is True

        # User2 has not voted
        dtos_user2 = get_topics_for_event("test-event", user=user2)
        assert dtos_user2[0].has_voted is False
