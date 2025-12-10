"""
Data migration to create default Site object with id=1.

This is required for django-allauth to work properly.
The Site object is used by allauth for OAuth redirects.
"""

from django.db import migrations


def create_default_site(apps: object, schema_editor: object) -> None:
    """Create default Site object with id=1 if it doesn't exist."""
    try:
        Site = apps.get_model("sites", "Site")
    except LookupError:
        # Sites app not available (e.g., during test migrations)
        return

    site, created = Site.objects.get_or_create(
        id=1,
        defaults={
            "domain": "localhost:8000",
            "name": "FloripaTalks",
        },
    )
    if created:
        print(f"✅ Created default Site: {site.name} (id={site.id})")
    else:
        print(f"ℹ️  Site with id=1 already exists: {site.name}")


def reverse_default_site(apps: object, schema_editor: object) -> None:
    """Remove default Site object (optional - usually not needed)."""
    Site = apps.get_model("sites", "Site")
    try:
        site = Site.objects.get(id=1)
        site.delete()
        print("✅ Removed default Site")
    except Site.DoesNotExist:
        pass


class Migration(migrations.Migration):
    """Create default Site object for django-allauth."""

    dependencies = [
        ("core", "0001_test_models"),
        # Note: sites migrations may not be in migration history yet
        # This migration will work once sites app is properly migrated
    ]

    operations = [
        migrations.RunPython(create_default_site, reverse_default_site),
    ]
