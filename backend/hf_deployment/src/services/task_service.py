"""
Task service migrated to use Neon PostgreSQL.
"""
from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select
from src.models.task import Task, TaskCreate, TaskUpdate


class TaskService:
    """Service for task CRUD operations with PostgreSQL."""

    @staticmethod
    def create_task(session: Session, user_id: int, task_data: TaskCreate) -> Task:
        """
        Create a new task for a user.

        Args:
            session: Database session
            user_id: ID of the user creating the task
            task_data: Task creation data

        Returns:
            Task: Created task entity
        """
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            client_id=task_data.client_id,
            category=task_data.category,
            tags=task_data.tags,
            status=task_data.status or "pending",
            priority=task_data.priority or "medium",
            shopping_list=task_data.shopping_list,
            recursion=task_data.recursion,
            due_date=task_data.due_date
        )

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_tasks(session: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get all tasks for a user with pagination.

        Args:
            session: Database session
            user_id: ID of the user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[Task]: List of user's tasks
        """
        statement = (
            select(Task)
            .where(Task.user_id == user_id)
            .order_by(Task.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(session.exec(statement).all())

    @staticmethod
    def get_task_by_id(session: Session, task_id: int, user_id: int) -> Optional[Task]:
        """
        Get a specific task by ID for a user.

        Args:
            session: Database session
            task_id: Task ID
            user_id: ID of the user

        Returns:
            Optional[Task]: Task if found and belongs to user, None otherwise
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def update_task(
        session: Session, task_id: int, user_id: int, task_data: TaskUpdate
    ) -> Optional[Task]:
        """
        Update a task.

        Args:
            session: Database session
            task_id: Task ID to update
            user_id: ID of the user
            task_data: Updated task data

        Returns:
            Optional[Task]: Updated task or None if not found
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return None

        # Track if we're completing the task
        was_incomplete = not task.completed
        is_being_completed = task_data.completed is True

        # Update only provided fields
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.completed is not None:
            task.completed = task_data.completed
        if task_data.subitems is not None:
            task.subitems = task_data.subitems
        if task_data.category is not None:
            task.category = task_data.category
        if task_data.tags is not None:
            task.tags = task_data.tags
        if task_data.status is not None:
            task.status = task_data.status
        if task_data.priority is not None:
            task.priority = task_data.priority
        if task_data.shopping_list is not None:
            task.shopping_list = task_data.shopping_list
        if task_data.recursion is not None:
            task.recursion = task_data.recursion
        if task_data.due_date is not None:
            task.due_date = task_data.due_date

        task.updated_at = datetime.utcnow()
        task.version += 1

        session.add(task)
        session.commit()
        session.refresh(task)

        # If task is being marked complete, create history entry
        if was_incomplete and is_being_completed:
            # Create history entry for completed task
            from .history_service import HistoryService
            from src.models.task_history import HistoryActionType
            try:
                HistoryService.create_history_entry(
                    session=session,
                    task=task,
                    action_type=HistoryActionType.COMPLETED,
                    action_by=user_id
                )
            except Exception as e:
                # Log but don't fail update if history creation fails
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to create history entry for task {task_id}: {e}")

            # If recurring, create next instance
            if task.is_recurring and task.due_date and task.recurrence_pattern:
                try:
                    TaskService.create_recurring_instance(session, task)
                except Exception as e:
                    # Log but don't fail update if instance creation fails
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to create recurring instance for task {task_id}: {e}")

        return task

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: int) -> bool:
        """
        Delete a task.

        Creates a history entry before deletion to enable restoration.

        Args:
            session: Database session
            task_id: Task ID to delete
            user_id: ID of the user

        Returns:
            bool: True if deleted, False if not found
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return False

        # Create history entry before deletion
        from .history_service import HistoryService
        from src.models.task_history import HistoryActionType
        try:
            HistoryService.create_history_entry(
                session=session,
                task=task,
                action_type=HistoryActionType.DELETED,
                action_by=user_id
            )
        except Exception as e:
            # Log but don't fail deletion if history creation fails
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create history entry for deleted task {task_id}: {e}")

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def get_task_by_client_id(session: Session, client_id: str, user_id: int) -> Optional[Task]:
        """
        Get a task by its client-generated ID (for offline sync).

        Args:
            session: Database session
            client_id: Client-generated unique ID
            user_id: ID of the user

        Returns:
            Optional[Task]: Task if found, None otherwise
        """
        statement = select(Task).where(
            Task.client_id == client_id, Task.user_id == user_id
        )
        return session.exec(statement).first()

    @staticmethod
    def create_recurring_instance(session: Session, original_task: Task) -> Task:
        """
        Create next instance of a recurring task.

        This method is called when a recurring task is completed to automatically
        create the next occurrence with the same properties but a new due date.

        Args:
            session: Database session
            original_task: The completed recurring task

        Returns:
            Task: Newly created recurring task instance

        Raises:
            ValueError: If task is not recurring or missing required fields
        """
        if not original_task.is_recurring:
            raise ValueError(f"Task {original_task.id} is not a recurring task")

        if not original_task.due_date or not original_task.recurrence_pattern:
            raise ValueError(
                f"Recurring task {original_task.id} missing due_date or recurrence_pattern"
            )

        # Calculate next occurrence
        next_due = original_task.calculate_next_occurrence()

        # Create new task instance with same properties
        new_task = Task(
            user_id=original_task.user_id,
            title=original_task.title,
            description=original_task.description,
            due_date=next_due,
            recurrence_pattern=original_task.recurrence_pattern,
            is_recurring=True,
            reminder_minutes=original_task.reminder_minutes,
            next_occurrence=None,  # Will be calculated on next completion
            completed=False,
            client_id=None  # Don't copy client_id to avoid duplicates
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        # Schedule notification for the new instance
        from .scheduler_service import get_scheduler
        try:
            scheduler = get_scheduler()
            scheduler.schedule_notification(
                task_id=new_task.id,
                task_title=new_task.title,
                due_date=new_task.due_date,
                reminder_minutes=new_task.reminder_minutes
            )
        except Exception as e:
            # Log but don't fail task creation if notification scheduling fails
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to schedule notification for recurring task {new_task.id}: {e}")

        return new_task

    @staticmethod
    def complete_task(session: Session, task_id: int, user_id: int) -> Optional[Task]:
        """
        Mark a task as completed.

        Creates a history entry and, for recurring tasks, creates the next instance.

        Args:
            session: Database session
            task_id: Task ID to complete
            user_id: ID of the user

        Returns:
            Optional[Task]: Completed task or None if not found
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return None
        try:
            # Mark as completed
            task.completed = True
            task.updated_at = datetime.utcnow()
            task.version += 1
            session.add(task)


            HistoryService.create_history_entry(
                session=session,
                task=task,
                action_type=HistoryActionType.COMPLETED,
                action_by=user_id
            )
            session.commit()  # commit both task + history in same transaction
            session.refresh(task)
        except Exception as e:
            session.rollback()
            raise e
        

            # Log but don't fail completion if history creation fails
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create history entry for task {task_id}: {e}")

        # If recurring, create next instance
        if task.is_recurring and task.due_date and task.recurrence_pattern:
            try:
                TaskService.create_recurring_instance(session, task)
            except Exception as e:
                # Log but don't fail completion if instance creation fails
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to create recurring instance for task {task_id}: {e}")

        return task



