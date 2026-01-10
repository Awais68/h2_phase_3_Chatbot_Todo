"""
Task data model for the Todo application.
Defines the Task class with validation and data management.
"""

from datetime import datetime, date
from typing import Optional
from src.models.enums import Priority, Recurrence, Status


class Task:
    """Represents a single task with its properties and state."""

    # Class variable to track next ID
    _next_id: int = 1

    def __init__(
        self,
        title: str,
        description: str = "",
        completed: bool = False,
        task_id: Optional[int] = None,
        priority: Priority = Priority.NONE,
        due_date: Optional[date] = None,
        recurrence: Recurrence = Recurrence.NONE,
        tags: Optional[list[str]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        Initialize a new task.

        Args:
            title: Task title (required, 1-200 characters)
            description: Task description (optional, max 1000 characters)
            completed: Completion status (default: False)
            task_id: Task ID (auto-generated if not provided)
            priority: Task priority (default: Priority.NONE)
            due_date: Optional due date for task
            recurrence: Recurrence pattern (default: Recurrence.NONE)
            tags: Optional list of tags (default: empty list)
            created_at: Creation timestamp (auto-generated if not provided)
            updated_at: Update timestamp (auto-generated if not provided)

        Raises:
            ValueError: If title or description validation fails
        """
        # Validate title
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title.strip()) > 200:
            raise ValueError("Title cannot exceed 200 characters")

        # Validate description
        if len(description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")

        # Validate recurrence requires due_date
        if recurrence != Recurrence.NONE and due_date is None:
            raise ValueError("Recurring tasks must have a due date")

        # Validate and sanitize tags
        if tags is None:
            tags = []
        validated_tags = []
        for tag in tags:
            if isinstance(tag, str) and tag.strip():
                clean_tag = tag.strip().lower()
                if len(clean_tag) <= 50 and clean_tag not in validated_tags:
                    validated_tags.append(clean_tag)

        # Set task properties
        self.id: int = task_id if task_id is not None else Task._get_next_id()
        self.title: str = title.strip()
        self.description: str = description
        self.completed: bool = completed
        self.priority: Priority = priority
        self.due_date: Optional[date] = due_date
        self.recurrence: Recurrence = recurrence
        self.tags: list[str] = validated_tags
        self.created_at: datetime = created_at if created_at is not None else datetime.utcnow()
        self.updated_at: datetime = updated_at if updated_at is not None else datetime.utcnow()

    @classmethod
    def _get_next_id(cls) -> int:
        """Get next available task ID and increment counter."""
        current_id = cls._next_id
        cls._next_id += 1
        return current_id

    @property
    def status(self) -> Status:
        """
        Compute task status based on completion and due date.

        Returns:
            Status.COMPLETED if completed=True
            Status.OVERDUE if due_date < today and not completed
            Status.PENDING otherwise
        """
        if self.completed:
            return Status.COMPLETED
        if self.due_date is not None and self.due_date < date.today():
            return Status.OVERDUE
        return Status.PENDING

    def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        due_date: Optional[date] = None,
        recurrence: Optional[Recurrence] = None,
        tags: Optional[list[str]] = None
    ) -> None:
        """
        Update task fields.

        Args:
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            due_date: New due date (optional)
            recurrence: New recurrence pattern (optional)
            tags: New tags list (optional)

        Raises:
            ValueError: If validation fails
        """
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            if len(title.strip()) > 200:
                raise ValueError("Title cannot exceed 200 characters")
            self.title = title.strip()

        if description is not None:
            if len(description) > 1000:
                raise ValueError("Description cannot exceed 1000 characters")
            self.description = description

        if priority is not None:
            self.priority = priority

        if due_date is not None:
            self.due_date = due_date

        if recurrence is not None:
            # Validate recurrence requires due_date
            if recurrence != Recurrence.NONE and self.due_date is None:
                raise ValueError("Recurring tasks must have a due date")
            self.recurrence = recurrence

        if tags is not None:
            validated_tags = []
            for tag in tags:
                if isinstance(tag, str) and tag.strip():
                    clean_tag = tag.strip().lower()
                    if len(clean_tag) <= 50 and clean_tag not in validated_tags:
                        validated_tags.append(clean_tag)
            self.tags = validated_tags

        self.updated_at = datetime.utcnow()

    def toggle_completed(self) -> None:
        """Toggle task completion status."""
        self.completed = not self.completed
        self.updated_at = datetime.utcnow()

    def __str__(self) -> str:
        """Return string representation of task."""
        status = "✓" if self.completed else "•"
        return f"ID: {self.id} | {status} | {self.title}"

    def __repr__(self) -> str:
        """Return detailed representation of task."""
        return (
            f"Task(id={self.id}, title='{self.title}', "
            f"completed={self.completed}, created={self.created_at.date()})"
        )

    def to_dict(self) -> dict:
        """
        Convert task to dictionary for JSON serialization.

        Returns:
            Dictionary representation of task
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority.value,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "recurrence": self.recurrence.value,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """
        Create task from dictionary (JSON deserialization).

        Args:
            data: Dictionary with task data

        Returns:
            Task instance

        Raises:
            ValueError: If required fields are missing or invalid
        """
        if "id" not in data or "title" not in data:
            raise ValueError("Task data must include 'id' and 'title'")

        # Parse priority
        priority_str = data.get("priority", "none")
        try:
            priority = Priority(priority_str)
        except ValueError:
            priority = Priority.NONE

        # Parse due_date
        due_date = None
        if data.get("due_date"):
            try:
                due_date = date.fromisoformat(data["due_date"])
            except (ValueError, TypeError):
                pass

        # Parse recurrence
        recurrence_str = data.get("recurrence", "none")
        try:
            recurrence = Recurrence(recurrence_str)
        except ValueError:
            recurrence = Recurrence.NONE

        # Parse tags
        tags = data.get("tags", [])
        if not isinstance(tags, list):
            tags = []

        # Parse timestamps
        created_at = None
        if "created_at" in data:
            try:
                created_at = datetime.fromisoformat(data["created_at"])
            except (ValueError, TypeError):
                pass

        updated_at = None
        if "updated_at" in data:
            try:
                updated_at = datetime.fromisoformat(data["updated_at"])
            except (ValueError, TypeError):
                pass

        task = cls(
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
            task_id=data["id"],
            priority=priority,
            due_date=due_date,
            recurrence=recurrence,
            tags=tags,
            created_at=created_at,
            updated_at=updated_at
        )

        return task
