"""
Shared utility functions for FloripaTalks.

This module contains common utility functions used across the application.
"""


def format_number_pt_br(number: int) -> str:
    """
    Format a number using Portuguese (pt-BR) formatting conventions.

    Formats numbers with thousands separator (.) without abbreviations.
    Example: 1234 -> "1.234", 567 -> "567"

    Args:
        number: The number to format

    Returns:
        Formatted number string in pt-BR format

    Examples:
        >>> format_number_pt_br(1234)
        '1.234'
        >>> format_number_pt_br(567)
        '567'
        >>> format_number_pt_br(1234567)
        '1.234.567'
    """
    return f"{number:,}".replace(",", ".")


def format_vote_count(count: int) -> str:
    """
    Format vote count for display in pt-BR.

    Args:
        count: The vote count

    Returns:
        Formatted string with "voto" or "votos" in pt-BR

    Examples:
        >>> format_vote_count(1)
        '1 voto'
        >>> format_vote_count(1234)
        '1.234 votos'
    """
    formatted = format_number_pt_br(count)
    plural = "votos" if count != 1 else "voto"
    return f"{formatted} {plural}"


def format_comment_count(count: int) -> str:
    """
    Format comment count for display in pt-BR.

    Args:
        count: The comment count

    Returns:
        Formatted string with "comentário" or "comentários" in pt-BR

    Examples:
        >>> format_comment_count(1)
        '1 comentário'
        >>> format_comment_count(567)
        '567 comentários'
    """
    formatted = format_number_pt_br(count)
    plural = "comentários" if count != 1 else "comentário"
    return f"{formatted} {plural}"
