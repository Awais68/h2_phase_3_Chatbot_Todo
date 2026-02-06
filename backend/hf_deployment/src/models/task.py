"""
Task model migrated to SQLModel with PostgreSQL support.

Extended for 012-advanced-todo-features with due dates, recurrence, and reminders.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, JSON


class RecurrencePattern(str, Enum):
    """Recurrence pattern enumeration for recurring tasks."""
    DAILY = "daily"
    WEEKLY = "weekly"
    BI_WEEKLY = "bi-weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Task(SQLModel, table=True):
    """Task entity for todo items."""

    __tablename__ = "tasks"

    # Existing fields from 001-todo-ai-chatbot
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # Removed foreign_key constraint for demo users
    title: str = Field(max_length=200, min_length=1)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    # Offline sync support
    client_id: Optional[str] = Field(default=None, max_length=100, index=True)
    version: int = Field(default=1)

    # NEW FIELDS for 012-advanced-todo-features (due dates, recurrence, reminders)
    due_date: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
        description="Task deadline in UTC timezone"
    )
    recurrence_pattern: Optional[RecurrencePattern] = Field(
        default=None,
        description="Recurrence type: daily/weekly/bi-weekly/monthly/yearly"
    )
    is_recurring: bool = Field(
        default=False,
        description="Whether task auto-creates next instance on completion"
    )
    reminder_minutes: int = Field(
        default=15,
        ge=0,
        le=1440,  # Max 24 hours
        description="Minutes before due_date to send reminder (0-1440)"
    )
    next_occurrence: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
        description="Auto-calculated next due date for recurring tasks"
    )
    
    # Subitems stored as JSON
    subitems: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Task subitems/checklist stored as JSON array"
    )

    def validate_due_date(self) -> None:
        """
        Validate due date constraints.

        Raises:
            ValueError: If due_date is not timezone-aware
        """
        if self.due_date and self.due_date.tzinfo is None:
            raise ValueError("due_date must be timezone-aware (UTC)")

    def validate_recurrence(self) -> None:
        """
        Validate recurrence configuration.

        Raises:
            ValueError: If recurrence settings are invalid
        """
        if self.is_recurring and not self.recurrence_pattern:
            raise ValueError("is_recurring requires recurrence_pattern to be set")
        if self.is_recurring and not self.due_date:
            raise ValueError("Recurring tasks must have a due_date")
        if self.recurrence_pattern and not self.is_recurring:
            # Auto-set is_recurring if pattern is set
            self.is_recurring = True

    def calculate_next_occurrence(self) -> datetime:
        """
        Calculate next occurrence for recurring tasks.

        Returns:
            Next occurrence datetime in UTC

        Raises:
            ValueError: If not a recurring task or missing due_date
        """
        if not self.is_recurring or not self.due_date or not self.recurrence_pattern:
            raise ValueError("Can only calculate next occurrence for recurring tasks")

        from ..utils.recurrence_calculator import RecurrenceCalculator

        return RecurrenceCalculator.calculate_next_occurrence(
            self.due_date,
            self.recurrence_pattern.value
        )


class TaskCreate(SQLModel):
    """Schema for creating a new task."""

    title: str = Field(max_length=200, min_length=1)
    description: str = Field(default="", max_length=1000)
    client_id: Optional[str] = Field(default=None, max_length=100)


class TaskUpdate(SQLModel):
    """Schema for updating a task."""

    title: Optional[str] = Field(default=None, max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)
    subitems: Optional[List[Dict[str, Any]]] = Field(default=None)


class TaskResponse(SQLModel):
    """Schema for task response."""

    id: int
    user_id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    client_id: Optional[str] = None
    version: int

    # NEW FIELDS for 012-advanced-todo-features
    due_date: Optional[datetime] = None
    recurrence_pattern: Optional[RecurrencePattern] = None
    is_recurring: bool = False
    reminder_minutes: int = 15
    next_occurrence: Optional[datetime] = None
    subitems: Optional[List[Dict[str, Any]]] = None
