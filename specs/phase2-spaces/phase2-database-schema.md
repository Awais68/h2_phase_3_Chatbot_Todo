# Phase 2 Database Schema Specification

**Feature:** phase2-database-schema
**Date:** 2026-01-01
**Status:** Draft

---

## Overview

This document defines the database schema for Phase 2 of the web application, covering user accounts and task management with Neon Serverless PostgreSQL, SQLModel ORM, and Alembic migrations.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Database | Neon Serverless PostgreSQL |
| ORM | SQLModel (SQLAlchemy + Pydantic) |
| Migrations | Alembic |

## Schema Overview

### Core Tables

| Table | Purpose |
|-------|---------|
| `users` | Store user account information |
| `tasks` | Store todo tasks for users |

### Relationships

- **One-to-Many**: One user has many tasks
- **Referential Integrity**: Each task belongs to exactly one user
- **Cascade Delete**: If a user is deleted, all their tasks are deleted

---

## Users Table

### Purpose

Store user account information including authentication details and profile data.

### Schema Definition

```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE
);
```

### Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `VARCHAR(36)` | `PRIMARY KEY` | UUID as string |
| `email` | `VARCHAR(255)` | `UNIQUE`, `NOT NULL` | User email address |
| `name` | `VARCHAR(100)` | `NOT NULL` | User full name |
| `hashed_password` | `VARCHAR(255)` | `NOT NULL` | Bcrypt hashed password |
| `created_at` | `TIMESTAMP` | `NOT NULL`, `DEFAULT NOW()` | Account creation time |
| `updated_at` | `TIMESTAMP` | `NOT NULL`, `AUTO UPDATE` | Last update time |
| `is_active` | `BOOLEAN` | `DEFAULT TRUE` | Account active status |
| `email_verified` | `BOOLEAN` | `DEFAULT FALSE` | Email verification status |

### Indexes

- `PRIMARY KEY` on `id`
- `UNIQUE INDEX` on `email`
- `INDEX` on `email` (for login queries)

### SQLModel Definition

```python
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True
    )
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        nullable=False
    )
    name: str = Field(max_length=100, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    email_verified: bool = Field(default=False)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")
```

---

## Tasks Table

### Purpose

Store todo tasks for users with completion tracking.

### Schema Definition

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

### Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO INC` | Auto-increment ID |
| `user_id` | `VARCHAR(36)` | `FOREIGN KEY`, `NOT NULL`, `INDEX` | References `users.id` |
| `title` | `VARCHAR(200)` | `NOT NULL` | Task title |
| `description` | `TEXT` | `NULLABLE` | Task description |
| `completed` | `BOOLEAN` | `DEFAULT FALSE` | Completion status |
| `created_at` | `TIMESTAMP` | `NOT NULL`, `DEFAULT NOW()` | Task creation time |
| `updated_at` | `TIMESTAMP` | `NOT NULL`, `AUTO UPDATE` | Last update time |
| `completed_at` | `TIMESTAMP` | `NULLABLE` | When task was completed |

### Foreign Keys

- `user_id REFERENCES users(id) ON DELETE CASCADE`

### Indexes

- `PRIMARY KEY` on `id`
- `INDEX` on `user_id` (for user-specific queries)
- `INDEX` on `(user_id, completed)` (for filtered queries)
- `INDEX` on `created_at` (for sorting)

### SQLModel Definition

```python
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        nullable=False
    )
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    # Relationship
    user: Optional[User] = Relationship(back_populates="tasks")
```

---

## Relationship Diagram

```
┌─────────────────────────────────────┐
│              users                  │
│ ┌─────────────────────────────────┐ │
│ │ id: VARCHAR(36) PK              │ │
│ │ email: VARCHAR(255) UNIQUE      │ │
│ │ name: VARCHAR(100)              │ │
│ │ hashed_password: VARCHAR(255)   │ │
│ │ created_at: TIMESTAMP           │ │
│ │ updated_at: TIMESTAMP           │ │
│ │ is_active: BOOLEAN              │ │
│ │ email_verified: BOOLEAN         │ │
│ └─────────────────────────────────┘ │
│                   │                 │
│                   │ 1:N            │
│                   │                 │
│                   ▼                 │
│ ┌─────────────────────────────────┐ │
│ │              tasks              │ │
│ │ ┌─────────────────────────────┐ │ │
│ │ │ id: INTEGER PK              │ │ │
│ │ │ user_id: VARCHAR(36) FK     │ │ │
│ │ │ title: VARCHAR(200)         │ │ │
│ │ │ description: TEXT           │ │ │
│ │ │ completed: BOOLEAN          │ │ │
│ │ │ created_at: TIMESTAMP       │ │ │
│ │ │ updated_at: TIMESTAMP       │ │ │
│ │ │ completed_at: TIMESTAMP     │ │ │
│ │ └─────────────────────────────┘ │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

---

## Migration Strategy

### Alembic Configuration

1. Initialize Alembic in the project
2. Create migration scripts for table creation
3. Apply migrations in order

### Migration Order

1. `001_create_users_table.sql` - Create users table
2. `002_create_tasks_table.sql` - Create tasks table with FK

### Sample Migration Script

```python
"""create users and tasks tables

Revision ID: 001
Revises:
Create Date: 2026-01-01

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('email_verified', sa.Boolean, default=False),
    )

    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
    )

    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('ix_tasks_user_completed', 'tasks', ['user_id', 'completed'])
    op.create_index('ix_tasks_created_at', 'tasks', ['created_at'])

def downgrade() -> None:
    op.drop_index('ix_tasks_created_at', table_name='tasks')
    op.drop_index('ix_tasks_user_completed', table_name='tasks')
    op.drop_index('ix_tasks_user_id', table_name='tasks')
    op.drop_table('tasks')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
```

---

## Considerations

### Better Auth Integration

- The `users` table is designed to integrate with Better Auth
- `hashed_password` field stores bcrypt-hashed passwords
- Better Auth handles authentication flows and token management

### Performance Considerations

- Indexes on `email` for login queries
- Indexes on `user_id` and `(user_id, completed)` for task queries
- Cascade delete for automatic cleanup when users are removed

### Future Extensibility

- `is_active` and `email_verified` fields support future account management features
- `completed_at` allows tracking when tasks were completed for analytics

---

## Sample Data

### Users Table Sample Data

```sql
INSERT INTO users (id, email, name, hashed_password, created_at)
VALUES
  ('user-123-abc', 'john@example.com', 'John Doe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4SIYoqLJ2NXC.Ky2', NOW()),
  ('user-456-def', 'jane@example.com', 'Jane Smith', '$2b$12$EqKcp1WFKs7ILHDI8t4qfe7fM0j8w1uV5tGVKqVXLqXLqXLqXLqXL', NOW());
```

### Tasks Table Sample Data

```sql
INSERT INTO tasks (user_id, title, description, completed, created_at)
VALUES
  ('user-123-abc', 'Buy groceries', 'Milk, eggs, bread', false, NOW()),
  ('user-123-abc', 'Finish report', 'Q4 sales report', false, NOW()),
  ('user-456-def', 'Call mom', 'Birthday wishes', true, NOW());
```

---

## Common Query Patterns

### 1. Get All Tasks for a User

```sql
SELECT * FROM tasks
WHERE user_id = 'user-123-abc'
ORDER BY created_at DESC;
```

### 2. Get Pending Tasks for a User

```sql
SELECT * FROM tasks
WHERE user_id = 'user-123-abc' AND completed = false
ORDER BY created_at DESC;
```

### 3. Get Completed Tasks for a User

```sql
SELECT * FROM tasks
WHERE user_id = 'user-123-abc' AND completed = true
ORDER BY completed_at DESC;
```

### 4. Create New Task

```sql
INSERT INTO tasks (user_id, title, description, completed, created_at, updated_at)
VALUES ('user-123-abc', 'New task', 'Description', false, NOW(), NOW())
RETURNING *;
```

### 5. Update Task

```sql
UPDATE tasks
SET title = 'Updated title',
    description = 'Updated description',
    updated_at = NOW()
WHERE id = 1 AND user_id = 'user-123-abc'
RETURNING *;
```

### 6. Toggle Task Completion

```sql
UPDATE tasks
SET completed = NOT completed,
    completed_at = CASE WHEN NOT completed THEN NOW() ELSE NULL END,
    updated_at = NOW()
WHERE id = 1 AND user_id = 'user-123-abc'
RETURNING *;
```

### 7. Delete Task

```sql
DELETE FROM tasks
WHERE id = 1 AND user_id = 'user-123-abc'
RETURNING *;
```

---

## SQLModel Query Examples

### Get All Tasks for User

```python
from sqlmodel import Session, select

async def get_user_tasks(session: Session, user_id: str):
    statement = select(Task).where(Task.user_id == user_id)
    results = await session.execute(statement)
    return results.scalars().all()
```

### Get Pending Tasks

```python
async def get_pending_tasks(session: Session, user_id: str):
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.completed == False
    ).order_by(Task.created_at.desc())
    results = await session.execute(statement)
    return results.scalars().all()
```

### Create Task

```python
async def create_task(session: Session, user_id: str, title: str, description: str = None):
    task = Task(
        user_id=user_id,
        title=title,
        description=description
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
```

### Toggle Completion

```python
from datetime import datetime

async def toggle_task_completion(session: Session, task_id: int, user_id: str):
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        return None

    task.completed = not task.completed
    task.completed_at = datetime.utcnow() if task.completed else None
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)
    return task
```

---

## Validation Rules

### Users Table Validation

| Field | Validation Rule |
|-------|-----------------|
| email | Valid email format, unique, 5-255 characters |
| name | Non-empty, 1-100 characters |
| password | Minimum 8 characters (before hashing) |

### Tasks Table Validation

| Field | Validation Rule |
|-------|-----------------|
| title | Non-empty, 1-200 characters, trimmed |
| description | Optional, max 1000 characters |
| user_id | Must exist in users table |
| completed | Boolean only (true/false) |

---

## Constraints

### Hard Constraints

- User email must be unique across all users
- Task must belong to a user (no orphan tasks allowed)
- All timestamps stored in UTC
- Cascade delete: when user is deleted, all their tasks are deleted

### Soft Constraints

- Title should be descriptive and meaningful
- Description is optional but recommended for clarity
- Completed tasks should have a `completed_at` timestamp

---

## Data Integrity

### Enforced by Database

- Foreign key constraints ensure referential integrity
- Unique constraints prevent duplicate emails
- NOT NULL constraints ensure required fields are present
- Default values provide sensible fallbacks

### Enforced by Application

- Input validation using Pydantic models
- User isolation with `WHERE user_id = ...` clauses
- Automatic timestamp management
- Secure password hashing with bcrypt

---

## Backup Strategy

### Neon Automatic Backups

- Daily automated backups of all database data
- 7-day retention period for point-in-time recovery
- One-click restore functionality available
- Geographic redundancy for disaster recovery

---

## Connection Pooling

### Configuration

```python
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600
)
```

### Pool Settings

| Setting | Value | Description |
|---------|-------|-------------|
| pool_size | 10 | Number of connections to maintain |
| max_overflow | 20 | Additional connections allowed |
| pool_timeout | 30 | Seconds to wait for connection |
| pool_recycle | 3600 | Recycle connections after 1 hour |
