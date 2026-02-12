"""
User service for authentication and profile management.
"""
from typing import Optional
from sqlmodel import Session, select
from src.models.user import User, UserCreate, UserResponse
from src.core.security import get_password_hash, verify_password
from datetime import datetime


class UserService:
    """Service for user management operations."""

    @staticmethod
    def create_user(session: Session, user_data: UserCreate) -> User:
        """
        Create a new user with hashed password.

        Args:
            session: Database session
            user_data: User creation data

        Returns:
            User: Created user entity

        Raises:
            ValueError: If username or email already exists
        """
        # Check if user exists
        existing_user = session.exec(
            select(User).where(
                (User.username == user_data.username) | (User.email == user_data.email)
            )
        ).first()

        if existing_user:
            if existing_user.username == user_data.username:
                raise ValueError("Username already exists")
            raise ValueError("Email already exists")

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def authenticate_user(session: Session, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username and password.

        Args:
            session: Database session
            username: Username to authenticate
            password: Plain text password

        Returns:
            Optional[User]: User if authenticated, None otherwise
        """
        user = session.exec(select(User).where(User.username == username)).first()

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
        """
        Get user by ID.

        Args:
            session: Database session
            user_id: User ID

        Returns:
            Optional[User]: User if found, None otherwise
        """
        return session.get(User, user_id)

    @staticmethod
    def get_user_by_username(session: Session, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            session: Database session
            username: Username to search for

        Returns:
            Optional[User]: User if found, None otherwise
        """
        return session.exec(select(User).where(User.username == username)).first()
