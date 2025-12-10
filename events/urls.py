"""URL configuration for events app."""

from django.urls import path

from events import views

app_name = "events"

urlpatterns = [
    path("<slug:slug>/", views.event_detail, name="event_detail"),
    path("<slug:slug>/topics/load-more/", views.load_more_topics, name="load_more_topics"),
]
