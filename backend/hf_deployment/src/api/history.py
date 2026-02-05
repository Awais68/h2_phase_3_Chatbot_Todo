"""
Task History API endpoints for audit trail and task restoration.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlmodel import Session
from src.db.session import get_session
from src.models.task_history import (
    TaskHistory,
    TaskHistoryResponse,
    TaskHistoryQuery,
    HistoryActionType
)
from src.models.task import TaskResponse
from src.models.user import User
from src.services.history_service import HistoryService
from src.services.user_registration_service import user_registration_service
from src.middleware.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/history", tags=["history"])


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


class HistoryListResponse(BaseModel):
    """Response model for paginated history list."""
    items: List[TaskHistoryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


@router.get("/", response_model=HistoryListResponse)
def get_history(
    action_type: HistoryActionType = Query(None, description="Filter by action type (completed/deleted)"),
    start_date: str = Query(None, description="Filter by start date (ISO format)"),
    end_date: str = Query(None, description="Filter by end date (ISO format)"),
    search: str = Query(None, description="Search query for task titles"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page (max 100)"),
    user_id: str = Query(None, description="User ID for demo/unauthenticated users"),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_name: str = Header(None, alias="X-User-Name"),
    session: Session = Depends(get_session),
    current_user: User = Depends(lambda: None)
):
    """
    Get paginated task history with optional filtering.

    Args:
        action_type: Filter by action type (completed or deleted)
        start_date: Filter by start date (ISO format)
        end_date: Filter by end date (ISO format)
        search: Search query for task titles (full-text search)
        page: Page number (1-indexed)
        page_size: Items per page (max 100)
        user_id: Optional user ID for demo users
        x_user_email: User email from Better Auth
        x_user_name: User name from Better Auth
        session: Database session
        current_user: Authenticated user (optional)

    Returns:
        HistoryListResponse: Paginated history entries with metadata
    """
    # Determine user ID
    if current_user and hasattr(current_user, 'id'):
        effective_user_id = current_user.id
    elif user_id:
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

    # Build query
    from datetime import datetime
    query = TaskHistoryQuery(
        action_type=action_type,
        start_date=datetime.fromisoformat(start_date) if start_date else None,
        end_date=datetime.fromisoformat(end_date) if end_date else None,
        search=search,
        page=page,
        page_size=page_size
    )

    # Get history entries
    entries, total = HistoryService.get_history(session, effective_user_id, query)

    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size

    # Convert to response models
    items = [TaskHistoryResponse(**entry.model_dump()) for entry in entries]

    return HistoryListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{history_id}", response_model=TaskHistoryResponse)
def get_history_entry(
    history_id: int,
    user_id: str = Query(None, description="User ID for demo/unauthenticated users"),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_name: str = Header(None, alias="X-User-Name"),
    session: Session = Depends(get_session),
    current_user: User = Depends(lambda: None)
):
    """
    Get a single history entry by ID.

    Args:
        history_id: History entry ID
        user_id: Optional user ID for demo users
        x_user_email: User email from Better Auth
        x_user_name: User name from Better Auth
        session: Database session
        current_user: Authenticated user (optional)

    Returns:
        TaskHistoryResponse: History entry details

    Raises:
        HTTPException: 404 if history entry not found
    """
    # Determine user ID
    if current_user and hasattr(current_user, 'id'):
        effective_user_id = current_user.id
    elif user_id:
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

    entry = HistoryService.get_history_by_id(session, history_id, effective_user_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"History entry {history_id} not found"
        )

    return TaskHistoryResponse(**entry.model_dump())


@router.post("/{history_id}/restore", response_model=TaskResponse)
def restore_deleted_task(
    history_id: int,
    user_id: str = Query(None, description="User ID for demo/unauthenticated users"),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_name: str = Header(None, alias="X-User-Name"),
    session: Session = Depends(get_session),
    current_user: User = Depends(lambda: None)
):
    """
    Restore a deleted task from history.

    Only works for deleted tasks (action_type='deleted', can_restore=True).
    Completed tasks cannot be restored.

    Args:
        history_id: History entry ID to restore from
        user_id: Optional user ID for demo users
        x_user_email: User email from Better Auth
        x_user_name: User name from Better Auth
        session: Database session
        current_user: Authenticated user (optional)

    Returns:
        TaskResponse: Newly restored task

    Raises:
        HTTPException: 404 if history not found, 400 if cannot restore
    """
    # Determine user ID
    if current_user and hasattr(current_user, 'id'):
        effective_user_id = current_user.id
    elif user_id:
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

    try:
        restored_task = HistoryService.restore_deleted_task(
            session, history_id, effective_user_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    if not restored_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"History entry {history_id} not found or already restored"
        )

    return TaskResponse(**restored_task.model_dump())


@router.get("/stats/count", response_model=dict)
def get_history_count(
    user_id: str = Query(None, description="User ID for demo/unauthenticated users"),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_name: str = Header(None, alias="X-User-Name"),
    session: Session = Depends(get_session),
    current_user: User = Depends(lambda: None)
):
    """
    Get total count of history entries for a user.

    Args:
        user_id: Optional user ID for demo users
        x_user_email: User email from Better Auth
        x_user_name: User name from Better Auth
        session: Database session
        current_user: Authenticated user (optional)

    Returns:
        dict: Total count of history entries
    """
    # Determine user ID
    if current_user and hasattr(current_user, 'id'):
        effective_user_id = current_user.id
    elif user_id:
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

    count = HistoryService.get_history_count(session, effective_user_id)
    return {"count": count}
