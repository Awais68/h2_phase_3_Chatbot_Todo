"""
Chat API endpoint for AI chatbot.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from src.db.session import get_session
from src.services.conversation_service import conversation_service
from src.services.agent_service import agent_service
from src.models import User
from openai import RateLimitError, APIError


router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: int
    response: str
    tool_calls: list


def user_id_to_int(user_id: str) -> int:
    """
    Convert string user_id to integer for database compatibility.
    Uses hash function to generate consistent integer from string.
    
    Args:
        user_id: User ID as string
        
    Returns:
        Integer representation of user ID
    """
    try:
        # If it's already a numeric string, convert directly
        return int(user_id)
    except ValueError:
        # Otherwise, use hash to generate consistent integer
        # Use abs() to ensure positive integer and modulo to keep it reasonable
        return abs(hash(user_id)) % (10 ** 9)


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint for AI chatbot.

    Args:
        user_id: User ID (string or numeric)
        request: Chat request with optional conversation_id and message
        session: Database session

    Returns:
        ChatResponse with conversation_id, response, and tool_calls
    """
    # Validate message
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        # Auto-register user in Neon DB and get the ACTUAL backend user ID
        from src.services.user_registration_service import user_registration_service
        user = user_registration_service.get_or_create_user(
            session=session,
            user_id=user_id,
            email=user_id if '@' in user_id else None
        )
        
        # Use the actual backend user ID for all operations
        backend_user_id = user.id
        
        # Get or create conversation
        if request.conversation_id:
            conversation = conversation_service.get_conversation(request.conversation_id, session)
            if not conversation or conversation.user_id != backend_user_id:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = conversation_service.create_conversation(backend_user_id, session)

        # Store user message
        conversation_service.store_message(
            conversation_id=conversation.id,
            user_id=backend_user_id,
            role="user",
            content=request.message,
            session=session
        )

        # Get conversation history
        history = conversation_service.get_history(conversation.id, session)
        messages = conversation_service.format_history_for_agent(history)

        # Run agent with the actual backend user ID
        try:
            result = agent_service.run_agent(
                messages=messages,
                user_id=backend_user_id,  # Use actual backend user ID for task creation
                session=session
            )
        except RateLimitError as e:
            # Handle OpenAI quota/rate limit errors
            error_msg = str(e)
            if "insufficient_quota" in error_msg or "quota" in error_msg.lower():
                print(f"⚠️  OpenAI API quota exceeded: {error_msg}")
                # Return a user-friendly fallback response
                fallback_response = (
                    "I apologize, but the AI service is temporarily unavailable due to quota limits. "
                    "Please check your OpenAI API billing and quota at https://platform.openai.com/account/billing/overview. "
                    "For support, contact your administrator."
                )
                conversation_service.store_message(
                    conversation_id=conversation.id,
                    user_id=backend_user_id,
                    role="assistant",
                    content=fallback_response,
                    session=session
                )
                return ChatResponse(
                    conversation_id=conversation.id,
                    response=fallback_response,
                    tool_calls=[]
                )
            else:
                # Re-raise if it's a different rate limit error
                raise
        except APIError as e:
            # Handle other OpenAI API errors
            error_msg = str(e)
            print(f"⚠️  OpenAI API error: {error_msg}")
            if "insufficient_quota" in error_msg or "quota" in error_msg.lower():
                fallback_response = (
                    "I apologize, but the AI service is temporarily unavailable due to quota limits. "
                    "Please check your OpenAI API billing and quota at https://platform.openai.com/account/billing/overview. "
                    "For support, contact your administrator."
                )
                conversation_service.store_message(
                    conversation_id=conversation.id,
                    user_id=backend_user_id,
                    role="assistant",
                    content=fallback_response,
                    session=session
                )
                return ChatResponse(
                    conversation_id=conversation.id,
                    response=fallback_response,
                    tool_calls=[]
                )
            raise

        # Store assistant response
        if result["response"]:
            conversation_service.store_message(
                conversation_id=conversation.id,
                user_id=backend_user_id,
                role="assistant",
                content=result["response"],
                session=session
            )

        return ChatResponse(
            conversation_id=conversation.id,
            response=result["response"],
            tool_calls=result["tool_calls"]
        )
    except RateLimitError as e:
        error_msg = str(e)
        print(f"❌ OpenAI Quota Error: {error_msg}")
        raise HTTPException(
            status_code=429,
            detail="OpenAI API quota exceeded. Please check your billing and quota limits at https://platform.openai.com/account/billing/overview"
        )
    except APIError as e:
        error_msg = str(e)
        if "insufficient_quota" in error_msg or "quota" in error_msg.lower():
            print(f"❌ OpenAI Quota Error: {error_msg}")
            raise HTTPException(
                status_code=429,
                detail="OpenAI API quota exceeded. Please check your billing and quota limits at https://platform.openai.com/account/billing/overview"
            )
        print(f"❌ Chat endpoint error: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Chat error: {error_msg}")
    except Exception as e:
        import traceback
        print(f"❌ Chat endpoint error: {str(e)}")
        print(f"❌ Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")
