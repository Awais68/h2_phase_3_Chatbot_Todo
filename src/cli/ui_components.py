"""
UI Components Module
Rich-formatted UI components for the Todo CLI application.
"""

from art import text2art
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich import box
from typing import Any, Callable
import time

from src.cli.themes import get_current_theme


console = Console()


def display_ascii_title() -> None:
    """Display ASCII art title banner."""
    theme = get_current_theme()
    title = text2art("TODO  APP", font="small")
    console.print(title, style=theme.primary, justify="center")


def display_welcome_panel(stats: dict[str, int]) -> None:
    """
    Display welcome panel with task statistics.

    Args:
        stats: Dictionary with 'total', 'completed', 'pending' keys
    """
    theme = get_current_theme()

    content = (
        f"[{theme.info}]Tasks:[/{theme.info}] {stats['total']} total\n"
        f"[{theme.success}]✓ Completed:[/{theme.success}] {stats['completed']}\n"
        f"[{theme.warning}]⏳ Pending:[/{theme.warning}] {stats['pending']}"
    )

    panel = Panel(
        content,
        title="[bold]Status Overview[/bold]",
        border_style=theme.primary,
        box=box.ROUNDED,
        padding=(1, 2),
    )

    console.print(panel)


def create_task_table(tasks: list[Any]) -> Table:
    """
    Create a Rich table for task display.

    Args:
        tasks: List of Task objects

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
    )

    table.add_column("ID", style=theme.info, justify="center", width=6)
    table.add_column("Status", justify="center", width=8)
    table.add_column("Title", style=theme.text, no_wrap=False)
    table.add_column("Created", style=theme.muted, justify="center", width=12)

    for task in tasks:
        # Color-coded status
        if task.completed:
            status_icon = f"[{theme.success}]✓[/{theme.success}]"
            status_text = f"[{theme.success}]Done[/{theme.success}]"
        else:
            status_icon = f"[{theme.warning}]⏳[/{theme.warning}]"
            status_text = f"[{theme.warning}]Pending[/{theme.warning}]"

        status = f"{status_icon} {status_text}"

        # Format title
        title = task.title if len(task.title) <= 50 else task.title[:47] + "..."

        # Format date
        created = task.created_at.strftime("%Y-%m-%d")

        table.add_row(str(task.id), status, title, created)

    return table


def show_progress_bar(description: str, duration: float = 0.5) -> None:
    """
    Show a progress bar animation for an operation.

    Args:
        description: Description of the operation
        duration: How long to show the progress bar (seconds)
    """
    theme = get_current_theme()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"[{theme.primary}]{description}[/{theme.primary}]",
            total=100
        )

        # Simulate progress
        step = duration / 10
        for i in range(10):
            time.sleep(step)
            progress.update(task, advance=10)


def display_success(message: str) -> None:
    """
    Display a success message.

    Args:
        message: Success message to display
    """
    theme = get_current_theme()
    console.print(f"\n[{theme.success}]✓ {message}[/{theme.success}]")


def display_error(message: str) -> None:
    """
    Display an error message.

    Args:
        message: Error message to display
    """
    theme = get_current_theme()
    console.print(f"\n[{theme.error}]✗ {message}[/{theme.error}]")


def display_warning(message: str) -> None:
    """
    Display a warning message.

    Args:
        message: Warning message to display
    """
    theme = get_current_theme()
    console.print(f"\n[{theme.warning}]⚠ {message}[/{theme.warning}]")


def display_info(message: str) -> None:
    """
    Display an info message.

    Args:
        message: Info message to display
    """
    theme = get_current_theme()
    console.print(f"\n[{theme.info}]💡 {message}[/{theme.info}]")


def display_header(text: str) -> None:
    """
    Display a section header.

    Args:
        text: Header text
    """
    theme = get_current_theme()
    console.print(f"\n[bold {theme.primary}]=== {text} ===[/bold {theme.primary}]")


def clear_screen() -> None:
    """Clear the console screen."""
    console.clear()


def print_separator() -> None:
    """Print a visual separator line."""
    theme = get_current_theme()
    console.print(f"[{theme.muted}]" + "-" * 70 + f"[/{theme.muted}]")
