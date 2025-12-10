"""
Integration tests for authentication redirects.

These tests verify that:
- Non-authenticated users are redirected to login when clicking interactive elements
- Login and signup pages are accessible
"""

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from model_bakery import baker


@pytest.mark.django_db
class TestAuthenticationRedirects:
    """Integration tests for authentication redirects."""

    @pytest.fixture
    def client(self) -> Client:
        """Create Django test client (non-authenticated)."""
        return Client()

    def test_vote_button_redirects_to_login_for_non_authenticated_user(
        self, client: Client
    ) -> None:
        """Verify clicking vote button redirects to login for non-authenticated users."""
        event = baker.make("events.Event", slug="test-event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, slug="test-topic")

        # Simulate clicking vote button with HTMX header and referrer
        # The referrer should be the event detail page (the host page)
        vote_url = reverse("events:vote_topic", kwargs={"slug": "test-topic"})
        event_url = reverse("events:event_detail", kwargs={"slug": "test-event"})
        response = client.post(
            vote_url,
            HTTP_HX_REQUEST="true",  # HTMX request header
            HTTP_REFERER=event_url,  # The page the user was viewing
        )

        # For HTMX requests, HttpResponseClientRedirect returns 200 with HX-Redirect header
        assert response.status_code == HTTPStatus.OK
        assert "HX-Redirect" in response.headers
        assert "/accounts/login/" in response.headers["HX-Redirect"]
        # The next parameter should be the referrer (event page), not the vote endpoint
        assert "next=" in response.headers["HX-Redirect"]
        assert event_url in response.headers["HX-Redirect"]

    def test_non_authenticated_user_can_access_login_page(self, client: Client) -> None:
        """Verify non-authenticated user can access login page."""
        url = reverse("account_login")
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK

    def test_non_authenticated_user_can_access_signup_page(self, client: Client) -> None:
        """Verify non-authenticated user can access signup page."""
        url = reverse("account_signup")
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
