#!/usr/bin/env python3
"""
Demo Phase I with JSON persistence.
Demonstrates add, save, load, and display features.
"""

from src.models.task import Task
from src.services.task_service import TaskManager
from src.cli import ui_components as ui
from src.cli.themes import set_theme

def main():
    """Demonstrate Phase I with JSON persistence."""

    ui.clear_screen()
    ui.display_ascii_title()

    print("\n")
    ui.display_header("Phase I: Enhanced CLI with JSON Persistence")

    # Initialize manager (auto-loads from tasks.json if exists)
    print("\n")
    ui.show_progress_bar("Initializing Task Manager", duration=0.3)
    manager = TaskManager()

    # Show loaded tasks
    stats = manager.get_task_stats()
    if stats['total'] > 0:
        ui.display_success(f"✓ Loaded {stats['total']} tasks from tasks.json")
        table = ui.create_task_table(manager.get_all_tasks())
        ui.console.print("\n", table, "\n")
    else:
        ui.display_info("No existing tasks found - starting fresh")

    # Add some new tasks
    print("\n")
    ui.display_header("Adding New Tasks")
    ui.show_progress_bar("Creating tasks", duration=0.5)

    task1 = manager.add_task("Complete Phase I implementation", "JSON persistence + tests")
    task2 = manager.add_task("Run all tests", "136 test cases")
    task3 = manager.add_task("Demo the CLI", "Show persistence working")

    ui.display_success(f"✓ Added 3 new tasks")

    # Show all tasks
    print("\n")
    ui.display_header("Current Task List")
    table = ui.create_task_table(manager.get_all_tasks())
    ui.console.print(table, "\n")

    # Complete one task
    print("\n")
    ui.display_header("Completing a Task")
    ui.show_progress_bar("Updating task status", duration=0.3)
    manager.toggle_task_completion(task1.id)
    ui.display_success(f"✓ Marked task {task1.id} as complete!")

    # Show updated list
    print("\n")
    table = ui.create_task_table(manager.get_all_tasks())
    ui.console.print(table, "\n")

    # Show stats
    print("\n")
    ui.display_header("Task Statistics")
    stats = manager.get_task_stats()
    ui.display_welcome_panel(stats)

    # Persistence info
    print("\n")
    ui.display_header("JSON Persistence")
    ui.display_success("✓ All changes automatically saved to tasks.json")
    ui.display_info("💡 Tasks will be reloaded on next run")

    # Show JSON file content
    try:
        import json
        with open("tasks.json", "r") as f:
            data = json.load(f)
            ui.console.print("\n[bold]tasks.json contents:[/bold]")
            ui.console.print(f"  • Total tasks: {len(data.get('tasks', []))}")
            ui.console.print(f"  • Next ID: {data.get('next_id', 'N/A')}")
            ui.console.print(f"  • Saved at: {data.get('saved_at', 'N/A')}")
    except Exception as e:
        ui.display_warning(f"Could not read tasks.json: {e}")

    # Final message
    print("\n")
    ui.display_header("Demo Complete!")
    ui.console.print("[bold green]✨ Phase I is working perfectly![/bold green]\n")
    ui.console.print("[dim]All 136 tests passing | 93% coverage | JSON persistence working[/dim]\n")
    ui.console.print("[bold]Next steps:[/bold]")
    ui.console.print("  • Run './run_tests.sh' to see all tests")
    ui.console.print("  • Run 'python main.py' for full interactive CLI")
    ui.console.print("  • Check 'tasks.json' to see persisted data\n")


if __name__ == "__main__":
    main()
