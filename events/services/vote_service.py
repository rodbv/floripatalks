"""
Vote service functions for handling vote operations.
"""

from typing import TYPE_CHECKING

from django.db import IntegrityError

from events.models import Topic, Vote

if TYPE_CHECKING:
    from accounts.models import User


def vote_topic(topic_slug: str, user: "User") -> bool:
    """
    Create a vote for a topic by a user.

    Args:
        topic_slug: The slug of the topic to vote on
        user: The user voting (can be None for anonymous users)

    Returns:
        True if vote was created successfully, False if user already voted (no action)

    Raises:
        Topic.DoesNotExist: If topic with given slug doesn't exist
    """
    topic = Topic.objects.get(slug=topic_slug)

    if Vote.objects.filter(topic=topic, user=user).exists():
        return False  # Already voted, no action needed

    try:
        Vote.objects.create(topic=topic, user=user)
        return True
    except IntegrityError:
        # Handle race condition where vote was created between check and create
        return False  # Already voted, no action needed


def unvote_topic(topic_slug: str, user: "User") -> bool:
    """
    Remove a vote for a topic by a user (hard delete).

    Args:
        topic_slug: The slug of the topic to unvote
        user: The user unvoting

    Returns:
        True if vote was deleted successfully, False if user hasn't voted (no action)

    Raises:
        Topic.DoesNotExist: If topic with given slug doesn't exist
    """
    topic = Topic.objects.get(slug=topic_slug)
    try:
        vote = Vote.objects.get(topic=topic, user=user)
        vote.delete()
        return True
    except Vote.DoesNotExist:
        return False  # Not voted, no action needed


def get_user_vote_status(topic_slug: str, user: "User | None") -> bool:
    """
    Check if a user has voted on a topic.

    Args:
        topic_slug: The slug of the topic to check
        user: The user to check (can be None for anonymous users)

    Returns:
        True if user has voted, False otherwise

    Raises:
        Topic.DoesNotExist: If topic with given slug doesn't exist
    """
    if user is None:
        return False

    topic = Topic.objects.get(slug=topic_slug)
    return Vote.objects.filter(topic=topic, user=user).exists()
