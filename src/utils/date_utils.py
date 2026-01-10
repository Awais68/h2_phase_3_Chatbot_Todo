"""
Date parsing utilities using dateparser for natural language support.
"""

from datetime import date
from typing import Optional
import dateparser


def parse_date(date_string: str) -> Optional[date]:
    """
    Parse natural language or ISO date string into date object.

    Args:
        date_string: Date string (e.g., "tomorrow", "next week", "2025-12-31")

    Returns:
        date object if parsing succeeds, None otherwise

    Examples:
        >>> parse_date("tomorrow")  # Returns today + 1 day
        >>> parse_date("next week")  # Returns today + 7 days
        >>> parse_date("2025-12-31")  # Returns Dec 31, 2025
        >>> parse_date("invalid")  # Returns None
    """
    if not date_string or not date_string.strip():
        return None

    # Use dateparser with settings for future dates
    parsed = dateparser.parse(
        date_string.strip(),
        settings={
            'PREFER_DATES_FROM': 'future',
            'TIMEZONE': 'UTC',
            'RETURN_AS_TIMEZONE_AWARE': False
        }
    )

    if parsed:
        return parsed.date()
    return None
