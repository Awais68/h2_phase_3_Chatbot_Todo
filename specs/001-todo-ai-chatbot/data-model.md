# Data Model: Todo AI Chatbot

**Feature**: 001-todo-ai-chatbot | **Date**: 2026-01-10
**Purpose**: Define database schema and entity relationships

## Overview

This document defines the data model for the Todo AI Chatbot system. The system uses Neon PostgreSQL with SQLModel ORM for type-safe database operations. The schema consists of four main entities: User (managed by Better Auth), Task, Conversation, and Message.

## Entity Definitions

### 1. User Entity

**Managed by Better Auth** - Not directly defined in application code

**Fields** (from Better Auth):
- `id`: Integer, primary key, auto-increment
- `email`: String, unique, required
- `password_hash`: String, required
- `created_at`: DateTime, auto-generated
- `updated_at`: DateTime, auto-updated

**Relationships**:
- One-to-many with Task
- One-to-many with Conversation

**Notes**:
- Better Auth handles user table creation and management
- Application code references user_id as foreign key
- Authentication and session management handled by Better Auth

---

### 2. Task Entity

**Purpose**: Represents a todo item created by a user

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """
    Task model representing a todo item.

    Attributes:
        id: Unique task identifier (auto-increment)
        user_id: Foreign key to user who owns this task
        title: Task title (1-200 characters)
        description: Optional detailed description (max 1000 characters)
        completed: Completion status (default: False)
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last modified
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Validation
    def validate_title(self) -> None:
        """Validate title is not empty or whitespace-only."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        if len(self.title) > 200:
            raise ValueError("Title cannot exceed 200 characters")

    def validate_description(self) -> None:
        """Validate description length."""
        if len(self.description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")
```

**Fields**:
| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | Integer | Primary key, auto-increment | Auto | Unique identifier |
| `user_id` | Integer | Foreign key, indexed, required | - | Owner of the task |
| `title` | String | 1-200 chars, required | - | Task title |
| `description` | String | Max 1000 chars, optional | "" | Detailed description |
| `completed` | Boolean | Required | False | Completion status |
| `created_at` | DateTime | Auto-generated, UTC | Now | Creation timestamp |
| `updated_at` | DateTime | Auto-updated, UTC | Now | Last update timestamp |

**Indexes**:
- Primary key on `id` (automatic)
- Index on `user_id` (for filtering user's tasks)
- Composite index on `(user_id, completed)` (for status filtering)

**Validation Rules**:
1. Title must not be empty or whitespace-only
2. Title length: 1-200 characters (after strip)
3. Description length: 0-1000 characters
4. `user_id` must reference existing user
5. `completed` must be boolean (True/False)

**Business Rules**:
- Task IDs are never reused (even after deletion)
- `created_at` is immutable once set
- `updated_at` is automatically updated on any modification
- Tasks are soft-deleted (marked as deleted, not removed from DB) - optional enhancement

---

### 3. Conversation Entity

**Purpose**: Represents a chat session between a user and the AI assistant

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

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
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    messages: List["Message"] = Relationship(back_populates="conversation")
```

**Fields**:
| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | Integer | Primary key, auto-increment | Auto | Unique identifier |
| `user_id` | Integer | Foreign key, indexed, required | - | Owner of conversation |
| `created_at` | DateTime | Auto-generated, UTC | Now | When conversation started |
| `updated_at` | DateTime | Auto-updated, UTC | Now | Last activity timestamp |

**Indexes**:
- Primary key on `id` (automatic)
- Index on `user_id` (for fetching user's conversations)
- Index on `updated_at` (for sorting by recent activity)

**Relationships**:
- One-to-many with Message (one conversation has many messages)

**Business Rules**:
- New conversation created if no `conversation_id` provided in chat request
- `updated_at` is updated whenever a new message is added
- Conversations can be archived but not deleted (preserve history)
- Users can have multiple concurrent conversations

---

### 4. Message Entity

**Purpose**: Represents a single message in a conversation (user or assistant)

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from enum import Enum

class MessageRole(str, Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"  # For system prompts

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
    user_id: int = Field(foreign_key="users.id", index=True)
    role: MessageRole = Field(sa_column_kwargs={"type_": "VARCHAR(20)"})
    content: str = Field(max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

    # Validation
    def validate_content(self) -> None:
        """Validate message content."""
        if not self.content or not self.content.strip():
            raise ValueError("Message content cannot be empty")
        if len(self.content) > 10000:
            raise ValueError("Message content cannot exceed 10000 characters")
```

**Fields**:
| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | Integer | Primary key, auto-increment | Auto | Unique identifier |
| `conversation_id` | Integer | Foreign key, indexed, required | - | Parent conversation |
| `user_id` | Integer | Foreign key, indexed, required | - | Message owner |
| `role` | Enum | "user", "assistant", "system" | - | Message sender role |
| `content` | String | Max 10000 chars, required | - | Message text |
| `created_at` | DateTime | Auto-generated, UTC | Now | Creation timestamp |

**Indexes**:
- Primary key on `id` (automatic)
- Index on `conversation_id` (for fetching conversation history)
- Index on `user_id` (for data isolation checks)
- Composite index on `(conversation_id, created_at)` (for ordered history)

**Validation Rules**:
1. Content must not be empty or whitespace-only
2. Content length: 1-10000 characters
3. Role must be one of: "user", "assistant", "system"
4. `conversation_id` must reference existing conversation
5. `user_id` must match conversation's user_id (data isolation)

**Business Rules**:
- Messages are immutable once created (no updates)
- Messages are never deleted (preserve conversation history)
- `created_at` determines message order in conversation
- System messages (prompts) are stored for debugging/replay

---

## Entity Relationships

### Relationship Diagram

```
User (Better Auth)
  |
  +-- 1:N --> Task
  |             - user_id (FK)
  |
  +-- 1:N --> Conversation
                - user_id (FK)
                |
                +-- 1:N --> Message
                              - conversation_id (FK)
                              - user_id (FK, redundant for isolation)
```

### Relationship Details

**User → Task** (One-to-Many):
- One user can have many tasks
- Each task belongs to exactly one user
- Foreign key: `tasks.user_id` → `users.id`
- Cascade: Delete user → Delete all user's tasks (handled by Better Auth)

**User → Conversation** (One-to-Many):
- One user can have many conversations
- Each conversation belongs to exactly one user
- Foreign key: `conversations.user_id` → `users.id`
- Cascade: Delete user → Delete all user's conversations

**Conversation → Message** (One-to-Many):
- One conversation contains many messages
- Each message belongs to exactly one conversation
- Foreign key: `messages.conversation_id` → `conversations.id`
- Cascade: Delete conversation → Delete all messages (preserve history, so no delete)

**User → Message** (One-to-Many, indirect):
- Redundant foreign key for data isolation
- Ensures message.user_id == conversation.user_id
- Enables efficient user-level queries
- Foreign key: `messages.user_id` → `users.id`

---

## Database Indexes

### Performance Indexes

```sql
-- Task indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);

-- Conversation indexes
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at DESC);

-- Message indexes
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at);
```

### Index Rationale

1. **idx_tasks_user_id**: Fast lookup of user's tasks
2. **idx_tasks_user_completed**: Filter tasks by status (pending/completed)
3. **idx_conversations_user_id**: Fast lookup of user's conversations
4. **idx_conversations_updated_at**: Sort conversations by recent activity
5. **idx_messages_conversation_id**: Fast lookup of conversation messages
6. **idx_messages_user_id**: Data isolation checks
7. **idx_messages_conversation_created**: Ordered message history retrieval

---

## Data Validation

### Application-Level Validation

**Task Validation**:
```python
def validate_task(task: Task) -> None:
    """Validate task before saving."""
    if not task.title or not task.title.strip():
        raise ValueError("Title cannot be empty")
    if len(task.title) > 200:
        raise ValueError("Title cannot exceed 200 characters")
    if len(task.description) > 1000:
        raise ValueError("Description cannot exceed 1000 characters")
```

**Message Validation**:
```python
def validate_message(message: Message) -> None:
    """Validate message before saving."""
    if not message.content or not message.content.strip():
        raise ValueError("Message content cannot be empty")
    if len(message.content) > 10000:
        raise ValueError("Message content too long")
    if message.role not in ["user", "assistant", "system"]:
        raise ValueError("Invalid message role")
```

### Database-Level Constraints

```sql
-- Task constraints
ALTER TABLE tasks
  ADD CONSTRAINT chk_title_length CHECK (LENGTH(title) BETWEEN 1 AND 200),
  ADD CONSTRAINT chk_description_length CHECK (LENGTH(description) <= 1000);

-- Message constraints
ALTER TABLE messages
  ADD CONSTRAINT chk_content_length CHECK (LENGTH(content) BETWEEN 1 AND 10000),
  ADD CONSTRAINT chk_role_valid CHECK (role IN ('user', 'assistant', 'system'));
```

---

## Migration Strategy

### Initial Schema Creation

```python
# backend/src/database/migrations/001_initial_schema.py

from sqlmodel import SQLModel, create_engine

def upgrade(engine):
    """Create initial schema."""
    # Better Auth creates users table
    # We create our tables
    SQLModel.metadata.create_all(engine)

def downgrade(engine):
    """Drop all tables."""
    SQLModel.metadata.drop_all(engine)
```

### Using Alembic (Production)

```bash
# Initialize Alembic
alembic init alembic

# Generate migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

---

## Data Access Patterns

### Common Queries

**1. Get User's Tasks**:
```python
def get_user_tasks(session: Session, user_id: int, status: str = "all") -> List[Task]:
    """Get user's tasks filtered by status."""
    query = session.query(Task).filter(Task.user_id == user_id)

    if status == "pending":
        query = query.filter(Task.completed == False)
    elif status == "completed":
        query = query.filter(Task.completed == True)

    return query.order_by(Task.created_at.desc()).all()
```

**2. Get Conversation History**:
```python
def get_conversation_history(session: Session, conversation_id: int, limit: int = 50) -> List[Message]:
    """Get recent messages from conversation."""
    return session.query(Message)\
        .filter(Message.conversation_id == conversation_id)\
        .order_by(Message.created_at.asc())\
        .limit(limit)\
        .all()
```

**3. Create Task**:
```python
def create_task(session: Session, user_id: int, title: str, description: str = "") -> Task:
    """Create a new task."""
    task = Task(
        user_id=user_id,
        title=title.strip(),
        description=description.strip()
    )
    task.validate_title()
    task.validate_description()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

**4. Store Message**:
```python
def store_message(session: Session, conversation_id: int, user_id: int, role: str, content: str) -> Message:
    """Store a message in conversation."""
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content
    )
    message.validate_content()

    session.add(message)

    # Update conversation timestamp
    conversation = session.get(Conversation, conversation_id)
    conversation.updated_at = datetime.utcnow()

    session.commit()
    session.refresh(message)
    return message
```

---

## Data Isolation & Security

### User Data Isolation

**Principle**: Users can only access their own data

**Implementation**:
1. All queries filter by `user_id`
2. API endpoints verify `user_id` matches authenticated user
3. Database foreign keys enforce referential integrity
4. Redundant `user_id` in messages for isolation checks

**Example**:
```python
@app.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify user_id matches authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Query only user's tasks
    tasks = session.query(Task).filter(Task.user_id == user_id).all()
    return tasks
```

### Data Integrity

**Constraints**:
1. Foreign keys enforce referential integrity
2. Check constraints validate data ranges
3. Unique constraints prevent duplicates
4. Not-null constraints ensure required fields

**Transaction Management**:
```python
def create_task_with_message(session: Session, user_id: int, conversation_id: int, task_data: dict, message: str):
    """Create task and store message in single transaction."""
    try:
        # Create task
        task = create_task(session, user_id, **task_data)

        # Store assistant message
        store_message(session, conversation_id, user_id, "assistant", message)

        session.commit()
        return task
    except Exception as e:
        session.rollback()
        raise e
```

---

## Performance Considerations

### Query Optimization

1. **Use indexes** for all foreign keys and filter columns
2. **Limit result sets** with pagination (LIMIT/OFFSET)
3. **Eager loading** for relationships when needed
4. **Connection pooling** for database connections

### Scaling Strategies

1. **Read replicas** for read-heavy workloads
2. **Partitioning** conversations/messages by date (if needed)
3. **Archiving** old conversations to separate table
4. **Caching** frequently accessed data (Redis)

### Monitoring

1. **Slow query log** to identify bottlenecks
2. **Index usage statistics** to optimize indexes
3. **Connection pool metrics** to tune pool size
4. **Query execution plans** to verify index usage

---

## Next Steps

1. ✅ Data model complete - All entities and relationships defined
2. → Implement SQLModel models in `backend/src/models/`
3. → Create database migrations with Alembic
4. → Implement data access layer in `backend/src/services/`
5. → Write unit tests for models and validation
