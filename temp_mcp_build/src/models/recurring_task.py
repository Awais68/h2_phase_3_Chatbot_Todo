"""
RecurringTask model for recurring task management.
"""
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class RecurringTask(SQLModel, table=True):
    """
    RecurringTask model for managing recurring tasks.

    Attributes:
        id: Unique identifier (auto-increment)
        user_id: Foreign key to user who owns this recurring task
        title: Task title
        description: Optional detailed description
        frequency: Recurrence frequency ('daily', 'weekly', 'monthly')
        frequency_value: Optional frequency value (e.g., day of week, day of month)
        is_active: Whether the recurring task is active
        last_generated: Timestamp when the last task instance was generated
        created_at: Timestamp when recurring task was created
        updated_at: Timestamp when recurring task was last modified
    """
    __tablename__ = "recurring_tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default="", max_length=1000)
    frequency: str = Field(max_length=20)  # 'daily', 'weekly', 'monthly'
    frequency_value: Optional[int] = Field(default=None)  # Day of week (0-6) or day of month (1-31)
    is_active: bool = Field(default=True)
    last_generated: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class RecurringTaskCreate(SQLModel):
    """Schema for creating a new recurring task."""
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default="", max_length=1000)
    frequency: str  # 'daily', 'weekly', 'monthly'
    frequency_value: Optional[int] = None


class RecurringTaskUpdate(SQLModel):
    """Schema for updating a recurring task."""
    title: Optional[str] = Field(default=None, max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=1000)
    frequency: Optional[str] = Field(default=None)
    frequency_value: Optional[int] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)


class RecurringTaskResponse(SQLModel):
    """Schema for recurring task response."""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    frequency: str
    frequency_value: Optional[int]
    is_active: bool
    last_generated: Optional[datetime]
    created_at: datetime
    updated_at: datetime
