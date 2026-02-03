"""
Push notification registration API endpoint.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from src.db.session import get_session
from src.models.push_subscription import (
    PushSubscription,
    PushSubscriptionCreate,
    PushSubscriptionResponse
)
from src.models.user import User
from src.middleware.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/push", tags=["push"])


@router.post("/subscribe", response_model=PushSubscriptionResponse, status_code=status.HTTP_201_CREATED)
def subscribe_push_notifications(
    subscription_data: PushSubscriptionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Register or update push notification subscription.

    Args:
        subscription_data: Push subscription data
        session: Database session
        current_user: Authenticated user

    Returns:
        PushSubscriptionResponse: Created or updated subscription
    """
    # Check if subscription already exists for this endpoint
    existing_subscription = session.exec(
        select(PushSubscription).where(PushSubscription.endpoint == subscription_data.endpoint)
    ).first()

    if existing_subscription:
        # Update existing subscription
        existing_subscription.p256dh = subscription_data.keys.get("p256dh", "")
        existing_subscription.auth = subscription_data.keys.get("auth", "")
        existing_subscription.updated_at = datetime.utcnow()
        session.add(existing_subscription)
        session.commit()
        session.refresh(existing_subscription)
        return PushSubscriptionResponse(
            id=existing_subscription.id,
            endpoint=existing_subscription.endpoint,
            created_at=existing_subscription.created_at
        )

    # Create new subscription
    subscription = PushSubscription(
        user_id=current_user.id,
        endpoint=subscription_data.endpoint,
        p256dh=subscription_data.keys.get("p256dh", ""),
        auth=subscription_data.keys.get("auth", "")
    )

    session.add(subscription)
    session.commit()
    session.refresh(subscription)

    return PushSubscriptionResponse(
        id=subscription.id,
        endpoint=subscription.endpoint,
        created_at=subscription.created_at
    )


@router.delete("/unsubscribe/{endpoint}")
def unsubscribe_push_notifications(
    endpoint: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Unsubscribe from push notifications.

    Args:
        endpoint: Push subscription endpoint to remove
        session: Database session
        current_user: Authenticated user

    Raises:
        HTTPException: If subscription not found
    """
    subscription = session.exec(
        select(PushSubscription).where(
            PushSubscription.endpoint == endpoint,
            PushSubscription.user_id == current_user.id
        )
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )

    session.delete(subscription)
    session.commit()

    return {"message": "Successfully unsubscribed"}
