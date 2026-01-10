# Implementation Plan: System Architecture for Phase I Console Application

**Branch**: `001-system-architecture` | **Date**: 2025-12-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-system-architecture/spec.md`

## Summary

Design and implement a modular, layered architecture for a Phase I console-based task management application. The architecture separates concerns across 5 distinct layers (data, storage, business logic, presentation, entry point) to enable independent testing, future extensibility, and clean code practices. Uses Python 3.8+ with in-memory storage, type hints throughout, and follows PEP 8 guidelines.

**Primary Goal**: Establish architectural foundation that supports all CRUD operations while being easily swappable for future phases (database persistence, web UI, AI integration, cloud deployment).

## Technical Context

**Language/Version**: Python 3.8+
**Primary Dependencies**: Python standard library only (no external dependencies for core functionality)
**Storage**: In-memory (Python dict/list)
**Testing**: pytest (optional but recommended for quality assurance)
**Target Platform**: Console/Terminal (Linux, macOS, Windows)
**Project Type**: Single (console application)
**Performance Goals**:
- Startup: <1 second
- Operations: <100ms each
- Support: 1000+ tasks without degradation
- Memory: <50MB for typical usage (≤100 tasks)

**Constraints**:
- No persistent storage (data lost on exit)
- Single-user, single-session model
- Terminal-based interaction only
- Type hints required for all functions
- 100% code generation via Claude Code (no manual coding)

**Scale/Scope**:
- 5 basic CRUD operations (add, view, update, delete, toggle status)
- 5 distinct architectural layers
- ~500-800 lines of code total
- 80%+ test coverage target

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Compliance

✅ **I. Spec-Driven Development First (NON-NEGOTIABLE)**
- Feature has complete specification in spec.md
- All code will be Claude Code generated
- No manual coding permitted
- STATUS: **PASS** - Spec complete, ready for implementation

✅ **II. Simplicity and Clean Code**
- Using simplest viable approach: in-memory dict/list storage
- PEP 8 compliance required
- Type hints on all functions
- Docstrings required
- Max 20 lines per function
- STATUS: **PASS** - Architecture favors simplicity

✅ **III. User Experience Excellence**
- Clear CLI prompts for all inputs
- Meaningful error messages
- Formatted output (tables, status indicators)
- Confirmation for destructive operations
- STATUS: **PASS** - UX requirements in spec

✅ **IV. Data Integrity and Validation**
- Unique auto-incrementing task IDs
- Input validation before processing
- No ID reuse
- Timestamps automatically managed
- Title: 1-200 chars, Description: 0-1000 chars
- STATUS: **PASS** - Validation rules defined

✅ **V. Modularity and Testability**
- 5 distinct layers with clear separation
- Pure functions where possible
- Dependency injection for testability
- 80%+ test coverage target
- pytest framework
- Independent tests (no shared state)
- STATUS: **PASS** - Modular architecture specified

✅ **VI. Standard Project Structure**
- Following Python best practices
- src/ for source code
- tests/ for test suite
- Clear module organization
- STATUS: **PASS** - Structure defined below

✅ **VII. Python Code Quality Standards**
- Type checking with mypy (zero errors)
- Linting with pylint/flake8 (score ≥8.0)
- Docstrings on all functions
- Try-except for exception handling
- No print() for debugging (use logging)
- STATUS: **PASS** - Quality standards clear

✅ **VIII. CLI Interface Excellence**
- Interactive menu mode as primary interface
- Numbered menu options
- Visual separators for readability
- Status indicators (✓, ✗, •)
- Graceful Ctrl+C handling
- STATUS: **PASS** - CLI requirements defined

✅ **IX. Performance and Resource Efficiency**
- Startup <1s, operations <100ms
- Support 1000+ tasks
- Memory <50MB typical usage
- No memory leaks
- STATUS: **PASS** - Targets established

✅ **X. Version Control and Documentation**
- Git for version control
- Meaningful commit messages
- README with setup/usage
- CLAUDE.md with instructions
- STATUS: **PASS** - Documentation requirements clear

### Constitution Gates Summary

**Overall Status**: ✅ **ALL GATES PASS**

No violations detected. Architecture aligns perfectly with all 10 constitution principles. Ready to proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/001-system-architecture/
├── spec.md              # Feature specification (COMPLETE)
├── plan.md              # This file (IN PROGRESS)
├── research.md          # Phase 0: Research findings (TO BE CREATED)
├── data-model.md        # Phase 1: Data model specification (TO BE CREATED)
├── quickstart.md        # Phase 1: Getting started guide (TO BE CREATED)
├── contracts/           # Phase 1: Function/interface contracts (TO BE CREATED)
│   ├── models.md        # Task data model contract
│   ├── storage.md       # Storage interface contract
│   ├── operations.md    # Business logic contracts
│   └── ui.md            # UI function contracts
└── checklists/
    └── requirements.md  # Spec quality checklist (COMPLETE)
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package initialization
├── main.py              # Application entry point (20-40 lines)
├── models/              # Data layer
│   ├── __init__.py
│   └── task.py          # Task dataclass with validation (50-80 lines)
├── storage/             # Storage layer
│   ├── __init__.py
│   └── task_storage.py  # In-memory storage manager (80-120 lines)
├── operations/          # Business logic layer
│   ├── __init__.py
│   └── task_ops.py      # CRUD operations (150-200 lines)
└── ui/                  # Presentation layer
    ├── __init__.py
    ├── menu.py          # CLI menu system (100-150 lines)
    └── formatter.py     # Output formatting (80-120 lines)

tests/
├── __init__.py
├── conftest.py          # pytest fixtures (30-50 lines)
├── contract/            # Contract tests (verify interfaces)
│   ├── test_storage_contract.py
│   └── test_operations_contract.py
├── integration/         # Integration tests
│   └── test_full_workflow.py  # End-to-end scenarios (100-150 lines)
└── unit/                # Unit tests
    ├── test_task_model.py     # Task model tests (100-150 lines)
    ├── test_task_storage.py   # Storage tests (150-200 lines)
    ├── test_task_ops.py       # Operations tests (200-300 lines)
    └── test_ui.py             # UI tests (100-150 lines)

.specify/                # Spec-Kit Plus (already exists)
history/                 # Development history (already exists)
pyproject.toml           # UV project configuration
README.md                # Project documentation
CLAUDE.md                # Claude Code instructions
.gitignore               # Git ignore patterns
```

**Structure Decision**: **Option 1: Single Project**

Rationale: Phase I is a console application with no separate frontend/backend or mobile components. A single src/ directory with clear module separation (models, storage, operations, ui) provides the clearest organization for this scope.

**Layer Responsibilities**:

1. **Data Layer** (`src/models/`): Defines Task entity, field types, validation logic. Pure data structures with no external dependencies.

2. **Storage Layer** (`src/storage/`): Manages in-memory task collection, generates unique IDs, provides CRUD interface. Single source of truth during session.

3. **Business Logic Layer** (`src/operations/`): Implements CRUD operations, input validation, business rules enforcement, error handling. Independent of storage implementation (uses dependency injection).

4. **Presentation Layer** (`src/ui/`): Handles CLI menu display, user input collection, output formatting, user feedback messages. Independent of business logic.

5. **Application Entry Point** (`src/main.py`): Initializes storage, displays menu loop, routes user choices to operations, handles graceful exit. Minimal orchestration only.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All complexity is justified by functional requirements:
- 5 layers are necessary for separation of concerns and future extensibility
- Type hints are required by constitution for code quality
- In-memory storage is the simplest viable approach for Phase I

## Phase 0: Research Plan

### Research Tasks

**R001: Python Data Structures for Task Storage**
- **Question**: What's the best in-memory data structure for storing tasks?
- **Options**:
  - List of dicts
  - List of dataclasses
  - Dict with ID keys
  - OrderedDict for insertion order
- **Research Focus**:
  - Performance characteristics (add, delete, lookup by ID)
  - Type safety and validation support
  - Serialization readiness for future phases
  - Developer ergonomics and readability
- **Deliverable**: Recommendation with rationale in research.md

**R002: ID Generation Strategy**
- **Question**: How to generate unique, auto-incrementing IDs that are never reused?
- **Options**:
  - Simple counter with deleted ID tracking
  - UUID (overkill but future-proof)
  - Timestamp-based IDs
  - Database-style sequences
- **Research Focus**:
  - Uniqueness guarantees
  - ID reuse prevention
  - Performance overhead
  - Simplicity vs future-proofing
- **Deliverable**: ID generation algorithm specification in research.md

**R003: Type Hints Best Practices**
- **Question**: What type hint patterns work best for this architecture?
- **Options**:
  - dataclass vs TypedDict
  - Optional vs Union[T, None]
  - Protocol vs ABC for interfaces
  - NewType for ID types
- **Research Focus**:
  - mypy compatibility
  - Runtime overhead
  - Code readability
  - IDE support
- **Deliverable**: Type hint style guide for project in research.md

**R004: CLI Input Validation Patterns**
- **Question**: How to validate user input gracefully in CLI context?
- **Options**:
  - Try-except with custom exceptions
  - Validator functions returning Result types
  - Decorator-based validation
  - Inline validation with early returns
- **Research Focus**:
  - Error message clarity
  - Code maintainability
  - Testability
  - User experience
- **Deliverable**: Validation pattern specification in research.md

**R005: Testing Strategy for Layered Architecture**
- **Question**: How to test each layer independently while ensuring integration?
- **Options**:
  - Pure unit tests only
  - Unit + integration + contract tests
  - Mock-based vs state-based testing
  - Fixture vs builder patterns
- **Research Focus**:
  - Test isolation
  - Test maintainability
  - Coverage metrics
  - Execution speed
- **Deliverable**: Testing strategy document in research.md

### Research Deliverable: research.md

Structure:
```markdown
# Research Findings: System Architecture

## R001: Python Data Structures for Task Storage
- **Decision**: [chosen approach]
- **Rationale**: [why chosen]
- **Alternatives Considered**: [what else evaluated]
- **Code Example**: [brief snippet]

## R002: ID Generation Strategy
[same structure]

## R003: Type Hints Best Practices
[same structure]

## R004: CLI Input Validation Patterns
[same structure]

## R005: Testing Strategy for Layered Architecture
[same structure]

## Summary
- Key architectural patterns decided
- Technology choices justified
- No blockers identified
```

## Phase 1: Design Artifacts

### 1. Data Model Specification (data-model.md)

**Content**:
- Task entity definition with all fields
- Field types, constraints, defaults
- Validation rules
- State transitions (pending ↔ completed)
- Relationships (none in Phase I, document for future)

**Example Structure**:
```markdown
# Data Model: Task Entity

## Fields

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | int | unique, auto-inc, >0 | auto | Unique identifier |
| title | str | 1-200 chars, required | none | Task title |
| description | str | max 1000 chars | "" | Task details |
| completed | bool | required | False | Completion status |
| created_at | datetime | auto-gen, UTC | now | Creation time |
| updated_at | datetime | auto-gen, UTC | now | Last update time |

## Validation Rules

1. Title: strip() then check 1-200 length
2. Description: check ≤1000 length
3. ID: never reuse, always increment
4. Timestamps: auto-managed, immutable (created_at)

## Python Implementation

dataclass Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime
    updated_at: datetime
```

### 2. API Contracts (contracts/ directory)

**contracts/models.md**: Task model interface
```python
class Task:
    """Represents a user task with validation."""

    def validate_title(self) -> bool:
        """Check title is 1-200 chars after strip."""

    def validate_description(self) -> bool:
        """Check description is ≤1000 chars."""

    def mark_complete(self) -> None:
        """Toggle completed status, update timestamp."""
```

**contracts/storage.md**: Storage interface
```python
class TaskStorage:
    """In-memory task storage manager."""

    def add_task(self, title: str, description: str) -> Task:
        """Create task with auto-generated ID."""

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve task by ID or None."""

    def list_tasks(self) -> List[Task]:
        """Return all tasks, sorted by creation date."""

    def update_task(self, task_id: int, title: str, description: str) -> Task:
        """Update task fields, auto-update timestamp."""

    def delete_task(self, task_id: int) -> bool:
        """Remove task, return success status."""

    def toggle_complete(self, task_id: int) -> Task:
        """Toggle task completion status."""
```

**contracts/operations.md**: Business logic contracts
```python
# CRUD Operations (pure functions using dependency injection)

def create_task(storage: TaskStorage, title: str, description: str) -> Result[Task, str]:
    """Validate inputs, create task via storage."""

def view_tasks(storage: TaskStorage) -> List[Task]:
    """Retrieve all tasks for display."""

def update_task_details(storage: TaskStorage, task_id: int, title: str, desc: str) -> Result[Task, str]:
    """Validate inputs, update task via storage."""

def remove_task(storage: TaskStorage, task_id: int) -> Result[bool, str]:
    """Delete task if exists, return success/error."""

def toggle_task_status(storage: TaskStorage, task_id: int) -> Result[Task, str]:
    """Toggle completion status, return updated task."""
```

**contracts/ui.md**: UI function contracts
```python
# Menu Functions

def display_main_menu(task_count: int, completed: int, pending: int) -> None:
    """Show interactive menu with task statistics."""

def get_menu_choice() -> int:
    """Get user menu selection (1-6), validate input."""

def prompt_task_creation() -> Tuple[str, str]:
    """Prompt for title and description, return values."""

def prompt_task_id(action: str) -> int:
    """Prompt for task ID with context (e.g., 'to delete')."""

def prompt_task_update(current_title: str, current_desc: str) -> Tuple[str, str]:
    """Prompt for updated values, allow keep current."""

def confirm_deletion(task: Task) -> bool:
    """Show task details, ask Y/N confirmation."""

# Formatting Functions

def format_task_list(tasks: List[Task]) -> str:
    """Format tasks as table with columns."""

def format_success_message(action: str, task: Task) -> str:
    """Format success message with checkmark."""

def format_error_message(error: str) -> str:
    """Format error message with X symbol."""
```

### 3. Quickstart Guide (quickstart.md)

**Content**:
- Prerequisites (Python 3.8+)
- Installation steps
- Running the application
- Running tests
- Code structure overview
- Adding a new feature workflow

**Example**:
```markdown
# Quickstart Guide: Phase I Console Todo App

## Prerequisites
- Python 3.8 or higher
- UV package manager (recommended) or pip

## Installation

1. Clone repository:
   ```bash
   git clone <repo-url>
   cd todo-phase-1
   ```

2. Install dependencies:
   ```bash
   uv add pytest  # optional for testing
   ```

## Running the Application

```bash
python src/main.py
```

## Running Tests

```bash
pytest tests/
pytest tests/ --cov=src  # with coverage
```

## Project Structure

- `src/models/`: Task data model
- `src/storage/`: In-memory storage
- `src/operations/`: Business logic (CRUD)
- `src/ui/`: CLI interface
- `src/main.py`: Entry point

## Adding a New Feature

1. Write specification in `specs/`
2. Submit to Claude Code with constitution
3. Review generated code
4. Run quality checks (mypy, pylint, pytest)
5. Test manually against acceptance criteria
6. Commit with meaningful message
```

### 4. Agent Context Update

Run the agent context update script to inform Claude Code about the architecture decisions:

```bash
.specify/scripts/bash/update-agent-context.sh claude
```

This will update `.claude/context.md` or similar file with:
- Data model structure (Task entity)
- Storage interface (TaskStorage)
- Layer responsibilities
- Type hint conventions
- Testing strategy

## Phase 2: Implementation Breakdown (Not Created Here)

Phase 2 involves creating `tasks.md` using the `/sp.tasks` command. This is NOT part of `/sp.plan`. The tasks file will break down implementation into:

- T001-T003: Project setup
- T004: Data model implementation
- T005-T009: Business logic implementation
- T010-T014: CLI interface implementation
- T015: Main application wiring
- T016-T020: Polish and testing

Each task will reference the contracts defined in Phase 1.

## Architecture Decision Records (ADRs)

### Significant Decisions to Document

**ADR-001: In-Memory Storage with Dict-Based Lookup**
- **Decision**: Use dict[int, Task] for O(1) lookup by ID
- **Alternatives**: List[Task] with linear search, OrderedDict
- **Rationale**: Performance for 1000+ tasks, simple implementation
- **Consequences**: Memory overhead minimal, future migration path clear

**ADR-002: Dependency Injection for Operations Layer**
- **Decision**: Operations receive storage instance as parameter
- **Alternatives**: Global storage, singleton pattern, service locator
- **Rationale**: Enables testing with mock storage, follows clean architecture
- **Consequences**: More verbose function signatures, better testability

**ADR-003: dataclass vs TypedDict for Task Model**
- **Decision**: Use dataclass with default values
- **Alternatives**: TypedDict, NamedTuple, plain dict
- **Rationale**: Validation support, type safety, IDE autocomplete
- **Consequences**: Runtime overhead negligible, easier to extend

These ADRs should be created using `/sp.adr` command after planning is complete.

## Next Steps

1. ✅ Specification complete (spec.md)
2. ✅ Plan complete (this file)
3. ⏳ Execute Phase 0: Create research.md
4. ⏳ Execute Phase 1: Create data-model.md, contracts/, quickstart.md
5. ⏳ Update agent context
6. ⏳ Run `/sp.tasks` to generate task breakdown
7. ⏳ Run `/sp.implement` to execute tasks
8. ⏳ Quality checks and testing
9. ⏳ Documentation and submission

## Summary

This plan establishes a clear path from specification to implementation for the Phase I console todo application. The 5-layer architecture (data, storage, business logic, presentation, entry point) ensures:

- **Modularity**: Each layer can be developed and tested independently
- **Testability**: Dependency injection enables comprehensive unit testing
- **Extensibility**: Layers can be swapped (e.g., in-memory → database) without affecting others
- **Simplicity**: Uses only Python standard library, minimal complexity
- **Quality**: Type hints, validation, error handling throughout

All work follows spec-driven development principles: specification → research → design → implementation → testing. No manual coding permitted; all code generated by Claude Code from contracts defined in this plan.

**Status**: Ready for Phase 0 (Research)
