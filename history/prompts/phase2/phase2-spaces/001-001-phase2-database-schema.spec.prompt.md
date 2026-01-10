---
id: "001-001-phase2-database-schema"
title: Phase 2 Database Schema Specification
stage: spec
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: phase2-database-schema
branch: 005-deployment-architecture
user: Awais
command: /sp.specify phase2-database-schema Create Phase II database schema specification
labels: ["database","schema","sqlmodel","postgresql"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - /media/data/hackathon series/hackathon-2/phase-ii_Web_App_Full Stack/specs/phase2-spaces/phase2-database-schema.md
tests: []
---

## Prompt

make a seprate directory in specs folder and keep my phase2 work in that directory name phase2 spacs
/sp.specify phase2-database-schema Create Phase II database schema specification

DATABASE: Neon Serverless PostgreSQL
ORM: SQLModel (SQLAlchemy + Pydantic)
MIGRATIONS: Alembic

SCHEMA OVERVIEW:

Tables: 2 core tables
- users (managed by Better Auth + custom fields)
- tasks (todo items)

Relationships:
- One user has many tasks (1:N)
- Each task belongs to one user

USERS TABLE:

Table Name: users
Purpose: Store user account information

Columns:
┌────────────────┬──────────────┬─────────────┬──────────────────────────┐
│ Column         │ Type         │ Constraints │ Description              │
├────────────────┼──────────────┼─────────────┼──────────────────────────┤
│ id             │ String(36)   │ PRIMARY KEY │ UUID as string           │
│ email          │ String(255)  │ UNIQUE,     │ User email address       │
│                │              │ NOT NULL    │                          │
│ name           │ String(100)  │ NOT NULL    │ User full name           │
│ hashed_password│ String(255)  │ NOT NULL    │ Bcrypt hashed password   │
│ created_at     │ DateTime     │ NOT NULL,   │ Account creation time    │
│                │              │ DEFAULT NOW │                          │
│ updated_at     │ DateTime     │ NOT NULL,   │ Last update time         │
│                │              │ AUTO UPDATE │                          │
│ is_active      │ Boolean      │ DEFAULT TRUE│ Account active status    │
│ email_verified │ Boolean      │ DEFAULT FALSE│ Email verification status│
└────────────────┴──────────────┴─────────────┴──────────────────────────┘

Indexes:
- PRIMARY KEY on id
- UNIQUE INDEX on email
- INDEX on email (for login queries)

SQLModel Definition:
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

TASKS TABLE:

Table Name: tasks
Purpose: Store todo tasks for users

Columns:
┌────────────────┬──────────────┬─────────────┬──────────────────────────┐
│ Column         │ Type         │ Constraints │ Description              │
├────────────────┼──────────────┼─────────────┼──────────────────────────┤
│ id             │ Integer      │ PRIMARY KEY,│ Auto-increment ID        │
│                │              │ AUTO INC    │                          │
│ user_id        │ String(36)   │ FOREIGN KEY,│ References users.id      │
│                │              │ NOT NULL,   │                          │
│                │              │ INDEX       │                          │
│ title          │ String(200)  │ NOT NULL    │ Task title               │
│ description    │ Text         │ NULLABLE    │ Task description         │
│ completed      │ Boolean      │ DEFAULT FALSE│ Completion status       │
│ created_at     │ DateTime     │ NOT NULL,   │ Task creation time       │
│                │              │ DEFAULT NOW │                          │
│ updated_at     │ DateTime     │ NOT NULL,   │ Last update time         │
│                │              │ AUTO UPDATE │                          │
│ completed_at   │ DateTime     │ NULLABLE    │ When task was completed  │
└────────────────┴──────────────┴─────────────┴──────────────────────────┘

Foreign Keys:
- user_id REFERENCES users(id) ON DELETE CASCADE

Indexes:
- PRIMARY KEY on id
- INDEX on user_id (for user-specific queries)
- INDEX on (user_id, completed) (for filtered queries)
- INDEX on created_at (for sorting)

SQLModel Definition:
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

RELATIONSHIPS:

User → Tasks (One-to-Many):
- One user can have multiple tasks
- Each task belongs to exactly one user
- Cascade delete: If user deleted, all their tasks deleted

Diagram: (empty)

## Response snapshot

Created database schema specification for Phase 2 with the following outputs:

1. Created directory: `specs/phase2-spaces/`
2. Created specification: `specs/phase2-spaces/phase2-database-schema.md`
   - Technology stack documentation (Neon PostgreSQL, SQLModel, Alembic)
   - Users table schema with SQL definition, columns, indexes, and SQLModel code
   - Tasks table schema with SQL definition, columns, foreign keys, indexes, and SQLModel code
   - Relationship diagram (ASCII)
   - Alembic migration strategy with sample migration script
   - Future extensibility considerations

3. Created PHR: `history/prompts/phase2/phase2-spaces/001-001-phase2-database-schema.spec.prompt.md`

## Outcome

- ✅ Impact: Created comprehensive database schema specification for Phase 2, documenting users and tasks tables with full SQL definitions, SQLModel code, indexes, foreign keys, and migration strategy
- 🧪 Tests: None (specification only)
- 📁 Files: 2 files created
- 🔁 Next prompts: Create implementation plan (plan.md), Generate tasks (tasks.md)
- 🧠 Reflection: User requested separation of Phase 2 work into dedicated directory structure for better organization

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
