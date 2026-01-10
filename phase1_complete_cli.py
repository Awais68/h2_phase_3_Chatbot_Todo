#!/usr/bin/env python3
"""
Phase I Complete Task Management System
Comprehensive CLI with priority, due dates, recurring tasks, filtering, search, and sorting.
"""

import sys
from datetime import date, timedelta
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from art import text2art
import questionary

from src.models.task import Task
from src.models.enums import Priority, Recurrence, Status, SortBy
from src.services.task_service import TaskManager
from src.services.filter_service import FilterState, FilterService
from src.services.search_service import SearchService
from src.utils.date_utils import parse_date
from src.utils.voice_commands import get_voice_input, parse_voice_command
from src.cli.themes import set_theme, get_current_theme

# Initialize console and services
console = Console()
task_manager = TaskManager()
filter_state = FilterState()
current_sort = SortBy.DEFAULT


def display_header():
    """Display ASCII art header."""
    theme = get_current_theme()
    title_art = text2art("TODO  APP", font="small")
    console.print(f"[{theme.primary}]{title_art}[/{theme.primary}]")
    console.print(f"[bold {theme.text}]Phase I Complete Task Management System[/bold {theme.text}]\n")


def display_tasks():
    """Display tasks in a Rich table with all fields."""
    tasks = task_manager.get_all_tasks()

    # Apply filters
    if filter_state.is_active():
        tasks = FilterService.apply_filters(tasks, filter_state)

    # Apply sorting
    tasks = task_manager.sort_tasks(tasks, current_sort)

    if not tasks:
        if filter_state.is_active():
            console.print("[yellow]No tasks match current filters.[/yellow]")
            console.print(f"[dim]Total tasks: {len(task_manager.get_all_tasks())}[/dim]")
        else:
            console.print("[yellow]No tasks yet! Create one to get started.[/yellow]")
        return

    # Show status overview
    theme = get_current_theme()
    all_tasks = task_manager.get_all_tasks()
    completed = sum(1 for t in all_tasks if t.status == Status.COMPLETED)
    pending = sum(1 for t in all_tasks if t.status == Status.PENDING)
    overdue = sum(1 for t in all_tasks if t.status == Status.OVERDUE)

    overview = Panel(
        f"[bold {theme.info}]Completed:[/bold {theme.info}] {completed}   "
        f"[bold {theme.success}]Pending:[/bold {theme.success}] {pending}   "
        f"[bold {theme.error}]Overdue:[/bold {theme.error}] {overdue}   "
        f"[bold {theme.primary}]Total:[/bold {theme.primary}] {len(all_tasks)}",
        title="Status Overview",
        box=box.ROUNDED,
        border_style=theme.primary
    )
    console.print(overview)
    console.print()

    # Show filter/sort info
    total_tasks = len(task_manager.get_all_tasks())
    if filter_state.is_active():
        console.print(f"[bold]Showing {len(tasks)} of {total_tasks} tasks[/bold]")
        console.print(f"[dim]Filters: {filter_state.describe()}[/dim]")
    else:
        console.print(f"[bold]Showing {len(tasks)} tasks[/bold]")

    if current_sort != SortBy.DEFAULT:
        console.print(f"[dim]Sort: {current_sort.value.replace('_', ' ').title()}[/dim]")
    console.print()

    # Create table with new column order
    table = Table(
        title="Task List",
        box=box.ROUNDED,
        show_header=True,
        header_style=f"bold {theme.primary}"
    )

    table.add_column("#", style="dim", width=3, justify="right")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Title", style="bold", width=25)
    table.add_column("Priority", width=12)
    table.add_column("Due Date", width=12)
    table.add_column("Recurrence", width=11)
    table.add_column("Tags", width=15)
    table.add_column("Status", width=12)
    table.add_column("Created", style="dim", width=12)

    for idx, task in enumerate(tasks, 1):
        # Status with emoji and NEW COLORS - Blue for completed, Green for pending, Red for overdue
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

        # Due date with color based on urgency
        if task.due_date:
            days_until = (task.due_date - date.today()).days
            if task.status == Status.OVERDUE:
                due_str = f"[red]{task.due_date}[/red]"
            elif days_until <= 2:
                due_str = f"[yellow]{task.due_date}[/yellow]"
            else:
                due_str = str(task.due_date)
        else:
            due_str = "[dim]No date[/dim]"

        # Recurrence with better icon
        if task.recurrence != Recurrence.NONE:
            recur_str = f"🔄 {task.recurrence.value.title()}"
        else:
            recur_str = "[dim]None[/dim]"

        # Tags display
        if task.tags and len(task.tags) > 0:
            tags_str = " ".join([f"🏷️ {tag}" for tag in task.tags[:2]])  # Show max 2 tags
            if len(task.tags) > 2:
                tags_str += f" +{len(task.tags) - 2}"
        else:
            tags_str = "[dim]No tags[/dim]"

        # Truncate title if too long
        title = task.title if len(task.title) <= 25 else task.title[:22] + "..."

        table.add_row(
            str(idx),
            str(task.id),
            title,
            priority_str,
            due_str,
            recur_str,
            tags_str,
            status_str,
            task.created_at.strftime("%Y-%m-%d")
        )

    console.print(table)


def add_task_flow():
    """Interactive flow for adding a new task."""
    console.print("\n[bold cyan]Add New Task[/bold cyan]\n")

    # Title
    title = questionary.text("Task title:").ask()
    if not title or not title.strip():
        console.print("[red]Task title cannot be empty![/red]")
        return

    # Description
    description = questionary.text(
        "Description (optional):",
        default=""
    ).ask()

    # Priority
    priority_choice = questionary.select(
        "Priority:",
        choices=[
            {"name": "🔴 High", "value": "high"},
            {"name": "🟡 Medium", "value": "medium"},
            {"name": "🟢 Low", "value": "low"},
            {"name": "None", "value": "none"}
        ]
    ).ask()
    priority = Priority(priority_choice)

    # Due date
    due_date_str = questionary.text(
        "Due date (optional - e.g., 'tomorrow', '2025-12-31', 'next week'):",
        default=""
    ).ask()

    due_date = None
    if due_date_str and due_date_str.strip():
        due_date = parse_date(due_date_str)
        if not due_date:
            console.print("[yellow]Could not parse date. Task will have no due date.[/yellow]")
        else:
            console.print(f"[green]Due date set to: {due_date}[/green]")

    # Recurrence
    recurrence_choice = questionary.select(
        "Recurrence:",
        choices=[
            {"name": "None", "value": "none"},
            {"name": "🔄 Daily", "value": "daily"},
            {"name": "🔄 Weekly", "value": "weekly"},
            {"name": "🔄 Monthly", "value": "monthly"},
            {"name": "🔄 Yearly", "value": "yearly"}
        ]
    ).ask()
    recurrence = Recurrence(recurrence_choice)

    # Validate recurring task has due date
    if recurrence != Recurrence.NONE and not due_date:
        console.print("[yellow]Recurring tasks must have a due date. Please enter one:[/yellow]")
        due_date_str = questionary.text("Due date:").ask()
        due_date = parse_date(due_date_str)
        if not due_date:
            console.print("[red]Invalid date. Task will not be recurring.[/red]")
            recurrence = Recurrence.NONE

    # Tags
    tags_input = questionary.text(
        "Tags (optional - comma or space separated, e.g., 'work, urgent' or 'personal health'):",
        default=""
    ).ask()

    tags = None
    if tags_input and tags_input.strip():
        # Split by comma or space
        import re
        tags = [t.strip() for t in re.split(r'[,\s]+', tags_input) if t.strip()]
        if tags:
            console.print(f"[green]Tags: {', '.join(tags)}[/green]")

    # Create task
    try:
        task = task_manager.add_task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            recurrence=recurrence,
            tags=tags
        )
        console.print(f"\n[green]✓ Task #{task.id} created successfully![/green]\n")
    except ValueError as e:
        console.print(f"[red]Error creating task: {e}[/red]")


def update_task_flow():
    """Interactive flow for updating a task."""
    console.print("\n[bold cyan]Update Task[/bold cyan]\n")

    task_id = questionary.text("Enter task ID to update:").ask()
    try:
        task_id = int(task_id)
    except ValueError:
        console.print("[red]Invalid task ID![/red]")
        return

    task = task_manager.get_task_by_id(task_id)
    if not task:
        console.print(f"[red]Task #{task_id} not found![/red]")
        return

    console.print(f"\n[bold]Current task:[/bold] {task.title}")
    console.print(f"[dim]Priority: {task.priority.value}, Due: {task.due_date or 'None'}[/dim]\n")

    # Ask what to update
    update_choices = questionary.checkbox(
        "What would you like to update? (Space to select, Enter to confirm)",
        choices=[
            "Title",
            "Description",
            "Priority",
            "Due Date",
            "Recurrence",
            "Tags"
        ]
    ).ask()

    if not update_choices:
        console.print("[yellow]No fields selected.[/yellow]")
        return

    new_title = None
    new_description = None
    new_priority = None
    new_due_date = None
    new_recurrence = None
    new_tags = None

    if "Title" in update_choices:
        new_title = questionary.text("New title:", default=task.title).ask()

    if "Description" in update_choices:
        new_description = questionary.text("New description:", default=task.description).ask()

    if "Priority" in update_choices:
        priority_choice = questionary.select(
            "New priority:",
            choices=[
                {"name": "🔴 High", "value": "high"},
                {"name": "🟡 Medium", "value": "medium"},
                {"name": "🟢 Low", "value": "low"},
                {"name": "None", "value": "none"}
            ]
        ).ask()
        new_priority = Priority(priority_choice)

    if "Due Date" in update_choices:
        due_date_str = questionary.text("New due date:").ask()
        if due_date_str and due_date_str.strip():
            new_due_date = parse_date(due_date_str)
            if not new_due_date:
                console.print("[yellow]Could not parse date. Due date will not be changed.[/yellow]")

    if "Recurrence" in update_choices:
        recurrence_choice = questionary.select(
            "New recurrence:",
            choices=[
                {"name": "None", "value": "none"},
                {"name": "🔄 Daily", "value": "daily"},
                {"name": "🔄 Weekly", "value": "weekly"},
                {"name": "🔄 Monthly", "value": "monthly"},
                {"name": "🔄 Yearly", "value": "yearly"}
            ]
        ).ask()
        new_recurrence = Recurrence(recurrence_choice)

    if "Tags" in update_choices:
        current_tags_str = ", ".join(task.tags) if task.tags else ""
        tags_input = questionary.text(
            f"New tags (current: {current_tags_str or 'none'}):",
            default=current_tags_str
        ).ask()

        if tags_input and tags_input.strip():
            import re
            new_tags = [t.strip() for t in re.split(r'[,\s]+', tags_input) if t.strip()]
            console.print(f"[green]Tags updated: {', '.join(new_tags)}[/green]")
        else:
            new_tags = []

    # Update task
    try:
        task_manager.update_task(
            task_id=task_id,
            title=new_title,
            description=new_description,
            priority=new_priority,
            due_date=new_due_date,
            recurrence=new_recurrence,
            tags=new_tags
        )
        console.print(f"\n[green]✓ Task #{task_id} updated successfully![/green]\n")
    except ValueError as e:
        console.print(f"[red]Error updating task: {e}[/red]")


def delete_task_flow():
    """Interactive flow for deleting a task."""
    console.print("\n[bold red]Delete Task[/bold red]\n")

    task_id = questionary.text("Enter task ID to delete:").ask()
    try:
        task_id = int(task_id)
    except ValueError:
        console.print("[red]Invalid task ID![/red]")
        return

    task = task_manager.get_task_by_id(task_id)
    if not task:
        console.print(f"[red]Task #{task_id} not found![/red]")
        return

    console.print(f"\n[bold]Task:[/bold] {task.title}")
    confirm = questionary.confirm(f"Are you sure you want to delete this task?").ask()

    if confirm:
        task_manager.delete_task(task_id)
        console.print(f"\n[green]✓ Task #{task_id} deleted successfully![/green]\n")
    else:
        console.print("[yellow]Deletion cancelled.[/yellow]")


def toggle_completion_flow():
    """Interactive flow for toggling task completion."""
    console.print("\n[bold cyan]Toggle Task Completion[/bold cyan]\n")

    task_id = questionary.text("Enter task ID to toggle:").ask()
    try:
        task_id = int(task_id)
    except ValueError:
        console.print("[red]Invalid task ID![/red]")
        return

    result = task_manager.toggle_task_completion(task_id)
    if not result:
        console.print(f"[red]Task #{task_id} not found![/red]")
        return

    # Check if a new recurring task was created
    if result.id != task_id:
        console.print(f"\n[green]✓ Task #{task_id} marked as complete![/green]")
        console.print(f"[cyan]↻ Created next occurrence: Task #{result.id} due {result.due_date}[/cyan]\n")
    else:
        status = "complete" if result.completed else "incomplete"
        console.print(f"\n[green]✓ Task #{task_id} marked as {status}![/green]\n")


def filter_menu():
    """Interactive filter menu."""
    while True:
        console.print("\n[bold cyan]Filter Tasks[/bold cyan]\n")

        if filter_state.is_active():
            console.print(f"[yellow]Active filters: {filter_state.describe()}[/yellow]\n")

        choice = questionary.select(
            "Filter options:",
            choices=[
                {"name": "🔍 Filter by Status", "value": "status"},
                {"name": "🎯 Filter by Priority", "value": "priority"},
                {"name": "📅 Filter by Due Date Range", "value": "date"},
                {"name": "🏷️ Filter by Tags", "value": "tags"},
                {"name": "🔎 Search by Keyword", "value": "search"},
                {"name": "✖ Clear All Filters", "value": "clear"},
                {"name": "← Back to Main Menu", "value": "back"}
            ]
        ).ask()

        if choice == "back":
            break
        elif choice == "clear":
            filter_state.clear()
            console.print("[green]✓ All filters cleared![/green]")
        elif choice == "status":
            filter_by_status()
        elif choice == "priority":
            filter_by_priority()
        elif choice == "date":
            filter_by_date_range()
        elif choice == "tags":
            filter_by_tags()
        elif choice == "search":
            search_tasks()


def filter_by_status():
    """Filter tasks by status."""
    choice = questionary.select(
        "Filter by status:",
        choices=[
            {"name": "All", "value": "all"},
            {"name": "⏳ Pending", "value": "pending"},
            {"name": "✓ Completed", "value": "completed"},
            {"name": "🔴 Overdue", "value": "overdue"}
        ]
    ).ask()

    if choice == "all":
        filter_state.status = None
        console.print("[green]✓ Status filter cleared![/green]")
    else:
        filter_state.status = Status(choice)
        console.print(f"[green]✓ Filtering by status: {choice.title()}[/green]")


def filter_by_priority():
    """Filter tasks by priority."""
    choice = questionary.select(
        "Filter by priority:",
        choices=[
            {"name": "All", "value": "all"},
            {"name": "🔴 High", "value": "high"},
            {"name": "🟡 Medium", "value": "medium"},
            {"name": "🟢 Low", "value": "low"},
            {"name": "None", "value": "none"}
        ]
    ).ask()

    if choice == "all":
        filter_state.priority = None
        console.print("[green]✓ Priority filter cleared![/green]")
    else:
        filter_state.priority = Priority(choice)
        console.print(f"[green]✓ Filtering by priority: {choice.title()}[/green]")


def filter_by_date_range():
    """Filter tasks by due date range."""
    choice = questionary.select(
        "Filter by due date:",
        choices=[
            {"name": "All", "value": "all"},
            {"name": "📅 Today", "value": "today"},
            {"name": "📅 This Week (next 7 days)", "value": "week"},
            {"name": "📅 This Month (next 30 days)", "value": "month"},
            {"name": "🔴 Overdue Only", "value": "overdue"},
            {"name": "📅 Custom Range", "value": "custom"}
        ]
    ).ask()

    if choice == "all":
        filter_state.date_range = None
        console.print("[green]✓ Date filter cleared![/green]")
    elif choice == "today":
        filter_state.date_range = (date.today(), date.today())
        console.print("[green]✓ Showing tasks due today![/green]")
    elif choice == "week":
        filter_state.date_range = (date.today(), date.today() + timedelta(days=7))
        console.print("[green]✓ Showing tasks due this week![/green]")
    elif choice == "month":
        filter_state.date_range = (date.today(), date.today() + timedelta(days=30))
        console.print("[green]✓ Showing tasks due this month![/green]")
    elif choice == "overdue":
        filter_state.date_range = (date(2000, 1, 1), date.today() - timedelta(days=1))
        console.print("[green]✓ Showing overdue tasks![/green]")
    elif choice == "custom":
        start_str = questionary.text("Start date:").ask()
        end_str = questionary.text("End date:").ask()
        start_date = parse_date(start_str)
        end_date = parse_date(end_str)
        if start_date and end_date:
            filter_state.date_range = (start_date, end_date)
            console.print(f"[green]✓ Showing tasks due between {start_date} and {end_date}![/green]")
        else:
            console.print("[red]Invalid date range![/red]")


def search_tasks():
    """Search tasks by keyword."""
    keyword = questionary.text("Enter search keyword:").ask()

    if not keyword or not keyword.strip():
        filter_state.search_keyword = None
        console.print("[green]✓ Search cleared![/green]")
    else:
        filter_state.search_keyword = keyword.strip()

        # Show preview of results
        all_tasks = task_manager.get_all_tasks()
        results = SearchService.search(all_tasks, keyword)
        console.print(f"[green]✓ Found {len(results)} tasks matching '{keyword}'[/green]")


def filter_by_tags():
    """Filter tasks by tags."""
    # Collect all unique tags from tasks
    all_tasks = task_manager.get_all_tasks()
    all_tags = set()
    for task in all_tasks:
        if task.tags:
            all_tags.update(task.tags)

    if not all_tags:
        console.print("[yellow]No tags found in any tasks![/yellow]")
        return

    # Allow user to select multiple tags
    selected_tags = questionary.checkbox(
        "Select tags to filter by (Space to select, Enter to confirm):",
        choices=[{"name": f"🏷️ {tag}", "value": tag} for tag in sorted(all_tags)]
    ).ask()

    if not selected_tags:
        filter_state.tags = None
        console.print("[green]✓ Tag filter cleared![/green]")
    else:
        filter_state.tags = selected_tags
        console.print(f"[green]✓ Filtering by tags: {', '.join(selected_tags)}[/green]")


def sort_menu():
    """Interactive sort menu."""
    global current_sort

    console.print("\n[bold cyan]Sort Tasks[/bold cyan]\n")

    choice = questionary.select(
        f"Current sort: {current_sort.value.replace('_', ' ').title()}",
        choices=[
            {"name": "📊 Default (Overdue first, then newest)", "value": "default"},
            {"name": "🎯 By Priority (High → Low)", "value": "priority"},
            {"name": "📅 By Due Date (Earliest → Latest)", "value": "due_date"},
            {"name": "🕒 By Created Date (Newest → Oldest)", "value": "created_date"}
        ]
    ).ask()

    current_sort = SortBy(choice)
    console.print(f"[green]✓ Sorting by: {current_sort.value.replace('_', ' ').title()}[/green]")


def theme_menu():
    """Interactive theme selection menu."""
    theme = get_current_theme()
    console.print(f"\n[bold {theme.primary}]Change Theme[/bold {theme.primary}]\n")

    choice = questionary.select(
        "Select theme:",
        choices=[
            {"name": "🌙 Dark Theme", "value": "dark"},
            {"name": "☀️  Light Theme", "value": "light"},
            {"name": "💻 Hacker Theme", "value": "hacker"}
        ]
    ).ask()

    set_theme(choice)
    new_theme = get_current_theme()
    console.print(f"[{new_theme.success}]✓ Theme changed to {choice.title()}![/{new_theme.success}]")
    console.print(f"[{new_theme.info}]The new theme will be visible in the next screen refresh.[/{new_theme.info}]")


def voice_command_flow():
    """Handle voice command input and execution."""
    console.print("\n[bold cyan]Voice Command Mode[/bold cyan]\n")
    console.print("[dim]Supported commands:[/dim]")
    console.print("[dim]  • Add task [title] [priority high/medium/low] [due date] [tags ...][/dim]")
    console.print("[dim]  • List tasks / Show tasks[/dim]")
    console.print("[dim]  • Update task [id] [new title][/dim]")
    console.print("[dim]  • Delete task [id][/dim]")
    console.print("[dim]  • Complete task [id][/dim]")
    console.print("[dim]  • Filter by [status/priority/tag] [value][/dim]")
    console.print("[dim]  • Search [keyword][/dim]")
    console.print("[dim]  • Sort by [priority/due date/created][/dim]\n")

    # Get voice input
    voice_text = get_voice_input()

    if not voice_text:
        console.print("[yellow]No voice input received.[/yellow]")
        return

    console.print(f"[cyan]You said: '{voice_text}'[/cyan]\n")

    # Parse command
    command = parse_voice_command(voice_text)

    if not command:
        console.print("[red]Could not understand command. Please try again.[/red]")
        return

    # Execute command
    try:
        if command.action == "add":
            if not command.title:
                console.print("[red]Could not extract task title.[/red]")
                return

            priority = Priority(command.priority) if command.priority else Priority.NONE
            due_date = parse_date(command.due_date) if command.due_date else None

            task = task_manager.add_task(
                title=command.title,
                priority=priority,
                due_date=due_date,
                tags=command.tags
            )
            console.print(f"[green]✓ Task #{task.id} created: {task.title}[/green]")

        elif command.action == "list":
            console.print("[green]Displaying tasks...[/green]")

        elif command.action == "update":
            if not command.task_id:
                console.print("[red]Could not extract task ID.[/red]")
                return

            task_manager.update_task(
                task_id=command.task_id,
                title=command.title
            )
            console.print(f"[green]✓ Task #{command.task_id} updated[/green]")

        elif command.action == "delete":
            if not command.task_id:
                console.print("[red]Could not extract task ID.[/red]")
                return

            task_manager.delete_task(command.task_id)
            console.print(f"[green]✓ Task #{command.task_id} deleted[/green]")

        elif command.action == "complete":
            if not command.task_id:
                console.print("[red]Could not extract task ID.[/red]")
                return

            task_manager.toggle_task_completion(command.task_id)
            console.print(f"[green]✓ Task #{command.task_id} marked complete[/green]")

        elif command.action == "filter":
            if command.filter_type == "status" and command.filter_value:
                filter_state.status = Status(command.filter_value)
                console.print(f"[green]✓ Filtering by status: {command.filter_value}[/green]")
            elif command.filter_type == "priority" and command.filter_value:
                filter_state.priority = Priority(command.filter_value)
                console.print(f"[green]✓ Filtering by priority: {command.filter_value}[/green]")
            elif command.filter_type == "tag" and command.filter_value:
                filter_state.tags = [command.filter_value]
                console.print(f"[green]✓ Filtering by tag: {command.filter_value}[/green]")

        elif command.action == "search":
            if command.search_keyword:
                filter_state.search_keyword = command.search_keyword
                console.print(f"[green]✓ Searching for: {command.search_keyword}[/green]")

        elif command.action == "sort":
            if command.sort_by:
                global current_sort
                current_sort = SortBy(command.sort_by)
                console.print(f"[green]✓ Sorting by: {command.sort_by}[/green]")

    except Exception as e:
        console.print(f"[red]Error executing command: {e}[/red]")


def main_menu():
    """Main menu loop."""
    while True:
        console.print()
        display_tasks()
        console.print()

        choice = questionary.select(
            "What would you like to do?",
            choices=[
                {"name": "➕ Add new task", "value": "1"},
                {"name": "✏️  Update task", "value": "2"},
                {"name": "🗑️  Delete task", "value": "3"},
                {"name": "✓ Toggle task completion", "value": "4"},
                {"name": "🔍 Filter / Search tasks", "value": "5"},
                {"name": "📊 Sort tasks", "value": "6"},
                {"name": "🎨 Change theme", "value": "7"},
                {"name": "🎤 Voice Commands", "value": "8"},
                {"name": "❌ Exit", "value": "9"}
            ]
        ).ask()

        if choice == "1":
            add_task_flow()
        elif choice == "2":
            update_task_flow()
        elif choice == "3":
            delete_task_flow()
        elif choice == "4":
            toggle_completion_flow()
        elif choice == "5":
            filter_menu()
        elif choice == "6":
            sort_menu()
        elif choice == "7":
            theme_menu()
        elif choice == "8":
            voice_command_flow()
        elif choice == "9":
            console.print("\n[cyan]Thanks for using TODO APP! Goodbye! 👋[/cyan]\n")
            sys.exit(0)


def main():
    """Main entry point."""
    try:
        console.clear()
        display_header()
        main_menu()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user. Exiting...[/yellow]")
        sys.exit(0)
    except Exception as e:
        # Escape square brackets in error message to prevent Rich markup errors
        error_msg = str(e).replace('[', '[[').replace(']', ']]')
        console.print(f"\n[red]An error occurred: {error_msg}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
