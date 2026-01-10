"""Voice input normalization for flexible natural language variations."""

from src.models.enums import Priority, Recurrence


class VoiceNormalizer:
    """Normalizes voice input variations to canonical enum values."""

    @staticmethod
    def normalize_priority(text: str) -> Priority:
        """Normalize priority variations to Priority enum.

        Handles flexible input like:
        - "high", "high priority", "make it high", "important", "urgent" → Priority.HIGH
        - "medium", "med", "moderate", "normal" → Priority.MEDIUM
        - "low", "minor", "low priority" → Priority.LOW
        - Anything else → Priority.NONE

        Args:
            text: Voice input text to normalize

        Returns:
            Normalized Priority enum value
        """
        if not text:
            return Priority.NONE

        text_lower = text.lower().strip()

        # High priority patterns
        high_patterns = ['high', 'important', 'urgent', 'critical', 'make it high']
        if any(pattern in text_lower for pattern in high_patterns):
            return Priority.HIGH

        # Medium priority patterns
        medium_patterns = ['medium', 'med', 'moderate', 'normal', 'regular']
        if any(pattern in text_lower for pattern in medium_patterns):
            return Priority.MEDIUM

        # Low priority patterns
        low_patterns = ['low', 'minor', 'small']
        if any(pattern in text_lower for pattern in low_patterns):
            return Priority.LOW

        # Default to NONE
        return Priority.NONE

    @staticmethod
    def normalize_recurrence(text: str) -> Recurrence:
        """Normalize recurrence variations to Recurrence enum.

        Handles flexible input like:
        - "daily", "every day", "each day" → Recurrence.DAILY
        - "weekly", "every week", "once a week" → Recurrence.WEEKLY
        - "monthly", "every month", "once a month" → Recurrence.MONTHLY
        - "none", "no", "never" → Recurrence.NONE

        Args:
            text: Voice input text to normalize

        Returns:
            Normalized Recurrence enum value
        """
        if not text:
            return Recurrence.NONE

        text_lower = text.lower().strip()

        # Daily patterns
        daily_patterns = ['daily', 'every day', 'each day', 'everyday']
        if any(pattern in text_lower for pattern in daily_patterns):
            return Recurrence.DAILY

        # Weekly patterns
        weekly_patterns = ['weekly', 'every week', 'each week', 'once a week']
        if any(pattern in text_lower for pattern in weekly_patterns):
            return Recurrence.WEEKLY

        # Monthly patterns
        monthly_patterns = ['monthly', 'every month', 'each month', 'once a month']
        if any(pattern in text_lower for pattern in monthly_patterns):
            return Recurrence.MONTHLY

        # Default to NONE
        return Recurrence.NONE

    @staticmethod
    def is_go_back_command(text: str) -> bool:
        """Check if user wants to go back to previous field.

        Args:
            text: Voice input text to check

        Returns:
            True if text indicates "go back" intent, False otherwise
        """
        if not text:
            return False

        text_lower = text.lower().strip()
        go_back_patterns = ['go back', 'back', 'previous', 'undo', 'change']

        return any(pattern in text_lower for pattern in go_back_patterns)

    @staticmethod
    def is_confirmation(text: str) -> bool:
        """Check if user is confirming.

        Args:
            text: Voice input text to check

        Returns:
            True if text indicates confirmation, False otherwise
        """
        if not text:
            return False

        text_lower = text.lower().strip()
        confirm_patterns = ['yes', 'yeah', 'yep', 'confirm', 'correct', 'good', 'ok', 'okay']

        return any(pattern in text_lower for pattern in confirm_patterns)

    @staticmethod
    def is_cancellation(text: str) -> bool:
        """Check if user is cancelling.

        Args:
            text: Voice input text to check

        Returns:
            True if text indicates cancellation, False otherwise
        """
        if not text:
            return False

        text_lower = text.lower().strip()
        cancel_patterns = ['no', 'nope', 'cancel', 'stop', 'nevermind', 'never mind']

        return any(pattern in text_lower for pattern in cancel_patterns)
