"""
PushSubscription model for web push notifications.
"""
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class PushSubscription(SQLModel, table=True):
    """Entity for storing web push notification subscriptions."""

    __tablename__ = "push_subscriptions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    endpoint: str = Field(max_length=500, unique=True)
    p256dh: str = Field(max_length=200)  # Public key
    auth: str = Field(max_length=200)    # Auth secret
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PushSubscriptionCreate(SQLModel):
    """Schema for creating a push subscription."""

    endpoint: str = Field(max_length=500)
    keys: dict  # Contains p256dh and auth


class PushSubscriptionResponse(SQLModel):
    """Schema for push subscription response."""

    id: int
    endpoint: str
    created_at: datetime
