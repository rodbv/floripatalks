"""
Use case for unvoting on a topic.
"""

from typing import TYPE_CHECKING

from events.services.vote_service import unvote_topic as unvote_topic_service

if TYPE_CHECKING:
    from accounts.models import User


def unvote_topic(topic_slug: str, user: "User") -> bool:
    """
    Unvote on a topic (remove vote).

    Args:
        topic_slug: The slug of the topic to unvote
        user: The user unvoting

    Returns:
        True if vote was deleted successfully

    Raises:
        Topic.DoesNotExist: If topic with given slug doesn't exist
        Vote.DoesNotExist: If user hasn't voted on this topic
    """
    return unvote_topic_service(topic_slug=topic_slug, user=user)
