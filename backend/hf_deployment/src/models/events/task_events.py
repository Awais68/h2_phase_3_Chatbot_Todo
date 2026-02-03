"""
Task event schemas for event-driven architecture.

These events are published to Kafka topics for async processing,
analytics, notifications, and auditing.
"""

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class BaseTaskEvent(BaseModel):
    """Base event model for all task events."""

    event_id: UUID = Field(default_factory=uuid4, description="Unique event identifier")
    event_type: str = Field(..., description="Type of event (created, updated, deleted, completed)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    user_id: Optional[str] = Field(None, description="User who triggered the event")
    source: str = Field(default="backend", description="Event source service")
    version: str = Field(default="1.0", description="Event schema version")

    class Config:
        json_schema_extra = {
            "example": {
                "event_id": "550e8400-e29b-41d4-a716-446655440000",
                "event_type": "task.created",
                "timestamp": "2024-01-01T12:00:00Z",
                "user_id": "user_123",
                "source": "backend",
                "version": "1.0"
            }
        }


class TaskCreatedEvent(BaseTaskEvent):
    """Event published when a new task is created."""

    event_type: Literal["task.created"] = "task.created"
    task_id: str = Field(..., description="ID of the created task")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    priority: Optional[str] = Field(None, description="Task priority (low, medium, high)")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    tags: list[str] = Field(default_factory=list, description="Task tags")

    class Config:
        json_schema_extra = {
            "example": {
                "event_id": "550e8400-e29b-41d4-a716-446655440000",
                "event_type": "task.created",
                "timestamp": "2024-01-01T12:00:00Z",
                "user_id": "user_123",
                "task_id": "task_456",
                "title": "Complete project documentation",
                "description": "Write comprehensive documentation for the project",
                "priority": "high",
                "due_date": "2024-01-15T17:00:00Z",
                "tags": ["documentation", "urgent"]
            }
        }


class TaskUpdatedEvent(BaseTaskEvent):
    """Event published when a task is updated."""

    event_type: Literal["task.updated"] = "task.updated"
    task_id: str = Field(..., description="ID of the updated task")
    changes: dict = Field(..., description="Changed fields and their new values")
    previous_values: Optional[dict] = Field(None, description="Previous values of changed fields")

    class Config:
        json_schema_extra = {
            "example": {
                "event_id": "550e8400-e29b-41d4-a716-446655440000",
                "event_type": "task.updated",
                "timestamp": "2024-01-01T12:00:00Z",
                "user_id": "user_123",
                "task_id": "task_456",
                "changes": {
                    "title": "Complete comprehensive project documentation",
                    "priority": "high"
                },
                "previous_values": {
                    "title": "Complete project documentation",
                    "priority": "medium"
                }
            }
        }


class TaskDeletedEvent(BaseTaskEvent):
    """Event published when a task is deleted."""

    event_type: Literal["task.deleted"] = "task.deleted"
    task_id: str = Field(..., description="ID of the deleted task")
    task_title: str = Field(..., description="Title of the deleted task")
    soft_delete: bool = Field(default=True, description="Whether this is a soft delete")

    class Config:
        json_schema_extra = {
            "example": {
                "event_id": "550e8400-e29b-41d4-a716-446655440000",
                "event_type": "task.deleted",
                "timestamp": "2024-01-01T12:00:00Z",
                "user_id": "user_123",
                "task_id": "task_456",
                "task_title": "Obsolete task",
                "soft_delete": True
            }
        }


class TaskCompletedEvent(BaseTaskEvent):
    """Event published when a task is marked as completed."""

    event_type: Literal["task.completed"] = "task.completed"
    task_id: str = Field(..., description="ID of the completed task")
    task_title: str = Field(..., description="Title of the completed task")
    completed_at: datetime = Field(default_factory=datetime.utcnow, description="Completion timestamp")
    time_to_complete: Optional[int] = Field(None, description="Time taken to complete (in seconds)")

    class Config:
        json_schema_extra = {
            "example": {
                "event_id": "550e8400-e29b-41d4-a716-446655440000",
                "event_type": "task.completed",
                "timestamp": "2024-01-01T12:00:00Z",
                "user_id": "user_123",
                "task_id": "task_456",
                "task_title": "Complete project documentation",
                "completed_at": "2024-01-01T12:00:00Z",
                "time_to_complete": 86400
            }
        }


# Event type mapping for deserialization
EVENT_TYPE_MAP = {
    "task.created": TaskCreatedEvent,
    "task.updated": TaskUpdatedEvent,
    "task.deleted": TaskDeletedEvent,
    "task.completed": TaskCompletedEvent,
}


def parse_task_event(event_data: dict) -> BaseTaskEvent:
    """
    Parse raw event data into the appropriate event model.

    Args:
        event_data: Raw event data dictionary

    Returns:
        Parsed event model instance

    Raises:
        ValueError: If event_type is unknown
    """
    event_type = event_data.get("event_type")
    event_class = EVENT_TYPE_MAP.get(event_type)

    if not event_class:
        raise ValueError(f"Unknown event type: {event_type}")

    return event_class(**event_data)
