"""
Enums for the Task model.
Defines Priority, Recurrence, Status, and SortBy enums.
"""

from enum import Enum


class Priority(Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"

    def __str__(self) -> str:
        """Return string representation."""
        return self.value


class Recurrence(Enum):
    """Task recurrence patterns."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

    def __str__(self) -> str:
        """Return string representation."""
        return self.value


class Status(Enum):
    """Task status based on completion and due date."""
    PENDING = "pending"
    COMPLETED = "completed"
    OVERDUE = "overdue"

    def __str__(self) -> str:
        """Return string representation."""
        return self.value


class SortBy(Enum):
    """Sort options for task list."""
    DEFAULT = "default"
    PRIORITY = "priority"
    DUE_DATE = "due_date"
    CREATED_DATE = "created_date"

    def __str__(self) -> str:
        """Return string representation."""
        return self.value


class ConversationStep(Enum):
    """Voice conversation state machine steps."""
    IDLE = "idle"
    AWAITING_COMMAND = "awaiting_command"
    AWAITING_TITLE = "awaiting_title"
    AWAITING_PRIORITY = "awaiting_priority"
    AWAITING_DUE_DATE = "awaiting_due_date"
    AWAITING_RECURRENCE = "awaiting_recurrence"
    CONFIRMATION = "confirmation"

    def __str__(self) -> str:
        """Return string representation."""
        return self.value
