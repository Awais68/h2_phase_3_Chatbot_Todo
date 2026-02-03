"""
SyncOperation model for offline change synchronization.
"""
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from enum import Enum


class SyncOperationType(str, Enum):
    """Types of sync operations."""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class SyncOperation(SQLModel, table=True):
    """Entity for tracking offline changes to be synchronized."""

    __tablename__ = "sync_operations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    task_id: Optional[int] = Field(default=None, foreign_key="tasks.id")
    operation_type: str = Field(max_length=20)  # create, update, delete
    client_id: str = Field(max_length=100, index=True)
    payload: Optional[str] = Field(default=None)  # JSON string of operation data
    created_at: datetime = Field(default_factory=datetime.utcnow)
    synced_at: Optional[datetime] = Field(default=None)
    is_synced: bool = Field(default=False)


class SyncRequest(SQLModel):
    """Schema for sync request from client."""

    operations: list[dict]  # List of pending operations from client


class SyncResponse(SQLModel):
    """Schema for sync response to client."""

    success: bool
    synced_count: int
    conflicts: list[dict] = []
    server_updates: list[dict] = []
