"""
RecurrenceCalculator: Calculate next occurrence for recurring tasks.

This module provides date calculation logic for recurring tasks with support
for 5 recurrence patterns: daily, weekly, bi-weekly, monthly, and yearly.

Uses dateutil.relativedelta for smart month/year handling that automatically
handles edge cases like Feb 31 → Feb 28/29.
"""

from datetime import datetime, timedelta
from typing import Optional
from dateutil.relativedelta import relativedelta


class RecurrencePattern:
    """Enumeration of supported recurrence patterns."""
    DAILY = "daily"
    WEEKLY = "weekly"
    BI_WEEKLY = "bi-weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

    @classmethod
    def all_patterns(cls) -> list[str]:
        """Return list of all valid recurrence patterns."""
        return [cls.DAILY, cls.WEEKLY, cls.BI_WEEKLY, cls.MONTHLY, cls.YEARLY]

    @classmethod
    def is_valid(cls, pattern: str) -> bool:
        """Check if a pattern string is valid."""
        return pattern in cls.all_patterns()


class RecurrenceCalculator:
    """
    Calculate next occurrence for recurring tasks.

    This calculator handles all supported recurrence patterns and automatically
    manages edge cases like month-end dates.

    Example usage:
        calculator = RecurrenceCalculator()
        next_date = calculator.calculate_next_occurrence(
            current_due=datetime(2026, 1, 31, 10, 0, 0),
            pattern="monthly"
        )
        # Returns: datetime(2026, 2, 28, 10, 0, 0) - last day of February
    """

    @staticmethod
    def calculate_next_occurrence(
        current_due: datetime,
        pattern: str
    ) -> datetime:
        """
        Calculate next occurrence based on recurrence pattern.

        Args:
            current_due: Current due date (must be timezone-aware)
            pattern: Recurrence pattern (daily/weekly/bi-weekly/monthly/yearly)

        Returns:
            Next occurrence datetime with same timezone as current_due

        Raises:
            ValueError: If pattern is invalid or current_due is not timezone-aware

        Examples:
            >>> from datetime import datetime
            >>> import pytz
            >>> utc = pytz.UTC
            >>> calc = RecurrenceCalculator()

            >>> # Daily pattern
            >>> calc.calculate_next_occurrence(
            ...     datetime(2026, 2, 5, 10, 0, 0, tzinfo=utc),
            ...     "daily"
            ... )
            datetime(2026, 2, 6, 10, 0, 0, tzinfo=<UTC>)

            >>> # Monthly pattern with edge case (Jan 31 → Feb 28)
            >>> calc.calculate_next_occurrence(
            ...     datetime(2026, 1, 31, 10, 0, 0, tzinfo=utc),
            ...     "monthly"
            ... )
            datetime(2026, 2, 28, 10, 0, 0, tzinfo=<UTC>)
        """
        # Validate input
        if not pattern:
            raise ValueError("Recurrence pattern cannot be empty")

        if not RecurrencePattern.is_valid(pattern):
            raise ValueError(
                f"Unknown recurrence pattern: {pattern}. "
                f"Valid patterns: {RecurrencePattern.all_patterns()}"
            )

        if not current_due:
            raise ValueError("current_due cannot be None")

        if current_due.tzinfo is None:
            raise ValueError("current_due must be timezone-aware")

        # Calculate based on pattern
        if pattern == RecurrencePattern.DAILY:
            return current_due + timedelta(days=1)

        elif pattern == RecurrencePattern.WEEKLY:
            return current_due + timedelta(days=7)

        elif pattern == RecurrencePattern.BI_WEEKLY:
            return current_due + timedelta(days=14)

        elif pattern == RecurrencePattern.MONTHLY:
            # Use dateutil.relativedelta for smart month handling
            # Automatically handles edge cases:
            # - Jan 31 + 1 month = Feb 28/29 (last day of February)
            # - Feb 28 + 1 month = Mar 28 (stays on 28th)
            # - Dec 15 + 1 month = Jan 15 next year
            return current_due + relativedelta(months=1)

        elif pattern == RecurrencePattern.YEARLY:
            # Use dateutil.relativedelta for smart year handling
            # Handles leap year edge case:
            # - Feb 29, 2024 + 1 year = Feb 28, 2025 (not a leap year)
            return current_due + relativedelta(years=1)

        # Should never reach here due to validation above
        raise ValueError(f"Unexpected pattern: {pattern}")

    @staticmethod
    def calculate_multiple_occurrences(
        start_date: datetime,
        pattern: str,
        count: int
    ) -> list[datetime]:
        """
        Calculate multiple future occurrences.

        Args:
            start_date: Starting due date (must be timezone-aware)
            pattern: Recurrence pattern
            count: Number of future occurrences to calculate

        Returns:
            List of future occurrence datetimes

        Raises:
            ValueError: If inputs are invalid or count is negative

        Example:
            >>> from datetime import datetime
            >>> import pytz
            >>> calc = RecurrenceCalculator()
            >>> dates = calc.calculate_multiple_occurrences(
            ...     start_date=datetime(2026, 2, 1, 10, 0, 0, tzinfo=pytz.UTC),
            ...     pattern="weekly",
            ...     count=3
            ... )
            >>> len(dates)
            3
            >>> dates[0]  # First occurrence
            datetime(2026, 2, 8, 10, 0, 0, tzinfo=<UTC>)
        """
        if count < 0:
            raise ValueError("count must be non-negative")

        if count == 0:
            return []

        occurrences = []
        current = start_date

        for _ in range(count):
            next_occurrence = RecurrenceCalculator.calculate_next_occurrence(
                current,
                pattern
            )
            occurrences.append(next_occurrence)
            current = next_occurrence

        return occurrences

    @staticmethod
    def get_pattern_description(pattern: str) -> str:
        """
        Get human-readable description of a recurrence pattern.

        Args:
            pattern: Recurrence pattern string

        Returns:
            Human-readable description

        Example:
            >>> RecurrenceCalculator.get_pattern_description("weekly")
            'Weekly (every 7 days)'
            >>> RecurrenceCalculator.get_pattern_description("monthly")
            'Monthly (same day each month)'
        """
        descriptions = {
            RecurrencePattern.DAILY: "Daily (every day)",
            RecurrencePattern.WEEKLY: "Weekly (every 7 days)",
            RecurrencePattern.BI_WEEKLY: "Bi-weekly (every 14 days)",
            RecurrencePattern.MONTHLY: "Monthly (same day each month)",
            RecurrencePattern.YEARLY: "Yearly (same date each year)"
        }

        return descriptions.get(pattern, f"Unknown pattern: {pattern}")

    @staticmethod
    def calculate_occurrences_until(
        start_date: datetime,
        pattern: str,
        end_date: datetime,
        max_count: int = 100
    ) -> list[datetime]:
        """
        Calculate all occurrences between start_date and end_date.

        Args:
            start_date: Starting due date (must be timezone-aware)
            pattern: Recurrence pattern
            end_date: End date boundary (must be timezone-aware)
            max_count: Maximum number of occurrences to return (safety limit)

        Returns:
            List of occurrence datetimes up to end_date

        Raises:
            ValueError: If inputs are invalid

        Example:
            >>> from datetime import datetime
            >>> import pytz
            >>> utc = pytz.UTC
            >>> calc = RecurrenceCalculator()
            >>> dates = calc.calculate_occurrences_until(
            ...     start_date=datetime(2026, 2, 1, 10, 0, 0, tzinfo=utc),
            ...     pattern="weekly",
            ...     end_date=datetime(2026, 3, 1, 10, 0, 0, tzinfo=utc)
            ... )
            >>> len(dates)  # 4 weeks in February
            4
        """
        if end_date <= start_date:
            return []

        occurrences = []
        current = start_date
        count = 0

        while count < max_count:
            next_occurrence = RecurrenceCalculator.calculate_next_occurrence(
                current,
                pattern
            )

            if next_occurrence > end_date:
                break

            occurrences.append(next_occurrence)
            current = next_occurrence
            count += 1

        return occurrences
