"""
Migration for test models used in unit tests.

These models are only used during testing and don't affect production.
"""

import uuid6
from django.db import migrations, models


class Migration(migrations.Migration):
    """Create test models for BaseModel and SoftDeleteModel testing."""

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ConcreteBaseModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid6.uuid6,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "test_base_model",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ConcreteSoftDeleteModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid6.uuid6,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(db_index=True, default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "test_soft_delete_model",
            },
            bases=(models.Model,),
        ),
    ]
