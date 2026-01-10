#!/usr/bin/env python3
"""
Phase I: Enhanced CLI Todo Application with JSON Persistence
Beautiful, colorful terminal interface with full CRUD operations.
"""

from src.models.task import Task
from src.services.task_service import TaskManager
from src.cli import ui_components as ui
from src.cli import menu
from src.cli.themes import set_theme, get_current_theme


def display_tasks(manager: TaskManager) -> None:
    """
    Display all tasks in a Rich-formatted table.

    Args:
        manager: TaskManager instance
    """
    tasks = manager.get_all_tasks()

    if not tasks:
        ui.display_info("No tasks found. Add your first task using option 1!")
        return

    table = ui.create_task_table(tasks)
    ui.console.print("\n", table, "\n")


def add_task_flow(manager: TaskManager) -> None:
    """
    Handle add task workflow with interactive prompts.

    Args:
        manager: TaskManager instance
    """
    ui.display_header("Add New Task")

    title = menu.prompt_text("Task title:")
    if not title or not title.strip():
        ui.display_error("Title cannot be empty")
        return

    description = menu.prompt_text("Description (optional):")

    try:
        ui.show_progress_bar("Creating task", duration=0.3)
        task = manager.add_task(title=title.strip(), description=description.strip())
        ui.display_success(f"Task created successfully! ID: {task.id}")
        ui.console.print(f"[bold]Title:[/bold] {task.title}")
        if task.description:
            ui.console.print(f"[bold]Description:[/bold] {task.description}")

    except ValueError as e:
        ui.display_error(str(e))


def update_task_flow(manager: TaskManager) -> None:
    """
    Handle update task workflow with interactive prompts.

    Args:
        manager: TaskManager instance
    """
    ui.display_header("Update Task")

    task_id = menu.prompt_integer("Task ID:")
    if task_id is None:
        ui.display_error("Invalid task ID")
        return

    task = manager.get_task_by_id(task_id)
    if not task:
        ui.display_error(f"Task ID {task_id} not found")
        return

    ui.console.print(f"\n[bold]Current title:[/bold] {task.title}")
    new_title = menu.prompt_text("New title (press Enter to keep):")

    ui.console.print(f"[bold]Current description:[/bold] {task.description}")
    new_description = menu.prompt_text("New description (press Enter to keep):")

    # Only update if user provided input
    title_to_update = new_title.strip() if new_title else None
    desc_to_update = new_description.strip() if new_description else None

    if title_to_update or desc_to_update:
        try:
            ui.show_progress_bar("Updating task", duration=0.3)
            manager.update_task(task_id, title=title_to_update, description=desc_to_update)
            ui.display_success(f"Task updated successfully! ID: {task.id}")
        except ValueError as e:
            ui.display_error(str(e))
    else:
        ui.display_info("No changes made")


def delete_task_flow(manager: TaskManager) -> None:
    """
    Handle delete task workflow with confirmation.

    Args:
        manager: TaskManager instance
    """
    ui.display_header("Delete Task")

    task_id = menu.prompt_integer("Task ID:")
    if task_id is None:
        ui.display_error("Invalid task ID")
        return

    task = manager.get_task_by_id(task_id)
    if not task:
        ui.display_error(f"Task ID {task_id} not found")
        return

    # Show task details
    theme = get_current_theme()
    ui.console.print(f"\n[bold]Task to delete:[/bold]")
    ui.console.print(f"ID: {task.id}")
    ui.console.print(f"Title: {task.title}")
    status = f"[{theme.success}]Complete[/{theme.success}]" if task.completed else f"[{theme.warning}]Pending[/{theme.warning}]"
    ui.console.print(f"Status: {status}")

    # Confirm deletion
    if menu.prompt_confirm("Are you sure you want to delete this task?", default=False):
        try:
            ui.show_progress_bar("Deleting task", duration=0.3)
            manager.delete_task(task_id)
            ui.display_success("Task deleted successfully!")
        except ValueError as e:
            ui.display_error(str(e))
    else:
        ui.display_info("Deletion cancelled")


def toggle_task_flow(manager: TaskManager) -> None:
    """
    Handle toggle task completion workflow.

    Args:
        manager: TaskManager instance
    """
    ui.display_header("Mark Task Complete/Incomplete")

    task_id = menu.prompt_integer("Task ID:")
    if task_id is None:
        ui.display_error("Invalid task ID")
        return

    task = manager.get_task_by_id(task_id)
    if not task:
        ui.display_error(f"Task ID {task_id} not found")
        return

    theme = get_current_theme()
    old_status = f"[{theme.success}]Complete[/{theme.success}]" if task.completed else f"[{theme.warning}]Pending[/{theme.warning}]"
    ui.console.print(f"\nCurrent status: {old_status}")

    try:
        ui.show_progress_bar("Updating status", duration=0.3)
        manager.toggle_task_completion(task_id)

        # Get updated task
        task = manager.get_task_by_id(task_id)
        new_status = f"[{theme.success}]Complete[/{theme.success}]" if task.completed else f"[{theme.warning}]Pending[/{theme.warning}]"
        ui.display_success(f"Task marked as {'complete' if task.completed else 'pending'}!")
        ui.console.print(f"ID: {task.id} | Title: {task.title} | Status: {new_status}")

    except ValueError as e:
        ui.display_error(str(e))


def change_theme_flow() -> None:
    """Handle theme change workflow."""
    ui.display_header("Change Theme")

    current_theme = get_current_theme()
    ui.console.print(f"\n[bold]Current theme:[/bold] {current_theme.name}")

    new_theme = menu.show_theme_menu()
    if new_theme:
        set_theme(new_theme)
        ui.show_progress_bar("Applying theme", duration=0.3)
        ui.display_success(f"Theme changed to {get_current_theme().name}!")


def main() -> None:
    """Main application loop with enhanced UI."""

    # Initialize manager (auto-loads from tasks.json)
    manager = TaskManager()

    # Display welcome screen
    ui.clear_screen()
    ui.display_ascii_title()

    # Show persistence status
    stats = manager.get_task_stats()
    if stats['total'] > 0:
        ui.display_success(f"Loaded {stats['total']} tasks from tasks.json")
    else:
        ui.display_info("No existing tasks - starting fresh")

    while True:
        try:
            stats = manager.get_task_stats()
            ui.display_welcome_panel(stats)

            choice = menu.show_main_menu()

            if choice == "1":
                add_task_flow(manager)

            elif choice == "2":
                display_tasks(manager)

            elif choice == "3":
                update_task_flow(manager)

            elif choice == "4":
                delete_task_flow(manager)

            elif choice == "5":
                toggle_task_flow(manager)

            elif choice == "6":
                change_theme_flow()

            elif choice == "7":
                # Save and exit
                ui.show_progress_bar("Saving tasks", duration=0.3)
                ui.display_success(f"Saved {stats['total']} tasks to tasks.json")
                ui.display_success("Thank you for using Todo Application!")
                ui.console.print("[bold]Goodbye![/bold]\n")
                break

            else:
                ui.display_error("Invalid choice. Please try again.")

        except KeyboardInterrupt:
            ui.console.print("\n")
            ui.show_progress_bar("Saving tasks", duration=0.3)
            ui.display_success(f"Saved {manager.get_task_stats()['total']} tasks to tasks.json")
            ui.display_success("Application interrupted. Goodbye!")
            break

        except Exception as e:
            ui.display_error(f"Unexpected error: {e}")
            ui.console.print("Please try again.")


if __name__ == "__main__":
    main()
