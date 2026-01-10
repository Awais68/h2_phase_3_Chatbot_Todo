#!/usr/bin/env python3
"""
Quick test script for Phase I Complete Task Management System.
Tests core functionality without requiring user interaction.
"""

from datetime import date, timedelta
from src.models.task import Task
from src.models.enums import Priority, Recurrence, Status, SortBy
from src.services.task_service import TaskManager
from src.services.filter_service import FilterState, FilterService
from src.services.search_service import SearchService
from src.utils.date_utils import parse_date

def test_task_model():
    """Test Task model with new fields."""
    print("Testing Task model...")

    # Test basic task
    task1 = Task(
        title="Test task",
        description="Test description",
        priority=Priority.HIGH,
        due_date=date.today() + timedelta(days=1),
        recurrence=Recurrence.NONE
    )
    assert task1.title == "Test task"
    assert task1.priority == Priority.HIGH
    assert task1.status == Status.PENDING
    print("✓ Basic task creation works")

    # Test overdue task
    task2 = Task(
        title="Overdue task",
        due_date=date.today() - timedelta(days=1)
    )
    assert task2.status == Status.OVERDUE
    print("✓ Overdue status detection works")

    # Test completed task
    task3 = Task(title="Completed task", completed=True)
    assert task3.status == Status.COMPLETED
    print("✓ Completed status works")

    # Test to_dict/from_dict
    task_dict = task1.to_dict()
    task_restored = Task.from_dict(task_dict)
    assert task_restored.title == task1.title
    assert task_restored.priority == task1.priority
    assert task_restored.due_date == task1.due_date
    print("✓ Serialization/deserialization works")


def test_date_parsing():
    """Test date parsing."""
    print("\nTesting date parsing...")

    # Test relative dates
    tomorrow = parse_date("tomorrow")
    assert tomorrow == date.today() + timedelta(days=1)
    print("✓ 'tomorrow' parses correctly")

    # Test ISO dates
    specific_date = parse_date("2025-12-31")
    assert specific_date == date(2025, 12, 31)
    print("✓ ISO date parsing works")

    # Test invalid date
    invalid = parse_date("invalid")
    assert invalid is None
    print("✓ Invalid date returns None")


def test_task_manager():
    """Test TaskManager with new features."""
    print("\nTesting TaskManager...")

    manager = TaskManager(auto_load=False, data_file="test_tasks.json")

    # Add tasks with new fields
    task1 = manager.add_task(
        title="High priority task",
        priority=Priority.HIGH,
        due_date=date.today() + timedelta(days=1)
    )
    print(f"✓ Created task #{task1.id} with priority and due date")

    # Add recurring task
    task2 = manager.add_task(
        title="Daily task",
        priority=Priority.MEDIUM,
        due_date=date.today(),
        recurrence=Recurrence.DAILY
    )
    print(f"✓ Created recurring task #{task2.id}")

    # Test recurring task completion
    result = manager.toggle_task_completion(task2.id)
    assert result.id != task2.id  # Should be new task
    assert result.due_date == date.today() + timedelta(days=1)
    print(f"✓ Recurring task created next occurrence #{result.id}")

    # Add overdue task
    task3 = manager.add_task(
        title="Overdue task",
        priority=Priority.LOW,
        due_date=date.today() - timedelta(days=2)
    )
    print(f"✓ Created overdue task #{task3.id}")


def test_filtering():
    """Test filtering functionality."""
    print("\nTesting filtering...")

    manager = TaskManager(auto_load=False, data_file="test_tasks2.json")

    # Create test tasks
    manager.add_task("Task 1", priority=Priority.HIGH, due_date=date.today())
    manager.add_task("Task 2", priority=Priority.LOW, due_date=date.today() + timedelta(days=7))
    manager.add_task("Task 3", priority=Priority.HIGH, due_date=date.today() - timedelta(days=1))

    tasks = manager.get_all_tasks()
    print(f"✓ Created {len(tasks)} test tasks")

    # Test status filter
    filter_state = FilterState(status=Status.OVERDUE)
    filtered = FilterService.apply_filters(tasks, filter_state)
    assert len(filtered) == 1
    print(f"✓ Status filter works ({len(filtered)} overdue tasks)")

    # Test priority filter
    filter_state = FilterState(priority=Priority.HIGH)
    filtered = FilterService.apply_filters(tasks, filter_state)
    assert len(filtered) == 2
    print(f"✓ Priority filter works ({len(filtered)} high priority tasks)")

    # Test search
    manager.add_task("Buy groceries")
    manager.add_task("Buy tickets")
    tasks = manager.get_all_tasks()
    results = SearchService.search(tasks, "buy")
    assert len(results) == 2
    print(f"✓ Search works ({len(results)} tasks match 'buy')")


def test_sorting():
    """Test sorting functionality."""
    print("\nTesting sorting...")

    manager = TaskManager(auto_load=False, data_file="test_tasks3.json")

    # Create tasks with different priorities and due dates
    task1 = manager.add_task(
        "Low priority",
        priority=Priority.LOW,
        due_date=date.today() + timedelta(days=5)
    )
    task2 = manager.add_task(
        "High priority",
        priority=Priority.HIGH,
        due_date=date.today() + timedelta(days=3)
    )
    task3 = manager.add_task(
        "Overdue",
        priority=Priority.MEDIUM,
        due_date=date.today() - timedelta(days=1)
    )

    tasks = manager.get_all_tasks()

    # Test DEFAULT sort (overdue first)
    sorted_tasks = manager.sort_tasks(tasks, SortBy.DEFAULT)
    assert sorted_tasks[0].id == task3.id  # Overdue should be first
    print("✓ DEFAULT sort works (overdue first)")

    # Test PRIORITY sort
    sorted_tasks = manager.sort_tasks(tasks, SortBy.PRIORITY)
    assert sorted_tasks[0].id == task3.id  # Overdue still first
    assert sorted_tasks[1].priority == Priority.HIGH  # Then high priority
    print("✓ PRIORITY sort works")

    # Test DUE_DATE sort
    sorted_tasks = manager.sort_tasks(tasks, SortBy.DUE_DATE)
    assert sorted_tasks[0].id == task3.id  # Overdue first
    print("✓ DUE_DATE sort works")


def test_persistence():
    """Test JSON persistence with new fields."""
    print("\nTesting persistence...")

    import os

    # Create manager and add tasks
    manager1 = TaskManager(auto_load=False, data_file="test_persistence.json")
    task = manager1.add_task(
        title="Persistent task",
        description="Test",
        priority=Priority.HIGH,
        due_date=date(2025, 12, 31),
        recurrence=Recurrence.WEEKLY
    )
    task_id = task.id
    manager1.save_to_json()
    print("✓ Saved tasks to JSON")

    # Load in new manager
    manager2 = TaskManager(auto_load=True, data_file="test_persistence.json")
    loaded_task = manager2.get_task_by_id(task_id)
    assert loaded_task is not None
    assert loaded_task.title == "Persistent task"
    assert loaded_task.priority == Priority.HIGH
    assert loaded_task.due_date == date(2025, 12, 31)
    assert loaded_task.recurrence == Recurrence.WEEKLY
    print("✓ Loaded tasks from JSON with all fields intact")

    # Cleanup
    if os.path.exists("test_persistence.json"):
        os.remove("test_persistence.json")


def cleanup_test_files():
    """Clean up test files."""
    import os
    test_files = [
        "test_tasks.json",
        "test_tasks2.json",
        "test_tasks3.json",
        "test_persistence.json"
    ]
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
    print("\n✓ Cleaned up test files")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Phase I Complete Task Management System - Test Suite")
    print("=" * 60)

    try:
        test_task_model()
        test_date_parsing()
        test_task_manager()
        test_filtering()
        test_sorting()
        test_persistence()
        cleanup_test_files()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nPhase I Complete Task Management System is working correctly.")
        print("\nRun the CLI app:")
        print("  python phase1_complete_cli.py")
        print()

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        cleanup_test_files()
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        cleanup_test_files()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
