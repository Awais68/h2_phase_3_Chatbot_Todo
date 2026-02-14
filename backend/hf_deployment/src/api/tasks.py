"""
Task CRUD API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlmodel import Session
from src.db.session import get_session
from src.models.task import TaskCreate, TaskUpdate, TaskResponse, Task
from src.models.user import User
from src.services.task_service import TaskService
from src.services.user_registration_service import user_registration_service
from src.middleware.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_or_create_backend_user(
    session: Session,
    user_id: str,
    user_email: str = None,
    user_name: str = None
) -> int:
    """Get or create backend user from Better Auth user info, returns integer user ID."""
    user = user_registration_service.get_or_create_user(
        session=session,
        user_id=user_id,
        email=user_email,
        name=user_name
    )
    return user.id


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    user_id: str = Query(None, description="User ID for demo/unauthenticated users"),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_name: str = Header(None, alias="X-User-Name"),
    session: Session = Depends(get_session),
    current_user: User = Depends(lambda: None)  # Make auth optional
):
    """
    Create a new task for the authenticated user or demo user.

    Args:
        task_data: Task creation data
        user_id: Optional user ID for demo users (if not authenticated)
        x_user_email: User email from Better Auth (header)
        x_user_name: User name from Better Auth (header)
        session: Database session
        current_user: Authenticated user (optional)

    Returns:
        TaskResponse: Created task
    """
    # Determine user ID: use authenticated user if available, otherwise use provided user_id
    if current_user and hasattr(current_user, 'id'):
        effective_user_id = current_user.id
    elif user_id:
        # Auto-register Better Auth user and get backend integer ID
        effective_user_id = get_or_create_backend_user(
            session=session,
            user_id=user_id,
            user_email=x_user_email,
            user_name=x_user_name
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required or user_id must be provided"
        )
    
    task = TaskService.create_task(session, effective_user_id, task_data)
    return TaskResponse(**task.model_dump())


@router.get("", response_model=List[TaskResponse])
def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    user_id: str = Query(None, description="User ID for demo/unauthenticated users"),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_name: str = Header(None, alias="X-User-Name"),
    session: Session = Depends(get_session),
    current_user: User = Depends(lambda: None)  # Make auth optional
):
    """
    Get all tasks for the authenticated user or demo user with pagination.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        user_id: Optional user ID for demo users (if not authenticated)
        x_user_email: User email from Better Auth (header)
        x_user_name: User name from Better Auth (header)
        session: Database session
        current_user: Authenticated user (optional)

    Returns:
        List[TaskResponse]: List of user's tasks
    """
    # Determine user ID: use authenticated user if available, otherwise use provided user_id
    if current_user and hasattr(current_user, 'id'):
        effective_user_id = current_user.id
    elif user_id:
        # Auto-register Better Auth user and get backend integer ID
        effective_user_id = get_or_create_backend_user(
            session=session,
            user_id=user_id,
            user_email=x_user_email,
            user_name=x_user_name
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required or user_id must be provided"
        )
    
    tasks = TaskService.get_tasks(session, effective_user_id, skip, limit)
    return [TaskResponse(**task.model_dump()) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    user_id: str = Query(None, description="User ID for demo/unauthenticated users"),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_name: str = Header(None, alias="X-User-Name"),
    session: Session = Depends(get_session),
    current_user: User = Depends(lambda: None)  # Make auth optional
):
    """
    Get a specific task by ID (either server ID or client ID).

    Args:
        task_id: Task ID (can be integer ID or string client_id)
        user_id: Optional user ID for demo users (if not authenticated)
        x_user_email: User email from Better Auth (header)
        x_user_name: User name from Better Auth (header)
        session: Database session
        current_user: Authenticated user (optional)

    Returns:
        TaskResponse: Requested task

    Raises:
        HTTPException: If task not found or doesn't belong to user
    """
    # Determine user ID: use authenticated user if available, otherwise use provided user_id
    if current_user and hasattr(current_user, 'id'):
        effective_user_id = current_user.id
    elif user_id:
        # Auto-register Better Auth user and get backend integer ID
        effective_user_id = get_or_create_backend_user(
            session=session,
            user_id=user_id,
            user_email=x_user_email,
            user_name=x_user_name
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required or user_id must be provided"
        )

    # Check if task_id is an integer (server ID) or string (client ID)
    try:
        # Try parsing as integer first
        task_id_int = int(task_id)
        task = TaskService.get_task_by_id(session, task_id_int, effective_user_id)
    except ValueError:
        # If it's not an integer, treat as client_id
        task = TaskService.get_task_by_client_id(session, task_id, effective_user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskResponse(**task.model_dump())


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_data: TaskUpdate,
    user_id: str = Query(None, description="User ID for demo/unauthenticated users"),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_name: str = Header(None, alias="X-User-Name"),
    session: Session = Depends(get_session),
    current_user: User = Depends(lambda: None)  # Make auth optional
):
    """
    Update a task (by either server ID or client ID).

    Args:
        task_id: Task ID to update (can be integer ID or string client_id)
        task_data: Updated task data
        user_id: Optional user ID for demo users (if not authenticated)
        x_user_email: User email from Better Auth (header)
        x_user_name: User name from Better Auth (header)
        session: Database session
        current_user: Authenticated user (optional)

    Returns:
        TaskResponse: Updated task

    Raises:
        HTTPException: If task not found or doesn't belong to user
    """
    # Determine user ID: use authenticated user if available, otherwise use provided user_id
    if current_user and hasattr(current_user, 'id'):
        effective_user_id = current_user.id
    elif user_id:
        # Auto-register Better Auth user and get backend integer ID
        effective_user_id = get_or_create_backend_user(
            session=session,
            user_id=user_id,
            user_email=x_user_email,
            user_name=x_user_name
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required or user_id must be provided"
        )

    # Check if task_id is an integer (server ID) or string (client ID)
    try:
        # Try parsing as integer first
        task_id_int = int(task_id)
        task = TaskService.update_task(session, task_id_int, effective_user_id, task_data)
    except ValueError:
        # If it's not an integer, treat as client_id
        # For client_id, we need to first get the task to get its server ID
        task_obj = TaskService.get_task_by_client_id(session, task_id, effective_user_id)
        if not task_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        task = TaskService.update_task(session, task_obj.id, effective_user_id, task_data)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskResponse(**task.model_dump())


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    user_id: str = Query(None, description="User ID for demo/unauthenticated users"),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_name: str = Header(None, alias="X-User-Name"),
    session: Session = Depends(get_session),
    current_user: User = Depends(lambda: None)  # Make auth optional
):
    """
    Delete a task (by either server ID or client ID).

    Args:
        task_id: Task ID to delete (can be integer ID or string client_id)
        user_id: Optional user ID for demo users (if not authenticated)
        x_user_email: User email from Better Auth (header)
        x_user_name: User name from Better Auth (header)
        session: Database session
        current_user: Authenticated user (optional)

    Raises:
        HTTPException: If task not found or doesn't belong to user
    """
    # Determine user ID: use authenticated user if available, otherwise use provided user_id
    if current_user and hasattr(current_user, 'id'):
        effective_user_id = current_user.id
    elif user_id:
        # Auto-register Better Auth user and get backend integer ID
        effective_user_id = get_or_create_backend_user(
            session=session,
            user_id=user_id,
            user_email=x_user_email,
            user_name=x_user_name
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required or user_id must be provided"
        )

    # Check if task_id is an integer (server ID) or string (client ID)
    try:
        # Try parsing as integer first
        task_id_int = int(task_id)
        deleted = TaskService.delete_task(session, task_id_int, effective_user_id)
    except ValueError:
        # If it's not an integer, treat as client_id
        # For client_id, we need to first get the task to get its server ID
        task_obj = TaskService.get_task_by_client_id(session, task_id, effective_user_id)
        if not task_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        deleted = TaskService.delete_task(session, task_obj.id, effective_user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
