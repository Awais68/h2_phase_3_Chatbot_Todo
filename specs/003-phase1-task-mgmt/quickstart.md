# Quickstart Guide: Phase I Task Management System

**Branch**: `003-phase1-task-mgmt` | **Date**: 2025-12-27

## Installation

### Prerequisites

- Python 3.13 or higher
- UV package manager (recommended) or pip

### Setup

```bash
# Clone the repository
git checkout 003-phase1-task-mgmt

# Create virtual environment with UV
uv venv
source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

# Install dependencies
uv sync

# Verify installation
python -c "from src.models.task import Task; print('Installation successful!')"
```

### Optional Voice Dependencies

```bash
# Install microphone support for voice input
uv sync --extra voice
```

**Note**: Voice input requires:
- Microphone hardware
- Internet connection (for Google Speech Recognition)
- PyAudio may require system dependencies (see below)

#### PyAudio Installation Notes

**Linux (Debian/Ubuntu)**:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

**macOS**:
```bash
brew install portaudio
pip install pyaudio
```

**Windows**:
```bash
pip install pyaudio
```

If PyAudio fails to install, voice input will be disabled but all other features work.

---

## Usage

### Running the Application

```bash
# Run with UV
uv run python main.py

# Or activate venv first
source .venv/bin/activate
python main.py
```

### Main Menu

```
╔════════════════════════════════════════╗
║     Todo App - Phase I (v1.0.0)        ║
║     Tasks: 0 total (0 done, 0 pending) ║
╚════════════════════════════════════════╝

Choose an option:

  1. Add new task
  2. View all tasks
  3. Update task
  4. Delete task
  5. Mark task complete/incomplete
  6. Filter/Search
  7. Sort Tasks
  8. Voice Input (optional)
  9. Change Theme
  0. Exit

Enter your choice (0-9): _
```

---

## Features Guide

### Adding a Task

1. Select option `1` (Add new task)
2. Enter task title when prompted
3. Optionally enter a description
4. Select priority level (High/Medium/Low/None)
5. Enter due date (optional, supports natural language)
6. Select recurrence (None/Daily/Weekly/Monthly)
7. Task is created and saved automatically

**Natural Language Date Examples**:
- `tomorrow`
- `next week`
- `next Monday`
- `2025-12-31`
- `in 3 days`

### Viewing Tasks

- Select option `2` to view all tasks
- Tasks displayed in a Rich table with:
  - ID, Status, Priority, Title, Due Date, Recurrence, Created Date
  - Color coding (Red=High, Yellow=Medium, Green=Low)
  - Emoji indicators (⏳ Pending, ✓ Complete, 🔴 Overdue)
  - Overdue tasks automatically sorted to top

### Filtering and Search

Select option `6` for Filter/Search menu:
- **Filter by Status**: Show only Pending, Completed, or Overdue
- **Filter by Priority**: Show only High, Medium, Low priority
- **Filter by Date**: Today, This Week, This Month, Overdue Only
- **Search**: Enter keyword to search titles and descriptions
- **Clear Filters**: Reset to show all tasks

### Sorting

Select option `7` to change sort order:
- **Default**: Overdue first, then by creation date (newest first)
- **By Priority**: High → Medium → Low → None
- **By Due Date**: Earliest due date first
- **By Created Date**: Newest first

### Marking Complete

1. Select option `5` (Mark complete/incomplete)
2. Enter the task ID
3. Task status toggles between complete and pending
4. For recurring tasks, marking complete creates the next occurrence

### Deleting a Task

1. Select option `4` (Delete task)
2. Enter the task ID
3. Review task details shown
4. Confirm deletion (Y/N)

### Voice Input (Optional)

1. Select option `8` (Voice Input)
2. If microphone is available, system enters voice mode
3. Follow spoken prompts:
   - "Say 'add task' to begin"
   - "What's the task title?"
   - "What priority? Say high, medium, low, or none"
   - "When is it due?"
   - "Any recurrence?"
4. Review confirmation summary
5. Say "confirm" to create task

**Error Recovery**:
- Say "go back" to re-enter the last field
- Say "type instead" to switch to keyboard input
- If confidence is low, system asks to repeat

### Changing Theme

Select option `9` to switch between:
- **Dark**: Cyan/white on black (default)
- **Light**: Blue/black on white
- **Hacker**: Green on black (retro style)

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `1-9` | Select menu option |
| `0` | Exit application |
| `Ctrl+C` | Graceful exit with save |
| `Enter` | Confirm selection |

---

## Data Storage

### File Location

Tasks are saved to `tasks.json` in the current working directory.

### Backup and Recovery

- **Auto-save**: After every operation (add, edit, delete, complete)
- **Corruption handling**: Corrupt files backed up to `tasks.json.corrupt.YYYYMMDD_HHMMSS`
- **Fresh start**: On corruption, starts with empty task list and shows error

### Export/Import

Tasks can be exported by copying `tasks.json`. No import function in Phase I.

---

## Troubleshooting

### "Module not found" Errors

```bash
# Reinstall dependencies
uv sync
```

### Voice Input Not Working

```bash
# Check microphone access (Linux)
arecord -l

# Verify PyAudio installation
python -c "import pyaudio; print('PyAudio OK')"

# If PyAudio fails, use keyboard only
# Voice input is optional - all features work without it
```

### Display Issues

- **No colors**: Terminal doesn't support 256 colors; themes still work
- **Table not formatting**: Terminal width < 80 characters; resize terminal
- **Text garbled**: Encoding issue; set `PYTHONIOENCODING=utf-8`

### Performance Issues

```bash
# Check task count
python -c "from src.services.task_service import TaskManager; m = TaskManager(); print(f'Tasks: {len(m.tasks)}')"

# If >1000 tasks, consider filtering to reduce display time
```

---

## Development

### Running Tests

```bash
# Run all tests
uv run pytest tests/

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/test_task_model.py -v
```

### Type Checking

```bash
uv run mypy src/
```

### Linting

```bash
uv run pylint src/ --fail-under=8.0
```

### Code Quality Check Script

```bash
#!/bin/bash
echo "Running quality checks..."

echo "1. Type checking..."
uv run mypy src/ || exit 1

echo "2. Linting..."
uv run pylint src/ --fail-under=8.0 || exit 1

echo "3. Tests..."
uv run pytest tests/ || exit 1

echo "4. Coverage..."
uv run pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=80 || exit 1

echo "All quality checks passed!"
```

---

## Architecture Overview

```
src/
├── main.py                    # Application entry point
├── models/
│   ├── task.py                # Task data model
│   ├── enums.py               # Priority, Recurrence, Status enums
│   ├── filter.py              # FilterState model
│   ├── sort_option.py         # SortBy enum
│   ├── voice_state.py         # VoiceState model
│   └── theme.py               # Theme configuration
├── services/
│   ├── task_service.py        # CRUD operations
│   ├── recurring_service.py   # Recurring task logic
│   ├── voice_service.py       # Speech recognition
│   ├── voice_normalizer.py    # Voice input normalization
│   └── persistence_service.py # JSON file I/O
├── cli/
│   ├── menu.py                # Interactive menu
│   ├── voice_menu.py          # Voice command handler
│   ├── formatter.py           # Rich table formatting
│   └── prompts.py             # Input prompts
└── lib/
    ├── date_parser.py         # Natural language dates
    ├── validators.py          # Input validation
    └── exceptions.py          # Custom exceptions
```

---

## Next Steps

After completing Phase I:

1. **Phase II**: Add persistent storage (PostgreSQL), user authentication, API endpoints
2. **Phase III**: AI chatbot integration, natural language processing
4. **Phase IV**: Cloud deployment, microservices architecture
5. **Phase V**: Advanced features (notifications, calendar integration, collaboration)

---

## Support

- **Issues**: Report bugs via GitHub issues
- **Documentation**: See [spec.md](./spec.md) for detailed requirements
- **Constitution**: See `.specify/memory/constitution.md` for development principles
