"""
Integration tests for vote/unvote flow.

These tests verify the full request/response cycle including:
- View imports and function calls
- Use case and service layer integration
- HTMX request handling
- Vote state changes
"""

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from model_bakery import baker

from accounts.models import User
from events.models import Event, Topic, Vote


@pytest.mark.django_db
class TestVoteFlow:
    """Integration tests for vote/unvote flow."""

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

    def test_vote_endpoint_creates_vote(self, client: Client, user: User, topic: Topic) -> None:
        """Verify vote endpoint creates a vote when user votes."""
        client.force_login(user)

        url = reverse("events:vote_topic", kwargs={"slug": topic.slug})
        response = client.post(url, HTTP_HX_REQUEST="true")

        assert response.status_code == HTTPStatus.OK
        assert Vote.objects.filter(topic=topic, user=user).exists()

    def test_vote_endpoint_increments_vote_count(
        self, client: Client, user: User, topic: Topic
    ) -> None:
        """Verify vote endpoint increments vote count."""
        client.force_login(user)

        initial_count = Vote.objects.filter(topic=topic).count()

        url = reverse("events:vote_topic", kwargs={"slug": topic.slug})
        response = client.post(url, HTTP_HX_REQUEST="true")

        assert response.status_code == HTTPStatus.OK
        assert Vote.objects.filter(topic=topic).count() == initial_count + 1

    def test_vote_endpoint_toggles_to_unvote(
        self, client: Client, user: User, topic: Topic
    ) -> None:
        """Verify vote endpoint toggles to unvote when user has already voted."""
        client.force_login(user)
        baker.make("events.Vote", topic=topic, user=user)

        url = reverse("events:vote_topic", kwargs={"slug": topic.slug})
        response = client.post(url, HTTP_HX_REQUEST="true")

        assert response.status_code == HTTPStatus.OK
        assert not Vote.objects.filter(topic=topic, user=user).exists()

    def test_vote_endpoint_requires_authentication(self, client: Client, topic: Topic) -> None:
        """Verify vote endpoint requires authentication."""
        url = reverse("events:vote_topic", kwargs={"slug": topic.slug})
        response = client.post(url, HTTP_HX_REQUEST="true")

        # For HTMX requests, HttpResponseClientRedirect returns 200 with HX-Redirect header
        assert response.status_code == HTTPStatus.OK
        assert "HX-Redirect" in response.headers
        assert "/accounts/login/" in response.headers["HX-Redirect"]

    def test_vote_endpoint_returns_404_for_invalid_topic(self, client: Client, user: User) -> None:
        """Verify vote endpoint returns 404 for invalid topic slug."""
        client.force_login(user)

        url = reverse("events:vote_topic", kwargs={"slug": "non-existent-topic"})
        response = client.post(url, HTTP_HX_REQUEST="true")

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_vote_flow_complete_cycle(self, client: Client, user: User, topic: Topic) -> None:
        """Verify complete vote/unvote cycle works correctly."""
        client.force_login(user)

        # Initial state: no vote
        assert not Vote.objects.filter(topic=topic, user=user).exists()

        # Vote
        url = reverse("events:vote_topic", kwargs={"slug": topic.slug})
        response = client.post(url, HTTP_HX_REQUEST="true")
        assert response.status_code == HTTPStatus.OK
        assert Vote.objects.filter(topic=topic, user=user).exists()

        # Unvote
        response = client.post(url, HTTP_HX_REQUEST="true")
        assert response.status_code == HTTPStatus.OK
        assert not Vote.objects.filter(topic=topic, user=user).exists()

        # Vote again
        response = client.post(url, HTTP_HX_REQUEST="true")
        assert response.status_code == HTTPStatus.OK
        assert Vote.objects.filter(topic=topic, user=user).exists()
