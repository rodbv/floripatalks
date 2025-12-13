"""
Integration tests for topic delete flow.

These tests verify the full request/response cycle including:
- View imports and function calls
- Use case and service layer integration
- HTMX request handling
- Soft delete behavior
"""

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from model_bakery import baker

from accounts.models import User
from events.models import Event, Topic


@pytest.mark.django_db
class TestTopicDeleteFlow:
    """Integration tests for topic delete flow."""

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
        return baker.make("events.Topic", event=event, creator=user, title="Test Topic")

    def test_delete_topic_soft_deletes(self, client: Client, user: User, topic: Topic) -> None:
        """Verify delete topic soft deletes the topic."""
        client.force_login(user)

        url = reverse("events:delete_topic", kwargs={"slug": topic.slug})
        response = client.post(url, HTTP_HX_REQUEST="true")

        assert response.status_code == HTTPStatus.OK
        topic.refresh_from_db()
        assert topic.is_deleted is True
        # Topic should not appear in regular queryset
        assert not Topic.objects.filter(id=topic.id).exists()
        # Topic should appear in all_objects queryset
        assert Topic.all_objects.filter(id=topic.id).exists()

    def test_delete_topic_requires_authentication(self, client: Client, topic: Topic) -> None:
        """Verify delete topic requires authentication."""
        url = reverse("events:delete_topic", kwargs={"slug": topic.slug})
        response = client.post(url, HTTP_HX_REQUEST="true")

        # Should redirect to login (HTMX redirect)
        assert response.status_code == HTTPStatus.OK
        assert "HX-Redirect" in response.headers
        assert "/accounts/login/" in response.headers["HX-Redirect"]

    def test_delete_topic_requires_ownership(self, client: Client, topic: Topic) -> None:
        """Verify delete topic requires ownership."""
        other_user = baker.make("accounts.User", username="otheruser")
        client.force_login(other_user)

        url = reverse("events:delete_topic", kwargs={"slug": topic.slug})
        response = client.post(url, HTTP_HX_REQUEST="true")

        # Should return 403 Forbidden
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_delete_topic_returns_404_for_invalid_slug(self, client: Client, user: User) -> None:
        """Verify delete topic returns 404 for invalid topic slug."""
        client.force_login(user)

        url = reverse("events:delete_topic", kwargs={"slug": "non-existent-topic"})
        response = client.post(url, HTTP_HX_REQUEST="true")

        assert response.status_code == HTTPStatus.NOT_FOUND
