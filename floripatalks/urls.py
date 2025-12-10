"""
URL configuration for floripatalks project.
"""

from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import include, path


def home(request: HttpRequest):
    """Temporary home view for testing."""
    return render(request, "home.html")


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),
    path("accounts/", include("accounts.urls")),
    # django-allauth URLs
    path("accounts/", include("allauth.urls")),
]
