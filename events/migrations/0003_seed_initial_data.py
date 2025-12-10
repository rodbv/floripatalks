"""
Data migration to seed initial data:
- Event: Python Floripa
- Topic: Conceitos Básicos de Pydantic (created by admin, upvoted by admin)

This migration creates the initial event and topic for the platform.
The admin user must exist (created via createsuperuser or other means).
If Vote model exists, it will also create a vote from admin on the topic.
"""

from django.conf import settings
from django.db import migrations
from django.utils.text import slugify


def create_initial_data(apps: object, schema_editor: object) -> None:
    """Create initial event and topic with admin user."""
    Event = apps.get_model("events", "Event")
    Topic = apps.get_model("events", "Topic")
    User = apps.get_model(settings.AUTH_USER_MODEL)

    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.filter(is_staff=True).first()
    if not admin_user:
        admin_user = User.objects.first()

    if not admin_user:
        print(
            "⚠️  Warning: No admin user found. Please create a superuser first using: "
            "python manage.py createsuperuser"
        )
        return

    event, created = Event.objects.get_or_create(
        slug="python-floripa",
        defaults={
            "name": "Python Floripa",
            "description": (
                "Evento mensal da comunidade Python de Florianópolis. "
                "Um espaço para compartilhar conhecimento, networking e "
                "aprender sobre Python e tecnologias relacionadas."
            ),
        },
    )

    if created:
        print(f"✅ Created event: {event.name}")

    topic_slug = slugify("Conceitos Básicos de Pydantic")
    topic, created = Topic.objects.get_or_create(
        slug=topic_slug,
        defaults={
            "event": event,
            "title": "Conceitos Básicos de Pydantic",
            "description": (
                "Uma introdução ao Pydantic, biblioteca Python para validação de dados "
                "usando type hints. Cobrindo modelos, validação, serialização e "
                "melhores práticas para uso em APIs e aplicações Python modernas."
            ),
            "creator": admin_user,
            "vote_count": 1,
        },
    )

    if created:
        print(f"✅ Created topic: {topic.title} (created by {admin_user.username})")

    try:
        Vote = apps.get_model("events", "Vote")
        vote, vote_created = Vote.objects.get_or_create(
            topic=topic,
            user=admin_user,
        )
        if vote_created:
            print(f"✅ Created vote from {admin_user.username} on topic: {topic.title}")
    except LookupError:
        print("ℹ️  Note: Vote model not found. Vote will be created when Vote model is added.")


def reverse_initial_data(apps: object, schema_editor: object) -> None:
    """Remove initial data created by this migration."""
    Event = apps.get_model("events", "Event")
    Topic = apps.get_model("events", "Topic")

    try:
        topic = Topic.objects.get(slug=slugify("Conceitos Básicos de Pydantic"))
        topic.delete()
        print("✅ Removed topic: Conceitos Básicos de Pydantic")
    except Topic.DoesNotExist:
        pass

    try:
        event = Event.objects.get(slug="python-floripa")
        event.delete()
        print("✅ Removed event: Python Floripa")
    except Event.DoesNotExist:
        pass


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0002_topic"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_initial_data),
    ]
