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
    user_id: str = Query(None, description="User ID for demo/unauthenticated users"),
    session: Session = Depends(get_session),
    current_user: User = Depends(lambda: None)  # Make auth optional
):
    """
    Create a new task for the authenticated user or demo user.

    Args:
        task_data: Task creation data
        user_id: Optional user ID for demo users (if not authenticated)
        session: Database session
        current_user: Authenticated user (optional)

    Returns:
        TaskResponse: Created task
    """
    # Determine user ID: use authenticated user if available, otherwise use provided user_id
    if current_user and hasattr(current_user, 'id'):
        effective_user_id = current_user.id
    elif user_id:
        # For demo users, use the provided user_id (could be email or any identifier)
        # Convert to integer if possible, otherwise use hash
        try:
            effective_user_id = int(user_id)
        except (ValueError, TypeError):
            # Use hash of string as user ID for non-numeric identifiers
            effective_user_id = abs(hash(user_id)) % (10**9)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required or user_id must be provided"
        )
    
    task = TaskService.create_task(session, effective_user_id, task_data)
    return TaskResponse(**task.model_dump())


@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    user_id: str = Query(None, description="User ID for demo/unauthenticated users"),
    session: Session = Depends(get_session),
    current_user: User = Depends(lambda: None)  # Make auth optional
):
    """
    Get all tasks for the authenticated user or demo user with pagination.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        user_id: Optional user ID for demo users (if not authenticated)
        session: Database session
        current_user: Authenticated user (optional)

    Returns:
        List[TaskResponse]: List of user's tasks
    """
    # Determine user ID: use authenticated user if available, otherwise use provided user_id
    if current_user and hasattr(current_user, 'id'):
        effective_user_id = current_user.id
    elif user_id:
        # For demo users, use the provided user_id (could be email or any identifier)
        # Convert to integer if possible, otherwise use hash
        try:
            effective_user_id = int(user_id)
        except (ValueError, TypeError):
            # Use hash of string as user ID for non-numeric identifiers
            effective_user_id = abs(hash(user_id)) % (10**9)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required or user_id must be provided"
        )
    
    tasks = TaskService.get_tasks(session, effective_user_id, skip, limit)
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
