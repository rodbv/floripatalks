# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models

from .models import AppUser, Talk, TalkVote


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "linkedin_url", "avatar")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "linkedin_url", "avatar")}),
    )
    list_display = UserAdmin.list_display + ("date_of_birth", "linkedin_url", "avatar")


class TalkVoteInline(admin.TabularInline):
    model = TalkVote
    extra = 0
    fields = ("user", "vote", "created_at")
    readonly_fields = ("created_at",)
    can_delete = True


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at", "upvotes_count")
    list_filter = ("created_at",)
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    list_per_page = 25
    list_max_show_all = 100
    inlines = [TalkVoteInline]

    def upvotes_count(self, obj):
        return obj.votes.aggregate(total=models.Sum("vote"))["total"] or 0

    upvotes_count.short_description = "Net Upvotes"
