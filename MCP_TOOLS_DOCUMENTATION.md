# MCP Tools Documentation

## Overview

This document provides comprehensive documentation for all MCP (Model Context Protocol) tools used by the AI agent in the Todo AI Chatbot.

**Total Tools**: 14 tools across 3 categories

## Table of Contents

1. [Basic Task Tools](#basic-task-tools)
2. [Recurring Task Tools](#recurring-task-tools)
3. [Analytics Tools](#analytics-tools)
4. [Integration Guide](#integration-guide)

---

## Basic Task Tools

### 1. add_task

Create a new task for the user.

**Function Signature**:
```python
def add_task(user_id: int, title: str, description: str = "", session: Session = None) -> Dict[str, Any]
```

**Parameters**:
- `user_id` (int, required): The ID of the user creating the task
- `title` (str, required): The task title (1-200 characters)
- `description` (str, optional): Optional task description (max 1000 characters)
- `session` (Session, optional): Database session (auto-provided)

**Returns**:
```python
{
    "task_id": 42,
    "status": "pending",
    "title": "Buy groceries"
}
```

**Error Responses**:
```python
# Invalid title
{
    "error": "INVALID_TITLE",
    "message": "Title must be between 1 and 200 characters"
}

# Invalid description
{
    "error": "INVALID_DESCRIPTION",
    "message": "Description cannot exceed 1000 characters"
}
```

**Usage Examples**:

**Natural Language**:
- "Add a task to buy groceries"
- "Create a task to call mom"
- "Remember to submit report"
- "I need to schedule dentist appointment"

**Agent Invocation**:
```python
result = add_task(
    user_id=1,
    title="Buy groceries",
    description="Milk, eggs, bread"
)
```

---

### 2. list_tasks

Retrieve the user's tasks, optionally filtered by completion status.

**Function Signature**:
```python
def list_tasks(user_id: int, status: str = "all", session: Session = None) -> Dict[str, Any]
```

**Parameters**:
- `user_id` (int, required): The ID of the user
- `status` (str, optional): Filter by status ("all", "pending", "completed")
- `session` (Session, optional): Database session

**Returns**:
```python
{
    "tasks": [
        {
            "task_id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false,
            "created_at": "2026-01-10T10:00:00Z",
            "updated_at": "2026-01-10T10:00:00Z"
        }
    ],
    "count": 1
}
```

**Usage Examples**:

**Natural Language**:
- "Show me all my tasks"
- "What are my pending tasks?"
- "List completed tasks"
- "What do I have to do?"

**Agent Invocation**:
```python
# All tasks
result = list_tasks(user_id=1, status="all")

# Pending only
result = list_tasks(user_id=1, status="pending")

# Completed only
result = list_tasks(user_id=1, status="completed")
```

---

### 3. complete_task

Mark a task as complete.

**Function Signature**:
```python
def complete_task(user_id: int, task_id: int, session: Session = None) -> Dict[str, Any]
```

**Parameters**:
- `user_id` (int, required): The ID of the user who owns the task
- `task_id` (int, required): The ID of the task to mark as complete
- `session` (Session, optional): Database session

**Returns**:
```python
{
    "task_id": 1,
    "status": "completed",
    "title": "Buy groceries"
}
```

**Error Responses**:
```python
# Task not found
{
    "error": "TASK_NOT_FOUND",
    "message": "Task with ID 999 not found"
}

# Already completed
{
    "error": "ALREADY_COMPLETED",
    "message": "Task is already marked as completed"
}
```

**Usage Examples**:

**Natural Language**:
- "Mark task 1 as done"
- "Complete task 1"
- "I finished task 1"
- "Task 1 is done"

**Agent Invocation**:
```python
result = complete_task(user_id=1, task_id=1)
```

---

### 4. delete_task

Delete a task permanently.

**Function Signature**:
```python
def delete_task(user_id: int, task_id: int, session: Session = None) -> Dict[str, Any]
```

**Parameters**:
- `user_id` (int, required): The ID of the user who owns the task
- `task_id` (int, required): The ID of the task to delete
- `session` (Session, optional): Database session

**Returns**:
```python
{
    "task_id": 1,
    "status": "deleted",
    "title": "Buy groceries"
}
```

**Error Responses**:
```python
# Task not found
{
    "error": "TASK_NOT_FOUND",
    "message": "Task with ID 999 not found"
}
```

**Usage Examples**:

**Natural Language**:
- "Delete task 1"
- "Remove task 1"
- "Cancel task 1"
- "Get rid of task 1"

**Agent Invocation**:
```python
result = delete_task(user_id=1, task_id=1)
```

---

### 5. update_task

Update a task's title or description.

**Function Signature**:
```python
def update_task(user_id: int, task_id: int, title: str = None, description: str = None, session: Session = None) -> Dict[str, Any]
```

**Parameters**:
- `user_id` (int, required): The ID of the user who owns the task
- `task_id` (int, required): The ID of the task to update
- `title` (str, optional): New task title (1-200 characters)
- `description` (str, optional): New task description (max 1000 characters)
- `session` (Session, optional): Database session

**Returns**:
```python
{
    "task_id": 1,
    "status": "updated",
    "title": "Buy groceries and fruits",
    "description": "Milk, eggs, bread, apples"
}
```

**Error Responses**:
```python
# Task not found
{
    "error": "TASK_NOT_FOUND",
    "message": "Task with ID 999 not found"
}

# No changes provided
{
    "error": "NO_CHANGES",
    "message": "No changes provided - specify title or description to update"
}

# Invalid title
{
    "error": "INVALID_TITLE",
    "message": "Title must be between 1 and 200 characters"
}
```

**Usage Examples**:

**Natural Language**:
- "Change task 1 to 'Buy groceries and fruits'"
- "Update task 1 description to include apples"
- "Rename task 1"
- "Modify task 1"

**Agent Invocation**:
```python
# Update title only
result = update_task(user_id=1, task_id=1, title="Buy groceries and fruits")

# Update description only
result = update_task(user_id=1, task_id=1, description="Milk, eggs, bread, apples")

# Update both
result = update_task(user_id=1, task_id=1, title="Shopping", description="Weekly groceries")
```

---

## Recurring Task Tools

### 6. create_recurring_task

Create a new recurring task.

**Function Signature**:
```python
def create_recurring_task(user_id: int, title: str, description: str = "", frequency: str = "daily", frequency_value: int = None, session: Session = None) -> Dict[str, Any]
```

**Parameters**:
- `user_id` (int, required): The ID of the user
- `title` (str, required): The task title
- `description` (str, optional): Task description
- `frequency` (str, required): "daily", "weekly", or "monthly"
- `frequency_value` (int, optional): Day of week (0-6) or day of month (1-31)
- `session` (Session, optional): Database session

**Returns**:
```python
{
    "recurring_task_id": 1,
    "status": "created",
    "title": "Daily standup",
    "frequency": "daily"
}
```

**Usage Examples**:

**Natural Language**:
- "Create a daily recurring task for standup"
- "Add a weekly task for team meeting on Monday"
- "Set up a monthly task for report on the 1st"

**Agent Invocation**:
```python
# Daily
result = create_recurring_task(user_id=1, title="Daily standup", frequency="daily")

# Weekly (Monday)
result = create_recurring_task(user_id=1, title="Team meeting", frequency="weekly", frequency_value=1)

# Monthly (1st)
result = create_recurring_task(user_id=1, title="Monthly report", frequency="monthly", frequency_value=1)
```

---

### 7. list_recurring_tasks

List all recurring tasks for a user.

**Function Signature**:
```python
def list_recurring_tasks(user_id: int, session: Session = None) -> Dict[str, Any]
```

**Parameters**:
- `user_id` (int, required): The ID of the user
- `session` (Session, optional): Database session

**Returns**:
```python
{
    "recurring_tasks": [
        {
            "recurring_task_id": 1,
            "title": "Daily standup",
            "description": "",
            "frequency": "daily",
            "frequency_value": null,
            "is_active": true,
            "last_generated": "2026-01-10T10:00:00Z",
            "created_at": "2026-01-01T09:00:00Z"
        }
    ],
    "count": 1
}
```

**Usage Examples**:

**Natural Language**:
- "Show me my recurring tasks"
- "List all recurring tasks"
- "What recurring tasks do I have?"

---

### 8-10. pause_recurring_task, resume_recurring_task, delete_recurring_task

Manage recurring task status.

**Function Signatures**:
```python
def pause_recurring_task(user_id: int, recurring_task_id: int, session: Session = None) -> Dict[str, Any]
def resume_recurring_task(user_id: int, recurring_task_id: int, session: Session = None) -> Dict[str, Any]
def delete_recurring_task(user_id: int, recurring_task_id: int, session: Session = None) -> Dict[str, Any]
```

**Usage Examples**:

**Natural Language**:
- "Pause recurring task 1"
- "Resume recurring task 1"
- "Delete recurring task 1"

---

## Analytics Tools

### 11. get_task_statistics

Get overall task statistics.

**Function Signature**:
```python
def get_task_statistics(user_id: int, session: Session = None) -> Dict[str, Any]
```

**Returns**:
```python
{
    "total_tasks": 10,
    "completed_tasks": 6,
    "pending_tasks": 4,
    "completion_rate": 60.0
}
```

**Usage Examples**:

**Natural Language**:
- "Show me my task statistics"
- "What's my completion rate?"
- "How many tasks do I have?"

---

### 12. get_tasks_over_time

Get task trends over time.

**Function Signature**:
```python
def get_tasks_over_time(user_id: int, days: int = 30, session: Session = None) -> Dict[str, Any]
```

**Returns**:
```python
{
    "timeline": [
        {"date": "2026-01-01", "created": 3, "completed": 2},
        {"date": "2026-01-02", "created": 5, "completed": 4}
    ],
    "days": 30
}
```

**Usage Examples**:

**Natural Language**:
- "Show me my task trends"
- "How have my tasks changed over time?"

---

### 13. get_completion_analytics

Get detailed completion analytics.

**Function Signature**:
```python
def get_completion_analytics(user_id: int, session: Session = None) -> Dict[str, Any]
```

**Returns**:
```python
{
    "total": 10,
    "completed": 6,
    "pending": 4,
    "completion_rate": 60.0,
    "avg_completion_time_hours": 24.5
}
```

---

### 14. get_productivity_hours

Get productivity by hour of day.

**Function Signature**:
```python
def get_productivity_hours(user_id: int, session: Session = None) -> Dict[str, Any]
```

**Returns**:
```python
{
    "productivity_by_hour": [
        {"hour": 0, "tasks_completed": 0},
        {"hour": 9, "tasks_completed": 5},
        {"hour": 14, "tasks_completed": 6}
    ]
}
```

---

## Integration Guide

### Adding MCP Tools to OpenAI Agent

```python
from src.mcp.server import mcp_server
from src.services.agent_service import agent_service

# Get tool definitions
tools = mcp_server.get_tool_definitions()

# Run agent with tools
result = agent_service.run_agent(
    messages=[{"role": "user", "content": "Add a task"}],
    user_id=1,
    session=db_session
)
```

### Creating Custom MCP Tools

```python
from src.mcp.server import mcp_server

@mcp_server.tool("my_custom_tool")
def my_custom_tool(user_id: int, param: str, session: Session = None) -> Dict[str, Any]:
    """
    Description of what this tool does.

    Args:
        user_id: User ID
        param: Parameter description
        session: Database session

    Returns:
        Result dictionary
    """
    # Implementation
    return {"result": "success"}
```

### Tool Execution Flow

```
1. User sends message
2. Agent analyzes message
3. Agent selects appropriate tool(s)
4. Backend executes tool(s)
5. Tool results returned to agent
6. Agent formulates response
7. Response sent to user
```

---

**Last Updated**: 2026-01-10
**Version**: 1.0
**Status**: Production Ready
