"""
Pytest configuration and shared fixtures.
"""

import pytest
from faker import Faker

from accounts.models import User

fake = Faker()


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
