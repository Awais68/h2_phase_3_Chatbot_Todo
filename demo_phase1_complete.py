#!/usr/bin/env python3
"""
Demo script for Phase I Complete Task Management System.
Creates sample tasks to showcase all features.
"""

from datetime import date, timedelta
from rich.console import Console
from rich.panel import Panel

from src.models.enums import Priority, Recurrence, Status, SortBy
from src.services.task_service import TaskManager
from src.services.filter_service import FilterState, FilterService
from src.services.search_service import SearchService

console = Console()


def create_demo_tasks(manager: TaskManager):
    """Create a variety of sample tasks."""
    console.print("\n[bold cyan]Creating demo tasks...[/bold cyan]\n")

    # High priority tasks
    manager.add_task(
        "Complete project proposal",
        "Q1 2025 strategic plan with budget estimates",
        priority=Priority.HIGH,
        due_date=date.today() + timedelta(days=2)
    )
    console.print("✓ Created high-priority task with near deadline")

    manager.add_task(
        "Review security audit",
        "Critical: Address findings from last week's security scan",
        priority=Priority.HIGH,
        due_date=date.today() + timedelta(days=1)
    )
    console.print("✓ Created high-priority urgent task")

    # Recurring tasks
    manager.add_task(
        "Daily standup meeting",
        "Team sync at 9am",
        priority=Priority.MEDIUM,
        due_date=date.today(),
        recurrence=Recurrence.DAILY
    )
    console.print("✓ Created daily recurring task")

    manager.add_task(
        "Weekly team report",
        "Submit status update to team lead",
        priority=Priority.MEDIUM,
        due_date=date.today() + timedelta(days=4),
        recurrence=Recurrence.WEEKLY
    )
    console.print("✓ Created weekly recurring task")

    manager.add_task(
        "Monthly budget review",
        "Review and approve departmental expenses",
        priority=Priority.HIGH,
        due_date=date.today() + timedelta(days=25),
        recurrence=Recurrence.MONTHLY
    )
    console.print("✓ Created monthly recurring task")

    # Overdue tasks
    manager.add_task(
        "Update documentation",
        "Overdue: API docs need updating",
        priority=Priority.MEDIUM,
        due_date=date.today() - timedelta(days=3)
    )
    console.print("✓ Created overdue task")

    manager.add_task(
        "Client follow-up",
        "URGENT: Respond to client inquiry from last week",
        priority=Priority.HIGH,
        due_date=date.today() - timedelta(days=5)
    )
    console.print("✓ Created overdue high-priority task")

    # Low priority / backlog
    manager.add_task(
        "Refactor old code",
        "Technical debt: Clean up legacy modules",
        priority=Priority.LOW,
        due_date=date.today() + timedelta(days=30)
    )
    console.print("✓ Created low-priority task")

    manager.add_task(
        "Research new frameworks",
        "Evaluate React alternatives for next project",
        priority=Priority.LOW
    )
    console.print("✓ Created backlog task (no due date)")

    # Completed tasks
    task = manager.add_task(
        "Setup development environment",
        "Configure local dev setup",
        priority=Priority.MEDIUM,
        due_date=date.today() - timedelta(days=1)
    )
    manager.toggle_task_completion(task.id)
    console.print("✓ Created completed task")

    # Shopping/personal tasks
    manager.add_task(
        "Buy groceries",
        "Milk, eggs, bread, vegetables",
        priority=Priority.MEDIUM,
        due_date=date.today()
    )
    console.print("✓ Created personal task")

    console.print(f"\n[green]Created {len(manager.get_all_tasks())} demo tasks![/green]\n")


def demo_filtering(manager: TaskManager):
    """Demonstrate filtering capabilities."""
    console.print("\n[bold cyan]Filtering Demo[/bold cyan]\n")

    all_tasks = manager.get_all_tasks()
    console.print(f"Total tasks: {len(all_tasks)}")

    # Filter by overdue
    filter_state = FilterState(status=Status.OVERDUE)
    overdue = FilterService.apply_filters(all_tasks, filter_state)
    console.print(f"[red]Overdue tasks: {len(overdue)}[/red]")
    for task in overdue:
        console.print(f"  - {task.title} (due {task.due_date})")

    # Filter by high priority
    filter_state = FilterState(priority=Priority.HIGH)
    high_priority = FilterService.apply_filters(all_tasks, filter_state)
    console.print(f"\n[bold]High priority tasks: {len(high_priority)}[/bold]")
    for task in high_priority:
        console.print(f"  - {task.title}")

    # Filter by date range (this week)
    filter_state = FilterState(
        date_range=(date.today(), date.today() + timedelta(days=7))
    )
    this_week = FilterService.apply_filters(all_tasks, filter_state)
    console.print(f"\n[yellow]Tasks due this week: {len(this_week)}[/yellow]")


def demo_search(manager: TaskManager):
    """Demonstrate search functionality."""
    console.print("\n[bold cyan]Search Demo[/bold cyan]\n")

    # Search for "meeting"
    results = SearchService.search(manager.get_all_tasks(), "meeting")
    console.print(f"[green]Tasks containing 'meeting': {len(results)}[/green]")
    for task in results:
        console.print(f"  - {task.title}")

    # Search for "review"
    results = SearchService.search(manager.get_all_tasks(), "review")
    console.print(f"\n[green]Tasks containing 'review': {len(results)}[/green]")
    for task in results:
        console.print(f"  - {task.title}")


def demo_sorting(manager: TaskManager):
    """Demonstrate sorting options."""
    console.print("\n[bold cyan]Sorting Demo[/bold cyan]\n")

    tasks = manager.get_all_tasks()

    # Sort by default (overdue first)
    sorted_tasks = manager.sort_tasks(tasks, SortBy.DEFAULT)
    console.print("[bold]Default Sort (Overdue first, then newest):[/bold]")
    for i, task in enumerate(sorted_tasks[:5], 1):
        status_emoji = "🔴" if task.status == Status.OVERDUE else "⏳"
        console.print(f"  {i}. {status_emoji} {task.title}")

    # Sort by priority
    sorted_tasks = manager.sort_tasks(tasks, SortBy.PRIORITY)
    console.print("\n[bold]Priority Sort (High → Low):[/bold]")
    for i, task in enumerate(sorted_tasks[:5], 1):
        priority_emoji = "🔴" if task.priority == Priority.HIGH else "🟡" if task.priority == Priority.MEDIUM else "🟢"
        console.print(f"  {i}. {priority_emoji} {task.title}")

    # Sort by due date
    sorted_tasks = manager.sort_tasks(tasks, SortBy.DUE_DATE)
    console.print("\n[bold]Due Date Sort (Earliest → Latest):[/bold]")
    for i, task in enumerate(sorted_tasks[:5], 1):
        due_str = str(task.due_date) if task.due_date else "No date"
        console.print(f"  {i}. {task.title} (due {due_str})")


def demo_recurring(manager: TaskManager):
    """Demonstrate recurring task functionality."""
    console.print("\n[bold cyan]Recurring Task Demo[/bold cyan]\n")

    # Find daily standup task
    daily_task = None
    for task in manager.get_all_tasks():
        if "Daily standup" in task.title:
            daily_task = task
            break

    if daily_task:
        console.print(f"[yellow]Completing recurring task: {daily_task.title}[/yellow]")
        console.print(f"  Current due date: {daily_task.due_date}")
        console.print(f"  Recurrence: {daily_task.recurrence.value}")

        # Complete the task
        new_task = manager.toggle_task_completion(daily_task.id)

        if new_task and new_task.id != daily_task.id:
            console.print(f"\n[green]✓ Task completed![/green]")
            console.print(f"[cyan]↻ Created next occurrence:[/cyan]")
            console.print(f"  Task ID: #{new_task.id}")
            console.print(f"  Title: {new_task.title}")
            console.print(f"  New due date: {new_task.due_date}")
            console.print(f"  Status: {new_task.status.value}")


def demo_statistics(manager: TaskManager):
    """Show task statistics."""
    console.print("\n[bold cyan]Task Statistics[/bold cyan]\n")

    stats = manager.get_task_stats()
    all_tasks = manager.get_all_tasks()

    # Count by status
    pending = sum(1 for t in all_tasks if t.status == Status.PENDING)
    completed = sum(1 for t in all_tasks if t.completed)
    overdue = sum(1 for t in all_tasks if t.status == Status.OVERDUE)

    # Count by priority
    high = sum(1 for t in all_tasks if t.priority == Priority.HIGH)
    medium = sum(1 for t in all_tasks if t.priority == Priority.MEDIUM)
    low = sum(1 for t in all_tasks if t.priority == Priority.LOW)

    # Count recurring
    recurring = sum(1 for t in all_tasks if t.recurrence != Recurrence.NONE)

    console.print(f"[bold]Total Tasks:[/bold] {stats['total']}")
    console.print(f"\n[bold]By Status:[/bold]")
    console.print(f"  ⏳ Pending: {pending}")
    console.print(f"  ✓ Completed: {completed}")
    console.print(f"  🔴 Overdue: {overdue}")
    console.print(f"\n[bold]By Priority:[/bold]")
    console.print(f"  🔴 High: {high}")
    console.print(f"  🟡 Medium: {medium}")
    console.print(f"  🟢 Low: {low}")
    console.print(f"\n[bold]Special:[/bold]")
    console.print(f"  ↻ Recurring: {recurring}")


def main():
    """Run demo."""
    import os

    # Use demo data file
    demo_file = "demo_tasks.json"

    # Clean up old demo file
    if os.path.exists(demo_file):
        os.remove(demo_file)
        console.print("[dim]Removed old demo data[/dim]")

    # Initialize manager
    manager = TaskManager(auto_load=False, data_file=demo_file)

    # Show header
    console.print()
    console.print(Panel.fit(
        "[bold cyan]Phase I Complete Task Management System[/bold cyan]\n"
        "[dim]Feature Demonstration[/dim]",
        border_style="cyan"
    ))

    # Run demos
    create_demo_tasks(manager)
    demo_statistics(manager)
    demo_filtering(manager)
    demo_search(manager)
    demo_sorting(manager)
    demo_recurring(manager)

    # Final message
    console.print()
    console.print(Panel.fit(
        "[bold green]Demo Complete![/bold green]\n\n"
        "[dim]Demo data saved to:[/dim] demo_tasks.json\n"
        "[dim]Run the full app:[/dim] uv run python phase1_complete_cli.py\n"
        "[dim]Open demo data:[/dim] cat demo_tasks.json",
        border_style="green"
    ))
    console.print()


if __name__ == "__main__":
    main()
