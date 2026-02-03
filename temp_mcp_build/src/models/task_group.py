"""
TaskGroup model for storing grouped tasks.
"""
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON


class TaskGroup(SQLModel, table=True):
    """Task group entity for organizing related tasks."""

    __tablename__ = "task_groups"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)

    # Group information
    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    category: str = Field(max_length=50, index=True)  # shopping, work, personal, health, finance, home, learning

    # Tasks in this group
    task_ids: List[int] = Field(sa_column=Column(JSON))

    # Metadata
    color: Optional[str] = Field(default=None, max_length=7)  # Hex color for UI display
    icon: Optional[str] = Field(default=None, max_length=50)  # Icon name for UI display
    sort_order: int = Field(default=0)  # Display order

    # Statistics
    total_tasks: int = Field(default=0)
    completed_tasks: int = Field(default=0)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskGroupCreate(SQLModel):
    """Schema for creating a new task group."""

    name: str = Field(max_length=100, min_length=1)
    description: Optional[str] = Field(default=None, max_length=500)
    category: str = Field(max_length=50)
    task_ids: List[int] = []
    color: Optional[str] = Field(default=None, max_length=7)
    icon: Optional[str] = Field(default=None, max_length=50)


class TaskGroupUpdate(SQLModel):
    """Schema for updating a task group."""

    name: Optional[str] = Field(default=None, max_length=100, min_length=1)
    description: Optional[str] = Field(default=None, max_length=500)
    category: Optional[str] = Field(default=None, max_length=50)
    task_ids: Optional[List[int]] = None
    color: Optional[str] = Field(default=None, max_length=7)
    icon: Optional[str] = Field(default=None, max_length=50)
    sort_order: Optional[int] = None


class TaskGroupResponse(SQLModel):
    """Schema for task group response."""

    id: int
    user_id: int
    name: str
    description: Optional[str]
    category: str
    task_ids: List[int]
    color: Optional[str]
    icon: Optional[str]
    sort_order: int
    total_tasks: int
    completed_tasks: int
    created_at: datetime
    updated_at: datetime


class TaskGroupStats(SQLModel):
    """Schema for task group statistics."""

    group_id: int
    group_name: str
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    completion_rate: float  # Percentage 0-100
    last_activity: Optional[datetime]
