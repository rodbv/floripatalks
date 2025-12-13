"""URL configuration for events app."""

from django.urls import path

from events import views

app_name = "events"

urlpatterns = [
    path("<slug:slug>/", views.event_detail, name="event_detail"),
    path("<slug:slug>/topics/load-more/", views.load_more_topics, name="load_more_topics"),
    path("topics/create/", views.create_topic_view, name="create_topic"),
    path("topics/<slug:slug>/edit/", views.edit_topic_view, name="edit_topic"),
    path("topics/<slug:slug>/delete/", views.delete_topic_view, name="delete_topic"),
    path("topics/<slug:slug>/vote/", views.vote_topic_view, name="vote_topic"),
]
