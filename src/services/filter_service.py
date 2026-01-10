"""
Filtering service for task lists.
Provides FilterState and filtering logic.
"""

from typing import List
from src.models.task import Task
from src.models.filter import FilterState


class FilterService:
    """Service for filtering task lists."""

    @staticmethod
    def apply_filters(tasks: List[Task], filter_state: FilterState) -> List[Task]:
        """
        Apply all active filters to task list.

        Args:
            tasks: List of tasks to filter
            filter_state: Active filter configuration

        Returns:
            Filtered list of tasks
        """
        filtered = tasks

        if filter_state.status:
            filtered = [t for t in filtered if t.status == filter_state.status]

        if filter_state.priority:
            filtered = [t for t in filtered if t.priority == filter_state.priority]

        if filter_state.date_range:
            start, end = filter_state.date_range
            filtered = [
                t for t in filtered
                if t.due_date and start <= t.due_date <= end
            ]

        if filter_state.search_keyword:
            keyword = filter_state.search_keyword.lower()
            filtered = [
                t for t in filtered
                if keyword in t.title.lower() or keyword in t.description.lower()
            ]

        if filter_state.tags and len(filter_state.tags) > 0:
            filtered = [
                t for t in filtered
                if any(tag in t.tags for tag in filter_state.tags)
            ]

        return filtered
