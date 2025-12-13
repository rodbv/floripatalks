"""
URL configuration for floripatalks project.
"""

from contextlib import suppress

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import include, path

from events.models import Event


def home(request: HttpRequest) -> HttpResponse:
    """
    Home page displaying list of events.

    Shows all available events as clickable links for easy navigation.
    """
    events = Event.objects.all().order_by("-created_at")
    context = {"events": events}
    return render(request, "home.html", context)


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),
    path("accounts/", include("accounts.urls")),
    # django-allauth URLs
    path("accounts/", include("allauth.urls")),
]

# Hot reload for development only (django-browser-reload)
# Only add if DEBUG is True and the package is installed
with suppress(Exception):
    from django.conf import settings

    if settings.DEBUG:
        with suppress(ImportError):
            urlpatterns += [
                path("__reload__/", include("django_browser_reload.urls")),
            ]

# WhiteNoise handles static file serving in production
# No need for static() helper - WhiteNoise middleware serves files automatically
