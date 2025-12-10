"""
Unit tests for events models.
"""

import pytest
from django.db import IntegrityError
from model_bakery import baker

from events.models import Event, Topic


@pytest.mark.django_db
class TestEventModel:
    """Tests for Event model."""

    def test_event_has_uuid_v6_primary_key(self) -> None:
        event = baker.make("events.Event")
        assert event.id is not None
        assert str(event.id).count("-") == 4
        assert event.id.version == 6

    def test_event_primary_key_is_not_editable(self) -> None:
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
        with pytest.raises(IntegrityError):
            baker.make("events.Event", name=None)

    def test_event_has_slug_field(self) -> None:
        event = baker.make("events.Event", slug="python-floripa")
        assert event.slug == "python-floripa"

    def test_event_slug_is_unique(self) -> None:
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

        events = list(Event.objects.all())
        assert events[0].created_at >= events[1].created_at


@pytest.mark.django_db
class TestTopicModel:
    """Tests for Topic model."""

    def test_topic_has_uuid_v6_primary_key(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)
        assert topic.id is not None
        assert str(topic.id).count("-") == 4
        assert topic.id.version == 6

    def test_topic_primary_key_is_not_editable(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user)
        field = Topic._meta.get_field("id")
        assert field.editable is False

    def test_topic_has_created_at_and_updated_at(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)
        assert topic.created_at is not None
        assert topic.updated_at is not None

    def test_topic_has_is_deleted_field(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)
        assert topic.is_deleted is False

    def test_topic_has_event_foreign_key(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)
        assert topic.event == event

    def test_topic_event_is_required(self) -> None:
        user = baker.make("accounts.User")
        with pytest.raises(IntegrityError):
            baker.make("events.Topic", event=None, creator=user)

    def test_topic_has_title_field(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user, title="Django Best Practices")
        assert topic.title == "Django Best Practices"

    def test_topic_title_is_required(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        with pytest.raises(IntegrityError):
            baker.make("events.Topic", event=event, creator=user, title=None)

    def test_topic_title_max_length(self) -> None:
        field = Topic._meta.get_field("title")
        assert field.max_length == 200

    def test_topic_has_slug_field(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user, slug="django-best-practices")
        assert topic.slug == "django-best-practices"

    def test_topic_slug_is_unique(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user, slug="django-best-practices")
        with pytest.raises(IntegrityError):
            baker.make("events.Topic", event=event, creator=user, slug="django-best-practices")

    def test_topic_has_description_field(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make(
            "events.Topic",
            event=event,
            creator=user,
            description="Learn about Django best practices",
        )
        assert topic.description == "Learn about Django best practices"

    def test_topic_description_can_be_null(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user, description=None)
        assert topic.description is None

    def test_topic_description_can_be_blank(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user, description="")
        assert topic.description == ""

    def test_topic_description_max_length(self) -> None:
        field = Topic._meta.get_field("description")
        assert field.max_length == 2000

    def test_topic_has_vote_count_field(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user, vote_count=5)
        assert topic.vote_count == 5

    def test_topic_vote_count_defaults_to_zero(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)
        assert topic.vote_count == 0

    def test_topic_has_creator_foreign_key(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user)
        assert topic.creator == user

    def test_topic_creator_is_required(self) -> None:
        event = baker.make("events.Event")
        with pytest.raises(IntegrityError):
            baker.make("events.Topic", event=event, creator=None)

    def test_topic_soft_delete_manager_filters_deleted(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic1 = baker.make("events.Topic", event=event, creator=user, is_deleted=False)
        topic2 = baker.make("events.Topic", event=event, creator=user, is_deleted=True)

        topics = list(Topic.objects.all())
        assert topic1 in topics
        assert topic2 not in topics

    def test_topic_all_objects_includes_deleted(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic1 = baker.make("events.Topic", event=event, creator=user, is_deleted=False)
        topic2 = baker.make("events.Topic", event=event, creator=user, is_deleted=True)

        topics = list(Topic.all_objects.all())
        assert topic1 in topics
        assert topic2 in topics

    def test_topic_str_representation(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        topic = baker.make("events.Topic", event=event, creator=user, title="Django Best Practices")
        assert str(topic) == "Django Best Practices"

    def test_topic_ordering_by_created_at_desc(self) -> None:
        event = baker.make("events.Event")
        user = baker.make("accounts.User")
        baker.make("events.Topic", event=event, creator=user)
        baker.make("events.Topic", event=event, creator=user)

        topics = list(Topic.objects.all())
        assert topics[0].created_at >= topics[1].created_at
