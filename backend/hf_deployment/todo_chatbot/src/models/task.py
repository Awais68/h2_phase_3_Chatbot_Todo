"""
Task model migrated to SQLModel with PostgreSQL support.
"""
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    """Task entity for todo items."""

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # Removed foreign_key constraint for demo users
    title: str = Field(max_length=200, min_length=1)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    # Due date support
    due_date: Optional[datetime] = Field(default=None)
    # Recurrence support
    recurrence_pattern: Optional[str] = Field(default=None)
    is_recurring: bool = Field(default=False)
    reminder_minutes: int = Field(default=15)
    next_occurrence: Optional[datetime] = Field(default=None)
    # Offline sync support
    client_id: Optional[str] = Field(default=None, max_length=100, index=True)
    version: int = Field(default=1)

    __table_args__ = {"extend_existing": True}

    def validate_due_date(self):
        """Validate due date constraints."""
        if self.due_date and self.due_date < datetime.utcnow():
            # Allow past due dates for existing tasks, but log a warning
            pass  # For now, just allow it

    def validate_recurrence(self):
        """Validate recurrence constraints."""
        if self.recurrence_pattern and not self.due_date:
            raise ValueError("Recurring tasks must have a due date")
        if self.recurrence_pattern and self.recurrence_pattern not in ['daily', 'weekly', 'monthly', 'yearly']:
            raise ValueError(f"Invalid recurrence pattern: {self.recurrence_pattern}")


class TaskCreate(SQLModel):
    """Schema for creating a new task."""

    title: str = Field(max_length=200, min_length=1)
    description: str = Field(default="", max_length=1000)
    due_date: Optional[datetime] = Field(default=None)
    client_id: Optional[str] = Field(default=None, max_length=100)


class TaskUpdate(SQLModel):
    """Schema for updating a task."""

    title: Optional[str] = Field(default=None, max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)


class TaskResponse(SQLModel):
    """Schema for task response."""

    id: int
    user_id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None
    client_id: Optional[str] = None
    version: int
