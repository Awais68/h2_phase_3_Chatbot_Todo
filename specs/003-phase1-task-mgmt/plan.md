# Implementation Plan: Phase I Complete Task Management System

**Branch**: `003-phase1-task-mgmt` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-phase1-task-mgmt/spec.md`

## Summary

Build a comprehensive CLI-based task management system with core CRUD operations (create, read, update, delete, complete/incomplete toggle), advanced filtering/search/sorting capabilities, recurring task support, and optional voice input using multi-turn conversation. The system will use Python 3.13+ with in-memory JSON persistence, Python SpeechRecognition library for voice input, and Rich library for terminal formatting. Voice commands use a guided sequential prompting approach where users are walked through each field (title → priority → due date → recurrence) with confirmation and error recovery capabilities.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**:
- Rich 13.0+ (terminal formatting, tables, colors)
- SpeechRecognition 3.10+ (voice input via Google Speech Recognition API)
- PyAudio (microphone access for voice input)
- python-dateutil (natural language date parsing)

**Storage**: JSON file (`tasks.json`) with in-memory caching during runtime
**Testing**: pytest 8.0+ with pytest-cov for coverage reporting
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows) with terminal support for 256 colors
**Project Type**: Single-project CLI application with modular architecture
**Performance Goals**:
- Menu response <50ms
- List rendering <200ms for 1000+ tasks
- Voice recognition latency <2s per field
- Filter/search operations <100ms

**Constraints**:
- Maximum 10,000 tasks for guaranteed performance
- Terminal width minimum 80 characters
- Internet connection required for voice input (Google Speech Recognition API)
- Microphone hardware required for voice input (optional feature)
- English language only for voice commands

**Scale/Scope**: Single-user CLI application with 6 major feature areas (Core Task Management, Filtering/Search, Recurring Tasks, Sorting, Voice Input, Visual Enhancements)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development First
✅ **PASS** - Full specification exists with user stories, acceptance criteria, clarifications

### Principle II: Simplicity and Clean Code
✅ **PASS** - Architecture uses standard Python patterns, modular structure, clear separation of concerns

### Principle III: User Experience Excellence
✅ **PASS** - CLI design includes clear prompts, menu-based navigation, helpful error messages, visual formatting. Voice input adds hands-free convenience with guided multi-turn conversation

### Principle IV: Data Integrity and Validation
✅ **PASS** - Comprehensive validation rules defined (title 1-200 chars, description max 1000 chars, priority enum, date validation, recurrence constraints)

### Principle V: Modularity and Testability
✅ **PASS** - Clear separation: models (Task, Filter, SortOption), services (TaskService, VoiceService), CLI (menu, voice, formatter), lib (utilities)

### Principle VI: Standard Project Structure
✅ **PASS** - Following Python best practices: src/ for code, tests/ for test suite, pyproject.toml for dependencies

### Principle VII: Python Code Quality Standards
✅ **PASS** - Will require type hints, docstrings, linting (pylint/flake8 ≥8.0), type checking (mypy)

### Principle VIII: CLI Interface Excellence
✅ **PASS** - Interactive menu mode, numbered options, visual separators, color coding, emoji indicators, graceful Ctrl+C handling

### Principle IX: Performance and Resource Efficiency
✅ **PASS** - Performance targets defined: <50ms menu, <200ms list render, <100ms operations, supports 1000+ tasks

### Principle X: Version Control and Documentation
✅ **PASS** - Git repository, commit conventions, README, CLAUDE.md documentation planned

**Overall Status**: ✅ ALL GATES PASSED - Proceed to Phase 0 Research

---

## Phase 0: Research & Technology Decisions

### Research Findings

#### Decision 1: Voice Recognition Engine
- **Choice**: Google Speech Recognition API (default engine in SpeechRecognition library)
- **Rationale**: Best accuracy for English speech, easy setup (no API key needed for basic use), supports multiple languages
- **Alternative**: PocketSphinx (offline, lower accuracy), Wit.ai (requires API key)

#### Decision 2: Date Parsing Library
- **Choice**: python-dateutil
- **Rationale**: Robust natural language parsing ("tomorrow", "next week"), active maintenance, comprehensive format support
- **Alternative**: dateparser (heavier, more dependencies), manual parsing (more code, less flexible)

#### Decision 3: Terminal Formatting
- **Choice**: Rich library
- **Rationale**: Beautiful tables with auto-layout, progress bars, syntax highlighting, theme support, actively maintained
- **Alternative**: Plain text (simpler but less visual appeal), colorama (colors only, no tables)

#### Decision 4: CLI Framework
- **Choice**: questionary for prompts + custom menu system
- **Rationale**: questionary provides clean interactive prompts, custom menu for better control over menu flow
- **Alternative**: inquirer (more features but heavier), click (command-based not menu-based)

---

## Phase 1: Data Model & Architecture

### Entity: Task

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | int | Unique, auto-increment, >0 | Auto-generated | Unique identifier, never reused |
| title | str | Required, 1-200 chars | None | Brief task description |
| description | str | Optional, max 1000 chars | "" | Detailed task information |
| completed | bool | Required | False | Completion status |
| priority | enum | HIGH, MEDIUM, LOW, NONE | NONE | Priority level |
| due_date | date or null | Optional | None | Due date for task |
| recurrence | enum | NONE, DAILY, WEEKLY, MONTHLY | NONE | Recurrence pattern |
| created_at | datetime | Auto-generated, UTC | Current timestamp | Creation time |
| updated_at | datetime | Auto-updated, UTC | Current timestamp | Last modification |
| status | computed | PENDING, COMPLETED, OVERDUE | - | Derived from completed + due_date |

### Entity: Theme

| Field | Type | Description |
|-------|------|-------------|
| name | str | Theme name (dark, light, hacker) |
| primary | str | Primary accent color |
| secondary | str | Secondary accent color |
| success | str | Success state color |
| warning | str | Warning state color |
| error | str | Error state color |
| info | str | Info state color |
| text | str | Default text color |
| muted | str | Muted text color |

### Entity: FilterState

| Field | Type | Description |
|-------|------|-------------|
| status_filter | enum or null | Filter by status |
| priority_filter | enum or null | Filter by priority |
| date_range | enum or null | Filter by date range |
| search_keyword | str or null | Search term |

### Entity: VoiceState

| Field | Type | Description |
|-------|------|-------------|
| current_step | enum | Current conversation step |
| collected_data | dict | Fields collected so far |
| step_history | list | History of completed steps |
| confidence | float | Last transcription confidence |

---

## Project Structure

### Documentation (this feature)

```text
specs/003-phase1-task-mgmt/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── cli-interface.md
│   └── voice-interface.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── main.py                    # Application entry point
├── models/
│   ├── __init__.py
│   ├── task.py                # Task dataclass with validation
│   ├── filter.py              # Filter state model
│   ├── sort_option.py         # Sort preference model
│   ├── voice_state.py         # Voice conversation state machine
│   └── theme.py               # Theme configuration
├── services/
│   ├── __init__.py
│   ├── task_service.py        # CRUD operations, filtering, sorting
│   ├── recurring_service.py   # Recurring task logic
│   ├── voice_service.py       # Speech recognition + multi-turn conversation
│   ├── voice_normalizer.py    # Voice input normalization ("high priority" → Priority.HIGH)
│   └── persistence_service.py # JSON file I/O
├── cli/
│   ├── __init__.py
│   ├── menu.py                # Interactive keyboard menu
│   ├── voice_menu.py          # Voice command handler
│   ├── formatter.py           # Rich table formatting
│   └── prompts.py             # Input prompts and validation
└── lib/
    ├── __init__.py
    ├── date_parser.py         # Natural language date parsing
    ├── validators.py          # Input validation utilities
    └── exceptions.py          # Custom exception classes

tests/
├── __init__.py
├── conftest.py                # Pytest fixtures
├── unit/
│   ├── test_task_model.py
│   ├── test_filter_model.py
│   ├── test_voice_state.py
│   ├── test_task_service.py
│   ├── test_recurring_service.py
│   ├── test_voice_normalizer.py
│   ├── test_date_parser.py
│   └── test_validators.py
├── integration/
│   ├── test_cli_menu.py
│   ├── test_voice_flow.py     # Multi-turn conversation tests
│   └── test_persistence.py
└── contract/
    ├── test_cli_interface.py
    └── test_voice_interface.py
```

**Structure Decision**: Selected **Single Project** structure (Option 1) as this is a CLI application with no web/mobile components. The structure follows Python best practices with clear separation between models (data), services (business logic), CLI (presentation), and lib (utilities). Voice functionality is integrated as a service layer with its own menu handler, keeping concerns separate while maintaining cohesive voice conversation flow.

---

## CLI Interface Contracts

### Main Menu Options

| Option | Action | Description |
|--------|--------|-------------|
| 1 | Add Task | Create new task with prompts |
| 2 | View Tasks | Display task list with filters/sort |
| 3 | Update Task | Edit existing task |
| 4 | Delete Task | Remove task with confirmation |
| 5 | Complete Task | Toggle completion status |
| 6 | Filter/Search | Filter tasks or search by keyword |
| 7 | Sort Tasks | Change sort order |
| 8 | Voice Input | (Optional) Launch voice conversation |
| 9 | Change Theme | Switch color theme |
| 0 | Exit | Save and quit |

### Add Task Flow

```
1. Enter title (required, 1-200 chars)
2. Enter description (optional, max 1000 chars)
3. Select priority (High/Medium/Low/None)
4. Enter due date (optional, natural language supported)
5. Select recurrence (None/Daily/Weekly/Monthly)
6. Confirm and create task
```

### Voice Conversation Flow

```
1. System: "Listening... Say 'add task'"
2. User: "add task"
3. System: "What task title?" (listening)
4. User: [title phrase]
5. System: "Title: [recognized]. What priority? Say high, medium, low, or none"
6. User: [priority phrase]
7. System: "Priority: [normalized]. When is it due?"
8. ...continues for due date, recurrence...
9. System: Shows confirmation summary
10. User: "Confirm" or "Edit [field]"
11. Task created
```

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. All constitution principles can be satisfied without exceptions.

---

## Next Steps

1. **Run `/sp.tasks`** to generate implementation task breakdown
2. **Run `/sp.implement`** to execute tasks phase-by-phase
3. **Quality Gates**: mypy (0 errors), pylint (≥8.0), pytest (100% pass), coverage (≥80%)
