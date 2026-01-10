"""
Phase I: Todo In-Memory Python Console App
Basic Level Functionality - Command-line todo application that stores tasks in memory.

Requirements:
- Add tasks with title and description
- List all tasks with status indicators
- Update task details
- Delete tasks by ID
- Mark tasks as complete/incomplete
- Filter and search tasks
- Sort tasks by priority, due date, or creation date
- Optional voice input for hands-free task creation
"""

from datetime import date, timedelta
from src.models.task import Task
from src.models.enums import Priority, Recurrence, Status, SortBy
from src.models.filter import FilterState, FilterService
from src.services.task_service import TaskManager
from src.services.voice_service import VoiceService
from src.cli import ui_components as ui
from src.cli import menu
from src.cli import prompts
from src.cli import formatter
from src.cli.themes import set_theme, get_current_theme
from src.lib.date_parser import parse_date
from rich.table import Table
from rich.panel import Panel


# Import helper functions from formatter for direct use
from src.cli.formatter import (
    get_priority_style,
    get_status_style,
    get_priority_emoji,
    get_status_emoji,
    get_recurrence_emoji,
    format_priority_cell,
    format_status_cell,
    format_due_date_cell,
    format_recurrence_cell,
)

# Global filter and sort state
_filter_state = FilterState()
_current_sort = SortBy.DEFAULT


def display_tasks(manager: TaskManager) -> None:
    """
    Display all tasks in a Rich-formatted table.
    Uses formatter module with color coding, filter, and sort support.

    Args:
        manager: TaskManager instance
    """
    global _filter_state, _current_sort

    tasks = manager.get_all_tasks()

    if not tasks:
        ui.display_info("No tasks found. Add your first task using option 1!")
        _filter_state.clear()
        return

    # Apply filters if active
    original_count = len(tasks)
    if _filter_state.is_active():
        tasks = FilterService.apply_filters(tasks, _filter_state)

    if not tasks:
        ui.display_info(f"No tasks match your filters. Showing 0 of {original_count} tasks.")
        # Show stats anyway
        stats = manager.get_task_stats()
        overdue_count = sum(1 for t in manager.tasks if t.status == Status.OVERDUE)
        stats["overdue"] = overdue_count
        stats["filtered"] = original_count
        summary_table = formatter.create_summary_table(stats)
        ui.console.print(summary_table)
        if _filter_state.is_active():
            theme = get_current_theme()
            ui.console.print(f"\n[{theme.warning}]Active Filters: {_filter_state.describe()}[/{theme.warning}]")
        ui.console.print()
        return

    # Apply sort
    tasks = manager.sort_tasks(tasks, _current_sort)

    # Use the new formatter with all columns and sort
    table = formatter.create_task_table(
        tasks,
        show_priority=True,
        show_due_date=True,
        show_status=True,
        show_recurrence=True,
        overdue_first=False  # Already sorted
    )
    ui.console.print("\n", table, "\n")

    # Show stats
    stats = manager.get_task_stats()
    overdue_count = sum(1 for t in manager.tasks if t.status == Status.OVERDUE)
    stats["overdue"] = overdue_count
    stats["filtered"] = original_count
    summary_table = formatter.create_summary_table(stats)
    ui.console.print(summary_table)

    # Show filter/sort info
    theme = get_current_theme()
    if _filter_state.is_active():
        ui.console.print(f"\n[{theme.warning}]Filters: {_filter_state.describe()}[/{theme.warning}]")
    ui.console.print(f"[{theme.info}]Sort: {_current_sort.value.replace('_', ' ').title()}[/{theme.info}]")
    ui.console.print(f"[{theme.info}]Showing {len(tasks)} of {original_count} tasks[/{theme.info}]")
    ui.console.print()


def add_task_flow(manager: TaskManager) -> None:
    """
    Handle add task workflow with interactive prompts.
    Uses prompts module for priority, due date, and recurrence.

    Args:
        manager: TaskManager instance
    """
    ui.display_header("Add New Task")

    # Use the comprehensive prompts module
    result = prompts.add_task_prompts()

    if result.get("cancelled"):
        ui.display_info("Task creation cancelled")
        return

    try:
        ui.show_progress_bar("Creating task", duration=0.3)
        task = manager.add_task(
            title=result["title"],
            description=result["description"],
            priority=result["priority"],
            due_date=result["due_date"],
            recurrence=result["recurrence"],
            tags=result["tags"],
        )
        ui.display_success(f"Task created successfully! ID: {task.id}")
        ui.console.print(f"[bold]Title:[/bold] {task.title}")
        if task.description:
            ui.console.print(f"[bold]Description:[/bold] {task.description}")

        # Show additional details
        theme = get_current_theme()
        priority_text = f"[{get_priority_style(task.priority)}]{task.priority.value.upper()}[/]"
        ui.console.print(f"[bold]Priority:[/bold] {priority_text}")

        if task.due_date:
            due_str = task.due_date.isoformat()
            ui.console.print(f"[bold]Due Date:[/bold] [cyan]{due_str}[/cyan]")

        if task.recurrence != Recurrence.NONE:
            recur_str = f"{get_recurrence_emoji(task.recurrence)} {task.recurrence.value}"
            ui.console.print(f"[bold]Recurrence:[/bold] {recur_str}")

        if task.tags:
            ui.console.print(f"[bold]Tags:[/bold] {', '.join(task.tags)}")

    except ValueError as e:
        ui.display_error(str(e))


def update_task_flow(manager: TaskManager) -> None:
    """
    Handle update task workflow with interactive prompts.
    Uses prompts module for editing priority, due date, and recurrence.

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

    # Show current task details using formatter
    theme = get_current_theme()
    ui.console.print(f"\n[bold {theme.primary}]Current Task Details[/]")
    status_cell = format_status_cell(task.status)
    priority_cell = format_priority_cell(task.priority)
    ui.console.print(f"ID: {task.id} | Status: {status_cell} | Priority: {priority_cell}")
    ui.console.print(f"Title: {task.title}")
    if task.description:
        ui.console.print(f"Description: {task.description}")
    if task.due_date:
        ui.console.print(f"Due Date: {format_due_date_cell(task.due_date)}")
    if task.recurrence != Recurrence.NONE:
        ui.console.print(f"Recurrence: {format_recurrence_cell(task.recurrence)}")
    ui.console.print()

    # Use the edit prompts module
    result = prompts.edit_task_prompts(task)

    # Collect updates
    updates = {}
    if result.get("title"):
        updates["title"] = result["title"]
    if result.get("description"):
        updates["description"] = result["description"]
    if result.get("priority") is not None:
        updates["priority"] = result["priority"]
    if result.get("due_date") is not None:
        updates["due_date"] = result["due_date"]
    if result.get("recurrence") is not None:
        updates["recurrence"] = result["recurrence"]

    if updates:
        try:
            ui.show_progress_bar("Updating task", duration=0.3)
            manager.update_task(task_id, **updates)
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


def filter_search_flow(manager: TaskManager) -> None:
    """
    Handle filter and search workflow.

    Args:
        manager: TaskManager instance
    """
    global _filter_state

    ui.display_header("Filter / Search Tasks")

    while True:
        choice = menu.show_filter_menu()

        if choice is None or choice == "back":
            return

        if choice == "status":
            status_choice = menu.show_status_filter_menu()
            if status_choice and status_choice != "back":
                _filter_state.status = Status(status_choice)
                ui.display_success(f"Filter set: Status = {status_choice.title()}")
            return

        elif choice == "priority":
            priority_choice = menu.show_priority_filter_menu()
            if priority_choice and priority_choice != "back":
                _filter_state.priority = Priority(priority_choice)
                ui.display_success(f"Filter set: Priority = {priority_choice.title()}")
            return

        elif choice == "date":
            date_choice = menu.show_date_range_menu()
            if date_choice and date_choice != "back":
                today = date.today()
                if date_choice == "today":
                    tomorrow = today + timedelta(days=1)
                    _filter_state.date_range = (today, tomorrow)
                elif date_choice == "week":
                    next_week = today + timedelta(days=7)
                    _filter_state.date_range = (today, next_week)
                elif date_choice == "month":
                    next_month = today + timedelta(days=30)
                    _filter_state.date_range = (today, next_month)
                elif date_choice == "overdue":
                    _filter_state.date_range = (date.min, today)
                ui.display_success(f"Filter set: Date = {date_choice.title()}")
            return

        elif choice == "search":
            keyword = menu.prompt_text("Enter search keyword:")
            if keyword and keyword.strip():
                _filter_state.search_keyword = keyword.strip()
                ui.display_success(f"Search: '{keyword}'")
            return

        elif choice == "tags":
            tag_input = menu.prompt_text("Filter by tags (comma-separated):")
            if tag_input and tag_input.strip():
                tags = [t.strip() for t in tag_input.split(',') if t.strip()]
                if tags:
                    _filter_state.tags = tags
                    ui.display_success(f"Filter tags: {', '.join(tags)}")
            return

        elif choice == "clear":
            _filter_state.clear()
            ui.display_success("All filters cleared!")
            return


def sort_tasks_flow() -> None:
    """Handle sort tasks workflow."""
    global _current_sort

    ui.display_header("Sort Tasks")

    while True:
        choice = menu.show_sort_menu()

        if choice is None or choice == "back":
            return

        _current_sort = SortBy(choice)
        ui.display_success(f"Sort: {_current_sort.value.replace('_', ' ').title()}")
        return


def voice_input_flow(manager: TaskManager) -> None:
    """
    Handle voice input workflow for hands-free task creation.

    Args:
        manager: TaskManager instance
    """
    ui.display_header("Voice Input")

    # Check if voice is available
    if not VoiceService.is_available():
        ui.display_warning("Voice input is not available.")
        ui.console.print("\nTo enable voice input, install:")
        ui.console.print("  uv add SpeechRecognition PyAudio")
        ui.console.print("\nNote: PyAudio may require system dependencies.")
        ui.console.print("Alternatively, use keyboard input for all features.")
        return

    try:
        voice_service = VoiceService()
    except ImportError as e:
        ui.display_warning(f"Voice service unavailable: {e}")
        return

    ui.console.print("\n[bold]Voice Task Creation[/bold]")
    ui.console.print("Follow the spoken prompts to create a task.\n")

    try:
        # Start conversation
        voice_service.start_conversation()

        # Collect title
        if not voice_service.state.collected_data.get('title'):
            if not voice_service.collect_title():
                ui.display_info("Voice input cancelled")
                return

        # Collect priority
        if not voice_service.state.collected_data.get('priority'):
            if not voice_service.collect_priority():
                return

        # Collect due date
        if not voice_service.state.collected_data.get('due_date'):
            if not voice_service.collect_due_date(parse_date):
                return

        # Collect recurrence
        if not voice_service.state.collected_data.get('recurrence'):
            if not voice_service.collect_recurrence():
                return

        # Show confirmation
        result = voice_service.show_confirmation()

        if result:
            # Create task
            ui.show_progress_bar("Creating task", duration=0.3)
            task = manager.add_task(
                title=result.get('title', 'Untitled'),
                description="",
                priority=result.get('priority', Priority.NONE),
                due_date=result.get('due_date'),
                recurrence=result.get('recurrence', Recurrence.NONE),
            )
            ui.display_success(f"Task created with voice! ID: {task.id}")
            ui.console.print(f"[bold]Title:[/bold] {task.title}")
            priority_text = f"[{get_priority_style(task.priority)}]{task.priority.value.upper()}[/]"
            ui.console.print(f"[bold]Priority:[/bold] {priority_text}")
            if task.due_date:
                ui.console.print(f"[bold]Due:[/bold] [cyan]{task.due_date.isoformat()}[/cyan]")
        else:
            ui.display_info("Voice task creation cancelled")

    except Exception as e:
        ui.display_error(f"Voice input error: {e}")
        ui.console.print("Falling back to keyboard input...")


def optimize_tasks_flow(manager: TaskManager) -> None:
    """
    Handle task optimization workflow with AI analysis.

    Args:
        manager: TaskManager instance
    """
    ui.display_header("Task Optimization (AI)")

    tasks = manager.get_all_tasks()

    if not tasks:
        ui.display_info("No tasks to optimize. Add some tasks first!")
        return

    ui.console.print(f"\n[bold]Analyzing {len(tasks)} tasks...[/bold]\n")
    ui.show_progress_bar("Running AI optimization", duration=2.0)

    # Create optimizer service
    optimizer = TaskOptimizerService()

    try:
        # Run optimization
        results = optimizer.optimize_tasks(tasks)

        theme = get_current_theme()

        # Display results summary
        ui.console.print(f"\n[bold {theme.primary}]Optimization Results[/bold {theme.primary}]")
        ui.console.print(f"Total suggestions: {results.total_suggestions}\n")

        # Display duplicates
        if results.duplicates:
            ui.console.print(f"[bold {theme.warning}]Duplicate Tasks Detected[/bold {theme.warning}]")
            for dup in results.duplicates:
                panel = Panel(
                    f"[bold]Tasks:[/bold] {', '.join(map(str, dup.task_ids))}\n"
                    f"[bold]Similarity:[/bold] {dup.similarity_score * 100:.0f}%\n"
                    f"[bold]Confidence:[/bold] {dup.confidence * 100:.0f}%\n"
                    f"[bold]Suggestion:[/bold] {dup.suggestion}",
                    title=f"Duplicate Group",
                    border_style=theme.warning
                )
                ui.console.print(panel)
                ui.console.print()

        # Display priority recommendations
        if results.priorities:
            ui.console.print(f"[bold {theme.info}]Priority Recommendations[/bold {theme.info}]")
            priority_table = Table(show_header=True, header_style=f"bold {theme.primary}")
            priority_table.add_column("Task ID", style=theme.muted, width=10)
            priority_table.add_column("Priority", width=12)
            priority_table.add_column("Confidence", width=12)
            priority_table.add_column("Keywords", width=30)

            for priority in results.priorities[:10]:  # Show top 10
                priority_color = theme.error if priority.priority == "high" else theme.warning if priority.priority == "medium" else theme.success
                priority_table.add_row(
                    str(priority.task_id),
                    f"[{priority_color}]{priority.priority.upper()}[/{priority_color}]",
                    f"{priority.confidence * 100:.0f}%",
                    ", ".join(priority.keywords[:3]) if priority.keywords else "none"
                )

            ui.console.print(priority_table)
            ui.console.print()

        # Display time estimates
        if results.time_estimates:
            ui.console.print(f"[bold {theme.info}]Time Estimates[/bold {theme.info}]")
            time_table = Table(show_header=True, header_style=f"bold {theme.primary}")
            time_table.add_column("Task ID", style=theme.muted, width=10)
            time_table.add_column("Estimated Hours", width=20)
            time_table.add_column("Range", width=20)
            time_table.add_column("Confidence", width=12)

            for estimate in results.time_estimates[:10]:  # Show top 10
                time_table.add_row(
                    str(estimate.task_id),
                    f"{estimate.estimated_hours}h",
                    f"{estimate.confidence_interval['min']}h - {estimate.confidence_interval['max']}h",
                    f"{estimate.confidence * 100:.0f}%"
                )

            ui.console.print(time_table)
            ui.console.print()

        # Display task groups
        if results.groups:
            ui.console.print(f"[bold {theme.success}]Task Grouping Suggestions[/bold {theme.success}]")
            for group in results.groups:
                panel = Panel(
                    f"[bold]Category:[/bold] {group.category}\n"
                    f"[bold]Tasks:[/bold] {len(group.task_ids)} tasks\n"
                    f"[bold]Confidence:[/bold] {group.confidence * 100:.0f}%\n"
                    f"[bold]Reasoning:[/bold] {group.reasoning}",
                    title=f"{group.name}",
                    border_style=theme.success
                )
                ui.console.print(panel)
                ui.console.print()

        # Display automation opportunities
        if results.automations:
            ui.console.print(f"[bold {theme.primary}]Automation Opportunities[/bold {theme.primary}]")
            for auto in results.automations:
                panel = Panel(
                    f"[bold]Type:[/bold] {auto.automation_type}\n"
                    f"[bold]Tasks:[/bold] {len(auto.task_ids)} task(s)\n"
                    f"[bold]Confidence:[/bold] {auto.confidence * 100:.0f}%\n"
                    f"[bold]Suggestion:[/bold] {auto.suggestion}\n"
                    f"[bold]Implementation:[/bold] {auto.implementation}",
                    title=f"Automation Opportunity",
                    border_style=theme.primary
                )
                ui.console.print(panel)
                ui.console.print()

        if results.total_suggestions == 0:
            ui.display_info("No optimization suggestions found. Your tasks are already well-organized!")

    except Exception as e:
        ui.display_error(f"Optimization failed: {e}")


def main() -> None:
    """Main application loop with enhanced UI and persistence."""
    # Initialize task manager with auto-load
    manager = TaskManager()

    # Display welcome screen
    ui.clear_screen()
    ui.display_ascii_title()

    # Show persistence status
    if manager._loaded_from_file:
        task_count = len(manager.tasks)
        ui.display_info(f"Loaded {task_count} task{'s' if task_count != 1 else ''} from {manager.data_file}")
    else:
        ui.display_info(f"Starting with empty task list. Tasks will be saved to {manager.data_file}")

    while True:
        try:
            stats = manager.get_task_stats()
            ui.display_welcome_panel(stats)

            choice = menu.show_main_menu()
            
            # Handle None (user cancelled or interrupted)
            if choice is None:
                ui.console.print("\n")
                ui.display_info("Operation cancelled")
                continue

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
                filter_search_flow(manager)

            elif choice == "7":
                sort_tasks_flow()

            elif choice == "8":
                voice_input_flow(manager)

            elif choice == "9":
                change_theme_flow()

            elif choice == "0":
                # Save before exit
                try:
                    manager.save_to_json()
                    task_count = len(manager.tasks)
                    ui.display_success(f"Saved {task_count} task{'s' if task_count != 1 else ''} to {manager.data_file}")
                except Exception as e:
                    ui.display_error(f"Error saving tasks: {e}")

                ui.display_success("Thank you for using Todo Application!")
                ui.console.print("[bold]Goodbye![/bold]\n")
                break

            else:
                ui.display_error("Invalid choice. Please try again.")

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            ui.console.print("\n")
            try:
                manager.save_to_json()
                task_count = len(manager.tasks)
                ui.display_info(f"Saved {task_count} task{'s' if task_count != 1 else ''} to {manager.data_file}")
            except Exception as e:
                ui.display_error(f"Error saving tasks: {e}")

            ui.display_success("Application interrupted. Goodbye!")
            break

        except Exception as e:
            ui.display_error(f"Unexpected error: {e}")
            ui.console.print("Please try again.")


if __name__ == "__main__":
    main()
