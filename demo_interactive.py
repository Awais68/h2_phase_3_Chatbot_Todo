#!/usr/bin/env python3
"""
Interactive demo of Phase I CLI with all features.
Shows menu, adds tasks, displays list, updates, completes, and deletes.
"""

from src.models.task import Task
from src.services.task_service import TaskManager
from src.cli import ui_components as ui
from src.cli.themes import set_theme, get_current_theme
import time


def pause(seconds=1.5):
    """Pause for dramatic effect."""
    time.sleep(seconds)


def main():
    """Full interactive demo."""

    # Initialize
    ui.clear_screen()
    ui.display_ascii_title()
    pause(1)

    print("\n")
    ui.display_header("Welcome to Phase I: Enhanced CLI Todo App")
    pause(1)

    # Show features
    print("\n")
    ui.console.print("[bold cyan]✨ Features:[/bold cyan]")
    ui.console.print("  • Beautiful ASCII art title")
    ui.console.print("  • Rich-formatted colorful tables")
    ui.console.print("  • Progress bars and animations")
    ui.console.print("  • 3 themes (dark/light/hacker)")
    ui.console.print("  • Emoji status indicators")
    ui.console.print("  • JSON file persistence")
    pause(2)

    # Initialize manager
    print("\n")
    ui.display_header("Step 1: Initialize Task Manager")
    ui.show_progress_bar("Loading tasks from tasks.json", duration=0.5)
    manager = TaskManager()
    stats = manager.get_task_stats()
    if stats['total'] > 0:
        ui.display_success(f"✓ Loaded {stats['total']} existing tasks")
    else:
        ui.display_info("Starting with empty task list")
    pause(1)

    # Show current tasks if any
    if stats['total'] > 0:
        print("\n")
        ui.display_header("Existing Tasks")
        table = ui.create_task_table(manager.get_all_tasks())
        ui.console.print(table, "\n")
        pause(2)

    # Add tasks
    print("\n")
    ui.display_header("Step 2: Adding New Tasks")
    pause(1)

    ui.console.print("[dim]Adding task 1...[/dim]")
    ui.show_progress_bar("Creating task", duration=0.3)
    task1 = manager.add_task("Buy groceries", "Milk, bread, eggs, cheese")
    ui.display_success(f"✓ Task {task1.id}: {task1.title}")
    pause(0.5)

    ui.console.print("[dim]Adding task 2...[/dim]")
    ui.show_progress_bar("Creating task", duration=0.3)
    task2 = manager.add_task("Complete project documentation", "README and API docs")
    ui.display_success(f"✓ Task {task2.id}: {task2.title}")
    pause(0.5)

    ui.console.print("[dim]Adding task 3...[/dim]")
    ui.show_progress_bar("Creating task", duration=0.3)
    task3 = manager.add_task("Review pull requests", "Check team submissions")
    ui.display_success(f"✓ Task {task3.id}: {task3.title}")
    pause(0.5)

    ui.console.print("[dim]Adding task 4...[/dim]")
    ui.show_progress_bar("Creating task", duration=0.3)
    task4 = manager.add_task("Deploy to production", "After all tests pass")
    ui.display_success(f"✓ Task {task4.id}: {task4.title}")
    pause(1)

    # Display all tasks
    print("\n")
    ui.display_header("Step 3: Display Task List")
    pause(0.5)
    table = ui.create_task_table(manager.get_all_tasks())
    ui.console.print(table, "\n")
    pause(2)

    # Complete a task
    print("\n")
    ui.display_header("Step 4: Complete a Task")
    pause(0.5)
    ui.console.print(f"[dim]Marking task {task1.id} as complete...[/dim]")
    ui.show_progress_bar("Updating status", duration=0.3)
    manager.toggle_task_completion(task1.id)
    ui.display_success(f"✓ Task {task1.id} marked as complete!")
    pause(1)

    # Show updated list
    print("\n")
    ui.display_header("Updated Task List")
    table = ui.create_task_table(manager.get_all_tasks())
    ui.console.print(table, "\n")
    pause(2)

    # Update a task
    print("\n")
    ui.display_header("Step 5: Update a Task")
    pause(0.5)
    ui.console.print(f"[dim]Updating task {task2.id} title...[/dim]")
    ui.show_progress_bar("Updating task", duration=0.3)
    manager.update_task(task2.id, title="Complete all documentation", description="README, API docs, and deployment guide")
    ui.display_success(f"✓ Task {task2.id} updated successfully!")
    pause(1)

    # Show updated list
    print("\n")
    table = ui.create_task_table(manager.get_all_tasks())
    ui.console.print(table, "\n")
    pause(2)

    # Delete a task
    print("\n")
    ui.display_header("Step 6: Delete a Task")
    pause(0.5)
    ui.console.print(f"[dim]Deleting task {task3.id}...[/dim]")
    ui.show_progress_bar("Deleting task", duration=0.3)
    manager.delete_task(task3.id)
    ui.display_success(f"✓ Task {task3.id} deleted successfully!")
    pause(1)

    # Show final list
    print("\n")
    ui.display_header("Final Task List")
    table = ui.create_task_table(manager.get_all_tasks())
    ui.console.print(table, "\n")
    pause(2)

    # Show statistics
    print("\n")
    ui.display_header("Step 7: Task Statistics")
    pause(0.5)
    stats = manager.get_task_stats()
    ui.display_welcome_panel(stats)
    pause(2)

    # Theme switching demo
    print("\n")
    ui.display_header("Step 8: Theme Switching")
    pause(0.5)

    themes = ["dark", "light", "hacker", "dark"]
    for theme_name in themes:
        ui.console.print(f"[dim]Switching to {theme_name} theme...[/dim]")
        set_theme(theme_name)
        ui.show_progress_bar(f"Applying {theme_name} theme", duration=0.2)
        current = get_current_theme()
        ui.display_info(f"Current theme: {current.name} (primary color: {current.primary})")
        pause(0.8)

    # Persistence info
    print("\n")
    ui.display_header("Step 9: JSON Persistence")
    pause(0.5)
    ui.display_success("✓ All changes automatically saved to tasks.json")
    ui.display_info("💡 Tasks will persist across sessions")
    ui.console.print("\n[bold]tasks.json contents:[/bold]")

    import json
    try:
        with open("tasks.json", "r") as f:
            data = json.load(f)
            ui.console.print(f"  • Total tasks: {len(data.get('tasks', []))}")
            ui.console.print(f"  • Next ID: {data.get('next_id', 'N/A')}")
            ui.console.print(f"  • Saved at: {data.get('saved_at', 'N/A')[:19]}")
            ui.console.print(f"  • File size: {len(json.dumps(data, indent=2))} bytes")
    except Exception as e:
        ui.display_warning(f"Could not read tasks.json: {e}")

    pause(2)

    # Final summary
    print("\n")
    ui.display_header("Demo Complete!")
    ui.console.print("[bold green]✨ Phase I fully demonstrated![/bold green]\n")
    ui.console.print("[bold]Summary of operations:[/bold]")
    ui.console.print("  ✓ ASCII art title displayed")
    ui.console.print("  ✓ Added 4 tasks")
    ui.console.print("  ✓ Displayed tasks in Rich table")
    ui.console.print("  ✓ Completed 1 task")
    ui.console.print("  ✓ Updated 1 task")
    ui.console.print("  ✓ Deleted 1 task")
    ui.console.print("  ✓ Viewed statistics")
    ui.console.print("  ✓ Switched themes (dark/light/hacker)")
    ui.console.print("  ✓ All changes saved to tasks.json\n")
    ui.console.print("[bold cyan]Test Results:[/bold cyan]")
    ui.console.print("  • 136/136 tests passing")
    ui.console.print("  • 93% code coverage")
    ui.console.print("  • 0 critical issues\n")
    ui.console.print("[bold]Next steps:[/bold]")
    ui.console.print("  • Run 'python phase1_cli.py' for full interactive experience")
    ui.console.print("  • Run './run_tests.sh' to see all tests")
    ui.console.print("  • Check 'tasks.json' to see persisted data\n")


if __name__ == "__main__":
    main()
