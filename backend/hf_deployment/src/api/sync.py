"""
Sync API endpoint for offline change synchronization.
"""
from fastapi import APIRouter, Depends, status, Query, Header, HTTPException
from sqlmodel import Session
from src.db.session import get_session
from src.models.sync_operation import SyncRequest, SyncResponse
from src.models.user import User
from src.services.sync_service import SyncService
from src.services.user_registration_service import user_registration_service
from src.middleware.auth import get_current_user

router = APIRouter(prefix="/sync", tags=["sync"])


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


@router.post("/", response_model=SyncResponse)
def sync_offline_changes(
    sync_request: SyncRequest,
    user_id: str = Query(None, description="User ID for demo/unauthenticated users"),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_name: str = Header(None, alias="X-User-Name"),
    session: Session = Depends(get_session),
    current_user: User = Depends(lambda: None)  # Make auth optional
):
    """
    Synchronize offline changes from client to server.

    Args:
        sync_request: Sync request containing pending operations
        user_id: Optional user ID for demo users (if not authenticated)
        x_user_email: User email from Better Auth (header)
        x_user_name: User name from Better Auth (header)
        session: Database session
        current_user: Authenticated user (optional)

    Returns:
        SyncResponse: Sync results with conflicts and server updates
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

    result = SyncService.sync_operations(
        session,
        effective_user_id,
        sync_request.operations
    )

    return SyncResponse(
        success=result["success"],
        synced_count=result["synced_count"],
        conflicts=result["conflicts"],
        server_updates=result["server_updates"]
    )
