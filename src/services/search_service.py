"""
Search service for task lists.
Provides keyword-based search functionality.
"""

from typing import List
from src.models.task import Task


class SearchService:
    """Service for searching tasks."""

    @staticmethod
    def search(tasks: List[Task], keyword: str) -> List[Task]:
        """
        Search tasks by keyword (case-insensitive substring matching).

        Args:
            tasks: List of tasks to search
            keyword: Search keyword

        Returns:
            List of tasks matching keyword in title or description
        """
        if not keyword or not keyword.strip():
            return tasks

        keyword_lower = keyword.strip().lower()

        return [
            task for task in tasks
            if keyword_lower in task.title.lower()
            or keyword_lower in task.description.lower()
        ]
