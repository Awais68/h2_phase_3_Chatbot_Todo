"""
Interactive Menu Module
Questionary-based interactive menus for the Todo CLI application.
"""

import questionary
from questionary import Style as QStyle

from src.cli.themes import get_current_theme
from src.models.enums import Priority, Status, SortBy


def get_menu_style() -> QStyle:
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


def show_main_menu() -> str:
    """
    Display main menu and get user choice.

    Returns:
        User's menu choice as a string
    """
    choices = [
        {"name": "➕ Add new task", "value": "1"},
        {"name": "📋 View all tasks", "value": "2"},
        {"name": "✏️  Update task", "value": "3"},
        {"name": "🗑️  Delete task", "value": "4"},
        {"name": "✓ Mark task complete/incomplete", "value": "5"},
        {"name": "🔍 Filter / Search", "value": "6"},
        {"name": "📊 Sort Tasks", "value": "7"},
        {"name": "🎤 Voice Input", "value": "8"},
        {"name": "🎨 Change theme", "value": "9"},
        {"name": "❌ Exit", "value": "0"},
    ]

    return questionary.select(
        "Choose an option:",
        choices=choices,
        style=get_menu_style(),
        use_shortcuts=True,
        use_arrow_keys=True,
    ).ask()


def show_filter_menu() -> str:
    """
    Display filter menu with filter options.

    Returns:
        User's filter choice as string
    """
    choices = [
        {"name": "📊 By Status", "value": "status"},
        {"name": "🔴 By Priority", "value": "priority"},
        {"name": "📅 By Due Date Range", "value": "date"},
        {"name": "🔍 Search Tasks", "value": "search"},
        {"name": "🏷️ By Tags", "value": "tags"},
        {"name": "❌ Clear Filters", "value": "clear"},
        {"name": "↩️ Back to Main Menu", "value": "back"},
    ]

    return questionary.select(
        "Filter Tasks:",
        choices=choices,
        style=get_menu_style(),
        use_shortcuts=True,
        use_arrow_keys=True,
    ).ask()


def show_status_filter_menu() -> str:
    """
    Display status filter options.

    Returns:
        Selected status filter
    """
    choices = [
        {"name": "⏳ Pending", "value": "pending"},
        {"name": "✓ Completed", "value": "completed"},
        {"name": "🔴 Overdue", "value": "overdue"},
        {"name": "↩️ Back", "value": "back"},
    ]

    return questionary.select(
        "Filter by Status:",
        choices=choices,
        style=get_menu_style(),
        use_shortcuts=True,
    ).ask()


def show_priority_filter_menu() -> str:
    """
    Display priority filter options.

    Returns:
        Selected priority filter
    """
    choices = [
        {"name": "🔴 High", "value": "high"},
        {"name": "🟡 Medium", "value": "medium"},
        {"name": "🟢 Low", "value": "low"},
        {"name": "⚪ None", "value": "none"},
        {"name": "↩️ Back", "value": "back"},
    ]

    return questionary.select(
        "Filter by Priority:",
        choices=choices,
        style=get_menu_style(),
        use_shortcuts=True,
    ).ask()


def show_date_range_menu() -> str:
    """
    Display date range filter options.

    Returns:
        Selected date range
    """
    choices = [
        {"name": "📅 Today", "value": "today"},
        {"name": "📅 This Week", "value": "week"},
        {"name": "📅 This Month", "value": "month"},
        {"name": "⚠️ Overdue Only", "value": "overdue"},
        {"name": "↩️ Back", "value": "back"},
    ]

    return questionary.select(
        "Filter by Date Range:",
        choices=choices,
        style=get_menu_style(),
        use_shortcuts=True,
    ).ask()


def show_sort_menu() -> str:
    """
    Display sort options menu.

    Returns:
        Selected sort option
    """
    choices = [
        {"name": "📋 Default (Overdue first, then newest)", "value": "default"},
        {"name": "🔴 Priority (High → Medium → Low)", "value": "priority"},
        {"name": "📅 Due Date (Earliest first)", "value": "due_date"},
        {"name": "🕐 Created Date (Newest first)", "value": "created_date"},
        {"name": "↩️ Back", "value": "back"},
    ]

    return questionary.select(
        "Sort Tasks:",
        choices=choices,
        style=get_menu_style(),
        use_shortcuts=True,
    ).ask()


def show_theme_menu() -> str:
    """
    Display theme selection menu.

    Returns:
        Selected theme name
    """
    choices = [
        {"name": "🌙 Dark Theme", "value": "dark"},
        {"name": "☀️  Light Theme", "value": "light"},
        {"name": "💻 Hacker Theme", "value": "hacker"},
    ]

    return questionary.select(
        "Select a theme:",
        choices=choices,
        style=get_menu_style(),
        use_shortcuts=True,
        use_arrow_keys=True,
    ).ask()


def prompt_text(message: str, default: str = "") -> str:
    """
    Prompt user for text input.

    Args:
        message: Prompt message
        default: Default value

    Returns:
        User's text input
    """
    return questionary.text(
        message,
        default=default,
        style=get_menu_style(),
    ).ask()


def prompt_confirm(message: str, default: bool = False) -> bool:
    """
    Prompt user for yes/no confirmation.

    Args:
        message: Confirmation message
        default: Default choice

    Returns:
        True if user confirmed, False otherwise
    """
    return questionary.confirm(
        message,
        default=default,
        style=get_menu_style(),
    ).ask()


def prompt_integer(message: str) -> int | None:
    """
    Prompt user for integer input.

    Args:
        message: Prompt message

    Returns:
        Integer value or None if invalid
    """
    result = questionary.text(
        message,
        style=get_menu_style(),
    ).ask()

    try:
        return int(result)
    except (ValueError, TypeError):
        return None
