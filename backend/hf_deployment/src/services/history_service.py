"""
HistoryService: Manage task history for audit trail and restoration.

This service provides:
- History entry creation on task completion/deletion
- Paginated history retrieval with filtering
- Full-text search on task titles
- Task restoration from history
- Automatic 2-year retention management
"""

from typing import List, Optional, Tuple
from datetime import datetime
from sqlmodel import Session, select, func, or_
from src.models.task import Task, TaskCreate
from src.models.task_history import TaskHistory, HistoryActionType, TaskHistoryQuery


class HistoryService:
    """Service for task history management and audit trail."""

    @staticmethod
    def create_history_entry(
        session: Session,
        task: Task,
        action_type: HistoryActionType,
        action_by: int
    ) -> TaskHistory:
        """
        Create a history entry for a completed or deleted task.

        Args:
            session: Database session
            task: Task being archived
            action_type: Type of action (completed or deleted)
            action_by: User ID who performed the action

        Returns:
            TaskHistory: Created history entry
        """
        history = TaskHistory.from_task(task, action_type, action_by)

        session.add(history)
        session.commit()
        session.refresh(history)

        return history

    @staticmethod
    def get_history(
        session: Session,
        user_id: str,
        query: Optional[TaskHistoryQuery] = None
    ) -> Tuple[List[TaskHistory], int]:
        """
        Get paginated task history with optional filtering.

        Args:
            session: Database session
            user_id: User ID to retrieve history for
            query: Optional query parameters for filtering and pagination

        Returns:
            Tuple of (history entries list, total count)
        """
        if query is None:
            query = TaskHistoryQuery()

        # Build base query
        statement = select(TaskHistory).where(TaskHistory.user_id == user_id)

        # Apply filters
        if query.action_type:
            statement = statement.where(TaskHistory.action_type == query.action_type)

        if query.start_date:
            statement = statement.where(TaskHistory.action_date >= query.start_date)

        if query.end_date:
            statement = statement.where(TaskHistory.action_date <= query.end_date)

        if query.search:
            # PostgreSQL full-text search on title
            search_pattern = f"%{query.search}%"
            statement = statement.where(TaskHistory.title.ilike(search_pattern))

        # Get total count
        count_statement = select(func.count()).select_from(statement.alias())
        total_count = session.exec(count_statement).one()

        # Apply pagination and ordering
        statement = statement.order_by(TaskHistory.action_date.desc())
        offset = (query.page - 1) * query.page_size
        statement = statement.offset(offset).limit(query.page_size)

        # Execute query
        results = list(session.exec(statement).all())

        return results, total_count

    @staticmethod
    def search_history(
        session: Session,
        user_id: str,
        search_query: str,
        page: int = 1,
        page_size: int = 50
    ) -> Tuple[List[TaskHistory], int]:
        """
        Search task history by title using full-text search.

        Args:
            session: Database session
            user_id: User ID to search within
            search_query: Search query string
            page: Page number (1-indexed)
            page_size: Items per page

        Returns:
            Tuple of (matching history entries, total count)
        """
        query = TaskHistoryQuery(
            search=search_query,
            page=page,
            page_size=page_size
        )
        return HistoryService.get_history(session, user_id, query)

    @staticmethod
    def restore_deleted_task(
        session: Session,
        history_id: int,
        user_id: str
    ) -> Optional[Task]:
        """
        Restore a deleted task from history.

        This creates a new active task with the same properties as the
        historical snapshot. Only works for deleted tasks (can_restore=True).

        Args:
            session: Database session
            history_id: History entry ID to restore from
            user_id: User ID (for authorization)

        Returns:
            Optional[Task]: Newly created task or None if history not found or not restorable

        Raises:
            ValueError: If task cannot be restored (completed tasks or already restored)
        """
        # Find history entry
        statement = select(TaskHistory).where(
            TaskHistory.id == history_id,
            TaskHistory.user_id == user_id
        )
        history = session.exec(statement).first()

        if not history:
            return None

        if not history.can_restore:
            raise ValueError(
                f"Cannot restore history entry {history_id}: "
                f"Only deleted tasks can be restored (action_type={history.action_type})"
            )

        # Create new task from history snapshot
        restored_task = Task(
            user_id=history.user_id,
            title=history.title,
            description=history.description,
            completed=history.completed,
            due_date=history.due_date,
            recurrence_pattern=history.recurrence_pattern,
            is_recurring=bool(history.recurrence_pattern),
            reminder_minutes=15,  # Default reminder
            next_occurrence=None
        )

        session.add(restored_task)
        session.commit()
        session.refresh(restored_task)

        # Mark history entry as no longer restorable to prevent duplicates
        history.can_restore = False
        session.add(history)
        session.commit()

        return restored_task

    @staticmethod
    def cleanup_old_history(session: Session, cutoff_date: datetime) -> int:
        """
        Delete history entries older than cutoff date (2-year retention).

        Args:
            session: Database session
            cutoff_date: Delete entries with retention_until < cutoff_date

        Returns:
            int: Number of entries deleted
        """
        statement = select(TaskHistory).where(
            TaskHistory.retention_until < cutoff_date
        )
        old_entries = list(session.exec(statement).all())

        count = len(old_entries)
        for entry in old_entries:
            session.delete(entry)

        session.commit()
        return count

    @staticmethod
    def get_history_by_id(
        session: Session,
        history_id: int,
        user_id: str
    ) -> Optional[TaskHistory]:
        """
        Get a single history entry by ID.

        Args:
            session: Database session
            history_id: History entry ID
            user_id: User ID (for authorization)

        Returns:
            Optional[TaskHistory]: History entry or None if not found
        """
        statement = select(TaskHistory).where(
            TaskHistory.id == history_id,
            TaskHistory.user_id == user_id
        )
        return session.exec(statement).first()

    @staticmethod
    def get_history_count(session: Session, user_id: str) -> int:
        """
        Get total count of history entries for a user.

        Args:
            session: Database session
            user_id: User ID

        Returns:
            int: Total count of history entries
        """
        statement = select(func.count()).select_from(TaskHistory).where(
            TaskHistory.user_id == user_id
        )
        return session.exec(statement).one()
