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
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200, min_length=1)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    # Offline sync support
    client_id: Optional[str] = Field(default=None, max_length=100, index=True)
    version: int = Field(default=1)


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
