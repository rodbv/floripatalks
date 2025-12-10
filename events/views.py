"""
Views for events app.
"""

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render

from core.decorators import require_authentication
from events.models import Event, Topic, Vote
from events.use_cases.get_event_topics import get_event_topics
from events.use_cases.unvote_topic import unvote_topic
from events.use_cases.vote_topic import vote_topic


def event_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Display event detail page with topics list.

    Args:
        request: HTTP request object
        slug: Event slug

    Returns:
        HTTP response with event detail page
    """
    event = get_object_or_404(Event, slug=slug)
    topics = get_event_topics(slug, offset=0, limit=20, user=request.user)

    context = {
        "event": event,
        "topics": topics,
    }

    return render(request, "events/event_detail.html", context)


def load_more_topics(request: HttpRequest, slug: str) -> HttpResponse:
    """
    HTMX endpoint to load more topics for infinite scroll.

    Args:
        request: HTTP request object (should have HX-Request header)
        slug: Event slug

    Returns:
        HTTP response with partial HTML fragment of topics
    """
    if not request.htmx:
        return HttpResponseNotFound()

    event = get_object_or_404(Event, slug=slug)
    offset = int(request.GET.get("offset", 0))
    limit = 20

    topics = get_event_topics(slug, offset=offset, limit=limit, user=request.user)

    context = {
        "event": event,
        "topics": topics,
        "offset": offset,
    }

    return render(request, "events/partials/topic_list_fragment.html", context)


@require_authentication
def vote_topic_view(request: HttpRequest, slug: str) -> HttpResponse:
    """
    HTMX endpoint to vote or unvote on a topic.

    Toggles between vote and unvote:
    - If user hasn't voted: creates a vote
    - If user has voted: removes the vote (unvote)

    Args:
        request: HTTP request object (should have HX-Request header and be authenticated)
        slug: Topic slug

    Returns:
        HTTP response with vote button partial HTML fragment
    """
    if not request.htmx:
        return HttpResponseNotFound()

    topic = get_object_or_404(Topic, slug=slug)

    # Check if user has already voted
    has_voted = Vote.objects.filter(topic=topic, user=request.user).exists()

    if has_voted:
        # Unvote
        unvote_topic(topic_slug=slug, user=request.user)
    else:
        # Vote
        vote_topic(topic_slug=slug, user=request.user)

    # Refresh vote status
    has_voted = Vote.objects.filter(topic=topic, user=request.user).exists()
    vote_count = Vote.objects.filter(topic=topic).count()

    context = {
        "topic": topic,
        "has_voted": has_voted,
        "vote_count": vote_count,
    }

    return render(request, "events/partials/vote_button.html", context)
