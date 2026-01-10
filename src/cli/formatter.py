"""
Task formatter for the Task Management System.
Provides Rich-formatted display for tasks with color coding and emoji indicators.
"""

from typing import Any, Optional
from rich.table import Table
from rich.text import Text
from rich import box
from rich.style import Style
from rich.color import Color

from src.models.task import Task
from src.models.enums import Priority, Status, Recurrence
from src.cli.themes import get_current_theme


# Priority color mappings
PRIORITY_COLORS = {
    Priority.HIGH: "red",
    Priority.MEDIUM: "yellow",
    Priority.LOW: "green",
    Priority.NONE: "white",
}

# Priority emoji mappings
PRIORITY_EMOJIS = {
    Priority.HIGH: "🔴",
    Priority.MEDIUM: "🟡",
    Priority.LOW: "🟢",
    Priority.NONE: "⚪",
}

# Status color mappings
STATUS_COLORS = {
    Status.COMPLETED: "green",
    Status.PENDING: "cyan",
    Status.OVERDUE: "red",
}

# Status emoji mappings
STATUS_EMOJIS = {
    Status.COMPLETED: "✓",
    Status.PENDING: "⏳",
    Status.OVERDUE: "🔴",
}

# Recurrence emoji mappings
RECURRENCE_EMOJIS = {
    Recurrence.DAILY: "🔄",
    Recurrence.WEEKLY: "📅",
    Recurrence.MONTHLY: "🗓️",
    Recurrence.YEARLY: "🗓️",
    Recurrence.NONE: "",
}


def get_priority_style(priority: Priority) -> str:
    """
    Get color style for priority level.

    Args:
        priority: Priority enum value

    Returns:
        Rich color style string
    """
    return PRIORITY_COLORS.get(priority, "white")


def get_status_style(status: Status) -> str:
    """
    Get color style for status.

    Args:
        status: Status enum value

    Returns:
        Rich color style string
    """
    return STATUS_COLORS.get(status, "white")


def get_priority_emoji(priority: Priority) -> str:
    """
    Get emoji indicator for priority.

    Args:
        priority: Priority enum value

    Returns:
        Emoji string
    """
    return PRIORITY_EMOJIS.get(priority, "⚪")


def get_status_emoji(status: Status) -> str:
    """
    Get emoji indicator for status.

    Args:
        status: Status enum value

    Returns:
        Emoji string
    """
    return STATUS_EMOJIS.get(status, "?")


def get_recurrence_emoji(recurrence: Recurrence) -> str:
    """
    Get emoji indicator for recurrence pattern.

    Args:
        recurrence: Recurrence enum value

    Returns:
        Emoji string with pattern name
    """
    emoji = RECURRENCE_EMOJIS.get(recurrence, "")
    if emoji:
        return f"{emoji} {recurrence.value}"
    return ""


def format_priority_cell(priority: Priority) -> str:
    """
    Format priority for table display.

    Args:
        priority: Priority enum value

    Returns:
        Formatted priority string with color and emoji
    """
    color = get_priority_style(priority)
    emoji = get_priority_emoji(priority)
    text = priority.value.upper()
    return f"[{color}]{emoji} {text}[/]"


def format_status_cell(status: Status) -> str:
    """
    Format status for table display.

    Args:
        status: Status enum value

    Returns:
        Formatted status string with color and emoji
    """
    color = get_status_style(status)
    emoji = get_status_emoji(status)
    text = status.value.upper()
    return f"[{color}]{emoji} {text}[/]"


def format_due_date_cell(due_date: Optional[Any]) -> str:
    """
    Format due date for table display.

    Args:
        due_date: Due date or None

    Returns:
        Formatted date string
    """
    if due_date is None:
        return "-"

    from datetime import date

    if isinstance(due_date, date):
        # Check if overdue
        if due_date < date.today():
            return f"[red]{due_date.isoformat()} ⚠[/red]"
        return f"[cyan]{due_date.isoformat()}[/cyan]"

    return str(due_date)


def format_recurrence_cell(recurrence: Recurrence) -> str:
    """
    Format recurrence for table display.

    Args:
        recurrence: Recurrence enum value

    Returns:
        Formatted recurrence string
    """
    if recurrence == Recurrence.NONE:
        return "-"

    emoji = RECURRENCE_EMOJIS.get(recurrence, "")
    return f"{emoji} {recurrence.value}"


def create_task_table(
    tasks: list[Task],
    show_priority: bool = True,
    show_due_date: bool = True,
    show_status: bool = True,
    show_recurrence: bool = True,
    overdue_first: bool = True
) -> Table:
    """
    Create a Rich table for task display with all formatting.

    Args:
        tasks: List of Task objects
        show_priority: Show priority column
        show_due_date: Show due date column
        show_status: Show status column
        show_recurrence: Show recurrence column
        overdue_first: Sort overdue tasks to top

    Returns:
        Configured Rich Table
    """
    theme = get_current_theme()

    table = Table(
        title="[bold]Task List[/bold]",
        box=box.ROUNDED,
        border_style=theme.primary,
        header_style=f"bold {theme.secondary}",
        show_lines=False,
        expand=True,
    )

    table.add_column("ID", style=theme.info, justify="center", width=6)

    if show_status:
        table.add_column("Status", justify="center", width=10)

    if show_priority:
        table.add_column("Priority", justify="center", width=10)

    table.add_column("Title", style=theme.text, no_wrap=False)

    if show_due_date:
        table.add_column("Due Date", justify="center", width=12)

    if show_recurrence:
        table.add_column("Recurrence", justify="center", width=12)

    table.add_column("Created", style=theme.muted, justify="center", width=12)

    # Sort tasks if overdue_first
    sorted_tasks = tasks
    if overdue_first:
        sorted_tasks = sorted(
            tasks,
            key=lambda t: (t.status != Status.OVERDUE, t.created_at),
            reverse=True
        )

    for task in sorted_tasks:
        # Format title with truncation
        title = task.title if len(task.title) <= 50 else task.title[:47] + "..."

        # Build row cells
        row = [str(task.id)]

        if show_status:
            status_cell = format_status_cell(task.status)
            row.append(status_cell)

        if show_priority:
            priority_cell = format_priority_cell(task.priority)
            row.append(priority_cell)

        row.append(title)

        if show_due_date:
            due_date_cell = format_due_date_cell(task.due_date)
            row.append(due_date_cell)

        if show_recurrence:
            recurrence_cell = format_recurrence_cell(task.recurrence)
            row.append(recurrence_cell)

        # Format created date
        created = task.created_at.strftime("%Y-%m-%d")
        row.append(f"[{theme.muted}]{created}[/{theme.muted}]")

        table.add_row(*row)

    return table


def create_summary_table(stats: dict) -> Table:
    """
    Create a summary statistics table.

    Args:
        stats: Dictionary with 'total', 'completed', 'pending', 'overdue' keys

    Returns:
        Configured Rich Table
    """
    theme = get_current_theme()

    table = Table(
        title="[bold]Task Summary[/bold]",
        box=box.ROUNDED,
        border_style=theme.primary,
        show_header=False,
        pad_edge=False,
    )

    table.add_column("Metric", style=theme.text)
    table.add_column("Count", justify="right", style=theme.info)

    # Total
    table.add_row(
        "Total Tasks",
        f"[{theme.primary}]{stats.get('total', 0)}[/{theme.primary}]"
    )

    # Completed
    completed = stats.get('completed', 0)
    table.add_row(
        f"[{theme.success}]✓ Completed[/]",
        f"[{theme.success}]{completed}[/]"
    )

    # Pending
    pending = stats.get('pending', 0)
    table.add_row(
        f"[{theme.warning}]⏳ Pending[/]",
        f"[{theme.warning}]{pending}[/]"
    )

    # Overdue
    overdue = stats.get('overdue', 0)
    table.add_row(
        f"[{theme.error}]🔴 Overdue[/]",
        f"[{theme.error}]{overdue}[/]"
    )

    return table


def get_task_details_panel(task: Task) -> str:
    """
    Create a detailed view of a single task.

    Args:
        task: Task object

    Returns:
        Formatted string with task details
    """
    theme = get_current_theme()

    lines = [
        f"[bold {theme.primary}]Task Details[/]",
        "",
        f"[{theme.info}]ID:[/{theme.info}] {task.id}",
        f"[{theme.text}]Title:[/{theme.text}] {task.title}",
    ]

    if task.description:
        desc = task.description if len(task.description) <= 100 else task.description[:97] + "..."
        f"[{theme.text}]Description:[/{theme.text}] {desc}"

    status_cell = format_status_cell(task.status)
    lines.append(f"[{theme.info}]Status:[/{theme.info}] {status_cell}")

    priority_cell = format_priority_cell(task.priority)
    lines.append(f"[{theme.info}]Priority:[/{theme.info}] {priority_cell}")

    if task.due_date:
        due_str = format_due_date_cell(task.due_date)
        lines.append(f"[{theme.info}]Due Date:[/{theme.info}] {due_str}")

    if task.recurrence != Recurrence.NONE:
        recur_str = format_recurrence_cell(task.recurrence)
        lines.append(f"[{theme.info}]Recurrence:[/{theme.info}] {recur_str}")

    if task.tags:
        tags_str = ", ".join(task.tags)
        lines.append(f"[{theme.info}]Tags:[/{theme.info}] {tags_str}")

    lines.extend([
        f"[{theme.info}]Created:[/{theme.info}] {task.created_at.strftime('%Y-%m-%d %H:%M')}",
        f"[{theme.info}]Updated:[/{theme.info}] {task.updated_at.strftime('%Y-%m-%d %H:%M')}",
    ])

    return "\n".join(lines)
