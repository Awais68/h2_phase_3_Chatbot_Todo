"""
Authentication API endpoints (register, login, logout).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.db.session import get_session
from src.models.user import UserCreate, UserLogin, UserResponse, User
from src.services.user_service import UserService
from src.core.security import create_access_token
from src.middleware.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user.

    Args:
        user_data: User registration data
        session: Database session

    Returns:
        UserResponse: Created user information

    Raises:
        HTTPException: If username or email already exists
    """
    try:
        user = UserService.create_user(session, user_data)
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login")
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    """
    Login and receive access token.

    Args:
        credentials: Username and password
        session: Database session

    Returns:
        dict: Access token and token type

    Raises:
        HTTPException: If credentials are invalid
    """
    user = UserService.authenticate_user(session, credentials.username, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at
        )
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.

    Args:
        current_user: Authenticated user from token

    Returns:
        UserResponse: Current user information
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )
