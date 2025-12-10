"""
Django admin configuration for accounts app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin interface for custom User model."""

    list_display = ["username", "email", "is_staff", "is_active", "date_joined"]
    list_filter = ["is_staff", "is_active", "date_joined"]
    search_fields = ["username", "email", "first_name", "last_name"]
    readonly_fields = ["id", "date_joined", "last_login"]
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": ("id",),
            },
        ),
    )
