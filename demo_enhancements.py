#!/usr/bin/env python3
"""
Demo script showcasing Phase I Complete CLI enhancements.
Demonstrates tags, yearly recurrence, improved UI, and all new features.
"""

import sys
import time
from datetime import date, timedelta

sys.path.insert(0, '.')

from src.models.task import Task
from src.models.enums import Priority, Recurrence, Status
from src.services.task_service import TaskManager
from src.services.filter_service import FilterState, FilterService
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

def demo_header():
    """Display demo header."""
    console.print("\n[bold magenta]═══════════════════════════════════════════════════[/bold magenta]")
    console.print("[bold cyan]    Phase I Complete CLI - Enhancements Demo      [/bold cyan]")
    console.print("[bold magenta]═══════════════════════════════════════════════════[/bold magenta]\n")


def demo_tags_feature():
    """Demonstrate tags feature."""
    console.print("[bold cyan]📌 Feature 1: Tags System[/bold cyan]\n")

    manager = TaskManager(auto_load=False)

    # Create tasks with tags
    console.print("Creating tasks with tags...")
    task1 = manager.add_task(
        "Complete project proposal",
        priority=Priority.HIGH,
        tags=["work", "urgent", "deadline"]
    )
    console.print(f"  ✓ Task #{task1.id}: {task1.title}")
    console.print(f"    Tags: {', '.join([f'🏷️ {t}' for t in task1.tags])}\n")

    task2 = manager.add_task(
        "Morning workout",
        priority=Priority.MEDIUM,
        tags=["health", "personal", "routine"]
    )
    console.print(f"  ✓ Task #{task2.id}: {task2.title}")
    console.print(f"    Tags: {', '.join([f'🏷️ {t}' for t in task2.tags])}\n")

    task3 = manager.add_task(
        "Team meeting",
        priority=Priority.HIGH,
        tags=["work", "meeting"]
    )
    console.print(f"  ✓ Task #{task3.id}: {task3.title}")
    console.print(f"    Tags: {', '.join([f'🏷️ {t}' for t in task3.tags])}\n")

    # Demo filtering by tags
    console.print("[bold]Filtering by tag 'work':[/bold]")
    filter_state = FilterState(tags=["work"])
    filtered = FilterService.apply_filters(manager.get_all_tasks(), filter_state)
    for task in filtered:
        console.print(f"  • {task.title}")
    console.print()

    time.sleep(1)


def demo_yearly_recurrence():
    """Demonstrate yearly recurrence."""
    console.print("[bold cyan]🔄 Feature 2: Yearly Recurrence[/bold cyan]\n")

    manager = TaskManager(auto_load=False)

    # Create yearly recurring task
    console.print("Creating yearly recurring task...")
    task = manager.add_task(
        "Annual performance review",
        priority=Priority.HIGH,
        due_date=date(2025, 12, 31),
        recurrence=Recurrence.YEARLY
    )

    console.print(f"  ✓ Task #{task.id}: {task.title}")
    console.print(f"    Due date: {task.due_date}")
    console.print(f"    Recurrence: {task.recurrence.value.upper()} 🔄\n")

    # Simulate completion
    console.print("Marking task as complete (simulating year-end completion)...")
    next_task = manager.toggle_task_completion(task.id)

    if next_task.id != task.id:
        console.print(f"  ✓ Next occurrence created automatically!")
        console.print(f"    Task #{next_task.id}: {next_task.title}")
        console.print(f"    New due date: {next_task.due_date}")
        console.print(f"    (Exactly 365 days later) ✨\n")

    time.sleep(1)


def demo_improved_ui():
    """Demonstrate improved UI elements."""
    console.print("[bold cyan]🎨 Feature 3: Improved UI & Status Colors[/bold cyan]\n")

    manager = TaskManager(auto_load=False)

    # Create tasks with different statuses
    task1 = manager.add_task(
        "Completed task example",
        priority=Priority.HIGH,
        tags=["demo"]
    )
    task1.toggle_completed()

    task2 = manager.add_task(
        "Pending task example",
        priority=Priority.MEDIUM,
        due_date=date.today() + timedelta(days=5),
        tags=["demo", "upcoming"]
    )

    task3 = manager.add_task(
        "Overdue task example",
        priority=Priority.LOW,
        due_date=date.today() - timedelta(days=2),
        tags=["demo"]
    )

    # Create status overview
    all_tasks = manager.get_all_tasks()
    completed = sum(1 for t in all_tasks if t.status == Status.COMPLETED)
    pending = sum(1 for t in all_tasks if t.status == Status.PENDING)
    overdue = sum(1 for t in all_tasks if t.status == Status.OVERDUE)

    overview = Panel(
        f"[bold blue]Completed:[/bold blue] {completed}   "
        f"[bold green]Pending:[/bold green] {pending}   "
        f"[bold red]Overdue:[/bold red] {overdue}   "
        f"[bold cyan]Total:[/bold cyan] {len(all_tasks)}",
        title="Status Overview Panel",
        box=box.ROUNDED,
        border_style="cyan"
    )
    console.print(overview)
    console.print()

    # Create enhanced table
    table = Table(
        title="Enhanced Task Table",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )

    table.add_column("#", style="dim", width=3, justify="right")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Title", style="bold", width=25)
    table.add_column("Priority", width=12)
    table.add_column("Tags", width=20)
    table.add_column("Status", width=12)

    for idx, task in enumerate(all_tasks, 1):
        # Status with NEW COLORS
        if task.status == Status.COMPLETED:
            status_str = "[blue]✅ Done[/blue]"
        elif task.status == Status.OVERDUE:
            status_str = "[red]⚠️ Overdue[/red]"
        else:
            status_str = "[green]⏳ Pending[/green]"

        # Priority with BETTER EMOJI
        if task.priority == Priority.HIGH:
            priority_str = "[red]🔴 High[/red]"
        elif task.priority == Priority.MEDIUM:
            priority_str = "[yellow]🟡 Medium[/yellow]"
        elif task.priority == Priority.LOW:
            priority_str = "[green]🟢 Low[/green]"
        else:
            priority_str = "[dim]⚪ None[/dim]"

        # Tags
        tags_str = " ".join([f"🏷️ {tag}" for tag in task.tags]) if task.tags else "[dim]No tags[/dim]"

        table.add_row(
            str(idx),
            str(task.id),
            task.title,
            priority_str,
            tags_str,
            status_str
        )

    console.print(table)
    console.print("\n[bold]Color Scheme:[/bold]")
    console.print("  • [blue]Blue (✅)[/blue] = Completed")
    console.print("  • [green]Green (⏳)[/green] = Pending")
    console.print("  • [red]Red (⚠️)[/red] = Overdue")
    console.print()

    time.sleep(1)


def demo_voice_commands_info():
    """Display voice commands information."""
    console.print("[bold cyan]🎤 Feature 4: Voice Commands[/bold cyan]\n")

    console.print("[bold]Supported voice commands:[/bold]")
    commands = [
        ("Add task", "Add task buy groceries high priority tomorrow tags shopping urgent"),
        ("List tasks", "Show tasks"),
        ("Update task", "Update task 1 new title finish report"),
        ("Delete task", "Delete task 5"),
        ("Complete task", "Complete task 2"),
        ("Filter", "Filter by status pending"),
        ("Search", "Search project"),
        ("Sort", "Sort by priority")
    ]

    table = Table(box=box.SIMPLE)
    table.add_column("Command", style="cyan")
    table.add_column("Example", style="dim")

    for cmd, example in commands:
        table.add_row(cmd, example)

    console.print(table)
    console.print("\n[dim]Note: Voice commands require microphone access and internet connection.[/dim]\n")

    time.sleep(1)


def demo_summary():
    """Display summary of all enhancements."""
    console.print("[bold cyan]📋 Summary of Enhancements[/bold cyan]\n")

    enhancements = [
        ("✅", "Serial number (#) column in task table"),
        ("✅", "Reordered columns with Status second-to-last"),
        ("✅", "New status colors (Blue/Green/Red)"),
        ("✅", "Better emoji strategy (🔴🟡🟢⚪✅⏳⚠️🔄🏷️)"),
        ("✅", "Tags feature (add, update, filter, display)"),
        ("✅", "Yearly recurrence option (365 days)"),
        ("✅", "Status overview panel with color-coded counters"),
        ("✅", "Voice commands for all operations"),
        ("✅", "Filter by tags option"),
        ("✅", "Improved table layout and spacing")
    ]

    for check, feature in enhancements:
        console.print(f"  {check} {feature}")

    console.print()


def main():
    """Run the demo."""
    demo_header()

    demos = [
        ("Tags Feature", demo_tags_feature),
        ("Yearly Recurrence", demo_yearly_recurrence),
        ("Improved UI", demo_improved_ui),
        ("Voice Commands", demo_voice_commands_info),
        ("Summary", demo_summary)
    ]

    for idx, (name, demo_func) in enumerate(demos, 1):
        console.print(f"[bold yellow]Demo {idx}/{len(demos)}[/bold yellow]")
        demo_func()
        if idx < len(demos):
            time.sleep(0.5)

    console.print("[bold green]Demo complete! 🎉[/bold green]")
    console.print("\n[bold]To run the full application:[/bold]")
    console.print("[cyan].venv/bin/python phase1_complete_cli.py[/cyan]\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted.[/yellow]")
        sys.exit(0)
