"""
Analytics API endpoints for task analytics and visualizations.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from typing import List, Dict, Any
from src.db.session import get_session
from src.mcp.tools import (
    get_task_statistics,
    get_tasks_over_time,
    get_completion_analytics,
    get_productivity_hours
)


router = APIRouter()


class TaskStatistics(BaseModel):
    """Task statistics response model."""
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    completion_rate: float


class TimelineData(BaseModel):
    """Timeline data point."""
    date: str
    created: int
    completed: int


class TasksOverTimeResponse(BaseModel):
    """Tasks over time response model."""
    timeline: List[TimelineData]
    days: int


class CompletionAnalytics(BaseModel):
    """Completion analytics response model."""
    total: int
    completed: int
    pending: int
    completion_rate: float
    avg_completion_time_hours: float


class ProductivityHour(BaseModel):
    """Productivity by hour data point."""
    hour: int
    tasks_completed: int


class ProductivityResponse(BaseModel):
    """Productivity response model."""
    productivity_by_hour: List[ProductivityHour]


@router.get("/{user_id}/analytics/overview", response_model=TaskStatistics)
async def get_analytics_overview(
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    Get overall task statistics.

    Args:
        user_id: User ID
        session: Database session

    Returns:
        Task statistics
    """
    result = get_task_statistics(user_id=user_id, session=session)
    return TaskStatistics(**result)


@router.get("/{user_id}/analytics/timeline", response_model=TasksOverTimeResponse)
async def get_analytics_timeline(
    user_id: int,
    days: int = 30,
    session: Session = Depends(get_session)
):
    """
    Get task creation and completion trends over time.

    Args:
        user_id: User ID
        days: Number of days to look back (default 30)
        session: Database session

    Returns:
        Timeline data
    """
    result = get_tasks_over_time(user_id=user_id, days=days, session=session)
    return TasksOverTimeResponse(**result)


@router.get("/{user_id}/analytics/completion", response_model=CompletionAnalytics)
async def get_analytics_completion(
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    Get detailed completion analytics.

    Args:
        user_id: User ID
        session: Database session

    Returns:
        Completion analytics
    """
    result = get_completion_analytics(user_id=user_id, session=session)
    return CompletionAnalytics(**result)


@router.get("/{user_id}/analytics/productivity", response_model=ProductivityResponse)
async def get_analytics_productivity(
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    Get productivity statistics by hour of day.

    Args:
        user_id: User ID
        session: Database session

    Returns:
        Productivity by hour
    """
    result = get_productivity_hours(user_id=user_id, session=session)
    return ProductivityResponse(**result)
