"""
NotificationPreference model for 012-advanced-todo-features.

Per-user notification settings and permission status for browser notifications.
"""

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class NotificationPreference(SQLModel, table=True):
    """
    User notification preferences and permission status.

    One preference record per user (user_id is primary key).
    Controls global notification settings and default reminder times.

    Attributes:
        user_id: Primary key and foreign key to users table
        notification_enabled: Whether user wants notifications (global toggle)
        reminder_minutes_before: Default reminder time (minutes before due)
        browser_permission_granted: Whether browser notification permission granted
        timezone: User's timezone for display (informational, not used for storage)
        created_at: When preferences were first created
        updated_at: When preferences were last modified
    """

    __tablename__ = "notification_preferences"

    # Primary key (one record per user)
    user_id: int = Field(primary_key=True, description="User identifier")

    # Notification settings
    notification_enabled: bool = Field(
        default=True,
        description="Global notification toggle (on/off)"
    )
    reminder_minutes_before: int = Field(
        default=15,
        ge=0,
        le=1440,
        description="Default reminder time in minutes (0-1440)"
    )
    browser_permission_granted: bool = Field(
        default=False,
        description="Whether browser Notification API permission granted"
    )

    # Timezone (informational only, not used for calculations)
    timezone: str = Field(
        default="UTC",
        max_length=50,
        description="User's timezone for display (informational)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When preferences were created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When preferences were last updated"
    )

    def validate_reminder_minutes(self) -> None:
        """
        Validate reminder time is within bounds.

        Raises:
            ValueError: If reminder_minutes_before is out of range
        """
        if not (0 <= self.reminder_minutes_before <= 1440):
            raise ValueError(
                "reminder_minutes_before must be between 0 and 1440 (24 hours)"
            )

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp to current time."""
        self.updated_at = datetime.utcnow()


class NotificationPreferenceCreate(SQLModel):
    """Schema for creating notification preferences."""

    user_id: int
    notification_enabled: bool = True
    reminder_minutes_before: int = Field(default=15, ge=0, le=1440)
    timezone: str = "UTC"


class NotificationPreferenceUpdate(SQLModel):
    """Schema for updating notification preferences."""

    notification_enabled: Optional[bool] = None
    reminder_minutes_before: Optional[int] = Field(default=None, ge=0, le=1440)
    browser_permission_granted: Optional[bool] = None
    timezone: Optional[str] = None


class NotificationPreferenceResponse(SQLModel):
    """Schema for notification preference response."""

    user_id: int
    notification_enabled: bool
    reminder_minutes_before: int
    browser_permission_granted: bool
    timezone: str
    created_at: datetime
    updated_at: datetime
