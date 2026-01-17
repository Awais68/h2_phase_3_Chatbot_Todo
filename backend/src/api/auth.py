"""
Authentication API endpoints (register, login, logout).
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlmodel import Session, select
from src.db.session import get_session
from src.models.user import UserCreate, UserLogin, UserResponse, User
from src.services.user_service import UserService
from src.core.security import create_access_token
from src.middleware.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


class TokenResponse(BaseModel):
    """Response model for token exchange."""
    access_token: str
    token_type: str
    user: dict


@router.post("/exchange-token", response_model=TokenResponse)
async def exchange_token(
    request: Request,
    session: Session = Depends(get_session),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_name: str = Header(None, alias="X-User-Name"),
    x_user_id: str = Header(None, alias="X-User-Id")
):
    """
    Exchange Better Auth session for JWT token.
    Called by frontend after Better Auth login.
    
    Better Auth should provide user info in headers:
    - X-User-Email: User's email
    - X-User-Name: User's name
    - X-User-Id: Better Auth user ID
    """
    # Try to get user info from headers first
    user_email = x_user_email
    user_name = x_user_name
    better_auth_id = x_user_id
    
    # If not in headers, try to get from Better Auth session cookie
    if not user_email:
        # Get Better Auth session from cookies
        session_cookie = request.cookies.get('better-auth.session_token')
        
        if not session_cookie:
            raise HTTPException(
                status_code=401, 
                detail="No session found. Please login first."
            )
        
        # In a real implementation, you would verify the session with Better Auth
        # For now, we'll require the headers to be sent from frontend
        raise HTTPException(
            status_code=400,
            detail="User information headers required (X-User-Email, X-User-Name)"
        )
    
    # Get or create user in backend DB
    query = select(User).where(User.email == user_email)
    user = session.exec(query).first()
    
    if not user:
        # Create new user from Better Auth data
        user = User(
            email=user_email,
            name=user_name or user_email.split('@')[0],
            is_active=True
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "email": user.email,
            "name": user.name if hasattr(user, 'name') else user.email.split('@')[0] # Fallback if 'name' isn't set
        }
    )


@router.get("/verify-token")
async def verify_token(
    current_user: User = Depends(lambda: None)  # Will add proper dependency later
):
    """
    Verify JWT token is valid.
    Returns current user info.
    """
    return {"status": "valid", "message": "Token verification endpoint"}
