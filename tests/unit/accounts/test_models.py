"""
Unit tests for accounts models.
"""

import uuid

import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker

User = get_user_model()


@pytest.mark.unit
@pytest.mark.django_db
class TestUserModel:
    """Test User model."""

    def test_user_has_uuid_v6_primary_key(self, sample_user: User) -> None:
        """User model should use UUID v6 as primary key."""
        assert isinstance(sample_user.id, uuid.UUID)
        # UUID v6 has version 6 in the first nibble of the 7th byte (time-ordered like v7)
        assert sample_user.id.version == 6

    def test_user_inherits_from_abstract_user(self, sample_user: User) -> None:
        """User model should inherit from AbstractUser."""
        # AbstractUser provides these fields
        assert hasattr(sample_user, "username")
        assert hasattr(sample_user, "email")
        assert hasattr(sample_user, "first_name")
        assert hasattr(sample_user, "last_name")
        assert hasattr(sample_user, "is_staff")
        assert hasattr(sample_user, "is_active")
        assert hasattr(sample_user, "date_joined")

    def test_user_primary_key_is_not_editable(self) -> None:
        """User primary key should not be editable."""
        user = baker.make(User)
        original_id = user.id

        # Verify the field is marked as not editable in the model
        field = User._meta.get_field("id")
        assert field.editable is False

        # ID should be set and immutable
        assert user.id == original_id

    def test_user_can_be_created_with_username_and_email(self) -> None:
        """User can be created with username and email."""
        from faker import Faker

        fake = Faker()
        username = fake.user_name()
        email = fake.email()

        user = User.objects.create_user(username=username, email=email, password="testpass123")

        assert user.username == username
        assert user.email == email
        assert user.check_password("testpass123")

    def test_user_email_is_optional(self) -> None:
        """User email should be optional."""
        from faker import Faker

        fake = Faker()
        username = fake.user_name()

        user = User.objects.create_user(username=username, password="testpass123")

        assert user.username == username
        assert user.email == ""
