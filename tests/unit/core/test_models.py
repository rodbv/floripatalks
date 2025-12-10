"""
Unit tests for core base models.
"""

import time
import uuid

import pytest
from django.utils import timezone
from model_bakery import baker

from events.models import Event, Topic


@pytest.mark.unit
@pytest.mark.django_db
class TestBaseModel:
    """Test BaseModel functionality through Event model (concrete implementation)."""

    def test_base_model_has_uuid_v6_primary_key(self) -> None:
        """BaseModel should use UUID v6 as primary key."""
        event = baker.make("events.Event")

        assert isinstance(event.id, uuid.UUID)
        assert event.id.version == 6

    def test_base_model_has_created_at(self) -> None:
        """BaseModel should have created_at timestamp."""
        event = baker.make("events.Event")

        assert event.created_at is not None
        assert isinstance(event.created_at, timezone.datetime)

    def test_base_model_has_updated_at(self) -> None:
        """BaseModel should have updated_at timestamp."""
        event = baker.make("events.Event")

        assert event.updated_at is not None
        assert isinstance(event.updated_at, timezone.datetime)

    def test_base_model_primary_key_is_not_editable(self) -> None:
        """BaseModel primary key should not be editable."""
        event = baker.make("events.Event")
        original_id = event.id

        # Verify the field is marked as not editable
        field = Event._meta.get_field("id")
        assert field.editable is False

        # ID should be set and remain the same after save
        event.save()
        event.refresh_from_db()
        assert event.id == original_id

    def test_base_model_updated_at_changes_on_save(self) -> None:
        """BaseModel updated_at should change when object is updated."""
        event = baker.make("events.Event")
        original_updated_at = event.updated_at

        # Wait a bit to ensure timestamp difference
        time.sleep(0.1)

        event.name = "Updated Name"
        event.save()

        event.refresh_from_db()
        assert event.updated_at > original_updated_at


@pytest.mark.unit
@pytest.mark.django_db
class TestSoftDeleteModel:
    """Test SoftDeleteModel functionality through Topic model (concrete implementation)."""

    def test_soft_delete_model_has_is_deleted_field(self) -> None:
        """SoftDeleteModel should have is_deleted field."""
        topic = baker.make("events.Topic")

        assert hasattr(topic, "is_deleted")
        assert topic.is_deleted is False

    def test_soft_delete_model_has_deleted_at_field(self) -> None:
        """SoftDeleteModel should have deleted_at field."""
        topic = baker.make("events.Topic")

        assert hasattr(topic, "deleted_at")
        assert topic.deleted_at is None

    def test_soft_delete_manager_filters_deleted_objects(self) -> None:
        """SoftDeleteManager should filter out deleted objects by default."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        active = baker.make("events.Topic", event=event, creator=user)
        deleted = baker.make("events.Topic", event=event, creator=user)
        deleted.is_deleted = True
        deleted.deleted_at = timezone.now()
        deleted.save()

        # Default manager should only return active objects
        all_active = list(Topic.objects.all())
        assert active in all_active
        assert deleted not in all_active

    def test_all_objects_manager_includes_deleted(self) -> None:
        """all_objects manager should include deleted objects."""
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        active = baker.make("events.Topic", event=event, creator=user)
        deleted = baker.make("events.Topic", event=event, creator=user)
        deleted.is_deleted = True
        deleted.deleted_at = timezone.now()
        deleted.save()

        # all_objects should return both active and deleted
        all_objects = list(Topic.all_objects.all())
        assert active in all_objects
        assert deleted in all_objects

    def test_soft_delete_method(self) -> None:
        """soft_delete() should mark object as deleted."""
        topic = baker.make("events.Topic")
        assert topic.is_deleted is False
        assert topic.deleted_at is None

        topic.soft_delete()

        topic.refresh_from_db()
        assert topic.is_deleted is True
        assert topic.deleted_at is not None

        # Should not appear in default manager
        assert topic not in Topic.objects.all()
        # Should appear in all_objects
        assert topic in Topic.all_objects.all()

    def test_restore_method(self) -> None:
        """restore() should restore a soft-deleted object."""
        topic = baker.make("events.Topic")
        topic.soft_delete()

        topic.refresh_from_db()
        assert topic.is_deleted is True

        topic.restore()

        topic.refresh_from_db()
        assert topic.is_deleted is False
        assert topic.deleted_at is None

        # Should appear in default manager again
        assert topic in Topic.objects.all()

    def test_soft_delete_model_inherits_from_base_model(self) -> None:
        """SoftDeleteModel should inherit BaseModel fields."""
        topic = baker.make("events.Topic")

        # Should have BaseModel fields
        assert hasattr(topic, "id")
        assert hasattr(topic, "created_at")
        assert hasattr(topic, "updated_at")
        assert isinstance(topic.id, uuid.UUID)
        assert topic.id.version == 6
