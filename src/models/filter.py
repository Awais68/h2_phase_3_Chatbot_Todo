"""
Filter State Model
Defines filter state for task filtering operations.
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional, TYPE_CHECKING
from src.models.enums import Status, Priority
from src.models.task import Task

if TYPE_CHECKING:
    from typing import Any


@dataclass
class FilterState:
    """Active filter configuration for task list."""
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    date_range: Optional[tuple[date, date]] = None
    search_keyword: Optional[str] = None
    tags: Optional[list[str]] = None

    def is_active(self) -> bool:
        """Check if any filters are active."""
        return any([
            self.status is not None,
            self.priority is not None,
            self.date_range is not None,
            self.search_keyword is not None,
            self.tags is not None and len(self.tags) > 0
        ])

    def describe(self) -> str:
        """Human-readable description of active filters."""
        parts = []
        if self.status:
            parts.append(f"Status={self.status.value.title()}")
        if self.priority:
            parts.append(f"Priority={self.priority.value.title()}")
        if self.date_range:
            start, end = self.date_range
            parts.append(f"Due: {start} to {end}")
        if self.search_keyword:
            parts.append(f'Search="{self.search_keyword}"')
        if self.tags and len(self.tags) > 0:
            parts.append(f'Tags={", ".join(self.tags)}')
        return ", ".join(parts) if parts else "No filters"

    def clear(self) -> None:
        """Clear all filters."""
        self.status = None
        self.priority = None
        self.date_range = None
        self.search_keyword = None
        self.tags = None


class FilterService:
    """Service for applying filters to task collections."""

    @staticmethod
    def apply_filters(tasks: list[Task], filter_state: FilterState) -> list[Task]:
        """
        Apply all active filters from filter_state to the task list.

        Args:
            tasks: List of tasks to filter
            filter_state: Filter configuration

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
            filtered = [t for t in filtered if t.due_date is not None and start <= t.due_date <= end]

        if filter_state.search_keyword:
            keyword = filter_state.search_keyword.lower()
            filtered = [t for t in filtered if keyword in t.title.lower() or keyword in (t.description or "").lower()]

        if filter_state.tags and len(filter_state.tags) > 0:
            filtered = [t for t in filtered if any(tag in (t.tags or []) for tag in filter_state.tags)]

        return filtered
