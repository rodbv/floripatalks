"""
URL configuration for floripatalks project.
"""

from django.conf import settings
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

# Serve static files in production (Azure App Service)
# In development, Django's runserver handles this automatically
if not settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
