# Research: Todo AI Chatbot

**Feature**: 001-todo-ai-chatbot | **Date**: 2026-01-10
**Purpose**: Research technical decisions and best practices for implementation

## Overview

This document consolidates research findings for implementing a conversational AI-powered todo management system. The system integrates multiple technologies: OpenAI Agents SDK for natural language understanding, MCP tools for task operations, FastAPI for the backend API, OpenAI ChatKit for the frontend, and Neon PostgreSQL for data persistence.

## Technology Research

### 1. OpenAI Agents SDK Integration

**Decision**: Use OpenAI Agents SDK (Swarm framework) for natural language understanding and tool invocation

**Rationale**:
- Provides built-in support for function calling and tool use
- Handles conversation context management automatically
- Simplifies intent parsing and parameter extraction
- Integrates seamlessly with OpenAI's GPT models

**Implementation Pattern**:
```python
from openai import OpenAI
from typing import List, Dict, Any

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_agent(messages: List[Dict[str, str]], tools: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Run OpenAI agent with conversation history and available tools."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    return response
```

**Key Considerations**:
- Agent needs system prompt defining its role and behavior
- Tools must be defined in OpenAI function calling format
- Conversation history must be provided as message array
- Tool calls are returned in response and must be executed server-side

**Alternatives Considered**:
- LangChain: More complex, heavier framework
- Custom NLP: Would require training and maintenance
- Rule-based parsing: Brittle, doesn't handle variations well

### 2. MCP (Model Context Protocol) Tools

**Decision**: Implement MCP server with 5 tools (add_task, list_tasks, complete_task, delete_task, update_task)

**Rationale**:
- MCP provides standardized interface for AI tool definitions
- Tools are discoverable and self-documenting
- Enables separation between tool definition and implementation
- Compatible with OpenAI function calling format

**Implementation Pattern**:
```python
from mcp import MCPServer, Tool

mcp_server = MCPServer()

@mcp_server.tool()
def add_task(user_id: int, title: str, description: str = "") -> Dict[str, Any]:
    """
    Add a new task for the user.

    Args:
        user_id: The ID of the user creating the task
        title: The task title (required, 1-200 characters)
        description: Optional task description (max 1000 characters)

    Returns:
        Dict with task_id, status, and title
    """
    # Implementation calls task_service.create_task()
    pass
```

**Tool Definition Format** (for OpenAI):
```json
{
  "type": "function",
  "function": {
    "name": "add_task",
    "description": "Add a new task for the user",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {"type": "integer", "description": "User ID"},
        "title": {"type": "string", "description": "Task title (1-200 chars)"},
        "description": {"type": "string", "description": "Optional description"}
      },
      "required": ["user_id", "title"]
    }
  }
}
```

**Key Considerations**:
- Each tool must validate inputs before executing
- Tools should return structured data (not just strings)
- Error handling must be consistent across all tools
- Tools must enforce user isolation (user_id parameter)

**Alternatives Considered**:
- Direct function calls: Less structured, harder to document
- GraphQL: Overkill for simple CRUD operations
- REST endpoints only: Doesn't integrate with AI agent

### 3. Stateless Backend Architecture

**Decision**: Implement stateless FastAPI backend with all state in PostgreSQL

**Rationale**:
- Enables horizontal scaling (multiple server instances)
- Simplifies deployment and recovery
- No session management complexity
- Conversation history persisted to database

**Request Flow**:
```
1. Client sends: POST /api/{user_id}/chat
   Body: { conversation_id?: int, message: string }

2. Backend:
   a. Authenticate user (Better Auth)
   b. Fetch conversation history from DB (if conversation_id provided)
   c. Append user message to history
   d. Store user message in DB
   e. Build message array for agent
   f. Run agent with tools
   g. Execute any tool calls
   h. Store assistant response in DB
   i. Return response to client

3. Client receives: { conversation_id: int, response: string, tool_calls: [] }
```

**Key Considerations**:
- Every request must be self-contained
- Database queries must be efficient (indexed lookups)
- Conversation history may need pagination for long conversations
- Connection pooling required for database performance

**Alternatives Considered**:
- Stateful sessions: Doesn't scale, requires sticky sessions
- Redis cache: Adds complexity, eventual consistency issues
- WebSocket: Overkill for request-response pattern

### 4. Better Auth Integration

**Decision**: Use Better Auth for user authentication with FastAPI

**Rationale**:
- Modern authentication library with good TypeScript/Python support
- Handles session management, token refresh, CSRF protection
- Supports multiple auth providers (email/password, OAuth)
- Integrates with FastAPI middleware

**Implementation Pattern**:
```python
from fastapi import FastAPI, Depends, HTTPException
from better_auth import BetterAuth, get_current_user

app = FastAPI()
auth = BetterAuth(
    secret_key=os.getenv("AUTH_SECRET"),
    database_url=os.getenv("DATABASE_URL")
)

@app.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: int,
    request: ChatRequest,
    current_user = Depends(get_current_user)
):
    # Verify user_id matches authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Process chat request
    pass
```

**Key Considerations**:
- User ID in URL must match authenticated user
- All endpoints must require authentication
- Token validation on every request
- CORS configuration for frontend

**Alternatives Considered**:
- JWT manually: More work, error-prone
- OAuth2 only: Requires external providers
- Session cookies: Doesn't work well with API architecture

### 5. Neon PostgreSQL Configuration

**Decision**: Use Neon Serverless PostgreSQL with SQLModel ORM

**Rationale**:
- Serverless: Auto-scaling, pay-per-use
- PostgreSQL: Robust, ACID compliant, supports complex queries
- SQLModel: Type-safe ORM, integrates with Pydantic and FastAPI
- Connection pooling built-in

**Connection Pattern**:
```python
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import NullPool

DATABASE_URL = os.getenv("DATABASE_URL")

# Neon requires NullPool for serverless
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=False  # Set True for debugging
)

def get_session():
    """Dependency for FastAPI routes."""
    with Session(engine) as session:
        yield session

# Create tables
SQLModel.metadata.create_all(engine)
```

**Key Considerations**:
- Use NullPool for serverless (Neon manages connections)
- Connection string must include SSL parameters
- Migrations should use Alembic for production
- Indexes required on user_id, conversation_id for performance

**Alternatives Considered**:
- SQLite: Not suitable for production, no concurrent writes
- MongoDB: Overkill, relational data fits SQL better
- Supabase: Similar to Neon, but Neon specified in requirements

### 6. OpenAI ChatKit Frontend

**Decision**: Use OpenAI ChatKit React component for chat interface

**Rationale**:
- Pre-built chat UI with message bubbles, input field, typing indicators
- Handles message rendering and scrolling
- Customizable styling
- Integrates with React ecosystem

**Implementation Pattern**:
```typescript
import { ChatKit } from '@openai/chatkit';
import { useState } from 'react';

function ChatInterface({ userId }: { userId: number }) {
  const [conversationId, setConversationId] = useState<number | null>(null);

  const handleSendMessage = async (message: string) => {
    const response = await fetch(`/api/${userId}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ conversation_id: conversationId, message })
    });

    const data = await response.json();
    setConversationId(data.conversation_id);
    return data.response;
  };

  return (
    <ChatKit
      onSendMessage={handleSendMessage}
      placeholder="Ask me to manage your tasks..."
    />
  );
}
```

**Key Considerations**:
- Must handle authentication tokens in API calls
- Error handling for network failures
- Loading states during API calls
- Message history persistence

**Alternatives Considered**:
- Custom chat UI: More work, reinventing the wheel
- react-chat-widget: Less feature-rich
- Stream Chat: Overkill, requires separate service

### 7. Natural Language Intent Patterns

**Decision**: Use OpenAI's function calling with descriptive tool definitions

**Rationale**:
- GPT-4 is trained to understand function descriptions
- No need for custom intent classification
- Handles variations and synonyms automatically
- Can ask clarifying questions when ambiguous

**Agent System Prompt**:
```
You are a helpful task management assistant. Users will ask you to manage their todo tasks using natural language.

Your capabilities:
- Create tasks: "add", "create", "remember", "new task"
- List tasks: "show", "list", "what are", "see tasks"
- Complete tasks: "done", "complete", "finished", "mark as done"
- Update tasks: "change", "update", "rename", "modify"
- Delete tasks: "delete", "remove", "cancel"

Always:
- Confirm actions with friendly messages
- Ask for clarification if the request is ambiguous
- Provide helpful error messages if something fails
- Be conversational and natural

When listing tasks, format them clearly with status indicators.
```

**Key Considerations**:
- System prompt defines personality and behavior
- Tool descriptions must be clear and specific
- Agent should handle edge cases gracefully
- Conversation context helps with ambiguous references

**Alternatives Considered**:
- Rule-based NLP: Brittle, doesn't handle variations
- Custom ML model: Requires training data and maintenance
- Regex patterns: Too rigid, poor user experience

## Architecture Decisions

### Request Cycle Design

**Stateless Request Flow**:
1. Client sends message with optional conversation_id
2. Backend authenticates user
3. Backend fetches conversation history (if conversation_id provided)
4. Backend appends user message to history
5. Backend stores user message in database
6. Backend builds message array for agent (system prompt + history + new message)
7. Backend runs OpenAI agent with MCP tools
8. Agent invokes tools as needed (backend executes them)
9. Backend stores assistant response in database
10. Backend returns response with conversation_id and tool_calls

**Benefits**:
- No server-side state (scales horizontally)
- Complete audit trail in database
- Can replay conversations for debugging
- Easy to implement conversation branching later

**Trade-offs**:
- Database query on every request (mitigated by indexing)
- Conversation history grows over time (can paginate)
- Slightly higher latency than in-memory (acceptable for chat)

### Database Schema Design

**Four Core Tables**:
1. **users**: Managed by Better Auth
2. **tasks**: User tasks with title, description, completed status
3. **conversations**: Chat sessions with user_id and timestamps
4. **messages**: Individual messages with conversation_id, role, content

**Relationships**:
- User → Tasks (one-to-many)
- User → Conversations (one-to-many)
- Conversation → Messages (one-to-many)

**Indexes**:
- tasks.user_id (for filtering user tasks)
- conversations.user_id (for user's conversations)
- messages.conversation_id (for fetching history)
- All primary keys (auto-indexed)

### Error Handling Strategy

**Three Error Categories**:
1. **Validation Errors**: Invalid input (400 Bad Request)
   - Empty title, title too long, invalid task ID
   - Return clear error message to user

2. **Authorization Errors**: User not allowed (403 Forbidden)
   - User trying to access another user's data
   - Return generic "Forbidden" message

3. **System Errors**: Database, API, or agent failures (500 Internal Server Error)
   - Log error details server-side
   - Return generic "Something went wrong" to user
   - Agent should handle gracefully and inform user

## Implementation Priorities

### Phase 1: Core Backend (P1)
1. Database models (Task, Conversation, Message)
2. Database connection and migrations
3. Task service (CRUD operations)
4. Conversation service (history management)

### Phase 2: MCP Tools (P1)
1. MCP server setup
2. Tool definitions (5 tools)
3. Tool implementations (call services)
4. Tool testing

### Phase 3: Agent Integration (P1)
1. OpenAI client setup
2. Agent service (run agent with tools)
3. System prompt definition
4. Tool execution logic

### Phase 4: API Endpoints (P1)
1. FastAPI application setup
2. Better Auth integration
3. Chat endpoint implementation
4. Error handling middleware

### Phase 5: Frontend (P2)
1. React application setup
2. ChatKit integration
3. API client
4. Authentication flow

### Phase 6: Testing & Polish (P2)
1. Unit tests (models, services, tools)
2. Integration tests (API endpoints, agent flow)
3. Manual testing (natural language variations)
4. Documentation (README, API docs)

## Open Questions & Risks

### Resolved Questions
- ✅ How to integrate OpenAI Agents SDK with FastAPI? → Use client library, run agent in endpoint
- ✅ How to define MCP tools? → Use MCP SDK decorators, convert to OpenAI format
- ✅ How to handle conversation history? → Store in database, fetch on each request
- ✅ How to authenticate users? → Better Auth with FastAPI middleware

### Remaining Risks

**Risk 1: OpenAI API Rate Limits**
- **Impact**: High - Could block user requests
- **Mitigation**: Implement rate limiting on backend, queue requests if needed
- **Fallback**: Cache common responses, implement retry logic

**Risk 2: Natural Language Interpretation Accuracy**
- **Impact**: Medium - Users may get frustrated with misinterpretations
- **Mitigation**: Comprehensive system prompt, ask clarifying questions
- **Fallback**: Provide example commands in UI, allow manual task creation

**Risk 3: Database Connection Limits (Neon)**
- **Impact**: Medium - Could cause request failures under load
- **Mitigation**: Use connection pooling, implement backoff/retry
- **Fallback**: Upgrade Neon plan, implement request queuing

**Risk 4: Conversation History Size**
- **Impact**: Low - Long conversations may slow down requests
- **Mitigation**: Paginate history (e.g., last 50 messages), summarize old messages
- **Fallback**: Implement conversation archiving, start new conversations

## Next Steps

1. ✅ Research complete - All technical decisions documented
2. → Proceed to Phase 1: Data Model Design (data-model.md)
3. → Define API contracts (contracts/)
4. → Create quickstart guide (quickstart.md)
5. → Update agent context with new technologies
