"""
User auto-registration service for Better Auth integration.
"""
from typing import Optional
from sqlmodel import Session, select
from src.models.user import User


class UserRegistrationService:
    """Auto-register users from Better Auth."""
    
    @staticmethod
    def get_or_create_user(
        session: Session,
        user_id: str,
        email: Optional[str] = None,
        name: Optional[str] = None
    ) -> User:
        """Get existing user or create new one in Neon DB using only email."""
        # Determine email
        user_email = email if email else (user_id if '@' in user_id else f"{user_id}@temp.local")
        
        # Try to find user by email
        query = select(User).where(User.email == user_email)
        user = session.exec(query).first()
        
        # Create new user if not found
        if not user:
            # Extract username from email
            username_part = user_email.split('@')[0]
            
            user = User(
                email=user_email,
                username=username_part,
                hashed_password="$2b$12$DUMMY_HASH_FOR_BETTER_AUTH_USERS_NO_PASSWORD_NEEDED",  # Dummy hash for Better Auth users
                is_active=True
            )
            
            session.add(user)
            session.commit()
            session.refresh(user)
            
            print(f"✓ User registered in Neon DB: {user.email} (ID: {user.id})")
        
        return user


user_registration_service = UserRegistrationService()
