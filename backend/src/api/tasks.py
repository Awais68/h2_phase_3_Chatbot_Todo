"""
Task CRUD API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from src.db.session import get_session
from src.models.task import TaskCreate, TaskUpdate, TaskResponse, Task
from src.models.user import User
from src.services.task_service import TaskService
from src.middleware.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new task for the authenticated user.

    Args:
        task_data: Task creation data
        session: Database session
        current_user: Authenticated user

    Returns:
        TaskResponse: Created task
    """
    task = TaskService.create_task(session, current_user.id, task_data)
    return TaskResponse(**task.model_dump())


@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get all tasks for the authenticated user with pagination.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        session: Database session
        current_user: Authenticated user

    Returns:
        List[TaskResponse]: List of user's tasks
    """
    tasks = TaskService.get_tasks(session, current_user.id, skip, limit)
    return [TaskResponse(**task.model_dump()) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific task by ID.

    Args:
        task_id: Task ID
        session: Database session
        current_user: Authenticated user

    Returns:
        TaskResponse: Requested task

    Raises:
        HTTPException: If task not found or doesn't belong to user
    """
    task = TaskService.get_task_by_id(session, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskResponse(**task.model_dump())


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update a task.

    Args:
        task_id: Task ID to update
        task_data: Updated task data
        session: Database session
        current_user: Authenticated user

    Returns:
        TaskResponse: Updated task

    Raises:
        HTTPException: If task not found or doesn't belong to user
    """
    task = TaskService.update_task(session, task_id, current_user.id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskResponse(**task.model_dump())


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a task.

    Args:
        task_id: Task ID to delete
        session: Database session
        current_user: Authenticated user

    Raises:
        HTTPException: If task not found or doesn't belong to user
    """
    deleted = TaskService.delete_task(session, task_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
