"""
Recurring tasks API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from src.db.session import get_session
from src.mcp.tools import (
    create_recurring_task,
    list_recurring_tasks,
    pause_recurring_task,
    resume_recurring_task,
    delete_recurring_task
)


router = APIRouter()


class RecurringTaskCreate(BaseModel):
    """Request model for creating recurring task."""
    title: str
    description: str = ""
    frequency: str  # 'daily', 'weekly', 'monthly'
    frequency_value: int = None


class RecurringTaskUpdate(BaseModel):
    """Request model for updating recurring task."""
    is_active: bool


class RecurringTaskResponse(BaseModel):
    """Response model for recurring task."""
    recurring_task_id: int
    title: str
    description: str
    frequency: str
    frequency_value: int = None
    is_active: bool
    last_generated: str = None
    created_at: str


@router.post("/{user_id}/recurring", response_model=dict)
async def create_recurring(
    user_id: int,
    request: RecurringTaskCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new recurring task.

    Args:
        user_id: User ID
        request: Recurring task creation request
        session: Database session

    Returns:
        Created recurring task info
    """
    result = create_recurring_task(
        user_id=user_id,
        title=request.title,
        description=request.description,
        frequency=request.frequency,
        frequency_value=request.frequency_value,
        session=session
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["message"])

    return result


@router.get("/{user_id}/recurring", response_model=dict)
async def list_recurring(
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    List all recurring tasks for a user.

    Args:
        user_id: User ID
        session: Database session

    Returns:
        List of recurring tasks
    """
    result = list_recurring_tasks(user_id=user_id, session=session)
    return result


@router.patch("/{user_id}/recurring/{recurring_task_id}/pause", response_model=dict)
async def pause_recurring(
    user_id: int,
    recurring_task_id: int,
    session: Session = Depends(get_session)
):
    """
    Pause a recurring task.

    Args:
        user_id: User ID
        recurring_task_id: Recurring task ID
        session: Database session

    Returns:
        Status
    """
    result = pause_recurring_task(
        user_id=user_id,
        recurring_task_id=recurring_task_id,
        session=session
    )

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["message"])

    return result


@router.patch("/{user_id}/recurring/{recurring_task_id}/resume", response_model=dict)
async def resume_recurring(
    user_id: int,
    recurring_task_id: int,
    session: Session = Depends(get_session)
):
    """
    Resume a paused recurring task.

    Args:
        user_id: User ID
        recurring_task_id: Recurring task ID
        session: Database session

    Returns:
        Status
    """
    result = resume_recurring_task(
        user_id=user_id,
        recurring_task_id=recurring_task_id,
        session=session
    )

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["message"])

    return result


@router.delete("/{user_id}/recurring/{recurring_task_id}", response_model=dict)
async def delete_recurring(
    user_id: int,
    recurring_task_id: int,
    session: Session = Depends(get_session)
):
    """
    Delete a recurring task.

    Args:
        user_id: User ID
        recurring_task_id: Recurring task ID
        session: Database session

    Returns:
        Status
    """
    result = delete_recurring_task(
        user_id=user_id,
        recurring_task_id=recurring_task_id,
        session=session
    )

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["message"])

    return result
