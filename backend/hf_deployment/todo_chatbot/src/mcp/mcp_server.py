"""
Official MCP Server using Model Context Protocol SDK.
Exposes task management tools via MCP protocol for AI chatbot integration.
"""
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlmodel import Session, select, func
from src.models.task import Task
from src.models.recurring_task import RecurringTask
from src.db.session import get_session

# Initialize MCP server with official SDK
mcp = FastMCP("Todo Task Manager")

# ============================================================================
# BASIC TASK TOOLS
# ============================================================================

@mcp.tool()
def add_task_with_due_date(user_id: int, title: str, due_date: str, description: str = "", timezone: str = "UTC") -> Dict[str, Any]:
    """
    Create a new task with a due date for the user.

    Args:
        user_id: The ID of the user creating the task
        title: The task title (required, 1-200 characters)
        due_date: Due date in ISO format (YYYY-MM-DDTHH:MM:SS) or natural language (e.g., "tomorrow", "next Monday")
        description: Optional task description (max 1000 characters)
        timezone: User's timezone for interpreting the due date (default: UTC)

    Returns:
        Dict with task_id, status, and title
    """
    session = next(get_session())

    # Validate
    if not title or len(title) < 1 or len(title) > 200:
        return {"error": "INVALID_TITLE", "message": "Title must be between 1 and 200 characters"}

    if len(description) > 1000:
        return {"error": "INVALID_DESCRIPTION", "message": "Description cannot exceed 1000 characters"}

    # Try to parse the due date
    from src.utils.datetime_parser import DateTimeParser
    parser = DateTimeParser()
    parsed_due_date = parser.parse(due_date, user_timezone=timezone)

    if not parsed_due_date:
        return {"error": "INVALID_DUE_DATE", "message": f"Could not parse due date: {due_date}"}

    # Create task with due date
    from datetime import datetime
    task = Task(
        user_id=user_id,
        title=title.strip(),
        description=description.strip(),
        completed=False,
        due_date=parsed_due_date
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "task_id": task.id,
        "status": "created",
        "title": task.title,
        "due_date": parsed_due_date.isoformat()
    }


@mcp.tool()
def add_task(user_id: int, title: str, description: str = "") -> Dict[str, Any]:
    """
    Create a new task for the user.
    
    Args:
        user_id: The ID of the user creating the task
        title: The task title (required, 1-200 characters)
        description: Optional task description (max 1000 characters)
    
    Returns:
        Dict with task_id, status, and title
    """
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
        completed=False
    )
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return {
        "task_id": task.id,
        "status": "created",
        "title": task.title
    }


@mcp.tool()
def list_tasks(user_id: int, status: str = "all") -> Dict[str, Any]:
    """
    Retrieve the user's tasks, optionally filtered by completion status.
    
    Args:
        user_id: The ID of the user whose tasks to retrieve
        status: Filter by status ('all', 'pending', 'completed')
    
    Returns:
        Dict with tasks array and count
    """
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


@mcp.tool()
def complete_task(user_id: int, task_id: int) -> Dict[str, Any]:
    """
    Mark a task as completed.
    
    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to complete
    
    Returns:
        Dict with success status and task details
    """
    session = next(get_session())
    
    # Get task
    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(query).first()
    
    if not task:
        return {"error": "TASK_NOT_FOUND", "message": f"Task {task_id} not found or doesn't belong to user"}
    
    if task.completed:
        return {"error": "ALREADY_COMPLETED", "message": "Task is already completed"}
    
    # Mark as completed
    task.completed = True
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return {
        "task_id": task.id,
        "status": "completed",
        "title": task.title,
        "completed_at": task.updated_at.isoformat()
    }


@mcp.tool()
def delete_task(user_id: int, task_id: int) -> Dict[str, Any]:
    """
    Delete a task.
    
    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to delete
    
    Returns:
        Dict with success status
    """
    session = next(get_session())
    
    # Get task
    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(query).first()
    
    if not task:
        return {"error": "TASK_NOT_FOUND", "message": f"Task {task_id} not found or doesn't belong to user"}
    
    # Delete task
    session.delete(task)
    session.commit()
    
    return {
        "task_id": task_id,
        "status": "deleted",
        "title": task.title
    }


@mcp.tool()
def update_task(user_id: int, task_id: int, title: Optional[str] = None, 
                description: Optional[str] = None, completed: Optional[bool] = None) -> Dict[str, Any]:
    """
    Update a task's details.
    
    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        title: New title (optional)
        description: New description (optional)
        completed: New completion status (optional)
    
    Returns:
        Dict with updated task details
    """
    session = next(get_session())
    
    # Get task
    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(query).first()
    
    if not task:
        return {"error": "TASK_NOT_FOUND", "message": f"Task {task_id} not found or doesn't belong to user"}
    
    # Update fields
    if title is not None:
        if len(title) < 1 or len(title) > 200:
            return {"error": "INVALID_TITLE", "message": "Title must be between 1 and 200 characters"}
        task.title = title.strip()
    
    if description is not None:
        if len(description) > 1000:
            return {"error": "INVALID_DESCRIPTION", "message": "Description cannot exceed 1000 characters"}
        task.description = description.strip()
    
    if completed is not None:
        task.completed = completed
    
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return {
        "task_id": task.id,
        "status": "updated",
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }


@mcp.tool()
def update_task_due_date(user_id: int, task_id: int, due_date: str, timezone: str = "UTC") -> Dict[str, Any]:
    """
    Update a task's due date.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        due_date: New due date in ISO format (YYYY-MM-DDTHH:MM:SS) or natural language (e.g., "tomorrow", "next Monday")
        timezone: User's timezone for interpreting the due date (default: UTC)

    Returns:
        Dict with updated task details
    """
    from datetime import datetime
    session = next(get_session())

    # Get task
    from sqlmodel import select
    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(query).first()

    if not task:
        return {"error": "TASK_NOT_FOUND", "message": f"Task {task_id} not found or doesn't belong to user"}

    # Try to parse the due date
    from src.utils.datetime_parser import DateTimeParser
    parser = DateTimeParser()
    parsed_due_date = parser.parse(due_date, user_timezone=timezone)

    if not parsed_due_date:
        return {"error": "INVALID_DUE_DATE", "message": f"Could not parse due date: {due_date}"}

    # Update due date
    task.due_date = parsed_due_date
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "task_id": task.id,
        "status": "due_date_updated",
        "title": task.title,
        "due_date": parsed_due_date.isoformat()
    }


# ============================================================================
# DUE DATE RELATED TOOLS
# ============================================================================

@mcp.tool()
def list_tasks_by_due_date(user_id: int, filter_type: str = "all") -> Dict[str, Any]:
    """
    Retrieve the user's tasks, optionally filtered by due date status.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        filter_type: Filter by due date status ('all', 'overdue', 'today', 'this_week', 'no_due_date')

    Returns:
        Dict with tasks array and count
    """
    session = next(get_session())
    from datetime import datetime, date
    from sqlalchemy import and_, or_

    # Build query
    query = select(Task).where(Task.user_id == user_id)

    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())
    week_start = datetime.combine(date.today(), datetime.min.time()) - timedelta(days=date.today().weekday())
    week_end = week_start + timedelta(days=7)

    if filter_type == "overdue":
        query = query.where(and_(Task.due_date != None, Task.due_date < datetime.utcnow(), Task.completed == False))
    elif filter_type == "today":
        query = query.where(and_(Task.due_date != None,
                                Task.due_date >= today_start,
                                Task.due_date <= today_end,
                                Task.completed == False))
    elif filter_type == "this_week":
        query = query.where(and_(Task.due_date != None,
                                Task.due_date >= week_start,
                                Task.due_date <= week_end,
                                Task.completed == False))
    elif filter_type == "no_due_date":
        query = query.where(or_(Task.due_date == None, Task.due_date == ""))
    # For "all", we don't add any additional filters

    tasks = session.exec(query.order_by(Task.due_date.asc(), Task.created_at.desc())).all()

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
        if task.due_date:
            task_dict["due_date"] = task.due_date.isoformat()
        task_list.append(task_dict)

    return {
        "tasks": task_list,
        "count": len(task_list),
        "filter_type": filter_type
    }


# ============================================================================
# RECURRING TASK TOOLS
# ============================================================================

@mcp.tool()
def create_recurring_task(user_id: int, title: str, description: str = "",
                         frequency: str = "daily", start_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new recurring task.
    
    Args:
        user_id: The ID of the user creating the task
        title: The task title
        description: Task description
        frequency: Recurrence frequency ('daily', 'weekly', 'monthly')
        start_date: Start date in ISO format (defaults to today)
    
    Returns:
        Dict with recurring_task_id and details
    """
    session = next(get_session())
    
    # Validate frequency
    valid_frequencies = ['daily', 'weekly', 'monthly']
    if frequency not in valid_frequencies:
        return {"error": "INVALID_FREQUENCY", "message": f"Frequency must be one of: {', '.join(valid_frequencies)}"}
    
    # Parse start date
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
        except ValueError:
            return {"error": "INVALID_DATE", "message": "start_date must be in ISO format"}
    else:
        start_dt = datetime.utcnow()
    
    # Create recurring task
    recurring_task = RecurringTask(
        user_id=user_id,
        title=title.strip(),
        description=description.strip(),
        frequency=frequency,
        next_occurrence=start_dt,
        is_active=True
    )
    
    session.add(recurring_task)
    session.commit()
    session.refresh(recurring_task)
    
    return {
        "recurring_task_id": recurring_task.id,
        "status": "created",
        "title": recurring_task.title,
        "frequency": recurring_task.frequency,
        "next_occurrence": recurring_task.next_occurrence.isoformat()
    }


@mcp.tool()
def list_recurring_tasks(user_id: int, active_only: bool = True) -> Dict[str, Any]:
    """
    List all recurring tasks for a user.
    
    Args:
        user_id: The ID of the user
        active_only: If True, only return active recurring tasks
    
    Returns:
        Dict with recurring tasks array and count
    """
    session = next(get_session())
    
    query = select(RecurringTask).where(RecurringTask.user_id == user_id)
    
    if active_only:
        query = query.where(RecurringTask.is_active == True)
    
    tasks = session.exec(query.order_by(RecurringTask.created_at.desc())).all()
    
    task_list = []
    for task in tasks:
        task_list.append({
            "recurring_task_id": task.id,
            "title": task.title,
            "description": task.description,
            "frequency": task.frequency,
            "next_occurrence": task.next_occurrence.isoformat() if task.next_occurrence else None,
            "is_active": task.is_active,
            "created_at": task.created_at.isoformat()
        })
    
    return {
        "recurring_tasks": task_list,
        "count": len(task_list)
    }


@mcp.tool()
def pause_recurring_task(user_id: int, recurring_task_id: int) -> Dict[str, Any]:
    """
    Pause a recurring task.
    
    Args:
        user_id: The ID of the user
        recurring_task_id: The ID of the recurring task to pause
    
    Returns:
        Dict with success status
    """
    session = next(get_session())
    
    query = select(RecurringTask).where(
        RecurringTask.id == recurring_task_id,
        RecurringTask.user_id == user_id
    )
    task = session.exec(query).first()
    
    if not task:
        return {"error": "TASK_NOT_FOUND", "message": "Recurring task not found"}
    
    task.is_active = False
    session.add(task)
    session.commit()
    
    return {
        "recurring_task_id": task.id,
        "status": "paused",
        "title": task.title
    }


@mcp.tool()
def resume_recurring_task(user_id: int, recurring_task_id: int) -> Dict[str, Any]:
    """
    Resume a paused recurring task.
    
    Args:
        user_id: The ID of the user
        recurring_task_id: The ID of the recurring task to resume
    
    Returns:
        Dict with success status
    """
    session = next(get_session())
    
    query = select(RecurringTask).where(
        RecurringTask.id == recurring_task_id,
        RecurringTask.user_id == user_id
    )
    task = session.exec(query).first()
    
    if not task:
        return {"error": "TASK_NOT_FOUND", "message": "Recurring task not found"}
    
    task.is_active = True
    session.add(task)
    session.commit()
    
    return {
        "recurring_task_id": task.id,
        "status": "resumed",
        "title": task.title
    }


@mcp.tool()
def delete_recurring_task(user_id: int, recurring_task_id: int) -> Dict[str, Any]:
    """
    Delete a recurring task.
    
    Args:
        user_id: The ID of the user
        recurring_task_id: The ID of the recurring task to delete
    
    Returns:
        Dict with success status
    """
    session = next(get_session())
    
    query = select(RecurringTask).where(
        RecurringTask.id == recurring_task_id,
        RecurringTask.user_id == user_id
    )
    task = session.exec(query).first()
    
    if not task:
        return {"error": "TASK_NOT_FOUND", "message": "Recurring task not found"}
    
    session.delete(task)
    session.commit()
    
    return {
        "recurring_task_id": recurring_task_id,
        "status": "deleted"
    }


# ============================================================================
# ANALYTICS TOOLS
# ============================================================================

@mcp.tool()
def get_task_statistics(user_id: int) -> Dict[str, Any]:
    """
    Get task statistics for a user.
    
    Args:
        user_id: The ID of the user
    
    Returns:
        Dict with task statistics
    """
    session = next(get_session())
    
    # Total tasks
    total = session.exec(select(func.count(Task.id)).where(Task.user_id == user_id)).one()
    
    # Completed tasks
    completed = session.exec(
        select(func.count(Task.id)).where(Task.user_id == user_id, Task.completed == True)
    ).one()
    
    # Pending tasks
    pending = total - completed
    
    # Completion rate
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "completion_rate": round(completion_rate, 2)
    }


@mcp.tool()
def get_tasks_over_time(user_id: int, days: int = 30) -> Dict[str, Any]:
    """
    Get task creation trend over time.
    
    Args:
        user_id: The ID of the user
        days: Number of days to analyze (default 30)
    
    Returns:
        Dict with daily task counts
    """
    session = next(get_session())
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get tasks in date range
    query = select(Task).where(
        Task.user_id == user_id,
        Task.created_at >= start_date
    )
    tasks = session.exec(query).all()
    
    # Group by date
    daily_counts = {}
    for task in tasks:
        date_key = task.created_at.date().isoformat()
        daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
    
    return {
        "period_days": days,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily_counts": daily_counts,
        "total_in_period": len(tasks)
    }


@mcp.tool()
def get_completion_analytics(user_id: int, days: int = 30) -> Dict[str, Any]:
    """
    Get task completion analytics.
    
    Args:
        user_id: The ID of the user
        days: Number of days to analyze (default 30)
    
    Returns:
        Dict with completion analytics
    """
    session = next(get_session())
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get completed tasks in period
    query = select(Task).where(
        Task.user_id == user_id,
        Task.completed == True,
        Task.updated_at >= start_date
    )
    completed_tasks = session.exec(query).all()
    
    # Group by date
    daily_completions = {}
    for task in completed_tasks:
        date_key = task.updated_at.date().isoformat()
        daily_completions[date_key] = daily_completions.get(date_key, 0) + 1
    
    # Calculate average
    avg_per_day = len(completed_tasks) / days if days > 0 else 0
    
    return {
        "period_days": days,
        "total_completed": len(completed_tasks),
        "average_per_day": round(avg_per_day, 2),
        "daily_completions": daily_completions
    }


@mcp.tool()
def get_productivity_hours(user_id: int, days: int = 7) -> Dict[str, Any]:
    """
    Analyze productivity by hour of day.
    
    Args:
        user_id: The ID of the user
        days: Number of days to analyze (default 7)
    
    Returns:
        Dict with hourly productivity data
    """
    session = next(get_session())
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get completed tasks in period
    query = select(Task).where(
        Task.user_id == user_id,
        Task.completed == True,
        Task.updated_at >= start_date
    )
    tasks = session.exec(query).all()
    
    # Group by hour
    hourly_counts = {hour: 0 for hour in range(24)}
    for task in tasks:
        hour = task.updated_at.hour
        hourly_counts[hour] += 1
    
    # Find peak hour
    peak_hour = max(hourly_counts.items(), key=lambda x: x[1])[0] if tasks else None
    
    return {
        "period_days": days,
        "hourly_completions": hourly_counts,
        "peak_productivity_hour": peak_hour,
        "total_analyzed": len(tasks)
    }


# Export MCP server instance
__all__ = ['mcp']
