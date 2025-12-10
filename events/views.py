"""
Views for events app.
"""

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render

from events.models import Event
from events.use_cases.get_event_topics import get_event_topics


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
    topics = get_event_topics(slug, offset=0, limit=20)

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

    topics = get_event_topics(slug, offset=offset, limit=limit)

    context = {
        "event": event,
        "topics": topics,
        "offset": offset,
    }

    return render(request, "events/partials/topic_list_fragment.html", context)
