"""
Message model for AI chatbot conversations.
"""
from typing import Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship


class MessageRole(str, Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(SQLModel, table=True):
    """
    Message model representing a single message in a conversation.

    Attributes:
        id: Unique message identifier (auto-increment)
        conversation_id: Foreign key to parent conversation
        user_id: Foreign key to user (for data isolation)
        role: Message role (user, assistant, system)
        content: Message text content
        created_at: Timestamp when message was created
        conversation: Relationship to parent conversation
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: int = Field(index=True)  # Removed foreign_key constraint to allow demo/guest users
    role: str = Field(max_length=20)  # "user", "assistant", "system"
    content: str = Field(max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

    def validate_content(self) -> None:
        """Validate message content."""
        if not self.content or not self.content.strip():
            raise ValueError("Message content cannot be empty")
        if len(self.content) > 10000:
            raise ValueError("Message content cannot exceed 10000 characters")


class MessageCreate(SQLModel):
    """Schema for creating a new message."""
    conversation_id: int
    user_id: int
    role: str
    content: str


class MessageResponse(SQLModel):
    """Schema for message response."""
    id: int
    conversation_id: int
    user_id: int
    role: str
    content: str
    created_at: datetime
