"""
Conversation model for AI chatbot sessions.
"""
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a chat session.

    Attributes:
        id: Unique conversation identifier (auto-increment)
        user_id: Foreign key to user who owns this conversation
        created_at: Timestamp when conversation started
        updated_at: Timestamp when conversation was last active
        messages: Relationship to messages in this conversation
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # Removed foreign_key constraint to allow demo/guest users
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    messages: List["Message"] = Relationship(back_populates="conversation")


class ConversationCreate(SQLModel):
    """Schema for creating a new conversation."""
    user_id: int


class ConversationResponse(SQLModel):
    """Schema for conversation response."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
