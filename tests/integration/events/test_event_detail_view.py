"""
Integration tests for event detail view.

These tests verify the full request/response cycle including:
- View imports and function calls
- Use case and service layer integration
- Template rendering
- URL routing

This helps catch regressions like import errors, NoneType errors, and template issues.
"""

import pytest
from django.test import Client
from django.urls import reverse
from model_bakery import baker


@pytest.mark.django_db
class TestEventDetailView:
    """Integration tests for event detail view."""

    @pytest.fixture
    def client(self) -> Client:
        """Create Django test client."""
        return Client()

    def test_event_detail_view_returns_200_for_valid_slug(self, client: Client) -> None:
        """Verify event detail view returns 200 for valid event slug."""
        event = baker.make("events.Event", slug="test-event", name="Test Event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, _quantity=3)

        url = reverse("events:event_detail", kwargs={"slug": "test-event"})
        response = client.get(url)

        assert response.status_code == 200

    def test_event_detail_view_returns_404_for_invalid_slug(self, client: Client) -> None:
        """Verify event detail view returns 404 for invalid event slug."""
        url = reverse("events:event_detail", kwargs={"slug": "non-existent"})
        response = client.get(url)

        assert response.status_code == 404

    def test_event_detail_view_displays_event_name(self, client: Client) -> None:
        """Verify event detail view displays event name in template."""
        baker.make("events.Event", slug="test-event", name="Test Event")

        url = reverse("events:event_detail", kwargs={"slug": "test-event"})
        response = client.get(url)

        assert response.status_code == 200
        assert "Test Event" in response.content.decode()

    def test_event_detail_view_displays_topics(self, client: Client) -> None:
        """Verify event detail view displays topics for the event."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, title="Topic 1")
        baker.make("events.Topic", event=event, creator=user, title="Topic 2")

        url = reverse("events:event_detail", kwargs={"slug": "test-event"})
        response = client.get(url)

        assert response.status_code == 200
        content = response.content.decode()
        assert "Topic 1" in content
        assert "Topic 2" in content

    def test_event_detail_view_displays_empty_state_when_no_topics(self, client: Client) -> None:
        """Verify event detail view handles empty topics gracefully."""
        baker.make("events.Event", slug="test-event", name="Test Event")

        url = reverse("events:event_detail", kwargs={"slug": "test-event"})
        response = client.get(url)

        assert response.status_code == 200

    def test_event_detail_view_renders_without_errors(self, client: Client) -> None:
        """
        Regression test: Verify view renders without import errors or NoneType errors.

        This test would catch issues like:
        - Import errors in views/use_cases/services
        - NoneType errors from incorrect imports
        - Template rendering errors
        - Missing context variables
        """
        event = baker.make("events.Event", slug="regression-test", name="Regression Test")
        user = baker.make("accounts.User", username="testuser")
        baker.make(
            "events.Topic",
            event=event,
            creator=user,
            title="Regression Topic",
            description="Test description",
        )

        url = reverse("events:event_detail", kwargs={"slug": "regression-test"})
        response = client.get(url)

        # Should return 200, not 500
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. Error: {response.content.decode()[:500]}"
        )

        # Should render template without errors
        content = response.content.decode()
        assert "Regression Test" in content
        assert "Regression Topic" in content
        assert "testuser" in content

    def test_event_detail_view_context_contains_topics_list(self, client: Client) -> None:
        """
        Regression test: Verify view context contains topics as a list.

        This catches issues where topics might be None or wrong type.
        """
        event = baker.make("events.Event", slug="context-test")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, _quantity=2)

        url = reverse("events:event_detail", kwargs={"slug": "context-test"})
        response = client.get(url)

        assert response.status_code == 200
        # Verify topics are in context and iterable
        assert "topics" in response.context
        topics = response.context["topics"]
        assert isinstance(topics, list)
        assert len(topics) == 2
