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
            client_id=task_data.client_id
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
