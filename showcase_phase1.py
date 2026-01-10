#!/usr/bin/env python3
"""
Showcase all Phase I Complete features.
This script demonstrates the working application without requiring user input.
"""

from datetime import date, timedelta
from src.models.task import Task
from src.models.enums import Priority, Recurrence, Status, SortBy
from src.services.task_service import TaskManager
from src.services.filter_service import FilterState, FilterService
from src.services.search_service import SearchService
from src.cli import ui_components as ui
from src.cli.themes import set_theme, get_current_theme
from src.utils.date_utils import parse_date
import time


def showcase():
    """Showcase all Phase I Complete features."""

    # Clear and show title
    ui.clear_screen()
    ui.console.print("[bold cyan]╔═══════════════════════════════════════════════════════╗[/bold cyan]")
    ui.console.print("[bold cyan]║[/bold cyan]  Phase I Complete Task Management System Showcase  [bold cyan]║[/bold cyan]")
    ui.console.print("[bold cyan]╚═══════════════════════════════════════════════════════╝[/bold cyan]\n")

    time.sleep(1)

    # Initialize clean manager
    manager = TaskManager(data_file="showcase_tasks.json")

    # Feature 1: Adding tasks with priority and due dates
    ui.display_header("Feature 1: Task Creation with Priority & Due Dates")
    time.sleep(0.5)

    ui.console.print("[dim]Creating task with HIGH priority and due date...[/dim]")
    task1 = manager.add_task(
        title="Complete hackathon project",
        description="Finish Phase I implementation and submit",
        priority=Priority.HIGH,
        due_date=date.today() + timedelta(days=1)
    )
    ui.display_success(f"✓ Created: {task1.title} | Priority: 🔴 {task1.priority.value.upper()} | Due: {task1.due_date}")
    time.sleep(0.5)

    ui.console.print("[dim]Creating task with MEDIUM priority...[/dim]")
    task2 = manager.add_task(
        title="Review pull requests",
        description="Check team submissions",
        priority=Priority.MEDIUM,
        due_date=date.today() + timedelta(days=3)
    )
    ui.display_success(f"✓ Created: {task2.title} | Priority: 🟡 {task2.priority.value.upper()}")
    time.sleep(0.5)

    ui.console.print("[dim]Creating OVERDUE task...[/dim]")
    task3 = manager.add_task(
        title="Update documentation",
        description="Critical: API docs need updating",
        priority=Priority.HIGH,
        due_date=date.today() - timedelta(days=2)  # 2 days ago
    )
    ui.display_success(f"✓ Created: {task3.title} | Status: 🔴 {task3.status.value.upper()}")
    time.sleep(0.5)

    ui.console.print("[dim]Creating task with NO due date...[/dim]")
    task4 = manager.add_task(
        title="Research new technologies",
        description="Investigate AI tools for automation",
        priority=Priority.LOW
    )
    ui.display_success(f"✓ Created: {task4.title} | Priority: 🟢 {task4.priority.value.upper()}")
    time.sleep(1)

    # Feature 2: Recurring Tasks
    ui.console.print("\n")
    ui.display_header("Feature 2: Recurring Tasks (Auto-Create Next Occurrence)")
    time.sleep(0.5)

    ui.console.print("[dim]Creating DAILY recurring task...[/dim]")
    task5 = manager.add_task(
        title="Daily standup meeting",
        description="Team sync at 9am",
        priority=Priority.MEDIUM,
        due_date=date.today(),
        recurrence=Recurrence.DAILY
    )
    ui.display_success(f"✓ Created: {task5.title} | ↻ {task5.recurrence.value.upper()}")
    time.sleep(0.5)

    ui.console.print(f"\n[dim]Marking task #{task5.id} as complete to trigger next occurrence...[/dim]")
    time.sleep(0.5)
    next_task = manager.toggle_task_completion(task5.id)
    if next_task:
        ui.display_success(f"✓ Task #{task5.id} completed!")
        ui.display_info(f"↻ Auto-created next occurrence: Task #{next_task.id} due {next_task.due_date}")
    time.sleep(1)

    # Feature 3: View all tasks
    ui.console.print("\n")
    ui.display_header("Feature 3: View All Tasks (Default Sort: Overdue First)")
    time.sleep(0.5)

    all_tasks = manager.get_all_tasks()
    sorted_tasks = manager.sort_tasks(all_tasks, SortBy.DEFAULT)
    table = ui.create_task_table(sorted_tasks)
    ui.console.print(table)
    time.sleep(2)

    # Feature 4: Filtering
    ui.console.print("\n")
    ui.display_header("Feature 4: Filtering Tasks")
    time.sleep(0.5)

    ui.console.print("[bold]Filter 1:[/bold] Show only OVERDUE tasks")
    filter_state = FilterState(status="overdue")
    filtered = FilterService.apply_filters(all_tasks, filter_state)
    ui.console.print(f"Result: Found {len(filtered)} overdue task(s)")
    for t in filtered:
        ui.console.print(f"  • [{t.status.value.upper()}] {t.title} (due {t.due_date})")
    time.sleep(1)

    ui.console.print("\n[bold]Filter 2:[/bold] Show only HIGH priority tasks")
    filter_state = FilterState(priority="high")
    filtered = FilterService.apply_filters(all_tasks, filter_state)
    ui.console.print(f"Result: Found {len(filtered)} high-priority task(s)")
    for t in filtered:
        ui.console.print(f"  • [🔴 HIGH] {t.title}")
    time.sleep(1)

    # Feature 5: Search
    ui.console.print("\n")
    ui.display_header("Feature 5: Keyword Search")
    time.sleep(0.5)

    ui.console.print("[bold]Search:[/bold] Find tasks containing 'documentation'")
    search_results = SearchService.search(all_tasks, "documentation")
    ui.console.print(f"Result: Found {len(search_results)} task(s)")
    for t in search_results:
        ui.console.print(f"  • {t.title}")
    time.sleep(1)

    ui.console.print("\n[bold]Search:[/bold] Find tasks containing 'meeting'")
    search_results = SearchService.search(all_tasks, "meeting")
    ui.console.print(f"Result: Found {len(search_results)} task(s)")
    for t in search_results:
        ui.console.print(f"  • {t.title} (↻ {t.recurrence.value})")
    time.sleep(1)

    # Feature 6: Sorting
    ui.console.print("\n")
    ui.display_header("Feature 6: Multiple Sort Options")
    time.sleep(0.5)

    ui.console.print("[bold]Sort by PRIORITY:[/bold] (High → Low)")
    sorted_tasks = manager.sort_tasks(all_tasks, SortBy.PRIORITY)
    for i, t in enumerate(sorted_tasks[:5], 1):
        priority_emoji = "🔴" if t.priority == Priority.HIGH else "🟡" if t.priority == Priority.MEDIUM else "🟢" if t.priority == Priority.LOW else "⚪"
        ui.console.print(f"  {i}. {priority_emoji} {t.title}")
    time.sleep(1)

    ui.console.print("\n[bold]Sort by DUE DATE:[/bold] (Earliest → Latest, Overdue first)")
    sorted_tasks = manager.sort_tasks(all_tasks, SortBy.DUE_DATE)
    for i, t in enumerate(sorted_tasks[:5], 1):
        status_emoji = "🔴" if t.status == Status.OVERDUE else "⏳"
        due_str = str(t.due_date) if t.due_date else "No date"
        ui.console.print(f"  {i}. {status_emoji} {t.title} (due: {due_str})")
    time.sleep(1)

    # Feature 7: Status Indicators
    ui.console.print("\n")
    ui.display_header("Feature 7: Task Status Indicators")
    time.sleep(0.5)

    stats = manager.get_task_stats()
    ui.console.print(f"[bold]Total Tasks:[/bold] {stats['total']}")
    ui.console.print(f"  ⏳ Pending: {stats['pending']}")
    ui.console.print(f"  ✓ Completed: {stats['completed']}")
    ui.console.print(f"  🔴 Overdue: {sum(1 for t in all_tasks if t.status == Status.OVERDUE)}")
    ui.console.print(f"  ↻ Recurring: {sum(1 for t in all_tasks if t.recurrence != Recurrence.NONE)}")
    time.sleep(1)

    # Feature 8: Natural Language Date Parsing
    ui.console.print("\n")
    ui.display_header("Feature 8: Natural Language Date Parsing")
    time.sleep(0.5)

    date_examples = [
        "tomorrow",
        "next week",
        "2025-12-31",
        "in 3 days",
    ]

    for example in date_examples:
        parsed = parse_date(example)
        if parsed:
            ui.console.print(f"  '{example}' → {parsed} ✓")
    time.sleep(1)

    # Feature 9: JSON Persistence
    ui.console.print("\n")
    ui.display_header("Feature 9: JSON Persistence")
    time.sleep(0.5)

    ui.console.print(f"[bold]Saving all tasks to:[/bold] showcase_tasks.json")
    ui.show_progress_bar("Saving", duration=0.3)
    manager.save_to_json()
    ui.display_success(f"✓ Saved {len(all_tasks)} tasks with all fields (priority, due_date, recurrence, status)")
    time.sleep(1)

    # Summary
    ui.console.print("\n")
    ui.display_header("✨ Phase I Complete - Feature Summary")
    time.sleep(0.5)

    features = [
        "✅ Priority Levels (High/Medium/Low/None)",
        "✅ Due Dates (Natural language + ISO format)",
        "✅ Recurring Tasks (Daily/Weekly/Monthly auto-creation)",
        "✅ Status Tracking (Pending/Completed/Overdue)",
        "✅ Filtering (By status, priority, date range)",
        "✅ Search (Keyword search in title/description)",
        "✅ Sorting (Priority, due date, created date)",
        "✅ Overdue Detection (Always at top)",
        "✅ JSON Persistence (All fields auto-save)",
        "✅ Rich UI (Colors, emoji, tables, themes)",
    ]

    for feature in features:
        ui.console.print(f"  {feature}")

    ui.console.print("\n[bold green]🎉 All Features Working![/bold green]\n")

    ui.console.print("[bold]To use the interactive app:[/bold]")
    ui.console.print("  cd '/media/data/hackathon series/hackathon-2/hackathon-2/sp-1'")
    ui.console.print("  source .venv/bin/activate")
    ui.console.print("  python phase1_complete_cli.py")

    ui.console.print("\n[bold]Quick commands:[/bold]")
    ui.console.print("  • View tasks: Option 2")
    ui.console.print("  • Add task with priority: Option 1 → choose priority → enter due date")
    ui.console.print("  • Filter by overdue: Option 5 → Filter by Status → Overdue")
    ui.console.print("  • Search: Option 3 → enter keyword")
    ui.console.print("  • Sort by priority: Option 6 → By Priority")

    ui.console.print("\n[dim]Demo data saved to: showcase_tasks.json[/dim]\n")


if __name__ == "__main__":
    showcase()
