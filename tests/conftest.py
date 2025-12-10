"""
Pytest configuration and shared fixtures.
"""

import pytest
from faker import Faker

from accounts.models import User

fake = Faker()


# User fixtures
@pytest.fixture
def user_factory() -> type[User]:
    """Factory fixture for creating User instances."""
    return User


@pytest.fixture
def sample_user(user_factory: type[User]) -> User:
    """Create a sample user for testing."""
    return user_factory.objects.create_user(
        username=fake.user_name(),
        email=fake.email(),
        password="testpass123",
    )


@pytest.fixture
def sample_superuser(user_factory: type[User]) -> User:
    """Create a sample superuser for testing."""
    return user_factory.objects.create_superuser(
        username=fake.user_name(),
        email=fake.email(),
        password="testpass123",
    )


# Event fixtures (will be available once Event model is created)
# These fixtures are defined here but will only work after Event model exists
@pytest.fixture
def event_factory() -> type | None:
    """
    Factory fixture for creating Event instances.

    Note: This fixture will only work after Event model is created.
    Returns the Event model class when available.
    """
    try:
        from events.models import Event

        return Event
    except ImportError:
        pytest.skip("Event model not yet created")
        return None


@pytest.fixture
def sample_event(event_factory: type | None) -> object:
    """
    Create a sample event for testing.

    Note: This fixture will only work after Event model is created.
    """
    if event_factory is None:
        pytest.skip("Event model not yet created")

    return event_factory.objects.create(
        name="Python Floripa",
        slug="python-floripa",
        description="Evento mensal da comunidade Python de Florianópolis",
    )
