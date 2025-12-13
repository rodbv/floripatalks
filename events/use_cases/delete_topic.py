"""
Use case for deleting a topic.
"""

from typing import TYPE_CHECKING

from events.models import Topic
from events.services.topic_service import soft_delete_topic as soft_delete_topic_service

if TYPE_CHECKING:
    from accounts.models import User


def delete_topic(
    user: "User",
    topic_slug: str,
) -> None:
    """
    Delete a topic (soft delete).

    Args:
        user: The user deleting the topic (must be the creator)
        topic_slug: Slug of the topic to delete

    Raises:
        Topic.DoesNotExist: If topic with given slug doesn't exist
        PermissionError: If user is not the creator of the topic
    """
    # Get topic and verify ownership - CRITICAL: Only creator can delete
    topic = Topic.objects.get(slug=topic_slug)

    if topic.creator != user:
        raise PermissionError("User is not the creator of this topic")

    soft_delete_topic_service(topic_slug=topic_slug)
