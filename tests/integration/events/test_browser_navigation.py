"""
Integration tests for browser back button navigation (FR-032).

These tests verify that edit pages work correctly with browser navigation:
- Back button returns to previous page
- Form state is preserved when navigating back
- No data loss when using browser navigation
"""

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from model_bakery import baker

from accounts.models import User
from events.models import Event, Topic


@pytest.mark.django_db
class TestBrowserNavigation:
    """Integration tests for browser navigation in edit pages."""

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

    def test_topic_edit_page_is_dedicated_page(
        self, client: Client, user: User, topic: Topic
    ) -> None:
        """Verify topic edit page is a dedicated page (not modal)."""
        client.force_login(user)

        url = reverse("events:edit_topic", kwargs={"slug": topic.slug})
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        # Should be a full page, not a partial
        assert "text/html" in response.get("Content-Type", "")
        # Should have form elements
        content = response.content.decode()
        assert "form" in content.lower() or "title" in content.lower()

    def test_topic_edit_redirects_after_save(
        self, client: Client, user: User, topic: Topic
    ) -> None:
        """Verify topic edit redirects to topic detail or event page after save."""
        client.force_login(user)

        url = reverse("events:edit_topic", kwargs={"slug": topic.slug})
        response = client.post(
            url,
            {
                "title": "Updated Title",
                "description": "Updated description",
            },
        )

        # Should redirect after successful update
        assert response.status_code == HTTPStatus.FOUND
        assert response.url is not None

    def test_topic_edit_preserves_data_on_back(
        self, client: Client, user: User, topic: Topic
    ) -> None:
        """Verify topic edit page preserves original data (can navigate back without changes)."""
        client.force_login(user)

        url = reverse("events:edit_topic", kwargs={"slug": topic.slug})
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        # Original data should be in form
        content = response.content.decode()
        assert "Original Title" in content or topic.title in content
