"""
Task service migrated to use Neon PostgreSQL.
Extended for 012-advanced-todo-features with due dates and recurrence support.
"""
from typing import List, Optional
from datetime import datetime
import pytz
from sqlmodel import Session, select
from src.models.task import Task, TaskCreate, TaskUpdate
from src.utils.datetime_parser import DateTimeParser
from src.utils.recurrence_calculator import RecurrenceCalculator


class TaskService:
    """Service for task CRUD operations with PostgreSQL."""

    @staticmethod
    def create_task(
        session: Session,
        user_id: int,
        task_data: TaskCreate,
        due_date_text: Optional[str] = None,
        user_timezone: str = "UTC",
        recurrence_pattern: Optional[str] = None,
        reminder_minutes: int = 15
    ) -> Task:
        """
        Create a new task for a user with optional due date and recurrence.

        Args:
            session: Database session
            user_id: ID of the user creating the task
            task_data: Task creation data
            due_date_text: Natural language due date (e.g., "tomorrow at 3pm")
            user_timezone: User's timezone for date parsing (default: UTC)
            recurrence_pattern: Recurrence type (daily/weekly/monthly/yearly)
            reminder_minutes: Minutes before due date to send reminder (default: 15)

        Returns:
            Task: Created task entity

        Raises:
            ValueError: If recurrence is set without due date
        """
        # Parse due date if provided
        due_date = None
        if due_date_text:
            parser = DateTimeParser()
            due_date = parser.parse(due_date_text, user_timezone=user_timezone)

            if due_date is None:
                raise ValueError(f"Could not parse due date: '{due_date_text}'")

        # Validate recurrence
        is_recurring = False
        next_occurrence = None
        if recurrence_pattern:
            if not due_date:
                raise ValueError("Recurring tasks must have a due date")
            is_recurring = True
            # Calculate next occurrence
            next_occurrence = RecurrenceCalculator.calculate_next_occurrence(
                due_date,
                recurrence_pattern
            )

        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            client_id=task_data.client_id,
            due_date=due_date,
            recurrence_pattern=recurrence_pattern,
            is_recurring=is_recurring,
            reminder_minutes=reminder_minutes,
            next_occurrence=next_occurrence
        )

        # Validate the task
        task.validate_due_date()
        task.validate_recurrence()

        session.add(task)
        session.commit()
        session.refresh(task)

        # Schedule notification if due date is set
        if task.due_date:
            from src.services.scheduler_service import get_scheduler
            try:
                scheduler = get_scheduler()
                scheduler.schedule_notification(
                    task_id=task.id,
                    task_title=task.title,
                    due_date=task.due_date,
                    reminder_minutes=task.reminder_minutes
                )
            except RuntimeError:
                # Scheduler not initialized yet (e.g., during testing)
                pass

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

        # Update only provided fields
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.completed is not None:
            task.completed = task_data.completed

        task.updated_at = datetime.utcnow()
        task.version += 1

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: int) -> bool:
        """
        Delete a task.

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
    def update_task_due_date(
        session: Session,
        task_id: int,
        user_id: int,
        due_date_text: str,
        user_timezone: str = "UTC",
        recurrence_pattern: Optional[str] = None,
        reminder_minutes: Optional[int] = None
    ) -> Optional[Task]:
        """
        Update a task's due date and optionally its recurrence pattern.

        Args:
            session: Database session
            task_id: Task ID to update
            user_id: ID of the user
            due_date_text: Natural language due date
            user_timezone: User's timezone for date parsing
            recurrence_pattern: New recurrence pattern (optional)
            reminder_minutes: New reminder time in minutes (optional)

        Returns:
            Optional[Task]: Updated task or None if not found

        Raises:
            ValueError: If due date parsing fails or recurrence invalid
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return None

        # Parse new due date
        parser = DateTimeParser()
        due_date = parser.parse(due_date_text, user_timezone=user_timezone)

        if due_date is None:
            raise ValueError(f"Could not parse due date: '{due_date_text}'")

        # Cancel existing notifications
        from src.services.scheduler_service import get_scheduler
        try:
            scheduler = get_scheduler()
            scheduler.cancel_notification(task_id)
        except RuntimeError:
            pass

        # Update task fields
        task.due_date = due_date
        if recurrence_pattern is not None:
            task.recurrence_pattern = recurrence_pattern
            task.is_recurring = bool(recurrence_pattern)
            if recurrence_pattern:
                task.next_occurrence = RecurrenceCalculator.calculate_next_occurrence(
                    due_date,
                    recurrence_pattern
                )
        if reminder_minutes is not None:
            task.reminder_minutes = reminder_minutes

        task.updated_at = datetime.utcnow()
        task.version += 1

        # Validate
        task.validate_due_date()
        task.validate_recurrence()

        session.add(task)
        session.commit()
        session.refresh(task)

        # Schedule new notification
        try:
            scheduler = get_scheduler()
            scheduler.schedule_notification(
                task_id=task.id,
                task_title=task.title,
                due_date=task.due_date,
                reminder_minutes=task.reminder_minutes
            )
        except RuntimeError:
            pass

        return task

    @staticmethod
    def complete_task(
        session: Session,
        task_id: int,
        user_id: int
    ) -> Optional[Task]:
        """
        Mark a task as completed and handle recurring task logic.

        For recurring tasks:
        - Creates a new instance with the next occurrence as due date
        - Marks current instance as completed

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

        # Cancel notifications for this task
        from src.services.scheduler_service import get_scheduler
        try:
            scheduler = get_scheduler()
            scheduler.cancel_notification(task_id)
        except RuntimeError:
            pass

        # Mark as completed
        task.completed = True
        task.updated_at = datetime.utcnow()
        task.version += 1

        session.add(task)
        session.commit()
        session.refresh(task)

        # If recurring, create next instance
        if task.is_recurring and task.next_occurrence:
            TaskService.create_recurring_instance(session, task)

        return task

    @staticmethod
    def create_recurring_instance(
        session: Session,
        original_task: Task
    ) -> Task:
        """
        Create the next instance of a recurring task.

        Args:
            session: Database session
            original_task: The completed recurring task

        Returns:
            Task: New task instance with next occurrence as due date

        Raises:
            ValueError: If task is not recurring or missing next_occurrence
        """
        if not original_task.is_recurring:
            raise ValueError("Task is not recurring")

        if not original_task.next_occurrence:
            raise ValueError("Recurring task missing next_occurrence")

        # Calculate occurrence after next_occurrence
        future_occurrence = RecurrenceCalculator.calculate_next_occurrence(
            original_task.next_occurrence,
            original_task.recurrence_pattern.value
        )

        # Create new task instance
        new_task = Task(
            user_id=original_task.user_id,
            title=original_task.title,
            description=original_task.description,
            due_date=original_task.next_occurrence,
            recurrence_pattern=original_task.recurrence_pattern,
            is_recurring=True,
            reminder_minutes=original_task.reminder_minutes,
            next_occurrence=future_occurrence,
            completed=False
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        # Schedule notification for new instance
        from src.services.scheduler_service import get_scheduler
        try:
            scheduler = get_scheduler()
            scheduler.schedule_notification(
                task_id=new_task.id,
                task_title=new_task.title,
                due_date=new_task.due_date,
                reminder_minutes=new_task.reminder_minutes
            )
        except RuntimeError:
            pass

        return new_task
