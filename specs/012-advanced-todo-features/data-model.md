# Data Model: Advanced Todo Features

**Feature**: 012-advanced-todo-features | **Date**: 2026-02-05
**Purpose**: Define database schema extensions and new entities for advanced features

## Overview

This document defines the data model extensions for advanced todo features including due dates, recurring tasks, and task history. It extends the existing Task model from `001-todo-ai-chatbot` and introduces three new entities: TaskHistory, NotificationPreference, and RecurrencePattern (embedded in Task).

**Base Models**: Extends `specs/001-todo-ai-chatbot/data-model.md`
**Database**: Neon Serverless PostgreSQL with SQLModel ORM
**Timezone Strategy**: Store all timestamps in UTC, display in user's browser timezone

---

## Entity Modifications

### 1. Task Entity (Extended)

**Purpose**: Extended todo item with due dates, recurrence, and reminder support

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DateTime
from datetime import datetime
from typing import Optional
from enum import Enum

class RecurrencePattern(str, Enum):
    """Recurrence pattern enumeration."""
    DAILY = "daily"
    WEEKLY = "weekly"
    BI_WEEKLY = "bi-weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class Task(SQLModel, table=True):
    """
    Task model representing a todo item with advanced features.

    NEW FIELDS for 012-advanced-todo-features:
        due_date: Optional deadline in UTC
        recurrence_pattern: Recurrence type (daily/weekly/monthly/yearly) or None
        is_recurring: Whether task auto-reschedules on completion
        reminder_minutes: Minutes before due_date to send reminder (default: 15)
        next_occurrence: Calculated next due date for recurring tasks (auto-set)

    EXISTING FIELDS from 001-todo-ai-chatbot:
        id, user_id, title, description, completed, created_at, updated_at
    """
    __tablename__ = "tasks"

    # Existing fields (from 001-todo-ai-chatbot)
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # NEW FIELDS for advanced features
    due_date: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
        description="Task deadline in UTC"
    )
    recurrence_pattern: Optional[RecurrencePattern] = Field(
        default=None,
        description="Recurrence pattern: daily/weekly/bi-weekly/monthly/yearly"
    )
    is_recurring: bool = Field(
        default=False,
        description="Whether task auto-creates next instance on completion"
    )
    reminder_minutes: int = Field(
        default=15,
        ge=0,
        le=1440,  # Max 24 hours
        description="Minutes before due_date to send reminder"
    )
    next_occurrence: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
        description="Calculated next due date for recurring tasks (auto-set)"
    )

    # Validation
    def validate_due_date(self) -> None:
        """Validate due date constraints."""
        if self.due_date and self.due_date.tzinfo is None:
            raise ValueError("due_date must be timezone-aware (UTC)")

    def validate_recurrence(self) -> None:
        """Validate recurrence configuration."""
        if self.is_recurring and not self.recurrence_pattern:
            raise ValueError("is_recurring requires recurrence_pattern to be set")
        if self.is_recurring and not self.due_date:
            raise ValueError("Recurring tasks must have a due_date")
        if self.recurrence_pattern and not self.is_recurring:
            # Auto-set is_recurring if pattern is set
            self.is_recurring = True

    def calculate_next_occurrence(self) -> datetime:
        """
        Calculate next occurrence for recurring tasks.

        Returns:
            Next occurrence datetime in UTC

        Raises:
            ValueError: If not a recurring task or missing due_date
        """
        if not self.is_recurring or not self.due_date or not self.recurrence_pattern:
            raise ValueError("Can only calculate next occurrence for recurring tasks")

        from dateutil.relativedelta import relativedelta
        from datetime import timedelta

        if self.recurrence_pattern == RecurrencePattern.DAILY:
            return self.due_date + timedelta(days=1)

        elif self.recurrence_pattern == RecurrencePattern.WEEKLY:
            return self.due_date + timedelta(days=7)

        elif self.recurrence_pattern == RecurrencePattern.BI_WEEKLY:
            return self.due_date + timedelta(days=14)

        elif self.recurrence_pattern == RecurrencePattern.MONTHLY:
            # relativedelta handles edge cases (Jan 31 → Feb 28/29)
            return self.due_date + relativedelta(months=1)

        elif self.recurrence_pattern == RecurrencePattern.YEARLY:
            return self.due_date + relativedelta(years=1)
```

**New Fields**:

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `due_date` | DateTime(TZ) | Optional, timezone-aware | NULL | Task deadline in UTC |
| `recurrence_pattern` | Enum | daily/weekly/bi-weekly/monthly/yearly or NULL | NULL | Recurrence type |
| `is_recurring` | Boolean | Required | False | Auto-reschedule on completion |
| `reminder_minutes` | Integer | 0-1440 (24 hours) | 15 | Minutes before due for reminder |
| `next_occurrence` | DateTime(TZ) | Optional, timezone-aware, auto-calculated | NULL | Next due date (recurring only) |

**New Indexes**:
```sql
CREATE INDEX idx_tasks_due_date ON tasks(due_date) WHERE due_date IS NOT NULL;
CREATE INDEX idx_tasks_user_due ON tasks(user_id, due_date);
CREATE INDEX idx_tasks_recurring ON tasks(user_id, is_recurring) WHERE is_recurring = TRUE;
CREATE INDEX idx_tasks_overdue ON tasks(user_id, due_date, completed) WHERE completed = FALSE;
```

**New Validation Rules**:
1. `due_date` must be timezone-aware (UTC) if provided
2. Recurring tasks (`is_recurring=True`) MUST have both `due_date` and `recurrence_pattern`
3. `reminder_minutes` must be between 0 and 1440 (24 hours)
4. `next_occurrence` is auto-calculated, not user-settable
5. Past due dates are allowed (marked as overdue)

**New Business Rules**:
- When recurring task is completed → create new instance with `due_date = next_occurrence`
- `next_occurrence` recalculated every time `due_date` or `recurrence_pattern` changes
- Deleting recurring task stops future occurrences (remove from scheduler)
- Past due dates immediately marked as "overdue" (visual indicator)
- Tasks without `due_date` have no reminders or overdue status

---

## New Entities

### 2. TaskHistory Entity

**Purpose**: Immutable record of completed or deleted tasks for audit trail and restoration

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, Text
from datetime import datetime
from typing import Optional
from enum import Enum

class HistoryActionType(str, Enum):
    """History action type enumeration."""
    COMPLETED = "completed"
    DELETED = "deleted"

class TaskHistory(SQLModel, table=True):
    """
    Task history record for completed and deleted tasks.

    Attributes:
        id: Unique history record identifier
        user_id: Foreign key to user (for data isolation)
        original_task_id: Reference to original task ID (may no longer exist)
        title: Snapshot of task title at time of action
        description: Snapshot of task description at time of action
        completed: Whether task was completed when archived
        due_date: Snapshot of due date (if any)
        recurrence_pattern: Snapshot of recurrence pattern (if any)
        action_type: What happened (completed or deleted)
        action_date: When the action occurred (UTC)
        action_by: User who performed the action
        can_restore: Whether task can be restored (true for deleted, false for completed)
    """
    __tablename__ = "task_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    original_task_id: int = Field(description="Original task ID before archival")

    # Snapshot fields (immutable copy of task at time of action)
    title: str = Field(max_length=200)
    description: str = Field(default="", sa_column=Column(Text))
    completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    recurrence_pattern: Optional[str] = Field(default=None, max_length=20)

    # History metadata
    action_type: HistoryActionType = Field(description="completed or deleted")
    action_date: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))
    action_by: int = Field(foreign_key="users.id", description="User who performed action")
    can_restore: bool = Field(default=False, description="Whether task can be restored")

    # Retention tracking
    retention_until: datetime = Field(
        description="Auto-calculated: action_date + 2 years",
        sa_column=Column(DateTime(timezone=True))
    )

    # Validation
    def __init__(self, **data):
        super().__init__(**data)
        if not self.retention_until:
            # Auto-set retention period to 2 years from action_date
            from dateutil.relativedelta import relativedelta
            self.retention_until = self.action_date + relativedelta(years=2)
```

**Fields**:

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | Integer | Primary key, auto-increment | Auto | Unique identifier |
| `user_id` | Integer | Foreign key, indexed, required | - | Owner of historical task |
| `original_task_id` | Integer | Required | - | Original task ID |
| `title` | String | Max 200 chars | - | Task title snapshot |
| `description` | Text | Optional | "" | Task description snapshot |
| `completed` | Boolean | Required | False | Completion status at archive time |
| `due_date` | DateTime(TZ) | Optional | NULL | Due date snapshot |
| `recurrence_pattern` | String | Optional, max 20 chars | NULL | Recurrence pattern snapshot |
| `action_type` | Enum | "completed" or "deleted" | - | What happened |
| `action_date` | DateTime(TZ) | Auto-generated, UTC | Now | When action occurred |
| `action_by` | Integer | Foreign key | - | User who performed action |
| `can_restore` | Boolean | Required | False | Restoration eligibility |
| `retention_until` | DateTime(TZ) | Auto-calculated | action_date + 2 years | When to purge |

**Indexes**:
```sql
CREATE INDEX idx_history_user_action_date ON task_history(user_id, action_date);
CREATE INDEX idx_history_action_type ON task_history(user_id, action_type);
CREATE INDEX idx_history_retention ON task_history(retention_until) WHERE retention_until < NOW();
CREATE INDEX idx_history_search ON task_history USING gin(to_tsvector('english', title));
```

**Validation Rules**:
1. `retention_until` auto-calculated as `action_date + 2 years`
2. `can_restore = True` only for `action_type = DELETED`
3. `action_by` must equal `user_id` (user can only archive their own tasks)
4. All timestamp fields must be timezone-aware (UTC)

**Business Rules**:
- Records are immutable once created (no updates)
- Records auto-purged when `retention_until` is reached (daily cron job)
- Completed tasks: `can_restore = False` (read-only)
- Deleted tasks: `can_restore = True` (can be restored to active tasks)
- Restoring task creates new Task with new ID (original_task_id preserved for reference)
- Search uses PostgreSQL full-text search on title field

---

### 3. NotificationPreference Entity

**Purpose**: Per-user notification settings and permission status

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class NotificationPreference(SQLModel, table=True):
    """
    User notification preferences and permission status.

    Attributes:
        user_id: Primary key and foreign key to users
        notification_enabled: Whether user wants notifications (global toggle)
        reminder_minutes_before: Default reminder time (minutes before due)
        browser_permission_granted: Whether browser notification permission granted
        timezone: User's timezone for display (informational, not used for storage)
        created_at: When preferences were first created
        updated_at: When preferences were last modified
    """
    __tablename__ = "notification_preferences"

    user_id: int = Field(primary_key=True, foreign_key="users.id")
    notification_enabled: bool = Field(default=True, description="Global notification toggle")
    reminder_minutes_before: int = Field(
        default=15,
        ge=0,
        le=1440,
        description="Default reminder time in minutes"
    )
    browser_permission_granted: bool = Field(
        default=False,
        description="Whether browser Notification API permission granted"
    )
    timezone: str = Field(
        default="UTC",
        max_length=50,
        description="User's timezone (informational, for display)"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Validation
    def validate_reminder_minutes(self) -> None:
        """Validate reminder time is within bounds."""
        if not (0 <= self.reminder_minutes_before <= 1440):
            raise ValueError("reminder_minutes_before must be between 0 and 1440 (24 hours)")
```

**Fields**:

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `user_id` | Integer | Primary key, foreign key | - | User identifier |
| `notification_enabled` | Boolean | Required | True | Global notification on/off |
| `reminder_minutes_before` | Integer | 0-1440 | 15 | Default reminder time |
| `browser_permission_granted` | Boolean | Required | False | Browser permission status |
| `timezone` | String | Max 50 chars | "UTC" | User timezone (display only) |
| `created_at` | DateTime | Auto-generated, UTC | Now | Creation timestamp |
| `updated_at` | DateTime | Auto-updated, UTC | Now | Last update timestamp |

**Indexes**:
```sql
-- Primary key on user_id is automatic
CREATE INDEX idx_notif_pref_enabled ON notification_preferences(user_id, notification_enabled)
WHERE notification_enabled = TRUE;
```

**Validation Rules**:
1. One preference record per user (user_id is primary key)
2. `reminder_minutes_before` must be 0-1440 (0 = at due time, 1440 = 24 hours before)
3. `timezone` is informational only (actual timezone comes from browser)
4. `browser_permission_granted` tracked but permission managed by browser

**Business Rules**:
- Created automatically when user sets first reminder
- `notification_enabled = False` disables all notifications globally
- `browser_permission_granted` updated based on frontend permission API response
- Default `reminder_minutes_before` applies to new tasks; individual tasks can override
- `timezone` stored for display purposes but not used for date calculations (UTC is source of truth)

---

## Entity Relationships

```
User (Better Auth)
├── 1:N → Task (extended with due_date, recurrence)
├── 1:N → TaskHistory (archived completed/deleted tasks)
├── 1:1 → NotificationPreference (notification settings)
├── 1:N → Conversation (existing from 001-todo-ai-chatbot)
└── 1:N → Message (existing from 001-todo-ai-chatbot)

Task (extended)
├── N:1 → User (owner)
└── 1:N → TaskHistory (when completed/deleted, creates history record)

TaskHistory
├── N:1 → User (owner, via user_id)
└── N:1 → User (actor, via action_by)

NotificationPreference
└── 1:1 → User (settings for user)
```

**Diagram**:
```
┌─────────────┐
│    User     │
│ (BetterAuth)│
└──────┬──────┘
       │
       ├─────────┬──────────┬───────────────┬────────────────┐
       │         │          │               │                │
       ▼         ▼          ▼               ▼                ▼
  ┌────────┐ ┌──────┐  ┌─────────┐  ┌─────────────┐  ┌──────────┐
  │  Task  │ │Convo │  │ Message │  │ TaskHistory │  │  NotifPref│
  │        │ └──────┘  └─────────┘  │             │  │           │
  │        │                        │ archived    │  │ settings  │
  │due_date│                        │ tasks       │  │ per user  │
  │recur   │                        └─────────────┘  └──────────┘
  └────────┘
```

---

## Database Migration Strategy

### Migration 001: Extend Task Table

```sql
-- Add new columns to existing tasks table
ALTER TABLE tasks
    ADD COLUMN due_date TIMESTAMP WITH TIME ZONE,
    ADD COLUMN recurrence_pattern VARCHAR(20),
    ADD COLUMN is_recurring BOOLEAN DEFAULT FALSE,
    ADD COLUMN reminder_minutes INTEGER DEFAULT 15,
    ADD COLUMN next_occurrence TIMESTAMP WITH TIME ZONE;

-- Add new indexes
CREATE INDEX idx_tasks_due_date ON tasks(due_date) WHERE due_date IS NOT NULL;
CREATE INDEX idx_tasks_user_due ON tasks(user_id, due_date);
CREATE INDEX idx_tasks_recurring ON tasks(user_id, is_recurring) WHERE is_recurring = TRUE;
CREATE INDEX idx_tasks_overdue ON tasks(user_id, due_date, completed) WHERE completed = FALSE;

-- Add constraints
ALTER TABLE tasks
    ADD CONSTRAINT chk_reminder_minutes CHECK (reminder_minutes >= 0 AND reminder_minutes <= 1440),
    ADD CONSTRAINT chk_recurring_has_pattern CHECK (
        (is_recurring = FALSE) OR
        (is_recurring = TRUE AND recurrence_pattern IS NOT NULL AND due_date IS NOT NULL)
    );
```

### Migration 002: Create TaskHistory Table

```sql
CREATE TABLE task_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    original_task_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT DEFAULT '',
    completed BOOLEAN DEFAULT FALSE,
    due_date TIMESTAMP WITH TIME ZONE,
    recurrence_pattern VARCHAR(20),
    action_type VARCHAR(20) NOT NULL CHECK (action_type IN ('completed', 'deleted')),
    action_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    action_by INTEGER NOT NULL REFERENCES users(id),
    can_restore BOOLEAN DEFAULT FALSE,
    retention_until TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Indexes for history
CREATE INDEX idx_history_user_action_date ON task_history(user_id, action_date);
CREATE INDEX idx_history_action_type ON task_history(user_id, action_type);
CREATE INDEX idx_history_retention ON task_history(retention_until) WHERE retention_until < NOW();
CREATE INDEX idx_history_search ON task_history USING gin(to_tsvector('english', title));
```

### Migration 003: Create NotificationPreference Table

```sql
CREATE TABLE notification_preferences (
    user_id INTEGER PRIMARY KEY REFERENCES users(id),
    notification_enabled BOOLEAN DEFAULT TRUE,
    reminder_minutes_before INTEGER DEFAULT 15 CHECK (reminder_minutes_before >= 0 AND reminder_minutes_before <= 1440),
    browser_permission_granted BOOLEAN DEFAULT FALSE,
    timezone VARCHAR(50) DEFAULT 'UTC',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for enabled notifications
CREATE INDEX idx_notif_pref_enabled ON notification_preferences(user_id, notification_enabled)
WHERE notification_enabled = TRUE;
```

### Migration 004: APScheduler Job Store

```sql
-- APScheduler requires this table for job persistence
CREATE TABLE apscheduler_jobs (
    id VARCHAR(191) PRIMARY KEY,
    next_run_time DOUBLE PRECISION,
    job_state BYTEA NOT NULL
);

CREATE INDEX idx_apscheduler_jobs_next_run_time ON apscheduler_jobs(next_run_time);
```

---

## Data Integrity Rules

### Cascading Deletes

**When User is deleted** (Better Auth handles this):
- CASCADE delete all Task records
- CASCADE delete all TaskHistory records
- CASCADE delete NotificationPreference record
- CASCADE delete all Conversation and Message records (existing)

**When Task is completed**:
- Create TaskHistory record (action_type='completed', can_restore=False)
- If recurring: create new Task instance with calculated next_occurrence
- Keep original Task record (do not delete)

**When Task is deleted**:
- Create TaskHistory record (action_type='deleted', can_restore=True)
- Delete original Task record
- Remove scheduled notifications from APScheduler

**When TaskHistory exceeds retention_until**:
- Permanent delete via daily cron job
- No cascade (immutable archive)

### Data Validation Order

1. **On Task Creation with due_date**:
   - Validate `due_date` is timezone-aware (UTC)
   - If `is_recurring=True`, validate `recurrence_pattern` is set
   - Calculate `next_occurrence` if recurring
   - Create NotificationPreference for user if doesn't exist

2. **On Task Completion**:
   - Create TaskHistory record (action_type='completed')
   - If recurring: create new Task with `due_date = next_occurrence`
   - Schedule notification for new recurring instance

3. **On Task Deletion**:
   - Create TaskHistory record (action_type='deleted', can_restore=True)
   - Cancel scheduled notifications (remove from APScheduler)
   - If recurring: stop future occurrences

4. **On History Restoration**:
   - Validate `can_restore = True`
   - Create new Task with new ID (copy snapshot fields)
   - Keep TaskHistory record (immutable)
   - Re-schedule notifications if due_date in future

---

## Performance Considerations

### Query Optimization

**Most Common Queries:**

1. **Get overdue tasks for user**:
   ```sql
   SELECT * FROM tasks
   WHERE user_id = ? AND completed = FALSE AND due_date < NOW()
   ORDER BY due_date ASC;
   -- Uses: idx_tasks_overdue
   ```

2. **Get upcoming tasks (due in next 7 days)**:
   ```sql
   SELECT * FROM tasks
   WHERE user_id = ? AND completed = FALSE
      AND due_date BETWEEN NOW() AND NOW() + INTERVAL '7 days'
   ORDER BY due_date ASC;
   -- Uses: idx_tasks_user_due
   ```

3. **Get user's history with pagination**:
   ```sql
   SELECT * FROM task_history
   WHERE user_id = ? AND action_date <= ?
   ORDER BY action_date DESC
   LIMIT 50 OFFSET ?;
   -- Uses: idx_history_user_action_date
   ```

4. **Search history by title**:
   ```sql
   SELECT * FROM task_history
   WHERE user_id = ? AND to_tsvector('english', title) @@ to_tsquery('groceries')
   ORDER BY action_date DESC;
   -- Uses: idx_history_search (GIN index)
   ```

### Expected Data Volume

| Table | Records per User | Total (1000 users) | Growth Rate |
|-------|------------------|-------------------|-------------|
| Task | 50-100 active | 50K-100K | Linear |
| TaskHistory | 500-1000 (2 years) | 500K-1M | Linear with 2-year cap |
| NotificationPreference | 1 | 1K | Static |
| APScheduler Jobs | 10-50 | 10K-50K | Linear with active tasks |

### Retention Management

**Daily Cleanup Job** (scheduled via APScheduler):
```python
async def cleanup_old_history():
    """Delete history entries where retention_until < NOW()"""
    result = await db.execute(
        "DELETE FROM task_history WHERE retention_until < NOW()"
    )
    return result.rowcount
```

---

## Summary

The data model extends the existing `001-todo-ai-chatbot` architecture with minimal disruption:

1. **Task table**: Added 5 new columns for due dates, recurrence, and reminders
2. **TaskHistory table**: New immutable archive with 2-year retention
3. **NotificationPreference table**: Per-user notification settings
4. **APScheduler jobs table**: Background job persistence

All changes are backward-compatible (new columns nullable or default values). Existing tasks without due dates continue working unchanged. New features opt-in via task creation parameters.

**Key Design Principles**:
- UTC storage, browser timezone display
- Immutable history records
- Automatic retention management
- Stateless backend (jobs in PostgreSQL)
- Data isolation enforced at database level
