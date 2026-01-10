#!/usr/bin/env python3
"""
Demo script to showcase the Enhanced CLI features without interactive input.
"""

from src.models.task import Task
from src.services.task_service import TaskManager
from src.cli import ui_components as ui
from src.cli.themes import set_theme, get_current_theme, THEMES

def demo_cli():
    """Demonstrate the enhanced CLI features."""

    # Initialize manager with some sample tasks
    manager = TaskManager()

    # Clear screen and show ASCII art
    ui.clear_screen()
    ui.display_ascii_title()

    print("\n")
    ui.display_header("🎉 Welcome to Todo Evolution - Enhanced CLI Demo")

    # Show available themes
    print("\n")
    ui.display_header("Available Themes")
    for theme_name in THEMES.keys():
        theme = THEMES[theme_name]
        print(f"  • {theme.name}: {theme.primary}")

    # Add some sample tasks
    print("\n")
    ui.display_header("Adding Sample Tasks")
    ui.show_progress_bar("Creating sample tasks", duration=0.5)

    task1 = manager.add_task("Buy groceries", "Milk, bread, eggs")
    task2 = manager.add_task("Complete hackathon project", "Implement all 5 user stories")
    task3 = manager.add_task("Review pull requests", "Check team submissions")
    task4 = manager.add_task("Write documentation", "README and API docs")

    ui.display_success(f"✓ Created {manager.get_task_stats()['total']} tasks")

    # Display tasks in beautiful table
    print("\n")
    ui.display_header("Task List (Beautiful Table)")
    tasks = manager.get_all_tasks()
    table = ui.create_task_table(tasks)
    ui.console.print(table)

    # Toggle a task to show status change
    print("\n")
    ui.display_header("Completing a Task")
    ui.show_progress_bar("Updating task status", duration=0.3)
    manager.toggle_task_completion(task1.id)
    ui.display_success(f"✓ Marked task {task1.id} as complete!")

    # Show updated table
    print("\n")
    table = ui.create_task_table(manager.get_all_tasks())
    ui.console.print(table)

    # Show task statistics
    print("\n")
    ui.display_header("Task Statistics")
    stats = manager.get_task_stats()
    ui.display_welcome_panel(stats)

    # Demonstrate theme switching
    print("\n")
    ui.display_header("Theme Switching Demo")

    for theme_name in ["dark", "light", "hacker"]:
        set_theme(theme_name)
        current_theme = get_current_theme()
        ui.show_progress_bar(f"Applying {current_theme.name} theme", duration=0.2)
        ui.display_info(f"Current theme: {current_theme.name}")

    # Reset to dark theme
    set_theme("dark")

    # Show all status indicators
    print("\n")
    ui.display_header("Status Indicators")
    ui.display_success("✓ This is a success message")
    ui.display_error("✗ This is an error message")
    ui.display_warning("⚠ This is a warning message")
    ui.display_info("ℹ This is an info message")

    # Final message
    print("\n")
    ui.display_header("Demo Complete!")
    ui.console.print("[bold green]✨ All CLI enhancement features demonstrated![/bold green]")
    ui.console.print("\n[dim]Run 'python main.py' for the full interactive experience.[/dim]\n")


if __name__ == "__main__":
    demo_cli()
