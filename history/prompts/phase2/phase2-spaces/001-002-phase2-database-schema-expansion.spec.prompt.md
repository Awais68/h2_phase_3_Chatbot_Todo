---
id: "001-002-phase2-database-schema-expansion"
title: Phase 2 Database Schema Expansion
stage: spec
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: phase2-database-schema
branch: 005-deployment-architecture
user: Awais
command: continue with above same prompt please
labels: ["database","schema","sqlmodel","postgresql","sample-data","queries"]
links:
  spec: /media/data/hackathon series/hackathon-2/phase-ii_Web_App_Full Stack/specs/phase2-spaces/phase2-database-schema.md
  ticket: null
  adr: null
  pr: null
files:
  - /media/data/hackathon series/hackathon-2/phase-ii_Web_App_Full Stack/specs/phase2-spaces/phase2-database-schema.md
tests: []
---

## Prompt

continue with above same prompt please SAMPLE DATA:

Users Table:
```sql
INSERT INTO users (id, email, name, hashed_password, created_at)
VALUES
  ('user-123-abc', 'john@example.com', 'John Doe', '$2b$12$...', NOW()),
  ('user-456-def', 'jane@example.com', 'Jane Smith', '$2b$12$...', NOW());
```

Tasks Table:
```sql
INSERT INTO tasks (user_id, title, description, completed, created_at)
VALUES
  ('user-123-abc', 'Buy groceries', 'Milk, eggs, bread', false, NOW()),
  ('user-123-abc', 'Finish report', 'Q4 sales report', false, NOW()),
  ('user-456-def', 'Call mom', 'Birthday wishes', true, NOW());
```

QUERIES:

Common Query Patterns:

1. Get all tasks for a user:
```sql
SELECT * FROM tasks
WHERE user_id = 'user-123-abc'
ORDER BY created_at DESC;
```

2. Get pending tasks for a user:
```sql
SELECT * FROM tasks
WHERE user_id = 'user-123-abc' AND completed = false
ORDER BY created_at DESC;
```

3. Get completed tasks for a user:
```sql
SELECT * FROM tasks
WHERE user_id = 'user-123-abc' AND completed = true
ORDER BY completed_at DESC;
```

4. Create new task:
```sql
INSERT INTO tasks (user_id, title, description, completed, created_at, updated_at)
VALUES ('user-123-abc', 'New task', 'Description', false, NOW(), NOW())
RETURNING *;
```

5. Update task:
```sql
UPDATE tasks
SET title = 'Updated title',
    description = 'Updated description',
    updated_at = NOW()
WHERE id = 1 AND user_id = 'user-123-abc'
RETURNING *;
```

6. Toggle task completion:
```sql
UPDATE tasks
SET completed = NOT completed,
    completed_at = CASE WHEN NOT completed THEN NOW() ELSE NULL END,
    updated_at = NOW()
WHERE id = 1 AND user_id = 'user-123-abc'
RETURNING *;
```

7. Delete task:
```sql
DELETE FROM tasks
WHERE id = 1 AND user_id = 'user-123-abc'
RETURNING *;
```

SQLModel Query Examples:
```python
from sqlmodel import Session, select

# Get all tasks for user
async def get_user_tasks(session: Session, user_id: str):
    statement = select(Task).where(Task.user_id == user_id)
    results = await session.execute(statement)
    return results.scalars().all()

# Get pending tasks
async def get_pending_tasks(session: Session, user_id: str):
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.completed == False
    ).order_by(Task.created_at.desc())
    results = await session.execute(statement)
    return results.scalars().all()

# Create task
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

# Toggle completion
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

MIGRATIONS:

Using Alembic for database migrations

Initial Migration:
```bash
alembic init migrations
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

Migration File Structure:
```python
# migrations/versions/001_initial_schema.py

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('email_verified', sa.Boolean, default=False)
    )

    op.create_index('ix_users_email', 'users', ['email'])

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('completed', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('completed_at', sa.DateTime)
    )

    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('ix_tasks_user_completed', 'tasks', ['user_id', 'completed'])

def downgrade():
    op.drop_table('tasks')
    op.drop_table('users')
```

VALIDATION RULES:

Users:
- email: Valid email format, unique, 5-255 characters
- name: Non-empty, 1-100 characters
- password: Minimum 8 characters (before hashing)

Tasks:
- title: Non-empty, 1-200 characters, trimmed
- description: Optional, max 1000 characters
- user_id: Must exist in users table
- completed: Boolean only (true/false)

CONSTRAINTS:

Hard Constraints:
- User email must be unique
- Task must belong to a user (no orphan tasks)
- All timestamps in UTC
- Cascade delete (user deleted = tasks deleted)

Soft Constraints:
- Title should be descriptive
- Description is optional but recommended
- Completed tasks should have completed_at timestamp

DATA INTEGRITY:

Enforced by Database:
- Foreign key constraints
- Unique constraints
- NOT NULL constraints
- Default values

Enforced by Application:
- Input validation (Pydantic)
- User isolation (WHERE user_id = ...)
- Timestamp management
- Password hashing

BACKUP STRATEGY:

Neon Automatic Backups:
- Daily automated backups
- 7-day retention
- Point-in-time recovery
- One-click restore

CONNECTION POOLING:

Configuration:
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

Include in database/schema.md:
- Complete table definitions
- SQLModel code examples
- All relationships
- Query patterns
- Migration scripts
- Validation rules
- Backup strategy

## Response snapshot

Expanded the Phase 2 database schema specification with additional sections:

1. **Sample Data**: Added INSERT statements for users and tasks tables with sample data
2. **Common Query Patterns**: Added 7 SQL query patterns including get all tasks, pending tasks, completed tasks, create, update, toggle completion, and delete
3. **SQLModel Query Examples**: Added Python async query examples using SQLModel for common operations
4. **Validation Rules**: Added field-level validation rules for users and tasks tables
5. **Constraints**: Documented hard constraints (FK, unique, UTC timestamps, cascade delete) and soft constraints
6. **Data Integrity**: Listed database-level and application-level integrity enforcement
7. **Backup Strategy**: Documented Neon automatic backup features (daily backups, 7-day retention, point-in-time recovery)
8. **Connection Pooling**: Added SQLModel connection pool configuration with pool settings table

## Outcome

- ✅ Impact: Extended database schema specification with comprehensive sample data, query patterns, SQLModel examples, validation rules, constraints, data integrity measures, backup strategy, and connection pooling configuration
- 🧪 Tests: None (specification only)
- 📁 Files: 1 file modified (specs/phase2-spaces/phase2-database-schema.md)
- 🔁 Next prompts: Create implementation plan (plan.md), Generate tasks (tasks.md)
- 🧠 Reflection: User requested continuation to add sample data, queries, migrations, validation rules, constraints, data integrity, backup strategy, and connection pooling to the existing schema specification

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
