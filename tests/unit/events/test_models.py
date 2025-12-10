"""
Unit tests for events models.
"""

import pytest
from model_bakery import baker


@pytest.mark.django_db
class TestEventModel:
    """Tests for Event model."""

    def test_event_has_uuid_v6_primary_key(self) -> None:
        event = baker.make("events.Event")
        assert event.id is not None
        assert str(event.id).count("-") == 4
        assert event.id.version == 6

    def test_event_primary_key_is_not_editable(self) -> None:
        from events.models import Event

        baker.make("events.Event")
        field = Event._meta.get_field("id")
        assert field.editable is False

    def test_event_has_created_at_and_updated_at(self) -> None:
        event = baker.make("events.Event")
        assert event.created_at is not None
        assert event.updated_at is not None

    def test_event_has_name_field(self) -> None:
        event = baker.make("events.Event", name="Python Floripa")
        assert event.name == "Python Floripa"

    def test_event_name_is_required(self) -> None:
        from django.db import IntegrityError

        with pytest.raises(IntegrityError):
            baker.make("events.Event", name=None)

    def test_event_has_slug_field(self) -> None:
        event = baker.make("events.Event", slug="python-floripa")
        assert event.slug == "python-floripa"

    def test_event_slug_is_unique(self) -> None:
        from django.db import IntegrityError

        baker.make("events.Event", slug="python-floripa")
        with pytest.raises(IntegrityError):
            baker.make("events.Event", slug="python-floripa")

    def test_event_has_description_field(self) -> None:
        event = baker.make("events.Event", description="Monthly Python meetup")
        assert event.description == "Monthly Python meetup"

    def test_event_description_can_be_null(self) -> None:
        event = baker.make("events.Event", description=None)
        assert event.description is None

    def test_event_description_can_be_blank(self) -> None:
        event = baker.make("events.Event", description="")
        assert event.description == ""

    def test_event_str_representation(self) -> None:
        event = baker.make("events.Event", name="Python Floripa")
        assert str(event) == "Python Floripa"

    def test_event_ordering_by_created_at_desc(self) -> None:
        baker.make("events.Event")
        baker.make("events.Event")
        from events.models import Event

        events = list(Event.objects.all())
        assert events[0].created_at >= events[1].created_at
