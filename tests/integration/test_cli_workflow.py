"""
Integration tests for CLI workflow.
Tests complete CRUD cycles, persistence workflows, and error recovery.
"""

import json
import os
import pytest
import tempfile
from pathlib import Path
from src.models.task import Task
from src.services.task_service import TaskManager
from src.cli.themes import set_theme, get_current_theme


@pytest.fixture
def temp_data_file():
    """Create a temporary data file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    yield temp_path
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)
    # Also cleanup backup files
    for backup in Path(temp_path).parent.glob(f"{Path(temp_path).name}.corrupt.*"):
        backup.unlink()


@pytest.fixture
def fresh_manager(temp_data_file):
    """Create a fresh TaskManager for each test."""
    Task._next_id = 1  # Reset ID counter
    return TaskManager(auto_load=False, data_file=temp_data_file)


class TestCRUDWorkflow:
    """Test complete CRUD workflow."""

    def test_full_crud_cycle(self, fresh_manager):
        """Test complete create-read-update-delete cycle."""
        # CREATE
        task = fresh_manager.add_task("Buy groceries", "Milk, bread, eggs")
        assert task.id == 1
        assert task.title == "Buy groceries"

        # READ
        all_tasks = fresh_manager.get_all_tasks()
        assert len(all_tasks) == 1

        retrieved = fresh_manager.get_task_by_id(task.id)
        assert retrieved is not None
        assert retrieved.title == "Buy groceries"

        # UPDATE
        updated = fresh_manager.update_task(task.id, title="Buy groceries and fruits")
        assert updated.title == "Buy groceries and fruits"

        # COMPLETE
        toggled = fresh_manager.toggle_task_completion(task.id)
        assert toggled.completed is True

        # DELETE
        deleted = fresh_manager.delete_task(task.id)
        assert deleted is True
        assert len(fresh_manager.get_all_tasks()) == 0

    def test_multiple_tasks_workflow(self, fresh_manager):
        """Test workflow with multiple tasks."""
        # Add multiple tasks
        task1 = fresh_manager.add_task("Task 1", "First task")
        task2 = fresh_manager.add_task("Task 2", "Second task")
        task3 = fresh_manager.add_task("Task 3", "Third task")

        assert len(fresh_manager.get_all_tasks()) == 3

        # Complete one
        fresh_manager.toggle_task_completion(task2.id)

        # Check stats
        stats = fresh_manager.get_task_stats()
        assert stats["total"] == 3
        assert stats["completed"] == 1
        assert stats["pending"] == 2

        # Update one
        fresh_manager.update_task(task1.id, description="Updated description")
        assert task1.description == "Updated description"

        # Delete one
        fresh_manager.delete_task(task3.id)
        assert len(fresh_manager.get_all_tasks()) == 2

    def test_task_sorting_workflow(self, fresh_manager):
        """Test that tasks are sorted correctly in workflow."""
        task1 = fresh_manager.add_task("First")
        task2 = fresh_manager.add_task("Second")
        task3 = fresh_manager.add_task("Third")

        # Get all tasks (should be newest first)
        tasks = fresh_manager.get_all_tasks()

        assert tasks[0].id == task3.id  # Newest
        assert tasks[1].id == task2.id
        assert tasks[2].id == task1.id  # Oldest


class TestPersistenceWorkflow:
    """Test persistence workflow."""

    def test_add_save_load_workflow(self, temp_data_file):
        """Test adding tasks, saving, and loading in new session."""
        # Session 1: Add tasks and save
        manager1 = TaskManager(auto_load=False, data_file=temp_data_file)
        Task._next_id = 1

        task1 = manager1.add_task("Task 1", "Description 1")
        task2 = manager1.add_task("Task 2", "Description 2")
        manager1.toggle_task_completion(task1.id)

        manager1.save_to_json()

        # Session 2: Load tasks
        Task._next_id = 1  # Reset
        manager2 = TaskManager(auto_load=True, data_file=temp_data_file)

        assert len(manager2.tasks) == 2

        loaded_task1 = manager2.get_task_by_id(task1.id)
        assert loaded_task1.title == "Task 1"
        assert loaded_task1.completed is True

        loaded_task2 = manager2.get_task_by_id(task2.id)
        assert loaded_task2.title == "Task 2"
        assert loaded_task2.completed is False

    def test_auto_save_workflow(self, temp_data_file):
        """Test that auto-save works throughout workflow."""
        manager = TaskManager(auto_load=False, data_file=temp_data_file)

        # Add task (triggers auto-save)
        task = manager.add_task("Auto-saved task")

        # Verify file was created
        assert os.path.exists(temp_data_file)

        # Load in new manager
        manager2 = TaskManager(auto_load=True, data_file=temp_data_file)
        assert len(manager2.tasks) == 1

        # Update task (triggers auto-save)
        manager.update_task(task.id, title="Updated title")

        # Reload and verify
        manager3 = TaskManager(auto_load=True, data_file=temp_data_file)
        loaded = manager3.get_task_by_id(task.id)
        assert loaded.title == "Updated title"

    def test_persistence_preserves_all_state(self, temp_data_file):
        """Test that persistence preserves all task state."""
        manager1 = TaskManager(auto_load=False, data_file=temp_data_file)
        Task._next_id = 1

        # Create task with specific state
        task = manager1.add_task("Complex Task", "Detailed description")
        manager1.toggle_task_completion(task.id)
        manager1.update_task(task.id, description="Updated description")

        manager1.save_to_json()

        # Load in new session
        manager2 = TaskManager(auto_load=True, data_file=temp_data_file)
        loaded = manager2.get_task_by_id(task.id)

        assert loaded.title == "Complex Task"
        assert loaded.description == "Updated description"
        assert loaded.completed is True
        assert loaded.id == task.id

    def test_persistence_with_empty_list(self, temp_data_file):
        """Test persistence workflow with empty task list."""
        manager1 = TaskManager(auto_load=False, data_file=temp_data_file)

        # Save empty list
        manager1.save_to_json()

        # Load empty list
        manager2 = TaskManager(auto_load=True, data_file=temp_data_file)

        assert len(manager2.tasks) == 0

    def test_persistence_after_delete_all(self, temp_data_file):
        """Test persistence after deleting all tasks."""
        manager = TaskManager(auto_load=False, data_file=temp_data_file)

        # Add and delete tasks
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")

        manager.delete_task(task1.id)
        manager.delete_task(task2.id)

        # Reload
        manager2 = TaskManager(auto_load=True, data_file=temp_data_file)

        assert len(manager2.tasks) == 0


class TestErrorRecovery:
    """Test error recovery scenarios."""

    def test_missing_file_recovery(self, fresh_manager):
        """Test recovery when JSON file doesn't exist."""
        # Try to load non-existent file
        try:
            fresh_manager.load_from_json("nonexistent.json")
            assert False, "Should raise FileNotFoundError"
        except FileNotFoundError:
            pass  # Expected

        # Should still be able to use manager
        task = fresh_manager.add_task("New Task")
        assert task.title == "New Task"
        assert len(fresh_manager.tasks) == 1

    def test_corrupt_json_recovery(self, temp_data_file):
        """Test recovery from corrupt JSON file."""
        # Create corrupt JSON file
        with open(temp_data_file, 'w') as f:
            f.write("{ this is not valid json }")

        manager = TaskManager(auto_load=False, data_file=temp_data_file)

        # Try to load corrupt file
        try:
            manager.load_from_json()
            assert False, "Should raise ValueError"
        except ValueError as e:
            assert "Corrupt JSON" in str(e)

        # Should have created backup
        backup_files = list(Path(temp_data_file).parent.glob(f"{Path(temp_data_file).name}.corrupt.*"))
        assert len(backup_files) > 0

        # Manager should still be usable
        task = manager.add_task("Recovery Task")
        assert task.title == "Recovery Task"

    def test_invalid_data_structure_recovery(self, temp_data_file):
        """Test recovery from invalid data structure."""
        # Create JSON with invalid structure
        with open(temp_data_file, 'w') as f:
            json.dump({"wrong": "structure"}, f)

        manager = TaskManager(auto_load=False, data_file=temp_data_file)

        # Try to load
        try:
            manager.load_from_json()
            assert False, "Should raise ValueError"
        except ValueError as e:
            assert "Invalid data format" in str(e)

        # Manager should still be usable
        task = manager.add_task("Recovery Task")
        assert len(manager.tasks) == 1

    def test_partial_corrupt_data_recovery(self, temp_data_file, capsys):
        """Test recovery when some tasks are corrupt."""
        # Create data with mix of valid and invalid tasks
        data = {
            "tasks": [
                {"id": 1, "title": "Valid Task 1"},
                {"id": 2},  # Missing title
                {"id": 3, "title": "Valid Task 2"}
            ],
            "next_id": 4
        }

        with open(temp_data_file, 'w') as f:
            json.dump(data, f)

        manager = TaskManager(auto_load=True, data_file=temp_data_file)

        # Should load valid tasks and skip invalid ones
        assert len(manager.tasks) == 2

        # Should have printed warning
        captured = capsys.readouterr()
        assert "Warning: Skipping invalid task" in captured.out

    def test_auto_load_with_corrupt_file(self, temp_data_file, capsys):
        """Test auto-load behavior with corrupt file."""
        # Create corrupt file
        with open(temp_data_file, 'w') as f:
            f.write("corrupt data")

        # Auto-load should not crash initialization
        manager = TaskManager(auto_load=True, data_file=temp_data_file)

        # Should have empty task list
        assert len(manager.tasks) == 0
        assert manager._loaded_from_file is False

        # Should have printed warning
        captured = capsys.readouterr()
        assert "Warning" in captured.out


class TestComplexWorkflows:
    """Test complex multi-step workflows."""

    def test_complete_user_session(self, temp_data_file):
        """Test complete user session workflow."""
        manager = TaskManager(auto_load=True, data_file=temp_data_file)

        # User adds several tasks
        task1 = manager.add_task("Write report", "Q4 financial report")
        task2 = manager.add_task("Call client", "Discuss project requirements")
        task3 = manager.add_task("Review code", "PR #123")

        # User checks stats
        stats = manager.get_task_stats()
        assert stats["total"] == 3
        assert stats["pending"] == 3

        # User completes one task
        manager.toggle_task_completion(task1.id)

        # User updates another
        manager.update_task(task2.id, description="Discuss project requirements and timeline")

        # User checks stats again
        stats = manager.get_task_stats()
        assert stats["completed"] == 1
        assert stats["pending"] == 2

        # User deletes completed task
        manager.delete_task(task1.id)

        # Final state
        assert len(manager.get_all_tasks()) == 2

        # Reload session
        manager2 = TaskManager(auto_load=True, data_file=temp_data_file)
        assert len(manager2.tasks) == 2

    def test_multi_session_workflow(self, temp_data_file):
        """Test workflow across multiple sessions."""
        # Session 1: Initial setup
        Task._next_id = 1
        manager1 = TaskManager(auto_load=False, data_file=temp_data_file)
        manager1.add_task("Task 1")
        manager1.add_task("Task 2")
        manager1.save_to_json()

        # Session 2: Add more and complete some
        manager2 = TaskManager(auto_load=True, data_file=temp_data_file)
        task3 = manager2.add_task("Task 3")
        manager2.toggle_task_completion(manager2.tasks[0].id)
        manager2.save_to_json()

        # Session 3: Update and delete
        manager3 = TaskManager(auto_load=True, data_file=temp_data_file)
        assert len(manager3.tasks) == 3
        manager3.update_task(task3.id, description="Updated in session 3")
        manager3.delete_task(manager3.tasks[0].id)

        # Session 4: Verify final state
        manager4 = TaskManager(auto_load=True, data_file=temp_data_file)
        assert len(manager4.tasks) == 2

    def test_concurrent_operations(self, temp_data_file):
        """Test multiple operations in quick succession."""
        manager = TaskManager(auto_load=False, data_file=temp_data_file)

        # Rapid operations
        tasks = []
        for i in range(10):
            task = manager.add_task(f"Task {i}", f"Description {i}")
            tasks.append(task)

        # Complete every other task
        for i in range(0, 10, 2):
            manager.toggle_task_completion(tasks[i].id)

        # Update half
        for i in range(5):
            manager.update_task(tasks[i].id, description=f"Updated {i}")

        # Delete some
        for i in range(7, 10):
            manager.delete_task(tasks[i].id)

        # Verify final state
        assert len(manager.get_all_tasks()) == 7
        stats = manager.get_task_stats()
        assert stats["completed"] == 4  # Tasks 0, 2, 4, 6 (task 8 was deleted)


class TestThemeIntegration:
    """Test theme integration with workflow."""

    def test_theme_switching_workflow(self):
        """Test theme switching during workflow."""
        # Start with dark theme
        set_theme("dark")
        assert get_current_theme().name == "Dark"

        # Switch to light
        set_theme("light")
        assert get_current_theme().name == "Light"

        # Switch to hacker
        set_theme("hacker")
        assert get_current_theme().name == "Hacker"

        # Reset
        set_theme("dark")

    def test_theme_colors_accessible_in_workflow(self):
        """Test that theme colors are accessible throughout workflow."""
        set_theme("dark")
        theme = get_current_theme()

        # Should be able to use theme colors
        assert theme.success is not None
        assert theme.error is not None
        assert theme.warning is not None
        assert theme.info is not None

        # Switch theme
        set_theme("light")
        theme = get_current_theme()

        # Colors should still be accessible
        assert theme.success is not None
        assert theme.error is not None

        # Reset
        set_theme("dark")


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_long_title(self, fresh_manager):
        """Test task with maximum length title."""
        long_title = "a" * 200
        task = fresh_manager.add_task(long_title)

        assert len(task.title) == 200

        # Should be able to retrieve
        retrieved = fresh_manager.get_task_by_id(task.id)
        assert len(retrieved.title) == 200

    def test_very_long_description(self, fresh_manager):
        """Test task with maximum length description."""
        long_desc = "a" * 1000
        task = fresh_manager.add_task("Task", long_desc)

        assert len(task.description) == 1000

    def test_many_tasks(self, fresh_manager):
        """Test workflow with many tasks."""
        # Add 100 tasks
        for i in range(100):
            fresh_manager.add_task(f"Task {i}")

        assert len(fresh_manager.tasks) == 100

        # Get all tasks (should handle sorting)
        all_tasks = fresh_manager.get_all_tasks()
        assert len(all_tasks) == 100

        # Stats should be correct
        stats = fresh_manager.get_task_stats()
        assert stats["total"] == 100

    def test_empty_description(self, fresh_manager):
        """Test task with empty description."""
        task = fresh_manager.add_task("Task", "")

        assert task.description == ""

        retrieved = fresh_manager.get_task_by_id(task.id)
        assert retrieved.description == ""

    def test_special_characters_in_task(self, fresh_manager):
        """Test task with special characters."""
        special_title = "Task with émojis 🚀 and spëcial chars: @#$%"
        special_desc = "Description with 中文 and symbols: €£¥"

        task = fresh_manager.add_task(special_title, special_desc)

        assert task.title == special_title
        assert task.description == special_desc

        # Should persist correctly
        retrieved = fresh_manager.get_task_by_id(task.id)
        assert retrieved.title == special_title
        assert retrieved.description == special_desc
