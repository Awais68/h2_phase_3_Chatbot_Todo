"""
TaskHistory model for 012-advanced-todo-features.

Immutable record of completed and deleted tasks for audit trail and restoration.
Implements 2-year retention policy with automatic cleanup.
"""

from typing import Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, Text
from dateutil.relativedelta import relativedelta


class HistoryActionType(str, Enum):
    """History action type enumeration."""
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    COMPLETED = "COMPLETED"
    DELETED = "DELETED"
    ARCHIVED = "ARCHIVED"
    RESTORED = "RESTORED"



class TaskHistory(SQLModel, table=True):
    """
    Task history record for completed and deleted tasks.

    This entity provides an immutable audit trail of task lifecycle events
    with automatic 2-year retention and restoration capabilities.

    Attributes:
        id: Unique history record identifier
        user_id: Foreign key to user (for data isolation)
        original_task_id: Reference to original task ID (may no longer exist)
        title: Snapshot of task title at time of action
        description: Snapshot of task description at time of action
        completed: Whether task was completed when archived
        due_date: Snapshot of due date (if any)
        recurrence_pattern: Snapshot of recurrence pattern (if any)
        action_type: What happened (completed or deleted)
        action_date: When the action occurred (UTC)
        action_by: User who performed the action
        can_restore: Whether task can be restored (true for deleted, false for completed)
        retention_until: Auto-calculated date when record should be purged
    """

    __tablename__ = "task_history"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign keys and references
    user_id: int = Field(index=True, description="Owner of historical task")
    original_task_id: int = Field(description="Original task ID before archival")

    # Snapshot fields (immutable copy of task at time of action)
    title: str = Field(max_length=200, description="Task title snapshot")
    description: str = Field(
        default="",
        sa_column=Column(Text),
        description="Task description snapshot"
    )
    completed: bool = Field(default=False, description="Completion status at archive time")
    due_date: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
        description="Due date snapshot"
    )
    recurrence_pattern: Optional[str] = Field(
        default=None,
        max_length=20,
        description="Recurrence pattern snapshot"
    )

    # History metadata
    action_type: HistoryActionType = Field(
    description="Action performed on task"
)
    action_date: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True)),
        description="When the action occurred (UTC)"
    )
    action_by: int = Field(description="User who performed the action")
    can_restore: bool = Field(default=False, description="Whether task can be restored")

    # Retention tracking
    retention_until: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
        description="Auto-calculated: action_date + 2 years"
    )

    def __init__(self, **data):
        super().__init__(**data)

        if not self.retention_until:
            self.retention_until = self.action_date + relativedelta(years=2)

        self.validate_action_type()


    def validate_action_type(self) -> None:
        """
        Validate action_type and can_restore consistency.

        Raises:
            ValueError: If action_type and can_restore are inconsistent
        """
        if self.action_type == HistoryActionType.COMPLETED and self.can_restore:
            raise ValueError("Completed tasks cannot be marked as restorable")

        if self.action_type == HistoryActionType.DELETED and not self.can_restore:
            # Auto-set can_restore for deleted tasks
            self.can_restore = True

    @classmethod
    def from_task(
        cls,
        task,
        action_type: HistoryActionType,
        action_by: int
    ) -> "TaskHistory":
        """
        Create TaskHistory record from a Task instance.

        Args:
            task: Task instance to archive
            action_type: Type of action (completed or deleted)
            action_by: User ID who performed the action

        Returns:
            TaskHistory instance ready to be saved

        Example:
            >>> from .task import Task
            >>> task = Task(id=1, user_id=1, title="Buy groceries", ...)
            >>> history = TaskHistory.from_task(
            ...     task,
            ...     HistoryActionType.COMPLETED,
            ...     action_by=1
            ... )
        """
        return cls(
            user_id=task.user_id,
            original_task_id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            due_date=task.due_date if hasattr(task, 'due_date') else None,
            recurrence_pattern=task.recurrence_pattern.value if hasattr(task, 'recurrence_pattern') and task.recurrence_pattern else None,
            action_type=action_type.value if isinstance(action_type, HistoryActionType) else action_type,
            action_by=action_by,
            can_restore=(action_type == HistoryActionType.DELETED)
        )


class TaskHistoryResponse(SQLModel):
    """Schema for task history response."""

    id: int
    user_id: int
    original_task_id: int
    title: str
    description: str
    completed: bool
    due_date: Optional[datetime] = None
    recurrence_pattern: Optional[str] = None
    action_type: HistoryActionType
    action_date: datetime
    action_by: int
    can_restore: bool
    retention_until: datetime


class TaskHistoryQuery(SQLModel):
    """Schema for task history query parameters."""

    action_type: Optional[HistoryActionType] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    search: Optional[str] = None
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=50, ge=1, le=100, description="Items per page (max 100)")
