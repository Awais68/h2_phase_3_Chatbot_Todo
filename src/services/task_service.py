"""
Business logic for task management operations.
Handles CRUD operations and maintains in-memory task storage with JSON persistence.
"""

import json
import os
import shutil
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Optional
from src.models.task import Task
from src.models.enums import Priority, Recurrence, Status, SortBy


class TaskManager:
    """Manages task collection and operations with JSON persistence."""

    def __init__(self, auto_load: bool = True, data_file: str = "tasks.json"):
        """
        Initialize task manager with optional auto-load from JSON.

        Args:
            auto_load: Whether to automatically load tasks from file (default: True)
            data_file: Path to JSON data file (default: tasks.json)
        """
        self.tasks: List[Task] = []
        self.data_file: str = data_file
        self._loaded_from_file: bool = False

        if auto_load and os.path.exists(data_file):
            try:
                self.load_from_json(data_file)
                self._loaded_from_file = True
            except Exception as e:
                # Don't fail initialization if load fails
                print(f"Warning: Could not load tasks from {data_file}: {e}")

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.NONE,
        due_date: Optional[date] = None,
        recurrence: Recurrence = Recurrence.NONE,
        tags: Optional[list[str]] = None
    ) -> Task:
        """
        Create and add a new task.

        Args:
            title: Task title (required)
            description: Task description (optional)
            priority: Task priority (default: Priority.NONE)
            due_date: Optional due date
            recurrence: Recurrence pattern (default: Recurrence.NONE)
            tags: Optional list of tags

        Returns:
            The created Task object

        Raises:
            ValueError: If validation fails
        """
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            recurrence=recurrence,
            tags=tags
        )
        self.tasks.append(task)
        self._auto_save()
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks sorted by creation date (newest first).

        Returns:
            List of all tasks
        """
        return sorted(self.tasks, key=lambda t: t.created_at, reverse=True)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Find a task by its ID.

        Args:
            task_id: The ID to search for

        Returns:
            Task if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        due_date: Optional[date] = None,
        recurrence: Optional[Recurrence] = None,
        tags: Optional[list[str]] = None
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: ID of task to update
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            due_date: New due date (optional)
            recurrence: New recurrence pattern (optional)
            tags: New tags list (optional)

        Returns:
            Updated Task if found, None otherwise

        Raises:
            ValueError: If validation fails
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.update(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                recurrence=recurrence,
                tags=tags
            )
            self._auto_save()
        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: ID of task to delete

        Returns:
            True if task was deleted, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self._auto_save()
            return True
        return False

    def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle completion status of a task.
        If completing a recurring task, creates next occurrence.

        Args:
            task_id: ID of task to toggle

        Returns:
            New task if recurring task was completed, original task otherwise,
            None if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        task.toggle_completed()

        # If completing a recurring task, create next occurrence
        if task.completed and task.recurrence != Recurrence.NONE:
            next_task = self._create_next_occurrence(task)
            self.tasks.append(next_task)
            self._auto_save()
            return next_task

        self._auto_save()
        return task

    def _create_next_occurrence(self, task: Task) -> Task:
        """
        Create next occurrence of recurring task.

        Args:
            task: Completed recurring task

        Returns:
            New Task with updated due date

        Raises:
            ValueError: If task has no due date
        """
        if not task.due_date:
            raise ValueError("Cannot create next occurrence without due date")

        # Calculate next due date based on recurrence
        if task.recurrence == Recurrence.DAILY:
            next_due = task.due_date + timedelta(days=1)
        elif task.recurrence == Recurrence.WEEKLY:
            next_due = task.due_date + timedelta(days=7)
        elif task.recurrence == Recurrence.MONTHLY:
            next_due = task.due_date + timedelta(days=30)
        elif task.recurrence == Recurrence.YEARLY:
            # Handle leap years properly
            next_due = task.due_date + timedelta(days=365)
        else:
            raise ValueError(f"Invalid recurrence: {task.recurrence}")

        # Create new task with same properties
        return Task(
            title=task.title,
            description=task.description,
            priority=task.priority,
            due_date=next_due,
            recurrence=task.recurrence,
            tags=task.tags.copy() if task.tags else [],
            completed=False
        )

    def get_task_stats(self) -> dict:
        """
        Get statistics about tasks.

        Returns:
            Dictionary with total, completed, and pending counts
        """
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.completed)
        pending = total - completed

        return {
            "total": total,
            "completed": completed,
            "pending": pending
        }

    def sort_tasks(self, tasks: List[Task], sort_by: SortBy = SortBy.DEFAULT) -> List[Task]:
        """
        Sort tasks with overdue always prioritized at top.

        Args:
            tasks: List of tasks to sort
            sort_by: Sort preference (default: SortBy.DEFAULT)

        Returns:
            Sorted list of tasks
        """
        # Separate overdue from others
        overdue = [t for t in tasks if t.status == Status.OVERDUE]
        others = [t for t in tasks if t.status != Status.OVERDUE]

        # Sort overdue by due_date (earliest first)
        overdue.sort(key=lambda t: t.due_date or date.max)

        # Sort others based on preference
        if sort_by == SortBy.PRIORITY:
            priority_order = {
                Priority.HIGH: 0,
                Priority.MEDIUM: 1,
                Priority.LOW: 2,
                Priority.NONE: 3
            }
            others.sort(key=lambda t: priority_order[t.priority])
        elif sort_by == SortBy.DUE_DATE:
            others.sort(key=lambda t: t.due_date or date.max)
        elif sort_by == SortBy.CREATED_DATE:
            others.sort(key=lambda t: t.created_at, reverse=True)
        else:  # DEFAULT
            others.sort(key=lambda t: t.created_at, reverse=True)

        # Overdue always at top
        return overdue + others

    def save_to_json(self, filename: Optional[str] = None) -> None:
        """
        Save all tasks to JSON file.

        Args:
            filename: Path to save file (default: use self.data_file)

        Raises:
            PermissionError: If file cannot be written due to permissions
            OSError: If disk is full or other OS-level error
        """
        target_file = filename or self.data_file

        # Prepare data structure
        data = {
            "tasks": [task.to_dict() for task in self.tasks],
            "next_id": Task._next_id,
            "saved_at": datetime.utcnow().isoformat()
        }

        try:
            # Write to temporary file first
            temp_file = f"{target_file}.tmp"
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Move temp file to target (atomic operation)
            shutil.move(temp_file, target_file)

        except PermissionError as e:
            raise PermissionError(
                f"Permission denied: Cannot write to {target_file}. "
                "Check file permissions or try a different location."
            ) from e
        except OSError as e:
            if "No space left on device" in str(e):
                raise OSError(
                    f"Disk full: Cannot save to {target_file}. "
                    "Free up some disk space and try again."
                ) from e
            raise OSError(f"Error saving to {target_file}: {e}") from e

    def load_from_json(self, filename: Optional[str] = None) -> int:
        """
        Load tasks from JSON file.

        Args:
            filename: Path to load file (default: use self.data_file)

        Returns:
            Number of tasks loaded

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If JSON is corrupt or invalid
            PermissionError: If file cannot be read due to permissions
        """
        source_file = filename or self.data_file

        if not os.path.exists(source_file):
            raise FileNotFoundError(
                f"Task file not found: {source_file}. "
                "No tasks to load - starting with empty list."
            )

        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

        except PermissionError as e:
            raise PermissionError(
                f"Permission denied: Cannot read {source_file}. "
                "Check file permissions."
            ) from e
        except json.JSONDecodeError as e:
            # Backup corrupt file
            backup_file = f"{source_file}.corrupt.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            try:
                shutil.copy2(source_file, backup_file)
                error_msg = (
                    f"Corrupt JSON file: {source_file}. "
                    f"Backed up to {backup_file}. "
                    "Starting with empty task list."
                )
            except Exception:
                error_msg = (
                    f"Corrupt JSON file: {source_file}. "
                    "Could not create backup. Starting with empty task list."
                )
            raise ValueError(error_msg) from e

        # Validate data structure
        if not isinstance(data, dict) or "tasks" not in data:
            raise ValueError(
                f"Invalid data format in {source_file}. "
                "Expected JSON object with 'tasks' array."
            )

        # Clear existing tasks
        self.tasks.clear()

        # Load tasks
        loaded_count = 0
        for task_data in data.get("tasks", []):
            try:
                task = Task.from_dict(task_data)
                self.tasks.append(task)
                loaded_count += 1
            except (ValueError, KeyError) as e:
                # Skip invalid tasks but continue loading others
                print(f"Warning: Skipping invalid task: {e}")
                continue

        # Restore ID counter
        if "next_id" in data:
            Task._next_id = data["next_id"]
        else:
            # Recalculate if not present
            if self.tasks:
                Task._next_id = max(task.id for task in self.tasks) + 1

        return loaded_count

    def _auto_save(self) -> None:
        """
        Automatically save tasks to JSON file after modifications.
        Silently fails to avoid disrupting user operations.
        """
        try:
            self.save_to_json()
        except Exception:
            # Silently fail - don't disrupt user operations
            # Error will be visible when user explicitly saves or exits
            pass
