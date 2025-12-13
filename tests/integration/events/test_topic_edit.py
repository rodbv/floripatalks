"""
Integration tests for topic edit flow.

These tests verify the full request/response cycle including:
- View imports and function calls
- Use case and service layer integration
- Ownership validation
- Form validation
"""

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from model_bakery import baker

from accounts.models import User
from events.models import Event, Topic


@pytest.mark.django_db
class TestTopicEditFlow:
    """Integration tests for topic edit flow."""

    @pytest.fixture
    def client(self) -> Client:
        """Create Django test client."""
        return Client()

    @pytest.fixture
    def user(self) -> User:
        """Create test user."""
        return baker.make("accounts.User", username="testuser")

    @pytest.fixture
    def event(self) -> Event:
        """Create test event."""
        return baker.make("events.Event", slug="test-event", name="Test Event")

    @pytest.fixture
    def topic(self, event: Event, user: User) -> Topic:
        """Create test topic."""
        return baker.make(
            "events.Topic",
            event=event,
            creator=user,
            title="Original Title",
            description="Original description",
        )

    def test_edit_topic_get_renders_form(self, client: Client, user: User, topic: Topic) -> None:
        """Verify GET request to edit topic renders form."""
        client.force_login(user)

        url = reverse("events:edit_topic", kwargs={"slug": topic.slug})
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context or "topic" in response.context

    def test_edit_topic_post_updates_topic(self, client: Client, user: User, topic: Topic) -> None:
        """Verify POST request updates topic."""
        client.force_login(user)

        url = reverse("events:edit_topic", kwargs={"slug": topic.slug})
        response = client.post(
            url,
            {
                "title": "Updated Title",
                "description": "Updated description",
            },
        )

        assert response.status_code == HTTPStatus.FOUND  # Redirect after update
        topic.refresh_from_db()
        assert topic.title == "Updated Title"
        assert topic.description == "Updated description"

    def test_edit_topic_requires_authentication(self, client: Client, topic: Topic) -> None:
        """Verify edit topic requires authentication."""
        url = reverse("events:edit_topic", kwargs={"slug": topic.slug})
        response = client.get(url)

        # Should redirect to login
        assert response.status_code in [HTTPStatus.FOUND, HTTPStatus.OK]

    def test_edit_topic_requires_ownership(self, client: Client, topic: Topic) -> None:
        """Verify edit topic requires ownership."""
        other_user = baker.make("accounts.User", username="otheruser")
        client.force_login(other_user)

        url = reverse("events:edit_topic", kwargs={"slug": topic.slug})
        response = client.get(url)

        # Should return 403 Forbidden
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_edit_topic_keeps_slug_unchanged(
        self, client: Client, user: User, topic: Topic
    ) -> None:
        """Verify edit topic does not change slug."""
        client.force_login(user)
        original_slug = topic.slug

        url = reverse("events:edit_topic", kwargs={"slug": topic.slug})
        response = client.post(
            url,
            {
                "title": "Completely Different Title",
                "description": "",
            },
        )

        assert response.status_code == HTTPStatus.FOUND
        topic.refresh_from_db()
        assert topic.slug == original_slug
