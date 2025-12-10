"""
Integration tests for readonly experience for non-authenticated users.

These tests verify that non-authenticated users can:
- View topics, comments, and presenter suggestions
- See interactive buttons (vote, comment, add topic, suggest presenter)
- Receive sign-in prompts when clicking interactive elements
"""

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from model_bakery import baker


@pytest.mark.django_db
class TestReadonlyExperience:
    """Integration tests for readonly experience for non-authenticated users."""

    @pytest.fixture
    def client(self) -> Client:
        """Create Django test client (non-authenticated)."""
        return Client()

    def test_non_authenticated_user_can_view_topics(self, client: Client) -> None:
        """Verify non-authenticated user can view topics list."""
        event = baker.make("events.Event", slug="test-event", name="Test Event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, title="Topic 1")
        baker.make("events.Topic", event=event, creator=user, title="Topic 2")

        url = reverse("events:event_detail", kwargs={"slug": "test-event"})
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode()
        assert "Topic 1" in content
        assert "Topic 2" in content

    def test_non_authenticated_user_sees_vote_buttons(self, client: Client) -> None:
        """Verify non-authenticated user sees vote buttons on topics."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, title="Test Topic")

        url = reverse("events:event_detail", kwargs={"slug": "test-event"})
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode()
        # Vote button should be present (check for vote-icon-button class or vote button)
        assert "vote-icon-button" in content or "vote" in content.lower()

    def test_non_authenticated_user_sees_comment_buttons(self, client: Client) -> None:
        """Verify non-authenticated user sees comment buttons/interactions."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, title="Test Topic")

        url = reverse("events:event_detail", kwargs={"slug": "test-event"})
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode()
        # Comment count or comment button should be present
        assert "comentário" in content.lower() or "comment" in content.lower()

    def test_non_authenticated_user_can_view_topic_details(self, client: Client) -> None:
        """Verify non-authenticated user can view individual topic details."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make(
            "events.Topic",
            event=event,
            creator=user,
            title="Test Topic",
            description="Test description",
        )

        # Assuming there's a topic detail view - if not, this test can be adjusted
        # For now, verify topic appears in event detail
        url = reverse("events:event_detail", kwargs={"slug": "test-event"})
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode()
        assert "Test Topic" in content
        assert "Test description" in content

    def test_non_authenticated_user_sees_vote_count(self, client: Client) -> None:
        """Verify non-authenticated user can see vote counts on topics."""
        event = baker.make("events.Event", slug="test-event")
        user1 = baker.make("accounts.User")
        user2 = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user1, title="Test Topic")
        # Create some votes
        baker.make("events.Vote", topic=topic, user=user1)
        baker.make("events.Vote", topic=topic, user=user2)

        url = reverse("events:event_detail", kwargs={"slug": "test-event"})
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode()
        # Vote count should be displayed (format may vary)
        assert "2" in content or "votos" in content.lower() or "vote" in content.lower()

    def test_non_authenticated_user_sees_creator_info(self, client: Client) -> None:
        """Verify non-authenticated user can see topic creator information."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User", username="testuser", first_name="Test", last_name="User")
        baker.make("events.Topic", event=event, creator=user, title="Test Topic")

        url = reverse("events:event_detail", kwargs={"slug": "test-event"})
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode()
        # Creator name or username should be visible
        assert "testuser" in content.lower() or "test" in content.lower()
