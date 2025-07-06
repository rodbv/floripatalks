# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AppUser


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "linkedin_url", "avatar")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "linkedin_url", "avatar")}),
    )
    list_display = UserAdmin.list_display + ("date_of_birth", "linkedin_url", "avatar")
