# Data Model: Phase I Task Management System

**Branch**: `003-phase1-task-mgmt` | **Date**: 2025-12-27 | **Related**: [spec.md](./spec.md)

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Task                                  │
├─────────────────────────────────────────────────────────────┤
│ • id: int (PK)                                              │
│ • title: str (1-200)                                        │
│ • description: str (0-1000)                                 │
│ • completed: bool                                           │
│ • priority: Priority enum                                   │
│ • due_date: date | None                                     │
│ • recurrence: Recurrence enum                               │
│ • tags: list[str]                                           │
│ • created_at: datetime                                      │
│ • updated_at: datetime                                      │
│ • status: Status (computed)                                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ optional
                              ▼
                    ┌─────────────────┐
                    │   Theme         │
                    ├─────────────────┤
                    │ • name: str     │
                    │ • colors: dict  │
                    └─────────────────┘

FilterState and SortOption are separate models used by services
```

---

## Core Entities

### Task Entity

```python
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, List
from enum import Enum
from src.models.enums import Priority, Recurrence, Status
```

**Field Specifications**:

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | `int` | `>0`, unique, auto-increment | Auto-generated | Primary key, never reused |
| `title` | `str` | `1 <= len <= 200`, required | None | Task title, stripped of whitespace |
| `description` | `str` | `0 <= len <= 1000`, optional | `""` | Detailed description |
| `completed` | `bool` | required | `False` | Completion status |
| `priority` | `Priority` | enum | `Priority.NONE` | Priority level |
| `due_date` | `date \| None` | optional | `None` | Due date for task |
| `recurrence` | `Recurrence` | enum | `Recurrence.NONE` | Recurrence pattern |
| `tags` | `List[str]` | max 10, max 50 chars each | `[]` | Task tags (lowercase, trimmed) |
| `created_at` | `datetime` | auto-generated, UTC | `datetime.utcnow()` | Creation timestamp |
| `updated_at` | `datetime` | auto-updated, UTC | `datetime.utcnow()` | Last modification timestamp |

**Computed Properties**:

| Property | Type | Logic |
|----------|------|-------|
| `status` | `Status` | `COMPLETED` if completed, `OVERDUE` if due_date < today and not completed, else `PENDING` |

**Validation Rules**:

1. Title must not be empty or whitespace-only
2. Title length after strip() must be 1-200 characters
3. Description must not exceed 1000 characters
4. Recurrence requires due_date (cannot recur without baseline)
5. Tags must be unique, lowercase, max 50 characters each

---

### Enums

#### Priority Enum

```python
class Priority(Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"

    def __str__(self) -> str:
        return self.value
```

#### Recurrence Enum

```python
class Recurrence(Enum):
    """Task recurrence patterns."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"  # Extended from spec for completeness

    def __str__(self) -> str:
        return self.value
```

#### Status Enum

```python
class Status(Enum):
    """Task status based on completion and due date."""
    PENDING = "pending"
    COMPLETED = "completed"
    OVERDUE = "overdue"

    def __str__(self) -> str:
        return self.value
```

#### SortBy Enum

```python
class SortBy(Enum):
    """Sort options for task list."""
    DEFAULT = "default"
    PRIORITY = "priority"
    DUE_DATE = "due_date"
    CREATED_DATE = "created_date"

    def __str__(self) -> str:
        return self.value
```

#### ConversationStep Enum (Voice)

```python
class ConversationStep(Enum):
    """Voice conversation state machine steps."""
    IDLE = "idle"
    AWAITING_COMMAND = "awaiting_command"
    AWAITING_TITLE = "awaiting_title"
    AWAITING_PRIORITY = "awaiting_priority"
    AWAITING_DUE_DATE = "awaiting_due_date"
    AWAITING_RECURRENCE = "awaiting_recurrence"
    CONFIRMATION = "confirmation"

    def __str__(self) -> str:
        return self.value
```

---

### FilterState Entity

```python
@dataclass
class FilterState:
    """Represents active filter state for task list."""
    status_filter: Optional[Status] = None
    priority_filter: Optional[Priority] = None
    date_range_filter: Optional[str] = None  # "today", "week", "month", "overdue"
    search_keyword: Optional[str] = None

    def is_active(self) -> bool:
        """Check if any filters are active."""
        return any([
            self.status_filter is not None,
            self.priority_filter is not None,
            self.date_range_filter is not None,
            self.search_keyword is not None
        ])

    def describe(self) -> str:
        """Get human-readable description of active filters."""
        if not self.is_active():
            return "No filters active"

        parts = []
        if self.status_filter:
            parts.append(f"Status={self.status_filter.value}")
        if self.priority_filter:
            parts.append(f"Priority={self.priority_filter.value}")
        if self.date_range_filter:
            parts.append(f"Date={self.date_range_filter}")
        if self.search_keyword:
            parts.append(f'Search="{self.search_keyword}"')

        return " | ".join(parts)
```

---

### VoiceState Entity

```python
@dataclass
class VoiceState:
    """Represents voice conversation state."""
    current_step: ConversationStep = ConversationStep.IDLE
    collected_data: dict = None  # {title, priority, due_date, recurrence}
    step_history: list = None    # List of completed steps
    confidence: float = 0.0      # Last transcription confidence

    def __post_init__(self):
        if self.collected_data is None:
            self.collected_data = {}
        if self.step_history is None:
            self.step_history = []

    def reset(self) -> None:
        """Reset state to idle."""
        self.current_step = ConversationStep.IDLE
        self.collected_data = {}
        self.step_history = []
        self.confidence = 0.0
```

---

### Theme Entity

```python
@dataclass
class Theme:
    """Theme configuration with color definitions."""
    name: str
    primary: str
    secondary: str
    success: str
    warning: str
    error: str
    info: str
    text: str
    muted: str

# Predefined themes
THEMES = {
    "dark": Theme(
        name="Dark",
        primary="cyan",
        secondary="magenta",
        success="green",
        warning="yellow",
        error="red",
        info="blue",
        text="white",
        muted="#808080",
    ),
    "light": Theme(
        name="Light",
        primary="blue",
        secondary="purple",
        success="green",
        warning="orange3",
        error="red",
        info="cyan",
        text="black",
        muted="grey50",
    ),
    "hacker": Theme(
        name="Hacker",
        primary="bright_green",
        secondary="green",
        success="bright_green",
        warning="yellow",
        error="red",
        info="cyan",
        text="bright_green",
        muted="dark_green",
    ),
}
```

---

## State Transitions

### Task Status Transitions

```
Created:      PENDING (default)
              ↓
    Toggle    COMPLETED ←───→ PENDING
    Complete
              ↓
    Due Date OVERDUE (if due_date < today and not completed)
    Expired
```

### Voice Conversation Transitions

```
IDLE
  ↓ (user selects voice input)
AWAITING_COMMAND
  ↓ ("add task" recognized)
AWAITING_TITLE
  ↓ (title recognized)
AWAITING_PRIORITY
  ↓ (priority recognized)
AWAITING_DUE_DATE
  ↓ (due date recognized or skipped)
AWAITING_RECURRENCE
  ↓ (recurrence selected)
CONFIRMATION
  ↓ (user confirms)
  → IDLE (task created) or AWAITING_* (user edits field)
```

---

## Data Validation Examples

### Valid Task Creation

```python
task = Task(
    title="Buy groceries",
    description="Milk, eggs, bread",
    priority=Priority.HIGH,
    due_date=date(2025, 12, 28),
    recurrence=Recurrence.WEEKLY,
    tags=["shopping", "home"]
)
# Result: Valid task with id=1, status=PENDING
```

### Invalid Task Creation (raises ValueError)

```python
task = Task(
    title="",  # Empty title
    priority=Priority.HIGH
)
# Raises: ValueError("Title cannot be empty")

task = Task(
    title="Buy groceries",
    recurrence=Recurrence.DAILY  # No due date
)
# Raises: ValueError("Recurring tasks must have a due date")
```

---

## Persistence Schema

### JSON File Format

```json
{
  "version": "1.0",
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "priority": "high",
      "due_date": "2025-12-28",
      "recurrence": "weekly",
      "tags": ["shopping", "home"],
      "created_at": "2025-12-27T10:00:00Z",
      "updated_at": "2025-12-27T10:00:00Z"
    }
  ],
  "next_id": 2,
  "saved_at": "2025-12-27T10:30:00Z"
}
```

### Migration Notes

- No migration needed (first version)
- Future versions should include version field for backward compatibility
- Corrupt files backed up with timestamp: `tasks.json.corrupt.20251227_103000`
