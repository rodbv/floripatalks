"""
Use case for editing a topic.
"""

from typing import TYPE_CHECKING

from events.dto.topic_dto import TopicDTO
from events.models import Topic
from events.services.topic_service import update_topic as update_topic_service

if TYPE_CHECKING:
    from accounts.models import User


def edit_topic(
    user: "User",
    topic_slug: str,
    title: str,
    description: str,
) -> TopicDTO:
    """
    Edit an existing topic.

    Args:
        user: The user editing the topic (must be the creator)
        topic_slug: Slug of the topic to edit
        title: New title (max 200 characters, required)
        description: New description (max 2000 characters, optional)

    Returns:
        TopicDTO with updated topic data

    Raises:
        Topic.DoesNotExist: If topic with given slug doesn't exist
        PermissionError: If user is not the creator of the topic
        ValidationError: If title is empty or exceeds max length
    """
    # Get topic and verify ownership
    topic = Topic.objects.get(slug=topic_slug)

    # CRITICAL: Only creator can edit
    if topic.creator != user:
        raise PermissionError("User is not the creator of this topic")

    # Validation
    if not title or not title.strip():
        raise ValueError("Title is required")

    if len(title) > 200:
        raise ValueError("Title must be 200 characters or less")

    if description and len(description) > 2000:
        raise ValueError("Description must be 2000 characters or less")

    return update_topic_service(
        topic_slug=topic_slug,
        title=title.strip(),
        description=description.strip() if description else "",
    )
