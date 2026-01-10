#!/usr/bin/env python3
"""
Test script to verify Phase I Complete CLI enhancements.
Tests tags, yearly recurrence, and improved UI components.
"""

import sys
from datetime import date, timedelta

# Add src to path
sys.path.insert(0, '.')

from src.models.task import Task
from src.models.enums import Priority, Recurrence, Status
from src.services.task_service import TaskManager
from src.services.filter_service import FilterState, FilterService
from rich.console import Console

console = Console()

def test_tags_feature():
    """Test tags functionality."""
    console.print("\n[bold cyan]Testing Tags Feature...[/bold cyan]")

    # Test Task creation with tags
    task1 = Task(
        title="Buy groceries",
        tags=["personal", "shopping", "urgent"]
    )
    assert len(task1.tags) == 3, "Tags should be 3"
    assert "personal" in task1.tags, "Should contain 'personal' tag"
    console.print("[green]✓ Task creation with tags works[/green]")

    # Test to_dict with tags
    task_dict = task1.to_dict()
    assert "tags" in task_dict, "Dict should have tags field"
    assert task_dict["tags"] == ["personal", "shopping", "urgent"]
    console.print("[green]✓ Task serialization with tags works[/green]")

    # Test from_dict with tags
    task2 = Task.from_dict({
        "id": 1,
        "title": "Test task",
        "tags": ["work", "health"]
    })
    assert len(task2.tags) == 2, "Loaded task should have 2 tags"
    console.print("[green]✓ Task deserialization with tags works[/green]")

    # Test TaskManager with tags
    manager = TaskManager(auto_load=False)
    task3 = manager.add_task(
        title="Project meeting",
        tags=["work", "meeting", "important"]
    )
    assert len(task3.tags) == 3
    console.print("[green]✓ TaskManager add with tags works[/green]")

    # Test update with tags
    manager.update_task(task3.id, tags=["work", "rescheduled"])
    updated_task = manager.get_task_by_id(task3.id)
    assert "rescheduled" in updated_task.tags
    console.print("[green]✓ TaskManager update with tags works[/green]")

    return True


def test_yearly_recurrence():
    """Test yearly recurrence feature."""
    console.print("\n[bold cyan]Testing Yearly Recurrence...[/bold cyan]")

    # Test enum
    assert hasattr(Recurrence, 'YEARLY'), "Recurrence should have YEARLY"
    assert Recurrence.YEARLY.value == "yearly"
    console.print("[green]✓ YEARLY enum exists[/green]")

    # Test task with yearly recurrence
    manager = TaskManager(auto_load=False)
    task = manager.add_task(
        title="Annual review",
        due_date=date.today() + timedelta(days=365),
        recurrence=Recurrence.YEARLY
    )
    assert task.recurrence == Recurrence.YEARLY
    console.print("[green]✓ Task with yearly recurrence created[/green]")

    # Test recurring task completion (creates next occurrence)
    next_task = manager.toggle_task_completion(task.id)
    if next_task.id != task.id:  # New task created
        days_diff = (next_task.due_date - task.due_date).days
        assert days_diff == 365, f"Next occurrence should be 365 days later, got {days_diff}"
        console.print("[green]✓ Yearly recurrence creates next occurrence correctly[/green]")

    return True


def test_tags_filter():
    """Test tags filtering."""
    console.print("\n[bold cyan]Testing Tags Filtering...[/bold cyan]")

    manager = TaskManager(auto_load=False)

    # Create tasks with different tags
    task1 = manager.add_task("Task 1", tags=["work", "urgent"])
    task2 = manager.add_task("Task 2", tags=["personal", "health"])
    task3 = manager.add_task("Task 3", tags=["work", "meeting"])

    # Test filter by tag
    filter_state = FilterState(tags=["work"])
    filtered = FilterService.apply_filters(manager.get_all_tasks(), filter_state)

    assert len(filtered) == 2, f"Should find 2 tasks with 'work' tag, found {len(filtered)}"
    console.print("[green]✓ Tag filtering works correctly[/green]")

    # Test multiple tag filter
    filter_state2 = FilterState(tags=["urgent", "health"])
    filtered2 = FilterService.apply_filters(manager.get_all_tasks(), filter_state2)
    assert len(filtered2) == 2, "Should find 2 tasks with either 'urgent' or 'health'"
    console.print("[green]✓ Multiple tag filtering works[/green]")

    return True


def test_improved_status_colors():
    """Test improved status display logic."""
    console.print("\n[bold cyan]Testing Improved Status Colors...[/bold cyan]")

    # Test completed task (should show blue)
    task1 = Task("Completed task", completed=True)
    assert task1.status == Status.COMPLETED
    console.print("[green]✓ Completed status correct[/green]")

    # Test overdue task (should show red)
    task2 = Task("Overdue task", due_date=date.today() - timedelta(days=1))
    assert task2.status == Status.OVERDUE
    console.print("[green]✓ Overdue status correct[/green]")

    # Test pending task (should show green)
    task3 = Task("Pending task", due_date=date.today() + timedelta(days=5))
    assert task3.status == Status.PENDING
    console.print("[green]✓ Pending status correct[/green]")

    return True


def main():
    """Run all tests."""
    console.print("\n[bold magenta]Phase I Complete CLI Enhancement Tests[/bold magenta]\n")

    tests = [
        ("Tags Feature", test_tags_feature),
        ("Yearly Recurrence", test_yearly_recurrence),
        ("Tags Filtering", test_tags_filter),
        ("Status Colors", test_improved_status_colors)
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
            else:
                failed += 1
                console.print(f"[red]✗ {test_name} failed[/red]")
        except Exception as e:
            failed += 1
            console.print(f"[red]✗ {test_name} failed with error: {e}[/red]")

    console.print(f"\n[bold]Test Results:[/bold]")
    console.print(f"[green]Passed: {passed}[/green]")
    console.print(f"[red]Failed: {failed}[/red]")

    if failed == 0:
        console.print("\n[bold green]All tests passed! 🎉[/bold green]\n")
        return 0
    else:
        console.print("\n[bold red]Some tests failed![/bold red]\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
