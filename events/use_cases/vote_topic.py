"""
Use case for voting on a topic.
"""

from typing import TYPE_CHECKING

from events.services.vote_service import vote_topic as vote_topic_service

if TYPE_CHECKING:
    from accounts.models import User


def vote_topic(topic_slug: str, user: "User") -> bool:
    """
    Vote on a topic.

    Args:
        topic_slug: The slug of the topic to vote on
        user: The user voting

    Returns:
        True if vote was created successfully

    Raises:
        Topic.DoesNotExist: If topic with given slug doesn't exist
        Vote.DoesNotExist: If user has already voted on this topic
    """
    return vote_topic_service(topic_slug=topic_slug, user=user)
