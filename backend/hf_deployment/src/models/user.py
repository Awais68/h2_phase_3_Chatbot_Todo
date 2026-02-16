"""
User model for authentication and authorization.
"""
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """User entity for authentication."""

    __tablename__ = "backend_users"

    id: Optional[str] = Field(default=None, primary_key=True, max_length=255)
    email: str =Field(unique=True, index=True, max_length=255)
    username: Optional[str] = Field(default=None, index=True, max_length=100)
    hashed_password: str = Field(default="$2b$12$DUMMY_HASH_NO_PASSWORD", max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(SQLModel):
    """Schema for creating a new user."""

    email: str = Field(max_length=255)
    username: str = Field(max_length=100)
    password: str = Field(min_length=8, max_length=100)


class UserLogin(SQLModel):
    """Schema for user login."""

    username: str = Field(max_length=100)
    password: str = Field(max_length=100)


class UserResponse(SQLModel):
    """Schema for user response (without sensitive data)."""

    id: str
    email: str
    username: str
    is_active: bool
    created_at: datetime
