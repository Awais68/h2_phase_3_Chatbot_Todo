"""MCP package."""
from .server import mcp_server
from .tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
    create_recurring_task,
    list_recurring_tasks,
    pause_recurring_task,
    resume_recurring_task,
    delete_recurring_task,
    get_task_statistics,
    get_tasks_over_time,
    get_completion_analytics,
    get_productivity_hours,
)

__all__ = [
    "mcp_server",
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "update_task",
    "create_recurring_task",
    "list_recurring_tasks",
    "pause_recurring_task",
    "resume_recurring_task",
    "delete_recurring_task",
    "get_task_statistics",
    "get_tasks_over_time",
    "get_completion_analytics",
    "get_productivity_hours",
]
