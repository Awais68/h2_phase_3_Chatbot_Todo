"""
MCP Tools for Todo AI Chatbot.
Implements all task management, recurring tasks, and analytics tools.
Extended for 012-advanced-todo-features with due dates and recurrence.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlmodel import Session, select, func
from src.mcp.server import mcp_server
from src.models import Task, RecurringTask
from src.models.task import TaskCreate
from src.db.session import get_session
from src.services.task_service import TaskService


# ============================================================================
# BASIC TASK TOOLS
# ============================================================================

@mcp_server.tool("add_task")
def add_task(user_id: int, title: str, description: str = "", session: Session = None) -> Dict[str, Any]:
    """
    Create a new task for the user.

    Args:
        user_id: The ID of the user creating the task
        title: The task title (required, 1-200 characters)
        description: Optional task description (max 1000 characters)
        session: Database session

    Returns:
        Dict with task_id, status, and title
    """
    if not session:
        session = next(get_session())

    # Validate
    if not title or len(title) < 1 or len(title) > 200:
        return {"error": "INVALID_TITLE", "message": "Title must be between 1 and 200 characters"}

    if len(description) > 1000:
        return {"error": "INVALID_DESCRIPTION", "message": "Description cannot exceed 1000 characters"}

    # Create task
    task = Task(
        user_id=user_id,
        title=title.strip(),
        description=description.strip(),
        status='pending'  # Use status instead of completed
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "task_id": task.id,
        "status": "pending",
        "title": task.title
    }


@mcp_server.tool("add_task_with_due_date")
def add_task_with_due_date(
    user_id: int,
    title: str,
    description: str = "",
    due_date_text: Optional[str] = None,
    user_timezone: str = "UTC",
    recurrence_pattern: Optional[str] = None,
    reminder_minutes: int = 15,
    session: Session = None
) -> Dict[str, Any]:
    """
    Create a new task with optional due date and recurrence pattern.

    Args:
        user_id: The ID of the user creating the task
        title: The task title (required, 1-200 characters)
        description: Optional task description (max 1000 characters)
        due_date_text: Natural language due date (e.g., "tomorrow at 3pm", "next Friday")
        user_timezone: User's timezone for date parsing (default: UTC)
        recurrence_pattern: Recurrence type (daily/weekly/bi-weekly/monthly/yearly)
        reminder_minutes: Minutes before due date to send reminder (default: 15)
        session: Database session

    Returns:
        Dict with task details including due_date, recurrence info

    Examples:
        >>> add_task_with_due_date(1, "Buy groceries", due_date_text="tomorrow at 3pm")
        >>> add_task_with_due_date(1, "Team meeting", due_date_text="every Monday at 9am", recurrence_pattern="weekly")
    """
    if not session:
        session = next(get_session())

    # Validate
    if not title or len(title) < 1 or len(title) > 200:
        return {"error": "INVALID_TITLE", "message": "Title must be between 1 and 200 characters"}

    if len(description) > 1000:
        return {"error": "INVALID_DESCRIPTION", "message": "Description cannot exceed 1000 characters"}

    # Create task data
    task_data = TaskCreate(
        title=title.strip(),
        description=description.strip()
    )

    try:
        # Use TaskService to create task with due date and recurrence
        task = TaskService.create_task(
            session=session,
            user_id=user_id,
            task_data=task_data,
            due_date_text=due_date_text,
            user_timezone=user_timezone,
            recurrence_pattern=recurrence_pattern,
            reminder_minutes=reminder_minutes
        )

        response = {
            "task_id": task.id,
            "status": "created",
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat()
        }

        # Add due date info if present
        if task.due_date:
            response["due_date"] = task.due_date.isoformat()
            response["reminder_minutes"] = task.reminder_minutes

        # Add recurrence info if present
        if task.is_recurring:
            response["is_recurring"] = True
            response["recurrence_pattern"] = task.recurrence_pattern
            response["next_occurrence"] = task.next_occurrence.isoformat() if task.next_occurrence else None

        return response

    except ValueError as e:
        return {"error": "VALIDATION_ERROR", "message": str(e)}
    except Exception as e:
        return {"error": "CREATION_FAILED", "message": f"Failed to create task: {str(e)}"}


@mcp_server.tool("update_task_due_date")
def update_task_due_date(
    user_id: int,
    task_id: int,
    due_date_text: Optional[str] = None,
    user_timezone: str = "UTC",
    reminder_minutes: int = 15,
    session: Session = None
) -> Dict[str, Any]:
    """
    Update the due date of an existing task.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        due_date_text: Natural language due date (e.g., "tomorrow at 3pm", "next Friday", None to clear)
        user_timezone: User's timezone for date parsing (default: UTC)
        reminder_minutes: Minutes before due date to send reminder (default: 15)
        session: Database session

    Returns:
        Dict with task details including updated due_date

    Examples:
        >>> update_task_due_date(1, 5, due_date_text="next Monday at 2pm")
        >>> update_task_due_date(1, 5, due_date_text=None)  # Clear due date
    """
    if not session:
        session = next(get_session())

    # Find task
    task = session.get(Task, task_id)

    if not task or task.user_id != user_id:
        return {"error": "TASK_NOT_FOUND", "message": f"Task with ID {task_id} not found"}

    try:
        # Update due date
        if due_date_text:
            # For now, store the text as-is since date parsing utilities may not be available yet
            # TODO: Integrate DateTimeParser when available
            # For basic implementation, try to parse ISO format
            try:
                from dateutil import parser
                task.due_date = parser.parse(due_date_text)
                task.reminder_minutes = reminder_minutes
            except:
                return {"error": "INVALID_DATE", "message": f"Unable to parse date: {due_date_text}. Please use ISO format (e.g., '2026-02-10T15:00:00')"}
        else:
            # Clear due date
            task.due_date = None
            task.reminder_minutes = None

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        response = {
            "task_id": task.id,
            "status": "updated",
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "updated_at": task.updated_at.isoformat()
        }

        # Add due date info if present
        if task.due_date:
            response["due_date"] = task.due_date.isoformat()
            response["reminder_minutes"] = task.reminder_minutes
        else:
            response["due_date"] = None
            response["message"] = "Due date cleared"

        return response

    except Exception as e:
        return {"error": "UPDATE_FAILED", "message": f"Failed to update task due date: {str(e)}"}


@mcp_server.tool("list_tasks")
def list_tasks(user_id: int, status: str = "all", session: Session = None) -> Dict[str, Any]:
    """
    Retrieve the user's tasks, optionally filtered by completion status.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        status: Filter by status ('all', 'pending', 'completed')
        session: Database session

    Returns:
        Dict with tasks array and count
    """
    if not session:
        session = next(get_session())

    # Build query
    query = select(Task).where(Task.user_id == user_id)

    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    tasks = session.exec(query.order_by(Task.created_at.desc())).all()

    # Format tasks
    task_list = []
    for task in tasks:
        task_list.append({
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        })

    return {
        "tasks": task_list,
        "count": len(task_list)
    }


@mcp_server.tool("list_tasks_by_due_date")
def list_tasks_by_due_date(
    user_id: int,
    filter_type: str = "all",
    session: Session = None
) -> Dict[str, Any]:
    """
    Retrieve the user's tasks filtered by due date status.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        filter_type: Filter type ('all', 'overdue', 'due_today', 'due_this_week', 'no_due_date')
        session: Database session

    Returns:
        Dict with tasks array, count, and filter info

    Examples:
        >>> list_tasks_by_due_date(1, filter_type="overdue")
        >>> list_tasks_by_due_date(1, filter_type="due_today")
        >>> list_tasks_by_due_date(1, filter_type="due_this_week")
    """
    if not session:
        session = next(get_session())

    # Validate filter type
    valid_filters = ["all", "overdue", "due_today", "due_this_week", "no_due_date"]
    if filter_type not in valid_filters:
        return {
            "error": "INVALID_FILTER",
            "message": f"Filter type must be one of: {', '.join(valid_filters)}"
        }

    # Get current time
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    week_end = today_start + timedelta(days=7)

    # Build base query for pending tasks only
    query = select(Task).where(
        Task.user_id == user_id,
        Task.completed == False
    )

    # Apply filter
    if filter_type == "overdue":
        query = query.where(
            Task.due_date.isnot(None),
            Task.due_date < now
        )
    elif filter_type == "due_today":
        query = query.where(
            Task.due_date.isnot(None),
            Task.due_date >= today_start,
            Task.due_date <= today_end
        )
    elif filter_type == "due_this_week":
        query = query.where(
            Task.due_date.isnot(None),
            Task.due_date >= now,
            Task.due_date <= week_end
        )
    elif filter_type == "no_due_date":
        query = query.where(Task.due_date.is_(None))
    elif filter_type == "all":
        # Include all tasks with or without due dates
        pass

    # Order by due date (nulls last)
    tasks = session.exec(query.order_by(Task.due_date.asc().nullslast())).all()

    # Format tasks
    task_list = []
    for task in tasks:
        task_dict = {
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }

        # Add due date info if present
        if task.due_date:
            task_dict["due_date"] = task.due_date.isoformat()
            task_dict["reminder_minutes"] = task.reminder_minutes

            # Calculate due date status
            if task.due_date < now:
                task_dict["due_status"] = "overdue"
            elif today_start <= task.due_date <= today_end:
                task_dict["due_status"] = "due_today"
            elif task.due_date <= week_end:
                task_dict["due_status"] = "due_this_week"
            else:
                task_dict["due_status"] = "upcoming"
        else:
            task_dict["due_date"] = None
            task_dict["due_status"] = "no_due_date"

        # Add recurrence info if present
        if task.is_recurring:
            task_dict["is_recurring"] = True
            task_dict["recurrence_pattern"] = str(task.recurrence_pattern) if task.recurrence_pattern else None
            task_dict["next_occurrence"] = task.next_occurrence.isoformat() if task.next_occurrence else None

        task_list.append(task_dict)

    return {
        "tasks": task_list,
        "count": len(task_list),
        "filter": filter_type,
        "timestamp": now.isoformat()
    }


@mcp_server.tool("complete_task")
def complete_task(user_id: int, task_id: int, session: Session = None) -> Dict[str, Any]:
    """
    Mark a task as complete.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to mark as complete
        session: Database session

    Returns:
        Dict with task_id, status, and title
    """
    if not session:
        session = next(get_session())

    # Find task
    task = session.get(Task, task_id)

    if not task or task.user_id != user_id:
        return {"error": "TASK_NOT_FOUND", "message": f"Task with ID {task_id} not found"}

    if task.completed:
        return {"error": "ALREADY_COMPLETED", "message": "Task is already marked as completed"}

    # Update task
    task.completed = True
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()

    return {
        "task_id": task.id,
        "status": "completed",
        "title": task.title
    }


@mcp_server.tool("delete_task")
def delete_task(user_id: int, task_id: int, session: Session = None) -> Dict[str, Any]:
    """
    Delete a task permanently.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to delete
        session: Database session

    Returns:
        Dict with task_id, status, and title
    """
    if not session:
        session = next(get_session())

    # Find task
    task = session.get(Task, task_id)

    if not task or task.user_id != user_id:
        return {"error": "TASK_NOT_FOUND", "message": f"Task with ID {task_id} not found"}

    title = task.title
    session.delete(task)
    session.commit()

    return {
        "task_id": task_id,
        "status": "deleted",
        "title": title
    }


@mcp_server.tool("update_task")
def update_task(user_id: int, task_id: int, title: str = None, description: str = None, session: Session = None) -> Dict[str, Any]:
    """
    Update a task's title or description.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        title: New task title (optional)
        description: New task description (optional)
        session: Database session

    Returns:
        Dict with task_id, status, title, and description
    """
    if not session:
        session = next(get_session())

    # Find task
    task = session.get(Task, task_id)

    if not task or task.user_id != user_id:
        return {"error": "TASK_NOT_FOUND", "message": f"Task with ID {task_id} not found"}

    if not title and not description:
        return {"error": "NO_CHANGES", "message": "No changes provided - specify title or description to update"}

    # Update fields
    if title:
        if len(title) < 1 or len(title) > 200:
            return {"error": "INVALID_TITLE", "message": "Title must be between 1 and 200 characters"}
        task.title = title.strip()

    if description is not None:
        if len(description) > 1000:
            return {"error": "INVALID_DESCRIPTION", "message": "Description cannot exceed 1000 characters"}
        task.description = description.strip()

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "task_id": task.id,
        "status": "updated",
        "title": task.title,
        "description": task.description
    }


# ============================================================================
# RECURRING TASK TOOLS
# ============================================================================

@mcp_server.tool("create_recurring_task")
def create_recurring_task(user_id: int, title: str, description: str = "", frequency: str = "daily", frequency_value: int = None, session: Session = None) -> Dict[str, Any]:
    """
    Create a new recurring task.

    Args:
        user_id: The ID of the user creating the recurring task
        title: The task title
        description: Optional task description
        frequency: Recurrence frequency ('daily', 'weekly', 'monthly')
        frequency_value: Optional frequency value (day of week for weekly, day of month for monthly)
        session: Database session

    Returns:
        Dict with recurring_task_id, status, and title
    """
    if not session:
        session = next(get_session())

    # Validate
    if frequency not in ['daily', 'weekly', 'monthly']:
        return {"error": "INVALID_FREQUENCY", "message": "Frequency must be 'daily', 'weekly', or 'monthly'"}

    # Create recurring task
    recurring_task = RecurringTask(
        user_id=user_id,
        title=title.strip(),
        description=description.strip(),
        frequency=frequency,
        frequency_value=frequency_value,
        is_active=True
    )

    session.add(recurring_task)
    session.commit()
    session.refresh(recurring_task)

    return {
        "recurring_task_id": recurring_task.id,
        "status": "created",
        "title": recurring_task.title,
        "frequency": recurring_task.frequency
    }


@mcp_server.tool("list_recurring_tasks")
def list_recurring_tasks(user_id: int, session: Session = None) -> Dict[str, Any]:
    """
    List all recurring tasks for a user.

    Args:
        user_id: The ID of the user
        session: Database session

    Returns:
        Dict with recurring_tasks array and count
    """
    if not session:
        session = next(get_session())

    query = select(RecurringTask).where(RecurringTask.user_id == user_id)
    recurring_tasks = session.exec(query.order_by(RecurringTask.created_at.desc())).all()

    task_list = []
    for task in recurring_tasks:
        task_list.append({
            "recurring_task_id": task.id,
            "title": task.title,
            "description": task.description,
            "frequency": task.frequency,
            "frequency_value": task.frequency_value,
            "is_active": task.is_active,
            "last_generated": task.last_generated.isoformat() if task.last_generated else None,
            "created_at": task.created_at.isoformat()
        })

    return {
        "recurring_tasks": task_list,
        "count": len(task_list)
    }


@mcp_server.tool("pause_recurring_task")
def pause_recurring_task(user_id: int, recurring_task_id: int, session: Session = None) -> Dict[str, Any]:
    """
    Pause a recurring task.

    Args:
        user_id: The ID of the user
        recurring_task_id: The ID of the recurring task to pause
        session: Database session

    Returns:
        Dict with status
    """
    if not session:
        session = next(get_session())

    task = session.get(RecurringTask, recurring_task_id)

    if not task or task.user_id != user_id:
        return {"error": "NOT_FOUND", "message": "Recurring task not found"}

    task.is_active = False
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()

    return {"status": "paused", "recurring_task_id": recurring_task_id}


@mcp_server.tool("resume_recurring_task")
def resume_recurring_task(user_id: int, recurring_task_id: int, session: Session = None) -> Dict[str, Any]:
    """
    Resume a paused recurring task.

    Args:
        user_id: The ID of the user
        recurring_task_id: The ID of the recurring task to resume
        session: Database session

    Returns:
        Dict with status
    """
    if not session:
        session = next(get_session())

    task = session.get(RecurringTask, recurring_task_id)

    if not task or task.user_id != user_id:
        return {"error": "NOT_FOUND", "message": "Recurring task not found"}

    task.is_active = True
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()

    return {"status": "resumed", "recurring_task_id": recurring_task_id}


@mcp_server.tool("delete_recurring_task")
def delete_recurring_task(user_id: int, recurring_task_id: int, session: Session = None) -> Dict[str, Any]:
    """
    Delete a recurring task.

    Args:
        user_id: The ID of the user
        recurring_task_id: The ID of the recurring task to delete
        session: Database session

    Returns:
        Dict with status
    """
    if not session:
        session = next(get_session())

    task = session.get(RecurringTask, recurring_task_id)

    if not task or task.user_id != user_id:
        return {"error": "NOT_FOUND", "message": "Recurring task not found"}

    session.delete(task)
    session.commit()

    return {"status": "deleted", "recurring_task_id": recurring_task_id}


# ============================================================================
# ANALYTICS TOOLS
# ============================================================================

@mcp_server.tool("get_task_statistics")
def get_task_statistics(user_id: int, session: Session = None) -> Dict[str, Any]:
    """
    Get overall task statistics for a user.

    Args:
        user_id: The ID of the user
        session: Database session

    Returns:
        Dict with statistics (total, completed, pending, completion_rate)
    """
    if not session:
        session = next(get_session())

    # Count tasks
    total_query = select(func.count(Task.id)).where(Task.user_id == user_id)
    total = session.exec(total_query).one()

    completed_query = select(func.count(Task.id)).where(Task.user_id == user_id, Task.completed == True)
    completed = session.exec(completed_query).one()

    pending = total - completed
    completion_rate = (completed / total * 100) if total > 0 else 0

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "completion_rate": round(completion_rate, 2)
    }


@mcp_server.tool("get_tasks_over_time")
def get_tasks_over_time(user_id: int, days: int = 30, session: Session = None) -> Dict[str, Any]:
    """
    Get task creation and completion trends over time.

    Args:
        user_id: The ID of the user
        days: Number of days to look back (default 30)
        session: Database session

    Returns:
        Dict with daily task data
    """
    if not session:
        session = next(get_session())

    # Get tasks from last N days
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = select(Task).where(Task.user_id == user_id, Task.created_at >= cutoff_date)
    tasks = session.exec(query).all()

    # Group by date
    daily_data = {}
    for task in tasks:
        date_key = task.created_at.date().isoformat()
        if date_key not in daily_data:
            daily_data[date_key] = {"created": 0, "completed": 0}

        daily_data[date_key]["created"] += 1
        if task.completed:
            daily_data[date_key]["completed"] += 1

    # Convert to list
    timeline = [{"date": date, **data} for date, data in sorted(daily_data.items())]

    return {
        "timeline": timeline,
        "days": days
    }


@mcp_server.tool("get_completion_analytics")
def get_completion_analytics(user_id: int, session: Session = None) -> Dict[str, Any]:
    """
    Get detailed completion analytics.

    Args:
        user_id: The ID of the user
        session: Database session

    Returns:
        Dict with completion analytics
    """
    if not session:
        session = next(get_session())

    # Get all tasks
    query = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(query).all()

    if not tasks:
        return {
            "total": 0,
            "completed": 0,
            "pending": 0,
            "completion_rate": 0,
            "avg_completion_time_hours": 0
        }

    completed_tasks = [t for t in tasks if t.completed]
    pending_tasks = [t for t in tasks if not t.completed]

    # Calculate average completion time
    completion_times = []
    for task in completed_tasks:
        time_diff = (task.updated_at - task.created_at).total_seconds() / 3600  # hours
        completion_times.append(time_diff)

    avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0

    return {
        "total": len(tasks),
        "completed": len(completed_tasks),
        "pending": len(pending_tasks),
        "completion_rate": round(len(completed_tasks) / len(tasks) * 100, 2),
        "avg_completion_time_hours": round(avg_completion_time, 2)
    }


@mcp_server.tool("get_productivity_hours")
def get_productivity_hours(user_id: int, session: Session = None) -> Dict[str, Any]:
    """
    Get productivity statistics by hour of day.

    Args:
        user_id: The ID of the user
        session: Database session

    Returns:
        Dict with hourly productivity data
    """
    if not session:
        session = next(get_session())

    # Get all completed tasks
    query = select(Task).where(Task.user_id == user_id, Task.completed == True)
    tasks = session.exec(query).all()

    # Group by hour
    hourly_data = {hour: 0 for hour in range(24)}
    for task in tasks:
        hour = task.updated_at.hour
        hourly_data[hour] += 1

    # Convert to list
    productivity = [{"hour": hour, "tasks_completed": count} for hour, count in sorted(hourly_data.items())]

    return {
        "productivity_by_hour": productivity
    }
