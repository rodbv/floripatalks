"""
Integration tests for topic creation flow.

These tests verify the full request/response cycle including:
- View imports and function calls
- Use case and service layer integration
- HTMX request handling
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
class TestTopicCreationFlow:
    """Integration tests for topic creation flow."""

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

    def test_create_topic_get_renders_form(self, client: Client, user: User, event: Event) -> None:
        """Verify GET request to create topic renders form."""
        client.force_login(user)

        url = reverse("events:create_topic")
        response = client.get(url, {"event": event.slug})

        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context or "topic_form" in str(response.content)

    def test_create_topic_post_creates_topic(
        self, client: Client, user: User, event: Event
    ) -> None:
        """Verify POST request creates topic and redirects."""
        client.force_login(user)

        url = reverse("events:create_topic")
        response = client.post(
            url,
            {
                "title": "New Topic",
                "description": "Topic description",
                "event": event.slug,
            },
            HTTP_HX_REQUEST="true",
        )

        assert response.status_code == HTTPStatus.OK
        assert Topic.objects.filter(title="New Topic", creator=user).exists()

    def test_create_topic_requires_authentication(self, client: Client) -> None:
        """Verify create topic requires authentication."""
        url = reverse("events:create_topic")
        response = client.get(url)

        # Should redirect to login
        assert response.status_code in [HTTPStatus.FOUND, HTTPStatus.OK]
        if response.status_code == HTTPStatus.OK:
            # HTMX redirect
            assert "HX-Redirect" in response.headers
            assert "/accounts/login/" in response.headers["HX-Redirect"]

    def test_create_topic_validates_required_fields(
        self, client: Client, user: User, event: Event
    ) -> None:
        """Verify create topic validates required fields."""
        client.force_login(user)

        url = reverse("events:create_topic")
        response = client.post(
            url,
            {
                "title": "",  # Empty title
                "description": "",
                "event": event.slug,
            },
        )

        # Should return form with errors
        assert response.status_code == HTTPStatus.OK
        assert not Topic.objects.filter(creator=user).exists()

    def test_create_topic_validates_title_max_length(
        self, client: Client, user: User, event: Event
    ) -> None:
        """Verify create topic validates title max length."""
        client.force_login(user)

        url = reverse("events:create_topic")
        response = client.post(
            url,
            {
                "title": "A" * 201,  # Exceeds max_length=200
                "description": "",
                "event": event.slug,
            },
        )

        # Should return form with errors
        assert response.status_code == HTTPStatus.OK
        assert not Topic.objects.filter(creator=user).exists()
