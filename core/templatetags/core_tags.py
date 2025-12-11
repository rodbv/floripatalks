"""
Custom template tags for core utilities.
"""

from django import template

from core.utils import format_comment_count as format_comment_count_util
from core.utils import format_vote_count as format_vote_count_util

register = template.Library()


@register.filter
def format_vote_count(value: int | str) -> str:
    """
    Format vote count for display in pt-BR.

    Args:
        value: Vote count (int or string)

    Returns:
        Formatted string (e.g., "1 voto" or "1.234 votos")
    """
    count = int(value) if isinstance(value, str) else value
    return format_vote_count_util(count)


@register.filter
def format_comment_count(value: int | str) -> str:
    """
    Format comment count for display in pt-BR.

    Args:
        value: Comment count (int or string)

    Returns:
        Formatted string (e.g., "1 comentário" or "567 comentários")
    """
    count = int(value) if isinstance(value, str) else value
    return format_comment_count_util(count)
