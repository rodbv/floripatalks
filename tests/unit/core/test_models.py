"""
Unit tests for core base models.
"""

import time
import uuid

import pytest
from django.db import models
from django.utils import timezone
from faker import Faker

from core.models import BaseModel, SoftDeleteModel

fake = Faker()


# Create concrete models for testing abstract base models
# These models are only used during tests and don't require migrations
class ConcreteBaseModel(BaseModel):
    """Concrete model for testing BaseModel."""

    name = models.CharField(max_length=100)

    class Meta:
        app_label = "core"
        # Use a unique db_table to avoid conflicts
        db_table = "test_base_model"


class ConcreteSoftDeleteModel(SoftDeleteModel):
    """Concrete model for testing SoftDeleteModel."""

    name = models.CharField(max_length=100)

    class Meta:
        app_label = "core"
        # Use a unique db_table to avoid conflicts
        db_table = "test_soft_delete_model"


@pytest.mark.unit
@pytest.mark.django_db
class TestBaseModel:
    """Test BaseModel functionality."""

    def test_base_model_has_uuid_v6_primary_key(self) -> None:
        """BaseModel should use UUID v6 as primary key."""
        instance = ConcreteBaseModel.objects.create(name=fake.word())

        assert isinstance(instance.id, uuid.UUID)
        assert instance.id.version == 6

    def test_base_model_has_created_at(self) -> None:
        """BaseModel should have created_at timestamp."""
        instance = ConcreteBaseModel.objects.create(name=fake.word())

        assert instance.created_at is not None
        assert isinstance(instance.created_at, timezone.datetime)

    def test_base_model_has_updated_at(self) -> None:
        """BaseModel should have updated_at timestamp."""
        instance = ConcreteBaseModel.objects.create(name=fake.word())

        assert instance.updated_at is not None
        assert isinstance(instance.updated_at, timezone.datetime)

    def test_base_model_primary_key_is_not_editable(self) -> None:
        """BaseModel primary key should not be editable."""
        instance = ConcreteBaseModel.objects.create(name=fake.word())
        original_id = instance.id

        # Verify the field is marked as not editable
        field = ConcreteBaseModel._meta.get_field("id")
        assert field.editable is False

        # ID should be set and remain the same after save
        instance.save()
        instance.refresh_from_db()
        assert instance.id == original_id

    def test_base_model_updated_at_changes_on_save(self) -> None:
        """BaseModel updated_at should change when object is updated."""
        instance = ConcreteBaseModel.objects.create(name=fake.word())
        original_updated_at = instance.updated_at

        # Wait a bit to ensure timestamp difference
        time.sleep(0.1)

        instance.name = fake.word()
        instance.save()

        instance.refresh_from_db()
        assert instance.updated_at > original_updated_at


@pytest.mark.unit
@pytest.mark.django_db
class TestSoftDeleteModel:
    """Test SoftDeleteModel functionality."""

    def test_soft_delete_model_has_is_deleted_field(self) -> None:
        """SoftDeleteModel should have is_deleted field."""
        instance = ConcreteSoftDeleteModel.objects.create(name=fake.word())

        assert hasattr(instance, "is_deleted")
        assert instance.is_deleted is False

    def test_soft_delete_model_has_deleted_at_field(self) -> None:
        """SoftDeleteModel should have deleted_at field."""
        instance = ConcreteSoftDeleteModel.objects.create(name=fake.word())

        assert hasattr(instance, "deleted_at")
        assert instance.deleted_at is None

    def test_soft_delete_manager_filters_deleted_objects(self) -> None:
        """SoftDeleteManager should filter out deleted objects by default."""
        active = ConcreteSoftDeleteModel.objects.create(name=fake.word())
        deleted = ConcreteSoftDeleteModel.objects.create(name=fake.word())
        deleted.is_deleted = True
        deleted.deleted_at = timezone.now()
        deleted.save()

        # Default manager should only return active objects
        all_active = list(ConcreteSoftDeleteModel.objects.all())
        assert active in all_active
        assert deleted not in all_active

    def test_all_objects_manager_includes_deleted(self) -> None:
        """all_objects manager should include deleted objects."""
        active = ConcreteSoftDeleteModel.objects.create(name=fake.word())
        deleted = ConcreteSoftDeleteModel.objects.create(name=fake.word())
        deleted.is_deleted = True
        deleted.deleted_at = timezone.now()
        deleted.save()

        # all_objects should return both active and deleted
        all_objects = list(ConcreteSoftDeleteModel.all_objects.all())
        assert active in all_objects
        assert deleted in all_objects

    def test_soft_delete_method(self) -> None:
        """soft_delete() should mark object as deleted."""
        instance = ConcreteSoftDeleteModel.objects.create(name=fake.word())
        assert instance.is_deleted is False
        assert instance.deleted_at is None

        instance.soft_delete()

        instance.refresh_from_db()
        assert instance.is_deleted is True
        assert instance.deleted_at is not None

        # Should not appear in default manager
        assert instance not in ConcreteSoftDeleteModel.objects.all()
        # Should appear in all_objects
        assert instance in ConcreteSoftDeleteModel.all_objects.all()

    def test_restore_method(self) -> None:
        """restore() should restore a soft-deleted object."""
        instance = ConcreteSoftDeleteModel.objects.create(name=fake.word())
        instance.soft_delete()

        instance.refresh_from_db()
        assert instance.is_deleted is True

        instance.restore()

        instance.refresh_from_db()
        assert instance.is_deleted is False
        assert instance.deleted_at is None

        # Should appear in default manager again
        assert instance in ConcreteSoftDeleteModel.objects.all()

    def test_soft_delete_model_inherits_from_base_model(self) -> None:
        """SoftDeleteModel should inherit BaseModel fields."""
        instance = ConcreteSoftDeleteModel.objects.create(name=fake.word())

        # Should have BaseModel fields
        assert hasattr(instance, "id")
        assert hasattr(instance, "created_at")
        assert hasattr(instance, "updated_at")
        assert isinstance(instance.id, uuid.UUID)
        assert instance.id.version == 6
