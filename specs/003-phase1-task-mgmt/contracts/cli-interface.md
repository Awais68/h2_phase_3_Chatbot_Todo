# CLI Interface Contract

**Branch**: `003-phase1-task-mgmt` | **Date**: 2025-12-27

## Menu Interface

### Main Menu

**Input**: Single digit (0-9) or arrow keys
**Output**: Formatted menu with options

```
╔════════════════════════════════════════╗
║     Todo App - Phase I (v1.0.0)        ║
║     Tasks: X total (Y done, Z pending) ║
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

### Error States

| Input | Error Message | Recovery |
|-------|---------------|----------|
| Invalid choice | `✗ Error: Invalid choice. Please enter 0-9.` | Redisplay menu |
| Empty input | `✗ Error: Please enter a value.` | Re-prompt |
| Ctrl+C | `Application interrupted. Goodbye!` | Exit gracefully |

---

## Add Task Flow

### Prompts Sequence

```python
# Step 1: Title
"Enter task title: "

# Step 2: Description
"Enter description (optional): "

# Step 3: Priority
"Select priority:"
  1. High
  2. Medium
  3. Low
  4. None

# Step 4: Due Date
"Enter due date (optional, e.g., tomorrow, next week, 2025-12-31): "

# Step 5: Recurrence
"Select recurrence:"
  1. None
  2. Daily
  3. Weekly
  4. Monthly
```

### Validation Rules

| Field | Valid Input | Invalid | Error Message |
|-------|-------------|---------|---------------|
| Title | 1-200 chars | Empty | `Title cannot be empty` |
| Title | 1-200 chars | >200 chars | `Title cannot exceed 200 characters` |
| Description | 0-1000 chars | >1000 chars | `Description cannot exceed 1000 characters` |
| Due Date | ISO/natural format | Invalid format | `Invalid date format. Try: tomorrow, next week, or YYYY-MM-DD` |
| Recurrence | enum value | Invalid | `Invalid recurrence option` |

### Success Response

```
✓ Task created successfully! ID: 1

Title: Buy groceries
Priority: HIGH
Due Date: 2025-12-28
Recurrence: None
```

---

## View Tasks Flow

### Table Display

```
=== Task List (5 tasks) ===

┌─────┬──────────┬──────────┬────────────────────┬────────────┬────────────┬─────────────┐
│ ID  │ Status   │ Priority │ Title              │ Due Date   │ Recurrence │ Created     │
├─────┼──────────┼──────────┼────────────────────┼────────────┼────────────┼─────────────┤
│ 1   │ 🔴 OVERD │ 🔴 HIGH  │ Buy groceries      │ 2025-12-26 │ None       │ 2025-12-25  │
│ 2   │ ⏳ PEND  │ 🟡 MED   │ Call dentist       │ 2025-12-28 │ None       │ 2025-12-25  │
│ 3   │ ✓ DONE  │ 🟢 LOW   │ Finish report      │ -          │ None       │ 2025-12-24  │
└─────┴──────────┴──────────┴────────────────────┴────────────┴────────────┴─────────────┘

Showing 5 tasks | 1 overdue | 2 pending | 2 completed
```

### Status Indicators

| Status | Color | Emoji | Meaning |
|--------|-------|-------|---------|
| PENDING | Cyan | ⏳ | Not complete, not overdue |
| COMPLETED | Green | ✓ | Marked complete |
| OVERDUE | Red | 🔴 | Past due date, not complete |

### Priority Indicators

| Priority | Color | Emoji |
|----------|-------|-------|
| HIGH | Red | 🔴 |
| MEDIUM | Yellow | 🟡 |
| LOW | Green | 🟢 |
| NONE | Default | ⚪ |

---

## Filter Menu

```
╔══════════════════════════════╗
║     Filter Tasks             ║
╠══════════════════════════════╣
│ 1. By Status                 │
│ 2. By Priority               │
│ 3. By Due Date Range         │
│ 4. Search Tasks              │
│ 5. Clear Filters             │
│ 0. Back to Main Menu         │
╚══════════════════════════════╝
```

### Filter Results

```
=== Filtered Tasks (Showing 3 of 10 - HIGH Priority) ===

[table with filtered tasks]

✓ Filters active: Priority=HIGH
```

---

## Edit Task Flow

### Current Task Display

```
=== Update Task ===
Current task:
ID: 1
Title: Buy groceries
Priority: HIGH
Due Date: 2025-12-28
Status: PENDING

Leave blank to keep current value.
```

### Update Prompts

```
New title (or press Enter to keep): _
New description (or press Enter to keep): _
Change priority? (current: HIGH) [y/N]: _
Change due date? (current: 2025-12-28) [y/N]: _
```

---

## Delete Task Flow

### Confirmation

```
=== Delete Task ===
Task to delete:
ID: 1 | Title: Buy groceries | Status: PENDING

Are you sure you want to delete this task? (y/N): _
```

### Responses

| Input | Result |
|-------|--------|
| `y`, `Y`, `yes` | Task deleted, `✓ Task deleted successfully!` |
| `n`, `N`, `no` | Deletion cancelled, `Deletion cancelled` |
| Empty | Treated as No |

---

## Theme Selection

```
╔══════════════════════╗
║   Select Theme       ║
╠══════════════════════╣
│ 1. 🌙 Dark Theme     │
│ 2. ☀️ Light Theme    │
│ 3. 💻 Hacker Theme   │
╚══════════════════════╝
```

---

## Exit Flow

### Normal Exit

```
Saving tasks to tasks.json...
✓ Saved 10 tasks
✓ Thank you for using Todo Application!
Goodbye!
```

### Ctrl+C Exit

```
^
Application interrupted.
Saving tasks...
✓ Saved 10 tasks
Application interrupted. Goodbye!
```

---

## Accessibility

All color-coded information has equivalent text indicators:
- Status: Emoji shown with text (🔴 OVERDUE)
- Priority: Color name in table header
- All messages use clear symbols (✓, ✗, ⚠, ℹ)
