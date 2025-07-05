"""
URL configuration for floripatalks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from core.views import home

# TODO: Add Event URLs (list, detail, create, update, delete)
# TODO: Add Talk URLs (list, detail, create, update, delete)
# TODO: Add Vote URLs (create, delete)
# TODO: Add Speaker URLs (list, detail, create, update)
# TODO: Add Dashboard URL
# TODO: Add API URLs for future REST API
# TODO: Add HTMX URLs for dynamic interactions

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]
