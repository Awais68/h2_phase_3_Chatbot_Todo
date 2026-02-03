"""
Conversation service for managing chat conversations.
"""
from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select
from src.models import Conversation, Message, MessageCreate


class ConversationService:
    """Service for managing conversations and messages."""

    @staticmethod
    def create_conversation(user_id: int, session: Session) -> Conversation:
        """
        Create a new conversation.

        Args:
            user_id: User ID
            session: Database session

        Returns:
            Created conversation
        """
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation(conversation_id: int, session: Session) -> Optional[Conversation]:
        """
        Get a conversation by ID.

        Args:
            conversation_id: Conversation ID
            session: Database session

        Returns:
            Conversation or None
        """
        return session.get(Conversation, conversation_id)

    @staticmethod
    def get_history(
        conversation_id: int,
        session: Session,
        limit: int = 50
    ) -> List[Message]:
        """
        Get conversation history (recent messages).

        Args:
            conversation_id: Conversation ID
            session: Database session
            limit: Maximum number of messages to retrieve

        Returns:
            List of messages
        """
        query = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).limit(limit)

        return list(session.exec(query).all())

    @staticmethod
    def store_message(
        conversation_id: int,
        user_id: int,
        role: str,
        content: str,
        session: Session
    ) -> Message:
        """
        Store a message in the conversation.

        Args:
            conversation_id: Conversation ID
            user_id: User ID
            role: Message role ('user', 'assistant', 'system')
            content: Message content
            session: Database session

        Returns:
            Created message
        """
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content
        )

        session.add(message)

        # Update conversation timestamp
        conversation = session.get(Conversation, conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)

        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def format_history_for_agent(messages: List[Message]) -> List[dict]:
        """
        Format message history for OpenAI agent.

        Args:
            messages: List of Message objects

        Returns:
            List of message dicts for OpenAI API
        """
        return [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]


# Global conversation service instance
conversation_service = ConversationService()
