# Feature Specification: Phase I Complete Task Management System

**Feature Branch**: `003-phase1-task-mgmt`
**Created**: 2025-12-26
**Status**: Draft
**Input**: User description: "Update Phase I spec with complete task management features: priority, due dates, recurring tasks (auto-create next), status (pending/completed/overdue), filter (menu-based), search (interactive), sort options, and OPTIONAL voice input (speech-to-text with confirmation). Task management features are PRIMARY, visual enhancements are SECONDARY."

## Clarifications

### Session 2025-12-27

- Q: How should voice commands be structured for task creation? → A: Multi-turn conversation - user says "add task", system prompts "what's the title?", user responds, system prompts "what priority?", etc. (guided sequential input)
- Q: How should error recovery work during voice conversation? → A: Edit previous field - user can say "go back" or "change priority" to modify the last confirmed field before proceeding
- Q: How flexible should voice command vocabulary be? → A: Flexible with normalization - user can use variations ("high", "high priority", "make it high") which system normalizes to canonical values
- Q: Which speech recognition library should be used? → A: Python SpeechRecognition library - popular Python library supporting multiple engines (Google, Sphinx, Wit.ai)
- Q: What voice interaction pattern should the system use - direct commands or multi-turn conversation? → A: Multi-turn conversation pattern - system guides user through sequential prompts (title → priority → due date → recurrence) with confirmation summary before saving. Direct single-utterance commands are not part of the Phase I scope.

### Session 2025-12-28

- Q: How should system handle missing PyAudio dependency for voice input? → A: Auto-install dependencies - Attempt to install PyAudio automatically on first run (may require sudo/root)
- Q: What speech recognition backend should be used for voice input? → A: Auto-fallback approach - Try Google API with key, fall back to Sphinx if missing/unavailable
- Q: How should Google Speech API key be provided by user? → A: Prompt user once on first use - Ask for Google Cloud Speech API key on first voice input, save for future sessions
- Q: How should system handle tasks with past due dates during creation? → A: Warn but allow - Show warning message "Task will be marked as Overdue" but allow creation
- Q: Where should data files (tasks.json, config) be stored? → A: Tasks in project root - Store all data files (tasks.json, config) in project root directory
- Q: What logging strategy should the system use for observability and debugging? → A: Structured JSON logs to stderr with ERROR by default, DEBUG optionally enabled
- Q: How should the system protect sensitive data (API keys, passwords) stored in config files? → A: Encrypt API keys at rest using system keyring/libsecret (Linux/macOS/Windows)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Core Task Management (Priority: P1)

As a CLI user, I want to create and manage tasks with priority levels, due dates, and completion tracking, so I can organize my work effectively and see what needs immediate attention.

**Why this priority**: This is the foundation of any task management system. Without these core features, the app cannot function as a useful todo application. All other features depend on this baseline capability.

**Independent Test**: Can be fully tested by adding tasks with different priorities and due dates, marking some as complete, and verifying that tasks display their current status (pending/completed/overdue). Delivers immediate value as a functional task manager.

**Acceptance Scenarios**:

1. **Given** user launches app, **When** selecting "Add Task", **Then** system prompts for title, description, priority (High/Medium/Low/None), and due date (optional)
2. **Given** user adds task with due date of tomorrow, **When** viewing task list, **Then** task shows as "Pending" with due date displayed
3. **Given** task has due date of yesterday, **When** viewing task list, **Then** task shows as "Overdue" highlighted in red
4. **Given** user has multiple tasks, **When** viewing task list, **Then** overdue tasks automatically sort to top regardless of other sort settings
5. **Given** user completes a task, **When** marking as complete, **Then** task shows as "Completed" with completion timestamp
6. **Given** user wants to update a task, **When** selecting edit, **Then** all fields (title, description, priority, due date) can be modified
7. **Given** user views task list, **When** tasks are displayed, **Then** priority is color-coded (Red=High, Yellow=Medium, Green=Low, No color=None)

---

### User Story 2 - Advanced Filtering and Search (Priority: P2)

As a CLI user, I want to filter tasks by status, priority, or due date range, and search by keywords, so I can quickly find specific tasks without scrolling through a long list.

**Why this priority**: Once users have many tasks, finding specific ones becomes critical. This builds on User Story 1 by making task management scalable.

**Independent Test**: Can be fully tested by creating 20+ tasks with various properties, then using filters (show only High priority, show only Overdue) and search (find all tasks containing "meeting") to verify correct results are returned.

**Acceptance Scenarios**:

1. **Given** user has 50+ tasks, **When** selecting "Filter Tasks" from menu, **Then** system presents filter options (by status, by priority, by due date range, clear filters)
2. **Given** user filters by status=Overdue, **When** viewing filtered list, **Then** only overdue tasks are displayed with count shown (e.g., "Showing 5 of 50 tasks")
3. **Given** user filters by priority=High, **When** viewing filtered list, **Then** only high-priority tasks are displayed
4. **Given** user filters by due date range (this week), **When** viewing filtered list, **Then** only tasks due within next 7 days are shown
5. **Given** user has active filters, **When** selecting "Clear Filters", **Then** full task list is restored
6. **Given** user selects "Search Tasks" from menu, **When** entering keyword "groceries", **Then** all tasks with "groceries" in title or description are displayed (case-insensitive)
7. **Given** user searches for non-existent keyword, **When** search executes, **Then** system displays "No tasks found matching 'keyword'" message

---

### User Story 3 - Recurring Tasks (Priority: P3)

As a CLI user, I want to create recurring tasks (daily, weekly, monthly) that automatically generate the next occurrence when marked complete, so I don't have to manually recreate repetitive tasks.

**Why this priority**: Recurring tasks are a quality-of-life feature that significantly reduces repetitive data entry. This builds on User Story 1 but isn't required for basic task management functionality.

**Independent Test**: Can be fully tested by creating a task with Daily recurrence, marking it complete, and verifying that a new instance is automatically created with the due date set to tomorrow. Delivers value by automating repetitive task creation.

**Acceptance Scenarios**:

1. **Given** user creates new task, **When** prompted for recurrence, **Then** options presented are None, Daily, Weekly, Monthly
2. **Given** user creates task with Daily recurrence and due date of today, **When** marking task as complete, **Then** system automatically creates new task with same title/description/priority and due date of tomorrow
3. **Given** user creates task with Weekly recurrence, **When** marking complete, **Then** new task created with due date 7 days from original due date
4. **Given** user creates task with Monthly recurrence, **When** marking complete, **Then** new task created with due date 30 days from original due date
5. **Given** user has recurring task, **When** viewing task details, **Then** recurrence pattern is displayed (e.g., "Recurs: Daily")
6. **Given** user updates recurring task, **When** changing recurrence from Daily to Weekly, **Then** next occurrence will follow new pattern
7. **Given** user deletes recurring task, **When** confirming deletion, **Then** only current occurrence is deleted (future occurrences not pre-created)

---

### User Story 4 - Sort and Display Options (Priority: P4)

As a CLI user, I want to sort my task list by different criteria (priority, due date, creation date) and customize how tasks are displayed, so I can view my tasks in the most useful order for my current context.

**Why this priority**: Flexible sorting improves usability but isn't essential for core functionality. This enhances User Story 1 by providing different views of the same data.

**Independent Test**: Can be fully tested by creating tasks with varied priorities and due dates, then cycling through sort options and verifying the list reorders correctly each time.

**Acceptance Scenarios**:

1. **Given** user views task list, **When** selecting "Sort By" option, **Then** choices presented are Priority (High→Low), Due Date (Earliest→Latest), Created Date (Newest→Oldest), Default (Overdue first, then created date)
2. **Given** user sorts by Priority, **When** viewing list, **Then** High priority tasks appear first, followed by Medium, Low, and None
3. **Given** user sorts by Due Date, **When** viewing list, **Then** tasks with earliest due dates appear first (overdue still prioritized at top)
4. **Given** user sorts by Created Date, **When** viewing list, **Then** most recently created tasks appear first
5. **Given** user changes sort order, **When** performing any task operation (add/edit/delete/complete), **Then** sort order persists after operation
6. **Given** user has no active filters, **When** sorting, **Then** all tasks are included in the sorted view
7. **Given** user has active filters, **When** sorting, **Then** only filtered tasks are sorted (filter + sort work together)

---

### User Story 5 - Optional Voice Input (Priority: P5)

As a CLI user with a microphone, I want the option to use voice input to create tasks quickly by speaking instead of typing, so I can add tasks hands-free when convenient.

**Why this priority**: This is a nice-to-have enhancement that doesn't block core functionality. It's optional and should not interfere with keyboard-based usage. Provides accessibility benefit and convenience.

**Independent Test**: Can be fully tested by clicking "Voice Input" button, being guided through sequential prompts (say "add task" → say "buy milk" for title → say "high" for priority → say "tomorrow" for due date → say "none" for recurrence), and verifying that a confirmation summary appears before saving. If voice is unavailable, button is disabled with explanation.

**Acceptance Scenarios**:

1. **Given** user has microphone available, **When** selecting "Voice Input" from add task screen, **Then** system activates speech recognition and shows "Listening... Say 'add task'" indicator
2. **Given** voice recognition is active, **When** user says "add task", **Then** system confirms command and prompts "What's the task title?" with listening active
3. **Given** system is prompting for title, **When** user speaks the title (e.g., "buy milk"), **Then** system confirms "Title: buy milk" and prompts "What priority? Say high, medium, low, or none"
4. **Given** system is prompting for priority, **When** user speaks priority level (e.g., "high"), **Then** system confirms "Priority: high" and prompts "When is it due? Say a date or none"
5. **Given** system is prompting for due date, **When** user speaks due date (e.g., "tomorrow"), **Then** system confirms "Due: tomorrow" and prompts "Any recurrence? Say daily, weekly, monthly, or none"
6. **Given** system is prompting for recurrence, **When** user speaks recurrence pattern (e.g., "none"), **Then** system shows summary with "Confirm" and "Edit" buttons
7. **Given** user realizes an error during conversation (e.g., said "high" but meant "low"), **When** user says "go back" or "change priority", **Then** system returns to previous field prompt and allows re-entry
8. **Given** user reviews multi-turn conversation summary, **When** selecting "Confirm", **Then** task is created with collected values
9. **Given** user reviews summary, **When** selecting "Edit", **Then** user can select which field to re-record or manually type corrections
10. **Given** voice recognition fails on any prompt, **When** transcription confidence is low, **Then** system repeats the prompt and offers "Type Instead" option
11. **Given** system has no microphone access, **When** user attempts voice input, **Then** button is disabled with message "Microphone not available - use keyboard input"
12. **Given** voice input feature exists, **When** user doesn't want to use it, **Then** all functionality is fully accessible via keyboard (voice is truly optional)

---

### User Story 6 - Visual Enhancements (Priority: P6)

As a CLI user, I want a visually appealing interface with colors, icons, and clear formatting, so using the task manager is pleasant and information is easy to scan.

**Why this priority**: Visual polish improves user experience but is secondary to functionality. These enhancements make the app more enjoyable to use but don't add core capabilities.

**Independent Test**: Can be fully tested by launching the app and verifying that ASCII art displays, colors render correctly, emoji icons appear for status indicators, and tables are properly formatted across different terminal emulators.

**Acceptance Scenarios**:

1. **Given** user launches app, **When** application starts, **Then** ASCII art title displays with colored welcome message
2. **Given** user views task list, **When** tasks are displayed, **Then** Rich-formatted table shows with proper borders and column alignment
3. **Given** user views tasks with different statuses, **When** looking at the list, **Then** status indicators use emoji (⏳ Pending, ✓ Complete, 🔴 Overdue)
4. **Given** user views tasks with different priorities, **When** scanning the list, **Then** priority colors are clearly visible (Red/Yellow/Green/default)
5. **Given** user performs any operation, **When** processing, **Then** progress bars or animations show activity
6. **Given** user wants different colors, **When** selecting "Change Theme", **Then** can switch between dark, light, and hacker themes
7. **Given** terminal doesn't support colors, **When** app launches, **Then** gracefully falls back to plain text with clear indicators

---

### Edge Cases

- What happens when user enters invalid date format for due date? (System rejects and prompts for valid format: YYYY-MM-DD or natural language like "tomorrow", "next week")
- How does system handle due dates in the past when creating new tasks? (System displays warning "Task will be marked as Overdue" but allows creation)
- What happens when user creates recurring task with no due date? (System requires due date for recurring tasks - cannot recur without baseline date)
- How does system handle 1000+ tasks? (Performance remains acceptable; pagination or scrolling supported; filters/search become critical)
- What happens when tasks.json file is corrupted? (System backs up corrupt file, starts with empty list, shows error message to user)
- How does voice input handle background noise or unclear speech? (If confidence score <70%, shows warning and asks user to confirm or retry)
- What happens when user marks recurring task complete multiple times rapidly? (Only one new occurrence created per completion to prevent duplicates)
- How does system handle leap years for monthly recurring tasks? (Uses same day-of-month; if invalid (e.g., Feb 30), uses last day of month)
- What happens when user filters tasks but all are filtered out? (Shows "No tasks match current filters" with count of total tasks and option to clear filters)
- How does system handle very long task titles (500+ characters)? (Titles truncated to 200 characters with "..." indicator; full text visible in details view)

## Requirements *(mandatory)*

### Functional Requirements

**Core Task Management**

- **FR-001**: System MUST allow users to create tasks with title (required, 1-200 characters) and description (optional, max 1000 characters)
- **FR-002**: System MUST support task priority levels: High, Medium, Low, and None (default)
- **FR-003**: System MUST allow optional due dates for tasks (format: YYYY-MM-DD or natural language like "tomorrow", "next week", "2025-12-31")
- **FR-004**: System MUST display warning message "Task will be marked as Overdue" when user enters past due date during task creation, but allow the task to be created
- **FR-005**: System MUST validate that due dates are valid calendar dates
- **FR-006**: System MUST allow users to mark tasks as complete/incomplete with toggle functionality
- **FR-007**: System MUST allow users to update any task field (title, description, priority, due date, recurrence) after creation
- **FR-008**: System MUST allow users to delete tasks with confirmation prompt showing task details

**Status and Display**

- **FR-009**: System MUST calculate and display task status as Pending, Completed, or Overdue based on completion state and due date
- **FR-010**: System MUST display overdue tasks (due date < today and not completed) at the top of list regardless of sort order
- **FR-011**: System MUST use color coding for priority: Red (High), Yellow (Medium), Green (Low), Default (None)
- **FR-012**: System MUST use color coding for status: Red (Overdue), Cyan (Pending), Green (Completed)
- **FR-013**: System MUST display task count at top of list (e.g., "Showing 5 tasks" or "Showing 3 of 10 tasks" when filtered)
- **FR-014**: System MUST show emoji status indicators: ⏳ (Pending), ✓ (Completed), 🔴 (Overdue)

**Filtering and Search**

- **FR-015**: System MUST provide menu-based filter interface with options: Filter by Status, Filter by Priority, Filter by Due Date Range, Clear Filters
- **FR-016**: System MUST allow filtering by status: All, Pending, Completed, Overdue
- **FR-017**: System MUST allow filtering by priority: All, High, Medium, Low, None
- **FR-018**: System MUST allow filtering by due date range: Today, This Week (next 7 days), This Month (next 30 days), Overdue Only, Custom Range
- **FR-019**: System MUST display filtered count (e.g., "Showing 5 of 20 tasks - High Priority")
- **FR-020**: System MUST preserve filters across operations (add/edit/delete) until user clears filters
- **FR-021**: System MUST provide interactive search interface prompting for keyword
- **FR-022**: System MUST search task titles and descriptions using case-insensitive substring matching
- **FR-023**: System MUST display search results with match count and option to clear search

**Sorting**

- **FR-024**: System MUST provide sort options: Default, By Priority, By Due Date, By Created Date
- **FR-025**: System MUST use Default sort: Overdue first (by due date), then non-overdue by created date (newest first)
- **FR-026**: System MUST sort by priority: High → Medium → Low → None (overdue still prioritized at top)
- **FR-027**: System MUST sort by due date: Earliest → Latest, with overdue always at top
- **FR-028**: System MUST sort by created date: Newest → Oldest
- **FR-029**: System MUST persist sort preference across operations until user changes it

**Recurring Tasks**

- **FR-030**: System MUST support recurrence patterns: None (default), Daily, Weekly, Monthly
- **FR-031**: System MUST require a due date for tasks with recurrence (cannot recur without baseline date)
- **FR-032**: System MUST automatically create next occurrence when recurring task is marked complete
- **FR-033**: System MUST set next occurrence due date as: Daily (+1 day), Weekly (+7 days), Monthly (+30 days) from original due date
- **FR-034**: System MUST copy title, description, priority, and recurrence pattern to next occurrence
- **FR-035**: System MUST NOT copy completion status to next occurrence (new task starts as Pending)
- **FR-036**: System MUST display recurrence indicator in task list (e.g., "↻ Daily")
- **FR-037**: System MUST allow users to change or remove recurrence pattern on existing recurring tasks
- **FR-038**: System MUST handle invalid dates for monthly recurrence (e.g., Feb 30 → Feb 28/29)

**Optional Voice Input**

- **FR-039**: System MAY provide optional voice input feature for task creation (not required for core functionality)
- **FR-040**: System MUST prompt user for Google Cloud Speech API key on first voice input attempt
- **FR-041**: System MUST encrypt API keys at rest using system keyring/libsecret (Linux/macOS/Windows)
- **FR-042**: System MUST fall back to Sphinx offline recognizer if system keyring unavailable or encryption fails
- **FR-043**: System MUST attempt Google Speech Recognition API if user provides API key (higher accuracy, requires internet)
- **FR-044**: System MUST fall back to Sphinx offline recognizer if no API key provided or Google API fails (no internet required, lower accuracy)
- **FR-045**: System MUST activate speech recognition only when user explicitly clicks "Voice Input" button
- **FR-046**: System MUST use multi-turn conversation approach: prompt user sequentially for each field (title, priority, due date, recurrence)
- **FR-047**: System MUST show real-time transcription for each individual prompt response
- **FR-048**: System MUST normalize voice input variations to canonical values (e.g., "high", "high priority", "make it high" all map to Priority: High)
- **FR-049**: System MUST confirm each recognized field value in normalized form before proceeding to next prompt (e.g., "Priority: High" confirmation)
- **FR-050**: System MUST guide user through sequence: command recognition ("add task") → title → priority → due date → recurrence
- **FR-051**: System MUST support mid-conversation correction via voice commands "go back" or "change [field name]" to re-enter the last confirmed field
- **FR-052**: System MUST display final confirmation summary showing all collected fields before saving task
- **FR-053**: System MUST allow user to edit any field from summary (re-record specific field or type manually)
- **FR-054**: System MUST handle low-confidence transcriptions (<70%) by repeating the current prompt and offering "Type Instead" option
- **FR-055**: System MUST attempt to automatically install PyAudio dependency on first voice input attempt if missing (may require sudo/root)
- **FR-056**: System MUST ensure all functionality is fully accessible via keyboard if voice is unavailable

**Data Persistence**

- **FR-057**: System MUST persist all tasks to JSON file (tasks.json) in project root directory including all fields
- **FR-058**: System MUST auto-save after every operation (add, update, delete, complete)
- **FR-059**: System MUST auto-load tasks from JSON file on application start
- **FR-060**: System MUST handle file I/O errors gracefully with user-friendly messages
- **FR-061**: System MUST back up corrupt JSON files to tasks.json.corrupt before starting fresh
- **FR-062**: System MUST validate JSON structure on load and skip invalid task entries with warning

**Visual Enhancements**

- **FR-063**: System MUST display ASCII art title on application start
- **FR-064**: System MUST render task list in Rich-formatted table with borders and column alignment
- **FR-065**: System MUST show progress bars or animations during long operations
- **FR-066**: System MUST support theme switching: Dark, Light, Hacker
- **FR-067**: System MUST gracefully fall back to plain text if terminal doesn't support colors
- **FR-068**: System MUST use emoji indicators throughout UI for improved scanability

**Observability & Logging**

- **FR-069**: System MUST use structured JSON logging to stderr with configurable log levels
- **FR-070**: System MUST log at ERROR level by default, with optional DEBUG mode for troubleshooting
- **FR-071**: System MUST include timestamp, level, and message in all structured log entries

### Key Entities

- **Task**: Represents a single todo item with properties:
  - id (integer, auto-increment)
  - title (string, 1-200 chars, required)
  - description (string, max 1000 chars, optional)
  - completed (boolean, default false)
  - priority (enum: High | Medium | Low | None, default None)
  - due_date (date or null, optional)
  - recurrence (enum: None | Daily | Weekly | Monthly, default None)
  - created_at (datetime, auto-generated)
  - updated_at (datetime, auto-updated)
  - status (computed property: Pending | Completed | Overdue based on completed + due_date)

- **Theme**: Represents color scheme configuration
  - name (string: Dark | Light | Hacker)
  - primary color (string: color code)
  - success, warning, error, info colors (strings)

- **Filter**: Represents active filter state
  - status_filter (enum: All | Pending | Completed | Overdue)
  - priority_filter (enum: All | High | Medium | Low | None)
  - date_range_filter (enum: All | Today | This Week | This Month | Overdue | Custom with start_date and end_date)
  - search_keyword (string or null)

- **SortOption**: Represents current sort preference
  - sort_by (enum: Default | Priority | DueDate | CreatedDate)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a task with title, priority, and due date in under 30 seconds
- **SC-002**: Users can find a specific task among 100+ tasks using filters or search in under 10 seconds
- **SC-003**: System maintains performance (menu response <50ms, list render <200ms) with 1000+ tasks
- **SC-004**: 95% of voice input transcriptions are accepted without manual editing (when voice is used)
- **SC-005**: Overdue tasks are immediately visible at top of list without user needing to scroll
- **SC-006**: Users can complete daily workflow (add task, filter by priority, mark complete) in under 1 minute
- **SC-007**: Task list remains readable and scannable on terminals as narrow as 80 characters wide
- **SC-008**: Recurring task next occurrence is created automatically within 1 second of marking complete
- **SC-009**: Filter results update instantly (<100ms) when user changes filter criteria
- **SC-010**: All color-coded information has equivalent text indicators for accessibility (not color-only)
- **SC-011**: Users can use the entire application without ever touching the mouse (keyboard-only workflow)
- **SC-012**: Task data persists across sessions with zero data loss under normal exit conditions
- **SC-013**: System recovers gracefully from file corruption with clear error message and fresh start
- **SC-014**: Users can switch between sort orders without losing current filters or search terms
- **SC-015**: Voice input feature (when available) reduces task creation time by at least 40% compared to typing

## Assumptions

- Users have Python 3.13+ environment available
- Users are comfortable with command-line interfaces
- Terminal supports 256 colors (graceful degradation for non-color terminals)
- For voice input: users have microphone hardware and internet connection (optional feature only; uses Python SpeechRecognition library with auto-fallback: Google Speech Recognition API if API key provided, Sphinx offline recognizer as fallback)
- Users prefer due dates in their local timezone
- Monthly recurrence means "every 30 days" not "same day next month" (simpler calculation)
- Single-user application (no multi-user sync or authentication required)
- English language UI (internationalization not required for Phase I)
- Voice commands are in English only (Urdu support deferred to future phases)
- Maximum task limit of 10,000 tasks for performance guarantees

## Out of Scope

- Multi-user support or user authentication
- Cloud synchronization or backup
- Mobile applications or web interface (Phase I is CLI only)
- Task sharing or collaboration features
- File attachments or task notes beyond description field
- Task categories or tags (can use description field)
- Time tracking or task duration estimates
- Notifications or reminders (system doesn't run in background)
- Calendar view or Gantt charts
- Subtasks or task hierarchy
- Task dependencies or workflow automation
- Undo/redo functionality
- Task history or audit log
- Export to other formats (only JSON persistence)
- Custom recurrence patterns beyond Daily/Weekly/Monthly
- Integration with external calendars or services
