"""
Unit tests for TaskManager service.
Tests CRUD operations, task statistics, and JSON persistence.
"""

import json
import os
import pytest
import tempfile
from pathlib import Path
from src.models.task import Task
from src.services.task_service import TaskManager


@pytest.fixture
def temp_json_file():
    """Create a temporary JSON file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    yield temp_path
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def task_manager():
    """Create a fresh TaskManager instance for testing."""
    # Reset ID counter
    Task._next_id = 1
    return TaskManager(auto_load=False, data_file="test_tasks.json")


class TestTaskManagerInit:
    """Test TaskManager initialization."""

    def test_init_empty(self):
        """Test initializing empty task manager."""
        manager = TaskManager(auto_load=False)

        assert len(manager.tasks) == 0
        assert manager.data_file == "tasks.json"

    def test_init_with_custom_file(self):
        """Test initializing with custom data file."""
        manager = TaskManager(auto_load=False, data_file="custom.json")

        assert manager.data_file == "custom.json"

    def test_init_auto_load_nonexistent_file(self):
        """Test auto-load with non-existent file doesn't fail."""
        manager = TaskManager(auto_load=True, data_file="nonexistent.json")

        assert len(manager.tasks) == 0
        assert manager._loaded_from_file is False

    def test_init_auto_load_existing_file(self, temp_json_file):
        """Test auto-load with existing file."""
        # Create test data
        test_data = {
            "tasks": [
                {"id": 1, "title": "Task 1", "description": "Desc 1", "completed": False},
                {"id": 2, "title": "Task 2", "description": "Desc 2", "completed": True}
            ],
            "next_id": 3
        }

        with open(temp_json_file, 'w') as f:
            json.dump(test_data, f)

        # Create manager with auto-load
        manager = TaskManager(auto_load=True, data_file=temp_json_file)

        assert len(manager.tasks) == 2
        assert manager._loaded_from_file is True


class TestTaskManagerAdd:
    """Test adding tasks."""

    def test_add_task_with_title_only(self, task_manager):
        """Test adding task with only title."""
        task = task_manager.add_task("New Task")

        assert task.title == "New Task"
        assert task.description == ""
        assert len(task_manager.tasks) == 1

    def test_add_task_with_description(self, task_manager):
        """Test adding task with title and description."""
        task = task_manager.add_task("Task", "Description")

        assert task.title == "Task"
        assert task.description == "Description"

    def test_add_multiple_tasks(self, task_manager):
        """Test adding multiple tasks."""
        task1 = task_manager.add_task("Task 1")
        task2 = task_manager.add_task("Task 2")
        task3 = task_manager.add_task("Task 3")

        assert len(task_manager.tasks) == 3
        assert task1.id != task2.id != task3.id

    def test_add_task_invalid_title_raises_error(self, task_manager):
        """Test adding task with invalid title raises error."""
        with pytest.raises(ValueError):
            task_manager.add_task("")


class TestTaskManagerGet:
    """Test retrieving tasks."""

    def test_get_all_tasks_empty(self, task_manager):
        """Test getting all tasks from empty manager."""
        tasks = task_manager.get_all_tasks()
        assert tasks == []

    def test_get_all_tasks_sorted_by_date(self, task_manager):
        """Test that get_all_tasks returns tasks sorted by creation date (newest first)."""
        task1 = task_manager.add_task("First Task")
        task2 = task_manager.add_task("Second Task")
        task3 = task_manager.add_task("Third Task")

        tasks = task_manager.get_all_tasks()

        # Newest first
        assert tasks[0].id == task3.id
        assert tasks[1].id == task2.id
        assert tasks[2].id == task1.id

    def test_get_task_by_id_found(self, task_manager):
        """Test getting task by ID when it exists."""
        task = task_manager.add_task("Test Task")
        found = task_manager.get_task_by_id(task.id)

        assert found is not None
        assert found.id == task.id
        assert found.title == "Test Task"

    def test_get_task_by_id_not_found(self, task_manager):
        """Test getting task by ID when it doesn't exist."""
        task_manager.add_task("Task")
        found = task_manager.get_task_by_id(9999)

        assert found is None


class TestTaskManagerUpdate:
    """Test updating tasks."""

    def test_update_task_title(self, task_manager):
        """Test updating task title."""
        task = task_manager.add_task("Original Title", "Original Description")
        updated = task_manager.update_task(task.id, title="New Title")

        assert updated is not None
        assert updated.title == "New Title"
        assert updated.description == "Original Description"

    def test_update_task_description(self, task_manager):
        """Test updating task description."""
        task = task_manager.add_task("Title", "Original")
        updated = task_manager.update_task(task.id, description="New Description")

        assert updated is not None
        assert updated.title == "Title"
        assert updated.description == "New Description"

    def test_update_task_both_fields(self, task_manager):
        """Test updating both title and description."""
        task = task_manager.add_task("Old Title", "Old Description")
        updated = task_manager.update_task(
            task.id,
            title="New Title",
            description="New Description"
        )

        assert updated is not None
        assert updated.title == "New Title"
        assert updated.description == "New Description"

    def test_update_nonexistent_task(self, task_manager):
        """Test updating non-existent task returns None."""
        result = task_manager.update_task(9999, title="New Title")
        assert result is None

    def test_update_task_invalid_title_raises_error(self, task_manager):
        """Test updating task with invalid title raises error."""
        task = task_manager.add_task("Valid Title")

        with pytest.raises(ValueError):
            task_manager.update_task(task.id, title="")


class TestTaskManagerDelete:
    """Test deleting tasks."""

    def test_delete_task_success(self, task_manager):
        """Test successfully deleting a task."""
        task = task_manager.add_task("To Delete")
        result = task_manager.delete_task(task.id)

        assert result is True
        assert len(task_manager.tasks) == 0
        assert task_manager.get_task_by_id(task.id) is None

    def test_delete_task_not_found(self, task_manager):
        """Test deleting non-existent task returns False."""
        result = task_manager.delete_task(9999)
        assert result is False

    def test_delete_task_preserves_others(self, task_manager):
        """Test deleting one task doesn't affect others."""
        task1 = task_manager.add_task("Task 1")
        task2 = task_manager.add_task("Task 2")
        task3 = task_manager.add_task("Task 3")

        result = task_manager.delete_task(task2.id)

        assert result is True
        assert len(task_manager.tasks) == 2
        assert task_manager.get_task_by_id(task1.id) is not None
        assert task_manager.get_task_by_id(task3.id) is not None
        assert task_manager.get_task_by_id(task2.id) is None


class TestTaskManagerToggle:
    """Test toggling task completion."""

    def test_toggle_task_to_complete(self, task_manager):
        """Test toggling task from incomplete to complete."""
        task = task_manager.add_task("Task")
        assert task.completed is False

        toggled = task_manager.toggle_task_completion(task.id)

        assert toggled is not None
        assert toggled.completed is True

    def test_toggle_task_to_incomplete(self, task_manager):
        """Test toggling task from complete to incomplete."""
        task = task_manager.add_task("Task")
        task.toggle_completed()  # Make it complete
        assert task.completed is True

        toggled = task_manager.toggle_task_completion(task.id)

        assert toggled is not None
        assert toggled.completed is False

    def test_toggle_nonexistent_task(self, task_manager):
        """Test toggling non-existent task returns None."""
        result = task_manager.toggle_task_completion(9999)
        assert result is None


class TestTaskManagerStats:
    """Test task statistics."""

    def test_stats_empty(self, task_manager):
        """Test statistics for empty task list."""
        stats = task_manager.get_task_stats()

        assert stats["total"] == 0
        assert stats["completed"] == 0
        assert stats["pending"] == 0

    def test_stats_all_pending(self, task_manager):
        """Test statistics with all pending tasks."""
        task_manager.add_task("Task 1")
        task_manager.add_task("Task 2")
        task_manager.add_task("Task 3")

        stats = task_manager.get_task_stats()

        assert stats["total"] == 3
        assert stats["completed"] == 0
        assert stats["pending"] == 3

    def test_stats_all_completed(self, task_manager):
        """Test statistics with all completed tasks."""
        task1 = task_manager.add_task("Task 1")
        task2 = task_manager.add_task("Task 2")

        task_manager.toggle_task_completion(task1.id)
        task_manager.toggle_task_completion(task2.id)

        stats = task_manager.get_task_stats()

        assert stats["total"] == 2
        assert stats["completed"] == 2
        assert stats["pending"] == 0

    def test_stats_mixed(self, task_manager):
        """Test statistics with mixed completion status."""
        task1 = task_manager.add_task("Task 1")
        task_manager.add_task("Task 2")
        task3 = task_manager.add_task("Task 3")
        task_manager.add_task("Task 4")

        task_manager.toggle_task_completion(task1.id)
        task_manager.toggle_task_completion(task3.id)

        stats = task_manager.get_task_stats()

        assert stats["total"] == 4
        assert stats["completed"] == 2
        assert stats["pending"] == 2


class TestTaskManagerSaveJSON:
    """Test saving tasks to JSON."""

    def test_save_empty_tasks(self, task_manager, temp_json_file):
        """Test saving empty task list."""
        task_manager.save_to_json(temp_json_file)

        assert os.path.exists(temp_json_file)

        with open(temp_json_file, 'r') as f:
            data = json.load(f)

        assert data["tasks"] == []
        assert "next_id" in data
        assert "saved_at" in data

    def test_save_with_tasks(self, task_manager, temp_json_file):
        """Test saving task list with tasks."""
        task_manager.add_task("Task 1", "Description 1")
        task_manager.add_task("Task 2", "Description 2")

        task_manager.save_to_json(temp_json_file)

        with open(temp_json_file, 'r') as f:
            data = json.load(f)

        assert len(data["tasks"]) == 2
        assert data["tasks"][0]["title"] == "Task 1"
        assert data["tasks"][1]["title"] == "Task 2"

    def test_save_preserves_task_state(self, task_manager, temp_json_file):
        """Test that save preserves all task state."""
        task = task_manager.add_task("Completed Task", "Description")
        task_manager.toggle_task_completion(task.id)

        task_manager.save_to_json(temp_json_file)

        with open(temp_json_file, 'r') as f:
            data = json.load(f)

        saved_task = data["tasks"][0]
        assert saved_task["completed"] is True
        assert saved_task["description"] == "Description"

    def test_save_to_invalid_location_raises_error(self, task_manager):
        """Test saving to invalid location raises error."""
        with pytest.raises(PermissionError):
            task_manager.save_to_json("/root/cannot_write_here.json")

    def test_save_uses_default_file(self, task_manager, temp_json_file):
        """Test that save uses default file if no filename provided."""
        task_manager.data_file = temp_json_file
        task_manager.add_task("Task")

        task_manager.save_to_json()  # No filename argument

        assert os.path.exists(temp_json_file)


class TestTaskManagerLoadJSON:
    """Test loading tasks from JSON."""

    def test_load_nonexistent_file_raises_error(self, task_manager):
        """Test loading non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            task_manager.load_from_json("nonexistent.json")

    def test_load_valid_file(self, task_manager, temp_json_file):
        """Test loading valid JSON file."""
        test_data = {
            "tasks": [
                {"id": 1, "title": "Task 1", "description": "Desc 1", "completed": False},
                {"id": 2, "title": "Task 2", "description": "Desc 2", "completed": True}
            ],
            "next_id": 3
        }

        with open(temp_json_file, 'w') as f:
            json.dump(test_data, f)

        count = task_manager.load_from_json(temp_json_file)

        assert count == 2
        assert len(task_manager.tasks) == 2
        assert task_manager.tasks[0].title == "Task 1"
        assert task_manager.tasks[1].completed is True

    def test_load_restores_id_counter(self, task_manager, temp_json_file):
        """Test that load restores the ID counter."""
        test_data = {
            "tasks": [{"id": 1, "title": "Task"}],
            "next_id": 10
        }

        with open(temp_json_file, 'w') as f:
            json.dump(test_data, f)

        task_manager.load_from_json(temp_json_file)

        assert Task._next_id == 10

    def test_load_corrupt_json_raises_error(self, task_manager, temp_json_file):
        """Test loading corrupt JSON raises ValueError."""
        with open(temp_json_file, 'w') as f:
            f.write("{ this is not valid json }")

        with pytest.raises(ValueError, match="Corrupt JSON"):
            task_manager.load_from_json(temp_json_file)

    def test_load_invalid_structure_raises_error(self, task_manager, temp_json_file):
        """Test loading JSON with invalid structure raises ValueError."""
        with open(temp_json_file, 'w') as f:
            json.dump({"wrong": "structure"}, f)

        with pytest.raises(ValueError, match="Invalid data format"):
            task_manager.load_from_json(temp_json_file)

    def test_load_clears_existing_tasks(self, task_manager, temp_json_file):
        """Test that load clears existing tasks."""
        task_manager.add_task("Existing Task")
        assert len(task_manager.tasks) == 1

        test_data = {
            "tasks": [{"id": 10, "title": "New Task"}],
            "next_id": 11
        }

        with open(temp_json_file, 'w') as f:
            json.dump(test_data, f)

        task_manager.load_from_json(temp_json_file)

        assert len(task_manager.tasks) == 1
        assert task_manager.tasks[0].title == "New Task"

    def test_load_skips_invalid_tasks(self, task_manager, temp_json_file, capsys):
        """Test that load skips invalid tasks but continues loading."""
        test_data = {
            "tasks": [
                {"id": 1, "title": "Valid Task"},
                {"id": 2},  # Missing title - invalid
                {"id": 3, "title": "Another Valid Task"}
            ],
            "next_id": 4
        }

        with open(temp_json_file, 'w') as f:
            json.dump(test_data, f)

        count = task_manager.load_from_json(temp_json_file)

        assert count == 2  # Only 2 valid tasks loaded
        assert len(task_manager.tasks) == 2

        # Check warning was printed
        captured = capsys.readouterr()
        assert "Warning: Skipping invalid task" in captured.out


class TestTaskManagerPersistence:
    """Test full persistence workflow."""

    def test_save_and_load_round_trip(self, task_manager, temp_json_file):
        """Test complete save and load cycle."""
        # Add tasks
        task1 = task_manager.add_task("Task 1", "Description 1")
        task2 = task_manager.add_task("Task 2", "Description 2")
        task_manager.toggle_task_completion(task1.id)

        # Save
        task_manager.save_to_json(temp_json_file)

        # Create new manager and load
        new_manager = TaskManager(auto_load=False, data_file=temp_json_file)
        new_manager.load_from_json()

        # Verify
        assert len(new_manager.tasks) == 2

        loaded_task1 = new_manager.get_task_by_id(task1.id)
        assert loaded_task1 is not None
        assert loaded_task1.title == "Task 1"
        assert loaded_task1.completed is True

        loaded_task2 = new_manager.get_task_by_id(task2.id)
        assert loaded_task2 is not None
        assert loaded_task2.title == "Task 2"
        assert loaded_task2.completed is False

    def test_auto_save_after_add(self, task_manager, temp_json_file):
        """Test that auto-save works after adding task."""
        task_manager.data_file = temp_json_file
        task_manager.add_task("New Task")

        # File should exist due to auto-save
        assert os.path.exists(temp_json_file)

        # Verify content
        with open(temp_json_file, 'r') as f:
            data = json.load(f)

        assert len(data["tasks"]) == 1

    def test_auto_save_after_update(self, task_manager, temp_json_file):
        """Test that auto-save works after updating task."""
        task_manager.data_file = temp_json_file
        task = task_manager.add_task("Original")

        task_manager.update_task(task.id, title="Updated")

        # Verify saved content
        with open(temp_json_file, 'r') as f:
            data = json.load(f)

        assert data["tasks"][0]["title"] == "Updated"

    def test_auto_save_after_delete(self, task_manager, temp_json_file):
        """Test that auto-save works after deleting task."""
        task_manager.data_file = temp_json_file
        task = task_manager.add_task("To Delete")
        task_manager.delete_task(task.id)

        # Verify saved content
        with open(temp_json_file, 'r') as f:
            data = json.load(f)

        assert len(data["tasks"]) == 0

    def test_auto_save_after_toggle(self, task_manager, temp_json_file):
        """Test that auto-save works after toggling task."""
        task_manager.data_file = temp_json_file
        task = task_manager.add_task("Task")

        task_manager.toggle_task_completion(task.id)

        # Verify saved content
        with open(temp_json_file, 'r') as f:
            data = json.load(f)

        assert data["tasks"][0]["completed"] is True
