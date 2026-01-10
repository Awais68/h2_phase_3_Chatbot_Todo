"""
Unit tests for FilterService.
"""

import pytest
from datetime import date, timedelta
from src.models.task import Task
from src.models.enums import Priority, Recurrence, Status
from src.models.filter import FilterState
from src.services.filter_service import FilterService


@pytest.fixture
def sample_tasks():
    """Create a list of sample tasks for testing."""
    tasks = [
        Task(
            title="High priority task",
            description="This is urgent",
            priority=Priority.HIGH,
            due_date=date.today() + timedelta(days=1),
        ),
        Task(
            title="Medium priority task",
            description="Normal importance",
            priority=Priority.MEDIUM,
            due_date=date.today() + timedelta(days=2),
        ),
        Task(
            title="Low priority task",
            description="Can wait",
            priority=Priority.LOW,
            due_date=date.today() + timedelta(days=3),
        ),
        Task(
            title="Completed task",
            description="Already done",
            priority=Priority.HIGH,
            completed=True,
            due_date=date.today() + timedelta(days=1),
        ),
    ]
    return tasks


class TestFilterServiceApplyFilters:
    """Test FilterService.apply_filters() method."""

    def test_no_filters_returns_all(self, sample_tasks):
        """Test that empty filter returns all tasks."""
        f = FilterState()
        result = FilterService.apply_filters(sample_tasks, f)
        assert len(result) == len(sample_tasks)

    def test_filter_by_status_pending(self, sample_tasks):
        """Test filtering by pending status."""
        f = FilterState(status=Status.PENDING)
        result = FilterService.apply_filters(sample_tasks, f)
        assert len(result) == 3
        for task in result:
            assert task.status == Status.PENDING

    def test_filter_by_status_completed(self, sample_tasks):
        """Test filtering by completed status."""
        f = FilterState(status=Status.COMPLETED)
        result = FilterService.apply_filters(sample_tasks, f)
        assert len(result) == 1
        assert result[0].title == "Completed task"

    def test_filter_by_priority_high(self, sample_tasks):
        """Test filtering by high priority."""
        f = FilterState(priority=Priority.HIGH)
        result = FilterService.apply_filters(sample_tasks, f)
        assert len(result) == 2
        for task in result:
            assert task.priority == Priority.HIGH

    def test_filter_by_priority_medium(self, sample_tasks):
        """Test filtering by medium priority."""
        f = FilterState(priority=Priority.MEDIUM)
        result = FilterService.apply_filters(sample_tasks, f)
        assert len(result) == 1
        assert result[0].title == "Medium priority task"

    def test_filter_by_date_range(self, sample_tasks):
        """Test filtering by date range."""
        today = date.today()
        f = FilterState(date_range=(today, today + timedelta(days=2)))
        result = FilterService.apply_filters(sample_tasks, f)
        assert len(result) == 3
        # All tasks should have due_date within the range
        for task in result:
            assert task.due_date is not None
            assert today <= task.due_date <= today + timedelta(days=2)

    def test_filter_by_search_keyword(self, sample_tasks):
        """Test filtering by search keyword."""
        f = FilterState(search_keyword="urgent")
        result = FilterService.apply_filters(sample_tasks, f)
        assert len(result) == 1
        assert result[0].title == "High priority task"

    def test_filter_by_search_case_insensitive(self, sample_tasks):
        """Test that search is case insensitive."""
        f = FilterState(search_keyword="URGENT")
        result = FilterService.apply_filters(sample_tasks, f)
        assert len(result) == 1

    def test_filter_searches_description(self, sample_tasks):
        """Test that search matches description."""
        f = FilterState(search_keyword="normal importance")
        result = FilterService.apply_filters(sample_tasks, f)
        assert len(result) == 1
        assert result[0].title == "Medium priority task"

    def test_filter_by_tags(self, sample_tasks):
        """Test filtering by tags."""
        # Add tags to tasks
        sample_tasks[0].tags = ["work", "urgent"]
        sample_tasks[1].tags = ["personal"]
        sample_tasks[2].tags = ["work"]

        f = FilterState(tags=["work"])
        result = FilterService.apply_filters(sample_tasks, f)
        assert len(result) == 2

    def test_filter_by_multiple_tags(self, sample_tasks):
        """Test filtering by multiple tags - any match."""
        # Set tags on first 3 tasks (task 4 has no tags)
        sample_tasks[0].tags = ["work", "urgent"]
        sample_tasks[1].tags = ["personal"]
        sample_tasks[2].tags = ["work"]
        # sample_tasks[3] has no tags

        f = FilterState(tags=["work", "urgent"])
        result = FilterService.apply_filters(sample_tasks, f)
        # Should match tasks with "work" OR "urgent" (task 0 and task 2)
        assert len(result) == 2

    def test_combined_filters(self, sample_tasks):
        """Test combining multiple filters."""
        sample_tasks[0].tags = ["work", "urgent"]
        sample_tasks[3].tags = ["work", "urgent"]

        f = FilterState(
            priority=Priority.HIGH,
            tags=["urgent"]
        )
        result = FilterService.apply_filters(sample_tasks, f)
        assert len(result) == 2

    def test_empty_result_no_matches(self, sample_tasks):
        """Test that filter returns empty list when no matches."""
        f = FilterState(priority=Priority.NONE)
        result = FilterService.apply_filters(sample_tasks, f)
        assert len(result) == 0

    def test_task_without_due_date_in_date_filter(self, sample_tasks):
        """Test that tasks without due_date are excluded from date filters."""
        sample_tasks[0].due_date = None
        today = date.today()

        f = FilterState(date_range=(today, today + timedelta(days=7)))
        result = FilterService.apply_filters(sample_tasks, f)
        # Task without due_date should not appear
        for task in result:
            assert task.due_date is not None
