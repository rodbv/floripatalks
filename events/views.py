"""
Views for events app.
"""

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from core.decorators import require_authentication
from events.forms import TopicForm
from events.models import Event, Topic, Vote
from events.use_cases.create_topic import create_topic
from events.use_cases.delete_topic import delete_topic
from events.use_cases.edit_topic import edit_topic
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


@require_authentication
@require_http_methods(["GET", "POST"])
def create_topic_view(request: HttpRequest) -> HttpResponse:
    """
    Create a new topic.

    GET: Display topic creation form
    POST: Create topic and redirect or return HTMX partial

    Args:
        request: HTTP request object (must be authenticated)

    Returns:
        HTTP response with form (GET) or redirect/partial (POST)
    """
    # CRITICAL: Explicit authentication check (defense in depth)
    if not request.user.is_authenticated:
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden("Você precisa estar autenticado para criar tópicos.")

    event_slug = request.GET.get("event") or request.POST.get("event")
    if not event_slug:
        return HttpResponseNotFound()

    event = get_object_or_404(Event, slug=event_slug)

    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            try:
                dto = create_topic(
                    user=request.user,
                    title=form.cleaned_data["title"],
                    description=form.cleaned_data.get("description", ""),
                    event_slug=event_slug,
                )

                if request.htmx:
                    # HTMX request: return partial with new topic (cotton component)
                    # Use OOB swap to reset the form
                    topic_response = render(
                        request,
                        "events/partials/topic_item.html",
                        {
                            "topic": dto,
                            "event": event,
                            "user": request.user,
                        },
                    )
                    # Add OOB swap to reset form
                    form_html = render(
                        request,
                        "events/partials/inline_topic_form.html",
                        {
                            "form": TopicForm(initial={"event": event}),
                            "event": event,
                        },
                    ).content.decode()
                    topic_response.content += f'<div id="inline-topic-form-container" hx-swap-oob="innerHTML">{form_html}</div>'.encode()
                    return topic_response
                else:
                    # Regular request: redirect to event page
                    return redirect("events:event_detail", slug=event_slug)
            except ValueError as e:
                form.add_error(None, str(e))
        # Form validation failed or ValueError occurred
        if request.htmx and not form.is_valid():
            # Return form with errors to swap into form container
            context = {
                "form": form,
                "event": event,
            }
            response = render(request, "events/partials/inline_topic_form.html", context)
            # Set HTMX target to swap the form container
            response["HX-Retarget"] = "#inline-topic-form-container"
            response["HX-Reswap"] = "innerHTML"
            return response
    else:
        form = TopicForm(initial={"event": event})

    context = {
        "form": form,
        "event": event,
    }
    return render(request, "events/topic_form.html", context)


@require_authentication
@require_http_methods(["GET", "POST"])
def edit_topic_view(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Edit an existing topic.

    GET: Display topic edit form
    POST: Update topic and redirect

    Args:
        request: HTTP request object (must be authenticated)
        slug: Topic slug

    Returns:
        HTTP response with form (GET) or redirect (POST)
    """
    topic = get_object_or_404(Topic, slug=slug)

    # Check ownership - CRITICAL: Only creator can edit
    if topic.creator != request.user:
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden("Você não é o criador deste tópico.")

    if request.method == "POST":
        # Support both form-based and direct POST (for inline editing)
        if "title" in request.POST:
            # Direct POST from inline edit
            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()

            try:
                dto = edit_topic(
                    user=request.user,
                    topic_slug=slug,
                    title=title,
                    description=description,
                )

                if request.htmx:
                    # HTMX request: return updated topic card
                    context = {
                        "topic": dto,
                        "event": topic.event,
                        "user": request.user,
                    }
                    return render(request, "events/partials/topic_item.html", context)
                else:
                    # Regular POST: redirect to event page
                    return redirect("events:event_detail", slug=topic.event.slug)
            except (ValueError, PermissionError) as e:
                if request.htmx:
                    # Return error in HTMX response
                    from django.http import HttpResponseBadRequest

                    return HttpResponseBadRequest(str(e))
                # Fall through to form rendering with error
                form = TopicForm(request.POST, instance=topic)
                form.add_error(None, str(e))
        else:
            # Form-based POST
            form = TopicForm(request.POST, instance=topic)
            if form.is_valid():
                try:
                    edit_topic(
                        user=request.user,
                        topic_slug=slug,
                        title=form.cleaned_data["title"],
                        description=form.cleaned_data.get("description", ""),
                    )
                    # Redirect to event page after successful edit
                    return redirect("events:event_detail", slug=topic.event.slug)
                except (ValueError, PermissionError) as e:
                    form.add_error(None, str(e))
    else:
        form = TopicForm(instance=topic)

    context = {
        "form": form,
        "topic": topic,
        "event": topic.event,
    }
    return render(request, "events/topic_edit.html", context)


@require_authentication
@require_http_methods(["POST"])
def delete_topic_view(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Delete a topic (soft delete).

    POST: Soft delete topic

    Args:
        request: HTTP request object (must be authenticated and HTMX)
        slug: Topic slug

    Returns:
        HTTP response (HTMX removes element or redirects)
    """
    if not request.htmx:
        return HttpResponseNotFound()

    topic = get_object_or_404(Topic, slug=slug)

    # Check ownership - CRITICAL: Only creator can edit
    if topic.creator != request.user:
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden("Você não é o criador deste tópico.")

    try:
        delete_topic(user=request.user, topic_slug=slug)
        # Return empty string - HTMX outerHTML swap with empty string removes the target element
        # The target is "closest .topic-item" which will be removed from the DOM
        response = HttpResponse("", status=200)
        response["HX-Trigger"] = "topicDeleted"
        return response
    except PermissionError:
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden("Você não é o criador deste tópico.")
