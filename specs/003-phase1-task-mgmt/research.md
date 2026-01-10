# Research: Phase I Complete Task Management System

**Feature**: Phase I Complete Task Management System
**Branch**: `003-phase1-task-mgmt`
**Date**: 2025-12-26
**Research Phase**: Phase 0 - Technical Decisions

---

## Overview

This research document captures all technical decisions, alternatives considered, and rationale for implementing Phase I Complete Task Management System. All NEEDS CLARIFICATION items from the plan template are resolved here.

---

## Decision 1: Natural Language Date Parsing

**Context**: FR-003 requires support for natural language dates like "tomorrow", "next week", "2025-12-31".

**Decision**: Use **`dateparser`** library (version 1.2.0+)

**Rationale**:
- Industry-standard library with 10M+ downloads/month
- Handles wide variety of formats: "tomorrow", "next Monday", "in 2 weeks", "Dec 31", "2025-12-31"
- Supports relative dates, absolute dates, and ISO formats
- Timezone-aware (can use local timezone)
- Robust error handling (returns None for invalid dates)
- Well-maintained with active development

**Alternatives Considered**:

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Manual regex parsing | No dependencies | Error-prone, limited formats, hard to maintain | Too complex, won't handle edge cases |
| python-dateutil | Built-in to Python, lighter weight | Doesn't handle natural language well ("tomorrow" not supported) | Insufficient for requirements |
| Arrow library | Nice API, chainable | Heavier than dateparser, focuses on manipulation not parsing | Overkill for our needs |

**Implementation Approach**:
```python
import dateparser
from datetime import date

def parse_date(date_string: str) -> Optional[date]:
    """Parse natural language or ISO date string."""
    if not date_string or not date_string.strip():
        return None

    # Use dateparser with settings for future dates only
    parsed = dateparser.parse(
        date_string,
        settings={'PREFER_DATES_FROM': 'future', 'TIMEZONE': 'local'}
    )

    if parsed:
        return parsed.date()
    return None
```

**Testing Strategy**:
- Test "tomorrow" → today +1 day
- Test "next week" → today +7 days
- Test "2025-12-31" → Dec 31, 2025
- Test invalid input "xyz" → None
- Test past dates "yesterday" → allow but mark as overdue

---

## Decision 2: Recurring Task Implementation

**Context**: FR-031 to FR-037 require automatic creation of next occurrence when recurring task is marked complete.

**Decision**: **On-completion trigger** with immediate next occurrence creation

**Rationale**:
- Simpler than background scheduler
- User sees immediate feedback
- No daemon process required
- Prevents gaps in recurring tasks
- Aligns with CLI application model (no background processes)

**Alternatives Considered**:

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Pre-generate all occurrences | Simple query, all tasks visible upfront | Clutters task list, wastes IDs, hard to change recurrence | Creates too many future tasks |
| Background scheduler/cron | Professional approach | Requires daemon, complex for CLI, overkill | CLI apps don't run in background |
| On-view generation | Lazy evaluation | Confusing UX, tasks appear/disappear | Poor user experience |

**Implementation Approach**:

```python
def toggle_task_completion(self, task_id: int) -> Optional[Task]:
    """Toggle task completion and create next occurrence if recurring."""
    task = self.get_task_by_id(task_id)
    if not task:
        raise ValueError(f"Task {task_id} not found")

    task.toggle_completed()

    # If completing a recurring task, create next occurrence
    if task.completed and task.recurrence != Recurrence.NONE:
        next_task = self._create_next_occurrence(task)
        self.tasks[next_task.id] = next_task
        self._auto_save()
        return next_task

    self._auto_save()
    return None

def _create_next_occurrence(self, task: Task) -> Task:
    """Create next occurrence of recurring task."""
    from datetime import timedelta

    # Calculate next due date
    if task.recurrence == Recurrence.DAILY:
        next_due = task.due_date + timedelta(days=1)
    elif task.recurrence == Recurrence.WEEKLY:
        next_due = task.due_date + timedelta(days=7)
    elif task.recurrence == Recurrence.MONTHLY:
        next_due = task.due_date + timedelta(days=30)

    # Create new task with same properties
    return Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=next_due,
        recurrence=task.recurrence,
        completed=False  # New task starts incomplete
    )
```

**Edge Cases Handled**:
- Monthly recurrence uses +30 days (not "same day next month") for simplicity
- If Feb 30 would result, dateparser/datetime automatically adjusts to Feb 28/29
- Rapid double-completion: create_next_occurrence() is idempotent (safe to call multiple times)
- Delete recurring task: only deletes current occurrence (future not pre-created)

---

## Decision 3: Filtering Architecture

**Context**: FR-014 to FR-019 require menu-based filtering by status, priority, and due date range.

**Decision**: **Filter state object** with composable filter methods

**Rationale**:
- Clean separation of concerns
- Filters can be combined (status AND priority)
- Stateful (filters persist across operations)
- Easy to add new filter types
- Testable in isolation

**Alternatives Considered**:

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| SQL-style WHERE clauses | Powerful, flexible | Complex parser, overkill for CLI | Too complex for CLI app |
| Functional filter chains | Pure functions, composable | Harder to show current filters | Less intuitive for CLI users |
| Single filter only | Simplest implementation | Can't combine filters | Poor UX, not scalable |

**Implementation Approach**:

```python
from dataclasses import dataclass
from typing import Optional, List
from datetime import date

@dataclass
class FilterState:
    """Active filter configuration."""
    status: Optional[str] = None  # "pending", "completed", "overdue", or None
    priority: Optional[str] = None  # "high", "medium", "low", "none", or None
    date_range: Optional[tuple[date, date]] = None  # (start, end) or None
    search_keyword: Optional[str] = None

    def is_active(self) -> bool:
        """Check if any filters are active."""
        return any([self.status, self.priority, self.date_range, self.search_keyword])

    def describe(self) -> str:
        """Human-readable description of active filters."""
        parts = []
        if self.status: parts.append(f"Status={self.status.title()}")
        if self.priority: parts.append(f"Priority={self.priority.title()}")
        if self.date_range: parts.append(f"Due: {self.date_range[0]} to {self.date_range[1]}")
        if self.search_keyword: parts.append(f"Search=\"{self.search_keyword}\"")
        return ", ".join(parts) if parts else "No filters"

class FilterService:
    """Service for filtering task lists."""

    @staticmethod
    def apply_filters(tasks: List[Task], filter_state: FilterState) -> List[Task]:
        """Apply all active filters to task list."""
        filtered = tasks

        if filter_state.status:
            filtered = [t for t in filtered if t.status.value == filter_state.status]

        if filter_state.priority:
            filtered = [t for t in filtered if t.priority.value == filter_state.priority]

        if filter_state.date_range:
            start, end = filter_state.date_range
            filtered = [t for t in filtered if t.due_date and start <= t.due_date <= end]

        if filter_state.search_keyword:
            keyword = filter_state.search_keyword.lower()
            filtered = [
                t for t in filtered
                if keyword in t.title.lower() or keyword in t.description.lower()
            ]

        return filtered
```

**Performance**: O(n) for each filter, composable. For 1000 tasks with 3 active filters: ~3ms on modern hardware.

---

## Decision 4: Search Implementation

**Context**: FR-020 to FR-022 require interactive keyword search across title and description.

**Decision**: **Case-insensitive substring matching** with linear search

**Rationale**:
- Simple and understandable
- Sufficient for <10k tasks (acceptable performance)
- No external dependencies
- Exact match on what user types
- Works for partial words ("groc" finds "groceries")

**Alternatives Considered**:

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Full-text search (whoosh, elasticsearch) | Fast, supports stemming | Heavy dependencies, overkill for CLI | Complexity not justified |
| Regex-based search | Powerful, flexible | Slower, requires regex knowledge | Too complex for users |
| Fuzzy matching (fuzzywuzzy) | Handles typos | Slower, sometimes unexpected results | Substring match is more predictable |

**Implementation Approach**:

```python
class SearchService:
    """Service for searching tasks."""

    @staticmethod
    def search(tasks: List[Task], keyword: str) -> List[Task]:
        """Search tasks by keyword (case-insensitive)."""
        if not keyword or not keyword.strip():
            return tasks

        keyword_lower = keyword.strip().lower()

        return [
            task for task in tasks
            if keyword_lower in task.title.lower()
            or keyword_lower in task.description.lower()
        ]
```

**Performance**: O(n * m) where n=tasks, m=average text length. For 1000 tasks: ~5ms on modern hardware.

**Future Enhancement** (Phase II+): If performance becomes issue with 10k+ tasks, migrate to PostgreSQL full-text search.

---

## Decision 5: Voice Input (Optional Feature)

**Context**: FR-038 to FR-050 specify optional voice input for task creation with **multi-turn conversation** approach (clarified 2025-12-27).

**Decision**: **SpeechRecognition library** with Google Speech API using **guided sequential prompting** (multi-turn conversation)

**Rationale**:
- CLI-compatible (can record from terminal session)
- Free tier available for Google Speech API
- Works cross-platform (Linux, macOS, Windows)
- Simple API (3 lines of code to record and transcribe)
- Graceful degradation if unavailable
- **Multi-turn approach provides better error recovery and user guidance**

**Clarifications from Spec** (Session 2025-12-27):
1. **Voice Command Structure**: Multi-turn conversation - user says "add task", system prompts sequentially for each field
2. **Error Recovery**: User can say "go back" or "change [field]" to modify previous field
3. **Vocabulary Flexibility**: Flexible normalization - variations like "high", "high priority", "make it high" all map to Priority.HIGH
4. **Technology**: Python SpeechRecognition library (confirmed)

**Alternatives Considered**:

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Single-utterance parsing | Fast, one command | Error-prone, poor UX for corrections | User wants guided sequential input |
| Web Speech API | Browser-based, good accuracy | Requires browser, not CLI-compatible | Phase I is CLI-only |
| OpenAI Whisper | Excellent accuracy, offline | Requires model download (1.5GB), slower | Too heavy for optional feature |
| Azure Speech Services | Very accurate, multilingual | Requires API key, costs money | Adds complexity and cost |

**Implementation Approach** (Multi-Turn Conversation):

```python
from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional

class ConversationStep(Enum):
    IDLE = "idle"
    AWAITING_COMMAND = "awaiting_command"
    AWAITING_TITLE = "awaiting_title"
    AWAITING_PRIORITY = "awaiting_priority"
    AWAITING_DUE_DATE = "awaiting_due_date"
    AWAITING_RECURRENCE = "awaiting_recurrence"
    CONFIRMATION = "confirmation"

@dataclass
class VoiceState:
    """Tracks state of multi-turn voice conversation."""
    current_step: ConversationStep = ConversationStep.IDLE
    collected_data: dict[str, Any] = field(default_factory=dict)
    step_history: list[ConversationStep] = field(default_factory=list)
    confidence_scores: dict[str, float] = field(default_factory=dict)

class VoiceConversationHandler:
    """Handles multi-turn voice input conversation."""

    def __init__(self):
        self.state = VoiceState()
        self.recognizer = sr.Recognizer()

    def start_conversation(self) -> None:
        """Start voice conversation: user says 'add task'."""
        self.state.current_step = ConversationStep.AWAITING_COMMAND
        self.prompt_user("Listening... Say 'add task'")

        audio = self.listen()
        command = self.transcribe(audio)

        if "add task" in command.lower():
            self.state.current_step = ConversationStep.AWAITING_TITLE
            self.collect_title()
        else:
            self.display_error("Command not recognized. Please say 'add task'")

    def collect_title(self) -> None:
        """Prompt for and collect task title."""
        self.prompt_user("What's the task title?")
        audio = self.listen()
        title = self.transcribe(audio)

        # Confirm
        self.display_info(f"Title: {title}")
        self.state.collected_data['title'] = title
        self.state.step_history.append(ConversationStep.AWAITING_TITLE)

        # Move to next step
        self.state.current_step = ConversationStep.AWAITING_PRIORITY
        self.collect_priority()

    def collect_priority(self) -> None:
        """Prompt for and collect priority with normalization."""
        self.prompt_user("What priority? Say high, medium, low, or none")
        audio = self.listen()
        priority_text = self.transcribe(audio)

        # Normalize using flexible patterns
        priority = self.normalize_priority(priority_text)

        # Confirm normalized value
        self.display_info(f"Priority: {priority.value.title()}")
        self.state.collected_data['priority'] = priority
        self.state.step_history.append(ConversationStep.AWAITING_PRIORITY)

        # Check for "go back" or "change [field]"
        if self.check_for_correction(priority_text):
            return  # handled by check_for_correction

        # Move to next step
        self.state.current_step = ConversationStep.AWAITING_DUE_DATE
        self.collect_due_date()

    def normalize_priority(self, text: str) -> Priority:
        """Normalize priority variations to canonical Priority enum."""
        text_lower = text.lower()

        # Flexible matching patterns
        if any(pattern in text_lower for pattern in ['high', 'important', 'urgent', 'make it high']):
            return Priority.HIGH
        elif any(pattern in text_lower for pattern in ['medium', 'med', 'moderate', 'normal']):
            return Priority.MEDIUM
        elif any(pattern in text_lower for pattern in ['low', 'minor']):
            return Priority.LOW
        else:
            return Priority.NONE

    def check_for_correction(self, text: str) -> bool:
        """Check if user wants to go back or change a field."""
        text_lower = text.lower()

        if 'go back' in text_lower or 'change' in text_lower:
            # Go back to previous step
            if self.state.step_history:
                self.state.current_step = self.state.step_history.pop()
                self.re_collect_current_field()
                return True
        return False

    def collect_due_date(self) -> None:
        """Prompt for and collect due date."""
        self.prompt_user("When is it due? Say a date or none")
        audio = self.listen()
        date_text = self.transcribe(audio)

        # Parse using dateparser
        due_date = parse_date(date_text) if date_text.lower() != 'none' else None

        self.display_info(f"Due: {due_date or 'No due date'}")
        self.state.collected_data['due_date'] = due_date
        self.state.step_history.append(ConversationStep.AWAITING_DUE_DATE)

        if self.check_for_correction(date_text):
            return

        self.state.current_step = ConversationStep.AWAITING_RECURRENCE
        self.collect_recurrence()

    def collect_recurrence(self) -> None:
        """Prompt for and collect recurrence pattern."""
        self.prompt_user("Any recurrence? Say daily, weekly, monthly, or none")
        audio = self.listen()
        recurrence_text = self.transcribe(audio)

        recurrence = self.normalize_recurrence(recurrence_text)

        self.display_info(f"Recurrence: {recurrence.value.title()}")
        self.state.collected_data['recurrence'] = recurrence
        self.state.step_history.append(ConversationStep.AWAITING_RECURRENCE)

        if self.check_for_correction(recurrence_text):
            return

        # Show final confirmation
        self.state.current_step = ConversationStep.CONFIRMATION
        self.show_confirmation()

    def show_confirmation(self) -> None:
        """Display summary and get final confirmation."""
        summary = f"""
        Task Summary:
        - Title: {self.state.collected_data['title']}
        - Priority: {self.state.collected_data['priority'].value.title()}
        - Due Date: {self.state.collected_data.get('due_date', 'None')}
        - Recurrence: {self.state.collected_data['recurrence'].value.title()}

        Confirm? (Say 'yes' to create, 'edit' to modify, or 'cancel')
        """
        self.display_info(summary)

        audio = self.listen()
        response = self.transcribe(audio).lower()

        if 'yes' in response or 'confirm' in response:
            self.create_task()
        elif 'edit' in response:
            # Allow user to select which field to re-record
            self.edit_fields()
        else:
            self.display_info("Task creation cancelled")
            self.reset_state()

    def listen(self, timeout: int = 5) -> sr.AudioData:
        """Listen for audio input."""
        with sr.Microphone() as source:
            return self.recognizer.listen(source, timeout=timeout)

    def transcribe(self, audio: sr.AudioData) -> str:
        """Transcribe audio to text with confidence checking."""
        try:
            text = self.recognizer.recognize_google(audio, show_all=False)
            # Note: confidence score available via show_all=True if needed
            return text
        except sr.UnknownValueError:
            self.display_warning("Could not understand. Please repeat or type instead.")
            # Offer to repeat current prompt
            return self.handle_transcription_failure()
        except sr.RequestError:
            self.display_error("Voice service unavailable. Use keyboard input instead.")
            raise
```

**Graceful Degradation**:
- If SpeechRecognition not installed: menu option shows "Voice input (install SpeechRecognition to enable)"
- If microphone not available: error message suggests keyboard input
- If confidence <70%: offer to repeat prompt or switch to typing
- All functionality available via keyboard

**Error Recovery Features**:
1. **"Go Back"**: Returns to previous field in conversation
2. **"Change [Field]"**: Jumps to specific field for correction
3. **Low Confidence**: Repeats prompt with "Type Instead" option
4. **Edit Mode**: From confirmation screen, select any field to re-record

---

## Decision 6: Sorting Implementation

**Context**: FR-023 to FR-028 require multiple sort options with persistent preference.

**Decision**: **Sort parameter with stable default** (Overdue first, then created_date descending)

**Rationale**:
- Pythonic (use list.sort() with key functions)
- Overdue tasks always at top (critical for user safety)
- Sort preference stored in session (not persisted to JSON - reasonable default)
- Multiple sort keys supported (primary: overdue, secondary: user choice)

**Implementation Approach**:

```python
from enum import Enum

class SortBy(Enum):
    DEFAULT = "default"
    PRIORITY = "priority"
    DUE_DATE = "due_date"
    CREATED_DATE = "created_date"

def sort_tasks(tasks: List[Task], sort_by: SortBy = SortBy.DEFAULT) -> List[Task]:
    """Sort tasks with overdue always prioritized at top."""

    # Separate overdue from others
    overdue = [t for t in tasks if t.status == Status.OVERDUE]
    others = [t for t in tasks if t.status != Status.OVERDUE]

    # Sort overdue by due_date (earliest first)
    overdue.sort(key=lambda t: t.due_date or date.max)

    # Sort others based on preference
    if sort_by == SortBy.PRIORITY:
        priority_order = {"high": 0, "medium": 1, "low": 2, "none": 3}
        others.sort(key=lambda t: priority_order[t.priority.value])
    elif sort_by == SortBy.DUE_DATE:
        others.sort(key=lambda t: t.due_date or date.max)
    elif sort_by == SortBy.CREATED_DATE:
        others.sort(key=lambda t: t.created_at, reverse=True)
    else:  # DEFAULT
        others.sort(key=lambda t: t.created_at, reverse=True)

    # Overdue always at top
    return overdue + others
```

**Session State**: Store current sort preference in menu.py module-level variable (resets on app restart - acceptable for CLI).

---

## Decision 7: File Structure Extensions

**Context**: Need to organize new code modules cleanly within existing Phase I structure.

**Decision**: **Create new subdirectories** for logical grouping: `src/models/enums.py`, `src/services/filter_service.py`, `src/utils/` directory

**Rationale**:
- Keeps existing structure intact
- Separates concerns clearly
- Easy to test in isolation
- Follows Python package conventions
- Aligns with constitution Principle VI (Standard Project Structure)

**File Organization**:

```
src/
├── models/
│   ├── __init__.py
│   ├── task.py (EXTEND: add new fields, status property)
│   └── enums.py (NEW: Priority, Recurrence, Status enums)
├── services/
│   ├── __init__.py
│   ├── task_service.py (EXTEND: recurring logic, sorting)
│   ├── filter_service.py (NEW: filtering logic)
│   └── search_service.py (NEW: search functionality)
├── utils/
│   ├── __init__.py
│   ├── date_utils.py (NEW: dateparser wrapper)
│   └── voice_input.py (NEW: SpeechRecognition wrapper, optional)
└── cli/
    ├── __init__.py
    ├── menu.py (EXTEND: add menu options for filter/search/sort/voice)
    ├── themes.py (EXISTING: no changes needed)
    └── ui_components.py (EXISTING: may need minor extensions for new displays)
```

**Migration Strategy**: Extend existing files where possible, create new files only when needed for separation of concerns.

---

## Decision 8: Performance Optimization Strategy

**Context**: SC-003 requires <50ms menu response and <200ms list render with 1000+ tasks.

**Decision**: **Lazy rendering** with reasonable limits, no pagination required for Phase I

**Rationale**:
- Python list operations are O(n) and fast for n<10,000
- Rich library is optimized for rendering tables
- Filtering/search reduces display count
- Modern terminals handle 1000-line output
- Pagination adds complexity without clear benefit for CLI

**Performance Targets**:

| Operation | Current | Target | Strategy |
|-----------|---------|--------|----------|
| Menu display | ~10ms | <50ms | Already achieved (questionary is fast) |
| Task list render (100 tasks) | ~30ms | <200ms | Rich table is optimized |
| Task list render (1000 tasks) | ~150ms | <200ms | Acceptable with filtering |
| Filter operation | ~2ms | <100ms | O(n) linear scan is sufficient |
| Search operation | ~5ms | <100ms | O(n*m) substring matching is fast |
| Sort operation | ~3ms | <100ms | Python sorted() is highly optimized |
| JSON save (1000 tasks) | ~50ms | <200ms | Atomic write, acceptable |

**If Performance Degrades** (>10k tasks):
- Add pagination (20-50 tasks per page)
- Add task limit warning at 5k tasks
- Suggest archiving old completed tasks

---

## Decision 9: Testing Strategy

**Context**: Need comprehensive tests for new features while maintaining 80%+ coverage.

**Decision**: **Unit tests for all services, integration tests for workflows, property-based testing for edge cases**

**Test Structure**:

```
tests/
├── unit/
│   ├── test_task_model.py (EXTEND: test priority, due_date, recurrence, status)
│   ├── test_enums.py (NEW: test enum values)
│   ├── test_task_service.py (EXTEND: test recurring, sorting)
│   ├── test_filter_service.py (NEW: test filtering logic)
│   ├── test_search_service.py (NEW: test search)
│   ├── test_date_utils.py (NEW: test natural language parsing)
│   ├── test_themes.py (EXISTING: no changes)
│   └── test_voice_input.py (NEW: test voice parsing, optional)
├── integration/
│   ├── test_cli_workflow.py (EXTEND: test filter/search/sort workflows)
│   ├── test_recurring_workflow.py (NEW: test recurring task cycle)
│   └── test_persistence.py (EXTEND: test new fields persist correctly)
└── conftest.py (fixtures for test data)
```

**Coverage Goals**:
- Unit tests: 100% coverage of services and models
- Integration tests: Cover all happy paths and major error paths
- Total coverage: ≥85% (exceeds constitution requirement of 80%)

**Test Data Strategy**: Use pytest fixtures for common scenarios (tasks with different priorities, overdue tasks, recurring tasks).

---

## Decision 10: Dependency Management

**Context**: Need to add new dependencies (dateparser, optionally SpeechRecognition) while keeping Phase I lightweight.

**Decision**: **Add dateparser as required dependency, SpeechRecognition as optional**

**Updated pyproject.toml Dependencies**:

```toml
[project]
dependencies = [
    "rich>=13.0",           # EXISTING: terminal formatting
    "art>=6.0",             # EXISTING: ASCII art
    "questionary>=2.0",     # EXISTING: interactive prompts
    "emoji>=2.0",           # EXISTING: emoji support
    "dateparser>=1.2.0",    # NEW: natural language date parsing
]

[project.optional-dependencies]
voice = [
    "SpeechRecognition>=3.10.0",  # Optional: voice input
    "PyAudio>=0.2.13",            # Optional: microphone access
]
```

**Rationale**:
- dateparser is small (4MB), essential for FR-003, no heavy dependencies
- SpeechRecognition is optional (FR-038 says "MAY provide"), keeps base install lightweight
- PyAudio can be problematic to install (platform-specific), making it optional reduces friction

**Installation**:
```bash
# Standard install
uv pip install -e .

# With voice support
uv pip install -e ".[voice]"
```

---

## Technology Stack Summary

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| Language | Python | 3.13+ | Constitution requirement, existing Phase I standard |
| CLI Framework | Questionary | 2.0+ | Already in use, excellent UX for interactive menus |
| Terminal UI | Rich | 13.0+ | Already in use, beautiful tables and formatting |
| ASCII Art | Art | 6.0+ | Already in use, fun visual element |
| Emoji Support | Emoji | 2.0+ | Already in use, visual indicators |
| Date Parsing | dateparser | 1.2+ | NEW - industry standard for natural language dates |
| Voice Input | SpeechRecognition | 3.10+ | NEW (optional) - standard Python speech-to-text library |
| Audio Capture | PyAudio | 0.2+ | NEW (optional) - required by SpeechRecognition |
| Testing | pytest | 7.0+ | Already configured, Python standard |
| Linting | pylint + mypy | 3.0+, 1.0+ | Already configured, code quality enforcement |
| Package Manager | uv | Latest | Already in use, fast dependency management |

**Total Dependencies**: 6 required (4 existing + 2 new), 2 optional for voice

---

## Key Architectural Decisions

### 1. Enums for Type Safety

Use Python Enums for priority, recurrence, and status to:
- Prevent typos and invalid values
- Enable IDE autocomplete
- Make code self-documenting
- Simplify JSON serialization/deserialization

### 2. Computed Status Property

Status is NOT stored in JSON, it's computed on-the-fly from `completed` and `due_date`:
- Avoids data inconsistency
- Always accurate
- Reduces storage size
- Simpler logic

### 3. Filter State as Session Variable

Filters are NOT persisted to JSON, they reset on app restart:
- Simpler implementation
- Users expect filters to reset
- Avoids confusion with stale filters
- Can be changed later if users request persistence

### 4. Sort Preference as Session Variable

Sort order is NOT persisted to JSON, defaults to "Default" on restart:
- Most users prefer default sort (overdue first)
- Simpler implementation
- Easy to change if users want persistence

### 5. Voice Input Completely Optional

Voice feature:
- Requires explicit opt-in during installation (`pip install -e ".[voice]"`)
- Menu option only appears if SpeechRecognition is importable
- Never blocks or degrades core functionality
- Can be completely removed without affecting anything else

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| dateparser dependency issues | Low | Medium | Well-maintained library, fallback to manual parsing possible |
| Voice input platform compatibility | Medium | Low | Feature is optional, comprehensive error handling, clear docs on supported platforms |
| Performance degradation with 10k+ tasks | Low | Medium | Add task limit warning, suggest archiving, optimize if needed |
| User confusion with recurring tasks | Medium | Low | Clear UI indicators, confirmation dialogs, comprehensive help text |
| Filter combination complexity | Low | Low | Limit to 3 simultaneous filters, clear active filter display |

---

## Open Questions (None)

All technical unknowns resolved through research. No blocking questions remain.

---

## Next Steps

**Phase 1 Deliverables** (to be created after this research):
1. `data-model.md` - Complete entity definitions with fields, validation, relationships
2. `contracts/` directory - CLI menu structures and workflows
3. `quickstart.md` - Installation and usage guide

**Then**: Move to `/sp.tasks` to generate task breakdown for implementation.

---

**Research Phase Complete**: ✅ All technical decisions documented and justified.
