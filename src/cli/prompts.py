"""
Input prompts for the Task Management System.
Handles interactive prompts for adding and editing tasks with priority, due date, and recurrence.
"""

from datetime import date
from typing import Optional
import questionary
from questionary import Style as QStyle

from src.models.enums import Priority, Recurrence
from src.cli.themes import get_current_theme
from src.lib.date_parser import parse_date


def get_prompt_style() -> QStyle:
    """
    Get Questionary style based on current theme.

    Returns:
        Questionary Style instance
    """
    theme = get_current_theme()

    return QStyle([
        ('qmark', f'fg:{theme.primary} bold'),
        ('question', f'fg:{theme.text} bold'),
        ('answer', f'fg:{theme.success} bold'),
        ('pointer', f'fg:{theme.primary} bold'),
        ('highlighted', f'fg:{theme.primary} bold'),
        ('selected', f'fg:{theme.success}'),
        ('separator', f'fg:{theme.muted}'),
        ('instruction', f'fg:{theme.info}'),
        ('text', f'fg:{theme.text}'),
    ])


def prompt_title() -> Optional[str]:
    """
    Prompt user for task title.

    Returns:
        Title string or None if cancelled
    """
    result = questionary.text(
        "Task title:",
        style=get_prompt_style(),
        validate=lambda x: len(x.strip()) > 0 or "Title cannot be empty"
    ).ask()

    return result.strip() if result else None


def prompt_description() -> str:
    """
    Prompt user for optional task description.

    Returns:
        Description string (empty if not provided)
    """
    result = questionary.text(
        "Description (optional):",
        style=get_prompt_style(),
    ).ask()

    return result.strip() if result else ""


def prompt_priority() -> Priority:
    """
    Prompt user for task priority.

    Returns:
        Priority enum value
    """
    choices = [
        {"name": "🔴 High", "value": "high"},
        {"name": "🟡 Medium", "value": "medium"},
        {"name": "🟢 Low", "value": "low"},
        {"name": "⚪ None", "value": "none"},
    ]

    result = questionary.select(
        "Priority:",
        choices=choices,
        style=get_prompt_style(),
        default="none"
    ).ask()

    if result is None:
        return Priority.NONE

    return Priority(result)


def prompt_due_date() -> Optional[date]:
    """
    Prompt user for task due date with natural language support.

    Returns:
        Due date or None if not provided
    """
    help_text = (
        "Enter a date in natural language or ISO format:\n"
        "  • 'tomorrow', 'next week', 'next Monday'\n"
        "  • '2025-12-31', '12/31/2025'\n"
        "  • 'today', 'yesterday'\n"
        "  • Leave empty for no due date"
    )

    print(f"\n[dim]{help_text}[/dim]")

    result = questionary.text(
        "Due date:",
        style=get_prompt_style(),
    ).ask()

    if not result or not result.strip():
        return None

    parsed = parse_date(result.strip())

    if parsed is None:
        print("[warning]Could not parse date. Please try again.[/warning]")
        return prompt_due_date()

    return parsed


def prompt_recurrence() -> Recurrence:
    """
    Prompt user for task recurrence pattern.

    Returns:
        Recurrence enum value
    """
    choices = [
        {"name": "🔄 Daily", "value": "daily"},
        {"name": "📅 Weekly", "value": "weekly"},
        {"name": "🗓️ Monthly", "value": "monthly"},
        {"name": "🗓️ Yearly", "value": "yearly"},
        {"name": "❌ None", "value": "none"},
    ]

    result = questionary.select(
        "Recurrence:",
        choices=choices,
        style=get_prompt_style(),
        default="none"
    ).ask()

    if result is None:
        return Recurrence.NONE

    return Recurrence(result)


def prompt_tags() -> list[str]:
    """
    Prompt user for task tags.

    Returns:
        List of tag strings
    """
    result = questionary.text(
        "Tags (comma-separated, optional):",
        style=get_prompt_style(),
    ).ask()

    if not result or not result.strip():
        return []

    # Parse comma-separated tags
    tags = [tag.strip() for tag in result.split(',') if tag.strip()]
    return tags


def add_task_prompts() -> dict:
    """
    Run all prompts for adding a new task.

    Returns:
        Dictionary with title, description, priority, due_date, recurrence, tags
    """
    title = prompt_title()
    if title is None:
        return {"cancelled": True}

    description = prompt_description()
    priority = prompt_priority()

    # Only prompt for due date if recurrence is not NONE
    recurrence = prompt_recurrence()
    due_date = None

    if recurrence != Recurrence.NONE:
        print("\n[info]Recurring tasks require a due date.[/info]")
        due_date = prompt_due_date()
        if due_date is None:
            print("[warning]Setting recurrence to 'none' due to missing due date[/warning]")
            recurrence = Recurrence.NONE
    else:
        due_date = prompt_due_date()

    tags = prompt_tags()

    return {
        "cancelled": False,
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "recurrence": recurrence,
        "tags": tags,
    }


def edit_task_prompts(current_task) -> dict:
    """
    Run prompts for editing an existing task.

    Args:
        current_task: Task object with current values

    Returns:
        Dictionary with updated fields (None means no change)
    """
    # Title
    new_title = questionary.text(
        f"New title (current: '{current_task.title}'):",
        style=get_prompt_style(),
    ).ask()

    title = new_title.strip() if new_title and new_title.strip() else None

    # Description
    current_desc = current_task.description or ""
    new_desc = questionary.text(
        f"New description (current: '{current_desc[:50]}...' if len > 50 else current_desc):",
        style=get_prompt_style(),
    ).ask()

    description = new_desc.strip() if new_desc and new_desc.strip() else None

    # Priority
    priority_choices = [
        {"name": "🔴 High", "value": "high"},
        {"name": "🟡 Medium", "value": "medium"},
        {"name": "🟢 Low", "value": "low"},
        {"name": f"⚪ Keep current ({current_task.priority.value})", "value": "keep"},
    ]

    priority_result = questionary.select(
        "New priority:",
        choices=priority_choices,
        style=get_prompt_style(),
    ).ask()

    priority = None
    if priority_result and priority_result != "keep":
        priority = Priority(priority_result)

    # Recurrence
    recurrence_choices = [
        {"name": "🔄 Daily", "value": "daily"},
        {"name": "📅 Weekly", "value": "weekly"},
        {"name": "🗓️ Monthly", "value": "monthly"},
        {"name": "🗓️ Yearly", "value": "yearly"},
        {"name": f"❌ Keep current ({current_task.recurrence.value})", "value": "keep"},
    ]

    recurrence_result = questionary.select(
        "New recurrence:",
        choices=recurrence_choices,
        style=get_prompt_style(),
    ).ask()

    recurrence = None
    if recurrence_result and recurrence_result != "keep":
        recurrence = Recurrence(recurrence_result)

    # Due date - handle recurring tasks specially
    due_date = None
    if recurrence is not None and recurrence != Recurrence.NONE:
        # New recurrence requires due date
        print(f"\n[info]Recurring tasks require a due date. Current: {current_task.due_date}[/info]")
        new_due_date = prompt_due_date()
        if new_due_date:
            due_date = new_due_date
        else:
            print("[warning]Cannot set recurring task without due date. Keeping current recurrence.[/warning]")
            recurrence = current_task.recurrence
    elif recurrence is None and current_task.recurrence != Recurrence.NONE:
        # User wants to keep recurrence, ask about due date
        if current_task.due_date:
            change_due = questionary.confirm(
                f"Change due date? (current: {current_task.due_date})",
                style=get_prompt_style(),
            ).ask()
            if change_due:
                new_due_date = prompt_due_date()
                if new_due_date:
                    due_date = new_due_date
    else:
        # Non-recurring task - ask if they want to add due date
        if current_task.due_date:
            change_due = questionary.confirm(
                f"Change due date? (current: {current_task.due_date})",
                style=get_prompt_style(),
            ).ask()
            if change_due:
                new_due_date = prompt_due_date()
                if new_due_date:
                    due_date = new_due_date
        else:
            add_due = questionary.confirm(
                "Add a due date?",
                style=get_prompt_style(),
            ).ask()
            if add_due:
                new_due_date = prompt_due_date()
                if new_due_date:
                    due_date = new_due_date

    return {
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "recurrence": recurrence,
    }
