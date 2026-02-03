"""
Sync API endpoint for offline change synchronization.
"""
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from src.db.session import get_session
from src.models.sync_operation import SyncRequest, SyncResponse
from src.models.user import User
from src.services.sync_service import SyncService
from src.middleware.auth import get_current_user

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/", response_model=SyncResponse)
def sync_offline_changes(
    sync_request: SyncRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Synchronize offline changes from client to server.

    Args:
        sync_request: Sync request containing pending operations
        session: Database session
        current_user: Authenticated user

    Returns:
        SyncResponse: Sync results with conflicts and server updates
    """
    result = SyncService.sync_operations(
        session,
        current_user.id,
        sync_request.operations
    )

    return SyncResponse(
        success=result["success"],
        synced_count=result["synced_count"],
        conflicts=result["conflicts"],
        server_updates=result["server_updates"]
    )
