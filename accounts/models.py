"""
Accounts models.
"""

import uuid6
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model inheriting from AbstractUser.

    Uses UUID v6 as primary key for security and sortability (time-ordered).
    """

    id = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)

    class Meta:
        """Meta options for User model."""

        db_table = "auth_user"
