"""
Use case for creating a topic.
"""

from typing import TYPE_CHECKING

from events.dto.topic_dto import TopicDTO
from events.services.topic_service import create_topic as create_topic_service

if TYPE_CHECKING:
    from accounts.models import User


def create_topic(
    user: "User",
    title: str,
    description: str,
    event_slug: str,
) -> TopicDTO:
    """
    Create a new topic.

    Args:
        user: The user creating the topic (must be authenticated - validated by view)
        title: Topic title (max 200 characters, required)
        description: Topic description (max 2000 characters, optional)
        event_slug: Event slug to associate topic with

    Returns:
        TopicDTO with created topic data

    Raises:
        Event.DoesNotExist: If event with given slug doesn't exist
        ValidationError: If title is empty or exceeds max length
    """
    # Validation
    if not title or not title.strip():
        raise ValueError("Title is required")

    if len(title) > 200:
        raise ValueError("Title must be 200 characters or less")

    if description and len(description) > 2000:
        raise ValueError("Description must be 2000 characters or less")

    return create_topic_service(
        user=user,
        title=title.strip(),
        description=description.strip() if description else "",
        event_slug=event_slug,
    )
