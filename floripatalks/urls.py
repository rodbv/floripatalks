"""
URL configuration for floripatalks project.
"""

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import include, path


def home(_request: HttpRequest) -> HttpResponse:
    """Temporary home view for testing."""
    return HttpResponse(
        "<h1>FloripaTalks</h1><p>Servidor Django funcionando!</p><p><a href='/admin/'>Admin</a></p>"
    )


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),
    path("accounts/", include("accounts.urls")),
    # django-allauth URLs
    path("accounts/", include("allauth.urls")),
]
