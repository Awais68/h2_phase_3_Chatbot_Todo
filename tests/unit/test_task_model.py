"""
Unit tests for Task model.
Tests task creation, validation, serialization, and state management.
"""

import pytest
from datetime import datetime
from src.models.task import Task


class TestTaskCreation:
    """Test task creation and initialization."""

    def test_create_task_with_title_only(self):
        """Test creating a task with only a title."""
        task = Task(title="Test Task")

        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False
        assert task.id >= 1
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_create_task_with_all_fields(self):
        """Test creating a task with all fields."""
        task = Task(
            title="Complete Task",
            description="This is a test description",
            completed=True
        )

        assert task.title == "Complete Task"
        assert task.description == "This is a test description"
        assert task.completed is True

    def test_create_task_with_custom_id(self):
        """Test creating a task with a custom ID."""
        task = Task(title="Custom ID Task", task_id=100)

        assert task.id == 100
        assert task.title == "Custom ID Task"

    def test_task_ids_auto_increment(self):
        """Test that task IDs auto-increment."""
        # Reset ID counter
        Task._next_id = 1

        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        task3 = Task(title="Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_title_whitespace_trimmed(self):
        """Test that title whitespace is trimmed."""
        task = Task(title="  Trimmed Title  ")
        assert task.title == "Trimmed Title"


class TestTaskValidation:
    """Test task validation rules."""

    def test_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task(title="")

    def test_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task(title="   ")

    def test_title_too_long_raises_error(self):
        """Test that title exceeding 200 chars raises ValueError."""
        long_title = "a" * 201
        with pytest.raises(ValueError, match="Title cannot exceed 200 characters"):
            Task(title=long_title)

    def test_title_exactly_200_chars_succeeds(self):
        """Test that title with exactly 200 chars succeeds."""
        max_title = "a" * 200
        task = Task(title=max_title)
        assert len(task.title) == 200

    def test_description_too_long_raises_error(self):
        """Test that description exceeding 1000 chars raises ValueError."""
        long_desc = "a" * 1001
        with pytest.raises(ValueError, match="Description cannot exceed 1000 characters"):
            Task(title="Valid", description=long_desc)

    def test_description_exactly_1000_chars_succeeds(self):
        """Test that description with exactly 1000 chars succeeds."""
        max_desc = "a" * 1000
        task = Task(title="Valid", description=max_desc)
        assert len(task.description) == 1000


class TestTaskUpdate:
    """Test task update operations."""

    def test_update_title(self):
        """Test updating task title."""
        task = Task(title="Original Title", description="Original Description")
        original_updated_at = task.updated_at

        task.update(title="Updated Title")

        assert task.title == "Updated Title"
        assert task.description == "Original Description"
        assert task.updated_at > original_updated_at

    def test_update_description(self):
        """Test updating task description."""
        task = Task(title="Title", description="Original")
        original_updated_at = task.updated_at

        task.update(description="Updated Description")

        assert task.title == "Title"
        assert task.description == "Updated Description"
        assert task.updated_at > original_updated_at

    def test_update_both_fields(self):
        """Test updating both title and description."""
        task = Task(title="Old Title", description="Old Description")

        task.update(title="New Title", description="New Description")

        assert task.title == "New Title"
        assert task.description == "New Description"

    def test_update_with_empty_title_raises_error(self):
        """Test that updating with empty title raises ValueError."""
        task = Task(title="Valid Title")

        with pytest.raises(ValueError, match="Title cannot be empty"):
            task.update(title="")

    def test_update_with_title_too_long_raises_error(self):
        """Test that updating with title > 200 chars raises ValueError."""
        task = Task(title="Valid Title")
        long_title = "a" * 201

        with pytest.raises(ValueError, match="Title cannot exceed 200 characters"):
            task.update(title=long_title)

    def test_update_with_description_too_long_raises_error(self):
        """Test that updating with description > 1000 chars raises ValueError."""
        task = Task(title="Valid Title")
        long_desc = "a" * 1001

        with pytest.raises(ValueError, match="Description cannot exceed 1000 characters"):
            task.update(description=long_desc)

    def test_update_with_none_keeps_original(self):
        """Test that passing None to update keeps original values."""
        task = Task(title="Original Title", description="Original Description")

        task.update(title=None, description=None)

        assert task.title == "Original Title"
        assert task.description == "Original Description"


class TestTaskCompletion:
    """Test task completion toggle."""

    def test_toggle_from_incomplete_to_complete(self):
        """Test toggling task from incomplete to complete."""
        task = Task(title="Task")
        assert task.completed is False

        task.toggle_completed()

        assert task.completed is True

    def test_toggle_from_complete_to_incomplete(self):
        """Test toggling task from complete to incomplete."""
        task = Task(title="Task", completed=True)
        assert task.completed is True

        task.toggle_completed()

        assert task.completed is False

    def test_toggle_multiple_times(self):
        """Test toggling task multiple times."""
        task = Task(title="Task")

        task.toggle_completed()
        assert task.completed is True

        task.toggle_completed()
        assert task.completed is False

        task.toggle_completed()
        assert task.completed is True

    def test_toggle_updates_timestamp(self):
        """Test that toggle updates the updated_at timestamp."""
        task = Task(title="Task")
        original_updated_at = task.updated_at

        task.toggle_completed()

        assert task.updated_at > original_updated_at


class TestTaskSerialization:
    """Test task serialization and deserialization."""

    def test_to_dict_basic(self):
        """Test converting task to dictionary."""
        task = Task(title="Test Task", description="Test Description", task_id=5)
        task_dict = task.to_dict()

        assert task_dict["id"] == 5
        assert task_dict["title"] == "Test Task"
        assert task_dict["description"] == "Test Description"
        assert task_dict["completed"] is False
        assert "created_at" in task_dict
        assert "updated_at" in task_dict

    def test_to_dict_completed_task(self):
        """Test converting completed task to dictionary."""
        task = Task(title="Completed Task", completed=True)
        task_dict = task.to_dict()

        assert task_dict["completed"] is True

    def test_to_dict_timestamps_iso_format(self):
        """Test that timestamps are in ISO format."""
        task = Task(title="Task")
        task_dict = task.to_dict()

        # Verify ISO format by parsing
        datetime.fromisoformat(task_dict["created_at"])
        datetime.fromisoformat(task_dict["updated_at"])

    def test_from_dict_basic(self):
        """Test creating task from dictionary."""
        data = {
            "id": 10,
            "title": "From Dict Task",
            "description": "From dict description",
            "completed": False
        }

        task = Task.from_dict(data)

        assert task.id == 10
        assert task.title == "From Dict Task"
        assert task.description == "From dict description"
        assert task.completed is False

    def test_from_dict_with_timestamps(self):
        """Test creating task from dictionary with timestamps."""
        created_time = "2025-12-25T10:30:00"
        updated_time = "2025-12-25T11:45:00"

        data = {
            "id": 20,
            "title": "Task with Timestamps",
            "description": "Description",
            "completed": True,
            "created_at": created_time,
            "updated_at": updated_time
        }

        task = Task.from_dict(data)

        assert task.id == 20
        assert task.created_at.isoformat() == created_time
        assert task.updated_at.isoformat() == updated_time

    def test_from_dict_missing_id_raises_error(self):
        """Test that from_dict raises error when id is missing."""
        data = {"title": "No ID Task"}

        with pytest.raises(ValueError, match="Task data must include 'id' and 'title'"):
            Task.from_dict(data)

    def test_from_dict_missing_title_raises_error(self):
        """Test that from_dict raises error when title is missing."""
        data = {"id": 30}

        with pytest.raises(ValueError, match="Task data must include 'id' and 'title'"):
            Task.from_dict(data)

    def test_from_dict_with_defaults(self):
        """Test that from_dict uses defaults for missing optional fields."""
        data = {"id": 40, "title": "Minimal Task"}

        task = Task.from_dict(data)

        assert task.description == ""
        assert task.completed is False

    def test_from_dict_invalid_timestamp_uses_default(self):
        """Test that invalid timestamps are handled gracefully."""
        data = {
            "id": 50,
            "title": "Task",
            "created_at": "invalid-timestamp",
            "updated_at": "also-invalid"
        }

        # Should not raise error - uses default timestamps
        task = Task.from_dict(data)

        assert task.id == 50
        assert task.title == "Task"

    def test_round_trip_serialization(self):
        """Test that task can be serialized and deserialized."""
        original = Task(
            title="Round Trip Task",
            description="Testing serialization",
            completed=True,
            task_id=99
        )

        # Serialize to dict
        task_dict = original.to_dict()

        # Deserialize from dict
        restored = Task.from_dict(task_dict)

        assert restored.id == original.id
        assert restored.title == original.title
        assert restored.description == original.description
        assert restored.completed == original.completed


class TestTaskStringRepresentation:
    """Test task string representations."""

    def test_str_incomplete_task(self):
        """Test __str__ for incomplete task."""
        task = Task(title="Test Task", task_id=5)
        task_str = str(task)

        assert "ID: 5" in task_str
        assert "Test Task" in task_str
        assert "•" in task_str  # Incomplete marker

    def test_str_completed_task(self):
        """Test __str__ for completed task."""
        task = Task(title="Completed Task", task_id=10, completed=True)
        task_str = str(task)

        assert "ID: 10" in task_str
        assert "Completed Task" in task_str
        assert "✓" in task_str  # Complete marker

    def test_repr(self):
        """Test __repr__ contains key information."""
        task = Task(title="Test Task", task_id=15, completed=True)
        task_repr = repr(task)

        assert "Task(" in task_repr
        assert "id=15" in task_repr
        assert "title='Test Task'" in task_repr
        assert "completed=True" in task_repr
