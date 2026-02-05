# Task Breakdown: Advanced Todo Features

**Feature**: 012-advanced-todo-features | **Branch**: `012-advanced-todo-features` | **Date**: 2026-02-05

## Executive Summary

This document provides a comprehensive, actionable task breakdown for implementing advanced todo features including due dates with reminders, recurring tasks, and task history. The implementation is organized by user story priority to enable incremental delivery and independent testing of each feature.

**Total Tasks**: 72 tasks across 6 phases
**Estimated Duration**: 18-24 hours
**MVP Scope**: Phase 1-3 (Setup + Foundational + US1) = ~8 hours

### Task Distribution by Phase

| Phase | Description | Tasks | Est. Time |
|-------|-------------|-------|-----------|
| Phase 1 | Setup & Dependencies | 8 tasks | 1 hour |
| Phase 2 | Foundational Infrastructure | 10 tasks | 2.5 hours |
| Phase 3 | US1: Due Dates & Reminders (P1) | 17 tasks | 5 hours |
| Phase 4 | US2: Recurring Tasks (P2) | 14 tasks | 4 hours |
| Phase 5 | US3: Task History (P3) | 15 tasks | 4 hours |
| Phase 6 | Polish & Documentation | 8 tasks | 1.5 hours |

### Technology Stack

**Backend**:
- Python 3.13+
- FastAPI (web framework)
- SQLModel (ORM)
- dateparser 1.3.0+ (natural language parsing)
- parsedatetime 2.6+ (fallback date parsing)
- APScheduler 3.10.0+ (background jobs)
- pytz 2024.1+ (timezone handling)
- Neon PostgreSQL (database)

**Frontend**:
- TypeScript/React
- OpenAI ChatKit (chat UI)
- Web Notifications API
- Service Worker API
- react-datepicker (date/time picker)

---

## Dependency Graph

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ← Must complete before any user stories
    ↓
    ├─→ Phase 3 (US1: Due Dates & Reminders) ← MVP Core (P1)
    │       ↓
    ├─→ Phase 4 (US2: Recurring Tasks) ← Depends on US1 (P2)
    │       ↓
    └─→ Phase 5 (US3: Task History) ← Independent of US1/US2 (P3)
            ↓
        Phase 6 (Polish)
```

**Parallel Opportunities**:
- Phase 4 (Recurring Tasks) and Phase 5 (History) can be developed in parallel after Phase 3 completes
- Within each phase: Frontend and backend tasks marked [P] can run in parallel
- US3 (History) is fully independent and can start immediately after Phase 2

---

## Phase 1: Setup & Dependencies

**Goal**: Install new dependencies and update project configuration

**Independent Test**: Run `pip list | grep -E "(dateparser|parsedatetime|apscheduler)"` to verify backend dependencies; verify frontend package.json includes new libraries

### Tasks

- [X] T001 Update backend/requirements_hf.txt to add dateparser>=1.3.0, parsedatetime>=2.6, APScheduler>=3.10.0, pytz>=2024.1, python-dateutil>=2.8.0
- [X] T002 [P] Run `cd backend && uv pip install -e .` to install new Python dependencies
- [X] T003 [P] Update frontend/package.json to add react-datepicker (or react-datetime-picker)
- [X] T004 [P] Run `cd frontend && npm install` to install new frontend dependencies
- [X] T005 Update backend/.env.example to add APSCHEDULER_DATABASE_URL and SCHEDULER_TIMEZONE variables
- [X] T006 [P] Update frontend/.env.example to add VITE_ENABLE_NOTIFICATIONS=true
- [X] T007 [P] Create backend/src/utils/__init__.py (new directory)
- [X] T008 Update .gitignore to exclude *.pyc, __pycache__/, .pytest_cache/, node_modules/, dist/, build/

**Validation**:
```bash
# Verify backend dependencies
cd backend && uv pip list | grep -E "(dateparser|parsedatetime|apscheduler)"

# Verify frontend dependencies
cd frontend && npm list react-datepicker

# Verify directory structure
ls -la backend/src/utils/
```

---

## Phase 2: Foundational Infrastructure

**Goal**: Implement core database schema and utility classes required by all user stories

**Independent Test**: Database migrations run successfully; DateTimeParser and RecurrenceCalculator can be imported and basic methods work

### Tasks

- [X] T009 Create backend/src/database/migrations/001_extend_tasks.sql to add 5 columns (due_date, recurrence_pattern, is_recurring, reminder_minutes, next_occurrence) to tasks table
- [X] T010 Create backend/src/database/migrations/002_task_history.sql to create task_history table with all fields per data-model.md
- [X] T011 Create backend/src/database/migrations/003_notif_prefs.sql to create notification_preferences table
- [X] T012 Create backend/src/database/migrations/004_apscheduler.sql to create apscheduler_jobs table
- [X] T013 Run database migrations against Neon PostgreSQL database
- [X] T014 [P] Implement DateTimeParser class in backend/src/utils/datetime_parser.py with parse() method using dateparser + parsedatetime fallback
- [X] T015 [P] Implement RecurrenceCalculator class in backend/src/utils/recurrence_calculator.py with calculate_next_occurrence() method for all 5 patterns
- [X] T016 Update backend/src/models/task.py to add 5 new fields with SQLModel Field definitions and validation methods
- [X] T017 [P] Create backend/src/models/task_history.py with TaskHistory and HistoryActionType models per data-model.md
- [X] T018 [P] Create backend/src/models/notification_preference.py with NotificationPreference model per data-model.md

**Validation**:
```bash
# Verify migrations applied
psql $DATABASE_URL -c "\d tasks" | grep due_date

# Test date parsing utility
cd backend
python -c "from src.utils.datetime_parser import DateTimeParser; print(DateTimeParser().parse('tomorrow at 3pm'))"

# Test recurrence calculator
python -c "from src.utils.recurrence_calculator import RecurrenceCalculator; print('OK')"
```

---

## Phase 3: User Story 1 - Due Dates & Reminders (P1)

**Story Goal**: Users can set deadlines for tasks using natural language or date/time picker, and receive browser notifications when tasks are due

**Independent Test**: Create task with "due tomorrow at 3pm", verify due date stored in database, receive browser notification 15 minutes before and at due time

**Why P1**: Core time management value - without due dates and reminders, users can easily forget tasks. This is the foundation for recurring tasks (US2).

### Backend Tasks

- [x] T019 [US1] Implement SchedulerService class in backend/src/services/scheduler_service.py with APScheduler setup using PostgreSQL jobstore
- [x] T020 [US1] Add schedule_notification() method to SchedulerService to schedule browser notification jobs
- [x] T021 [US1] Add schedule_history_cleanup() method to SchedulerService for daily cleanup cron job
- [x] T022 [US1] Update backend/src/main.py to initialize SchedulerService on FastAPI startup and shutdown
- [x] T023 [US1] Update TaskService.create_task() in backend/src/services/task_service.py to accept due_date_text parameter and parse using DateTimeParser
- [x] T024 [US1] Add TaskService.update_task_due_date() method to modify due dates and reschedule notifications
- [x] T025 [US1] Update TaskService.complete_task() to handle due date completion tracking
- [x] T026 [US1] Implement add_task_with_due_date MCP tool in backend/src/mcp/tools.py per mcp-tools-extended.json
- [x] T027 [US1] Implement update_task_due_date MCP tool in backend/src/mcp/tools.py
- [x] T028 [US1] Implement list_tasks_by_due_date MCP tool in backend/src/mcp/tools.py with filtering (overdue, due_today, due_this_week)
- [x] T029 [US1] Update backend/src/mcp/server.py to register 3 new MCP tools
- [x] T030 [US1] Update agent system prompt in backend/src/services/agent_service.py to include due date intent patterns

### Frontend Tasks

- [x] T031 [P] [US1] Create useNotifications hook in frontend/src/hooks/useNotifications.ts with permission request and scheduleNotification methods
- [x] T032 [P] [US1] Create DateTimePicker component in frontend/src/components/DateTimePicker.tsx using react-datepicker library
- [x] T033 [P] [US1] Create service worker in frontend/public/service-worker.js for background notification handling
- [x] T034 [P] [US1] Update frontend/src/types/task.ts to add new Task fields (due_date, recurrence_pattern, is_recurring, reminder_minutes, next_occurrence)
- [x] T035 [US1] Update ChatInterface component in frontend/src/components/ChatInterface.tsx to display due dates in chat responses
- [x] T036 [US1] Update TaskList component in frontend/src/components/TaskList.tsx to show due date indicators (red=overdue, yellow=due today, blue=upcoming)
- [x] T037 [US1] Create dateUtils.ts in frontend/src/utils/ with timezone display helpers and status calculation (overdue, due_today, upcoming)
- [x] T038 [US1] Update formatters.ts in frontend/src/utils/ to format due dates in user's timezone
- [x] T039 [US1] Register service worker in frontend/src/App.tsx on component mount
- [x] T040 [US1] Update chat.ts in frontend/src/services/ to send due_date_text parameter to backend

**Validation**:
```bash
# Backend test: Create task with due date
curl -X POST http://localhost:8000/api/1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add task to buy groceries tomorrow at 3pm"}'

# Verify due date in database
psql $DATABASE_URL -c "SELECT id, title, due_date, reminder_minutes FROM tasks WHERE title LIKE '%groceries%';"

# Frontend test:
# 1. Open http://localhost:5173
# 2. Type: "Add task due tomorrow at 3pm"
# 3. Verify: Due date displayed with correct timezone
# 4. Verify: Notification permission requested
# 5. Wait 15 minutes before due time: Verify notification appears
```

**Acceptance Criteria**:
- [ ] Users can set due dates using natural language ("tomorrow at 3pm", "next Friday")
- [ ] Date/time picker allows precise date selection
- [ ] Browser notification permission is requested on first reminder setup
- [ ] Notifications appear 15 minutes before due time (default) and at due time
- [ ] Overdue tasks highlighted in red, due today in yellow, upcoming in blue
- [ ] All due dates stored in UTC, displayed in user's browser timezone

---

## Phase 4: User Story 2 - Recurring Tasks (P2)

**Story Goal**: Users can create tasks that automatically reschedule after completion (daily, weekly, monthly, yearly patterns)

**Independent Test**: Create task "weekly standup every Monday at 9am", complete it, verify new task auto-created for next Monday at 9am

**Why P2**: Saves time for repetitive responsibilities, but requires US1 (due dates) to work first

**Dependencies**: Requires Phase 3 (US1) complete - recurring tasks depend on due dates

### Backend Tasks

- [x] T041 [US2] Add TaskService.create_recurring_instance() method in backend/src/services/task_service.py to create next occurrence when recurring task completes
- [x] T042 [US2] Update TaskService.complete_task() to check is_recurring flag and call create_recurring_instance()
- [x] T043 [US2] Add schedule_recurring_task_creation() method to SchedulerService for delayed recurring task creation
- [ ] T044 [US2] Add TaskService.update_recurrence_pattern() method to modify or stop recurrence on existing tasks
- [ ] T045 [US2] Add TaskService.stop_recurrence() method to convert recurring task to one-time task
- [ ] T046 [US2] Implement update_recurrence validation logic (ensure due_date exists if is_recurring=True)
- [ ] T047 [US2] Update add_task_with_due_date MCP tool to accept recurrence_pattern parameter
- [ ] T048 [US2] Update agent system prompt to recognize recurrence intent patterns ("weekly meeting", "monthly report", "daily standup")

### Frontend Tasks

- [ ] T049 [P] [US2] Add recurrence selector to DateTimePicker component with options (daily, weekly, bi-weekly, monthly, yearly, none)
- [ ] T050 [P] [US2] Create RecurrenceIndicator component in frontend/src/components/ to display "Repeats: Weekly on Monday" text
- [ ] T051 [US2] Update TaskList component to show recurrence indicator for recurring tasks
- [ ] T052 [US2] Update ChatInterface to handle recurrence pattern in natural language ("create weekly meeting task")
- [ ] T053 [US2] Add stop recurrence button to task detail view (when viewing recurring task)
- [ ] T054 [US2] Update chat.ts service to send recurrence_pattern parameter to backend

**Validation**:
```bash
# Backend test: Create recurring task
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"message": "Add weekly team meeting every Monday at 9am"}'

# Verify recurring task created
psql $DATABASE_URL -c "SELECT id, title, is_recurring, recurrence_pattern, due_date, next_occurrence FROM tasks WHERE is_recurring=TRUE;"

# Complete the task
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"conversation_id": 1, "message": "Mark task 1 as complete"}'

# Verify new instance created
psql $DATABASE_URL -c "SELECT COUNT(*) FROM tasks WHERE title LIKE '%team meeting%';"
# Expected: 2 tasks (completed original + new instance)

# Frontend test:
# 1. Create task: "weekly standup every Monday"
# 2. Verify: "Repeats: Weekly" displayed
# 3. Complete task
# 4. Verify: New task appears for next week
```

**Acceptance Criteria**:
- [ ] Users can specify recurrence when creating tasks ("weekly meeting", "monthly report")
- [ ] 5 recurrence patterns supported: daily, weekly, bi-weekly, monthly, yearly
- [ ] Recurrence information displayed in task details
- [ ] Completing recurring task auto-creates next instance with calculated next_occurrence
- [ ] Users can stop recurrence on existing recurring tasks
- [ ] Edge case handled: Monthly tasks on day 31 use last day of month for shorter months

---

## Phase 5: User Story 3 - Task History (P3)

**Story Goal**: Users can view completed and deleted tasks from past 2 years in a History tab, with search, filter, and restore capabilities

**Independent Test**: Complete 5 tasks, delete 3 tasks, navigate to History tab, verify all 8 actions displayed with metadata, restore 1 deleted task

**Why P3**: Valuable for record-keeping and accountability, but users can function without it

**Dependencies**: Independent of US1 and US2 - can be developed in parallel with Phase 4

### Backend Tasks

- [x] T055 [US3] Create HistoryService class in backend/src/services/history_service.py
- [x] T056 [US3] Implement HistoryService.create_history_entry() to store completed/deleted tasks
- [x] T057 [US3] Implement HistoryService.get_history() with pagination (50 per page), filtering (completed/deleted/all), and date range
- [x] T058 [US3] Implement HistoryService.search_history() using PostgreSQL full-text search on title field
- [x] T059 [US3] Implement HistoryService.restore_deleted_task() to move task from history back to active tasks
- [x] T060 [US3] Add cleanup_old_history() method to SchedulerService for 2-year retention purge (daily cron)
- [x] T061 [US3] Update TaskService.complete_task() to call HistoryService.create_history_entry() with action_type='completed'
- [x] T062 [US3] Update TaskService.delete_task() to call HistoryService.create_history_entry() with action_type='deleted' before deletion
- [x] T063 [US3] Create history.py in backend/src/api/ with GET /users/{user_id}/history and POST /users/{user_id}/history/{history_id}/restore endpoints per history-api.yaml
- [x] T064 [US3] Implement view_task_history MCP tool in backend/src/mcp/tools.py
- [x] T065 [US3] Implement restore_deleted_task MCP tool in backend/src/mcp/tools.py
- [ ] T066 [US3] Update agent system prompt to recognize history-related intents ("show my history", "restore deleted task")

### Frontend Tasks

- [x] T067 [P] [US3] Create HistoryTab component in frontend/src/components/HistoryTab.tsx with table view, filters, search input
- [ ] T068 [P] [US3] Create useTaskHistory hook in frontend/src/hooks/useTaskHistory.ts for data fetching with pagination
- [ ] T069 [P] [US3] Create history.ts API client in frontend/src/services/ with getHistory() and restoreTask() methods
- [ ] T070 [P] [US3] Create history types in frontend/src/types/history.ts (TaskHistoryItem, HistoryActionType, PaginationInfo)
- [ ] T071 [US3] Add "History" tab to dashboard navigation in frontend/src/App.tsx
- [ ] T072 [US3] Implement filter UI in HistoryTab (dropdowns for action_type, date range pickers)
- [ ] T073 [US3] Implement search functionality in HistoryTab with debounced input
- [ ] T074 [US3] Add "Restore" button to deleted tasks in history (only for action_type='deleted', can_restore=true)
- [ ] T075 [US3] Implement pagination controls (Previous/Next buttons, page indicator)

**Validation**:
```bash
# Backend test: Create history entries
# 1. Complete 5 tasks
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/1/chat \
    -d "{\"message\": \"Mark task $i as complete\"}"
done

# 2. Delete 3 tasks
for i in {6..8}; do
  curl -X POST http://localhost:8000/api/1/chat \
    -d "{\"message\": \"Delete task $i\"}"
done

# 3. Verify history entries
curl http://localhost:8000/api/users/1/history?page=1&page_size=50

# 4. Test search
curl http://localhost:8000/api/users/1/history?search=groceries

# 5. Test restoration
curl -X POST http://localhost:8000/api/users/1/history/123/restore

# Frontend test:
# 1. Complete 5 tasks, delete 3 tasks
# 2. Navigate to History tab
# 3. Verify: 8 entries displayed (5 completed, 3 deleted)
# 4. Apply filter: "Deleted only"
# 5. Verify: Only 3 deleted tasks shown
# 6. Search: "groceries"
# 7. Verify: Only matching tasks shown
# 8. Click "Restore" on deleted task
# 9. Verify: Task moves back to active list
```

**Acceptance Criteria**:
- [ ] History tab accessible from dashboard navigation
- [ ] All completed and deleted tasks visible with action_date, action_type
- [ ] Pagination works (50 entries per page)
- [ ] Filter by action_type (completed/deleted/all) and date range
- [ ] Search by title using full-text search
- [ ] Deleted tasks can be restored (completed tasks read-only)
- [ ] History entries auto-purged after 2 years

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Add notification preferences, error handling, documentation, and integration polish

### Tasks

- [ ] T076 [P] Implement get_notification_preferences and update_notification_preferences MCP tools in backend/src/mcp/tools.py
- [ ] T077 [P] Create NotificationPreferenceService in backend/src/services/ with CRUD methods
- [ ] T078 [P] Add notification settings UI in frontend (toggle enabled/disabled, set default reminder_minutes)
- [ ] T079 [P] Add comprehensive error handling for date parsing failures with user-friendly messages
- [ ] T080 [P] Add error handling for notification permission denial with inline warning banner
- [ ] T081 [P] Implement optimistic locking warning for concurrent task updates from multiple tabs
- [ ] T082 Update backend README.md to document new features (due dates, recurring tasks, history)
- [ ] T083 Update frontend README.md to document notification setup and service worker registration

**Validation**:
```bash
# Test notification preferences
curl http://localhost:8000/api/users/1/notification-preferences

# Update preferences
curl -X PUT http://localhost:8000/api/users/1/notification-preferences \
  -d '{"notification_enabled": true, "reminder_minutes_before": 30}'

# Test error handling: Invalid date
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"message": "Add task due xyz"}'
# Expected: Helpful error message

# Frontend test:
# 1. Open notification settings
# 2. Toggle notifications off
# 3. Try to set reminder: Verify warning displayed
# 4. Toggle back on
# 5. Change reminder time to 30 minutes
# 6. Create task with due date: Verify 30-minute reminder works
```

---

## Implementation Timeline

### Week 1: MVP (Phases 1-3)

**Day 1-2**: Setup & Foundational (Phases 1-2)
- Install dependencies
- Run database migrations
- Implement DateTimeParser and RecurrenceCalculator utilities
- Extend Task model

**Day 3-5**: Due Dates & Reminders (Phase 3)
- Implement SchedulerService
- Add due date support to TaskService and MCP tools
- Build frontend date picker and notification system
- Test end-to-end notification flow

**Day 6**: Testing & MVP Demo
- Comprehensive testing of due dates and reminders
- Fix bugs
- Prepare MVP demo

### Week 2: Full Feature Set (Phases 4-6)

**Day 7-8**: Recurring Tasks (Phase 4)
- Implement recurrence calculation logic
- Add recurring task creation on completion
- Build recurrence UI controls
- Test weekly/monthly patterns

**Day 9-10**: Task History (Phase 5)
- Implement HistoryService
- Build History tab with pagination
- Add search and filter functionality
- Test restoration flow

**Day 11**: Polish & Documentation (Phase 6)
- Add notification preferences
- Comprehensive error handling
- Update documentation
- Final integration testing

---

## Quick Start Guide

### First 5 Tasks to Get Started

1. **T001**: Update backend/pyproject.toml dependencies
   ```bash
   cd backend
   # Add to pyproject.toml:
   # dateparser = ">=1.3.0"
   # parsedatetime = ">=2.6"
   # APScheduler = ">=3.10.0"
   ```

2. **T002**: Install dependencies
   ```bash
   cd backend && uv pip install -e .
   ```

3. **T009**: Create database migration for extending tasks table
   ```sql
   -- backend/src/database/migrations/001_extend_tasks.sql
   ALTER TABLE tasks
   ADD COLUMN due_date TIMESTAMP WITH TIME ZONE,
   ADD COLUMN recurrence_pattern VARCHAR(20),
   ADD COLUMN is_recurring BOOLEAN DEFAULT FALSE,
   ADD COLUMN reminder_minutes INTEGER DEFAULT 15,
   ADD COLUMN next_occurrence TIMESTAMP WITH TIME ZONE;
   ```

4. **T014**: Implement DateTimeParser utility
   ```bash
   # Create backend/src/utils/datetime_parser.py
   # Implement dual-library parsing (dateparser + parsedatetime)
   ```

5. **T016**: Extend Task model
   ```bash
   # Update backend/src/models/task.py
   # Add 5 new fields with SQLModel Field definitions
   ```

---

## Parallel Execution Examples

### Within Phase 3 (US1: Due Dates & Reminders)

**Backend Team**:
- T019-T030: Implement SchedulerService, update TaskService, add MCP tools

**Frontend Team** (parallel):
- T031-T040: Build notification hook, date picker, update TaskList

**Timeline**: Both teams work simultaneously, integrate at end

### Phase 4 vs Phase 5

**Developer A** (Phase 4: Recurring Tasks):
- T041-T054: Implement recurring task logic

**Developer B** (Phase 5: History - parallel):
- T055-T075: Implement history service and UI

**Timeline**: Both features developed in parallel after Phase 3 completes, no dependencies between them

---

## Testing Strategy

### Manual Testing Checklist

**US1 (Due Dates & Reminders)**:
- [ ] Create task: "Add task to buy groceries tomorrow at 3pm"
- [ ] Verify: Due date stored in UTC, displayed in local timezone
- [ ] Verify: Notification appears 15 minutes before 3pm
- [ ] Verify: Notification appears at 3pm
- [ ] Verify: Overdue tasks highlighted in red (after 3pm)
- [ ] Test: Deny notification permission → verify warning displayed

**US2 (Recurring Tasks)**:
- [ ] Create: "weekly team meeting every Monday at 9am"
- [ ] Verify: Task shows "Repeats: Weekly on Monday"
- [ ] Complete task
- [ ] Verify: New task auto-created for next Monday at 9am
- [ ] Stop recurrence: Verify future instances not created
- [ ] Test edge case: Monthly task on day 31 → verify Feb uses day 28/29

**US3 (Task History)**:
- [ ] Complete 5 tasks, delete 3 tasks
- [ ] Navigate to History tab
- [ ] Verify: 8 entries displayed with correct metadata
- [ ] Filter: "Deleted only" → verify 3 entries
- [ ] Search: "groceries" → verify matching results
- [ ] Restore deleted task → verify task back in active list
- [ ] Verify: Pagination works for >50 entries

---

## Success Criteria

### MVP Success (Phases 1-3)

- [ ] Users can set due dates using natural language
- [ ] Browser notifications work (with permission)
- [ ] Due dates persist to database in UTC
- [ ] Visual indicators show task urgency (overdue/due today/upcoming)
- [ ] DateTimePicker allows precise date selection

### Full Feature Success (All Phases)

- [ ] All 3 user stories implemented (US1, US2, US3)
- [ ] 5 recurrence patterns working (daily, weekly, bi-weekly, monthly, yearly)
- [ ] Task history stores 2 years with auto-cleanup
- [ ] History search and filter functional
- [ ] Deleted tasks can be restored
- [ ] Notification preferences customizable
- [ ] Error handling comprehensive with user-friendly messages
- [ ] Documentation complete

---

## Notes & Tips

### Critical Dependencies

1. **Phase 2 MUST complete before Phase 3**: Database migrations must run before any services use new fields
2. **US1 MUST complete before US2**: Recurring tasks depend on due dates working
3. **US3 is independent**: History can be developed in parallel with US2 (Phase 4)

### Common Pitfalls

1. **Timezone handling**: Always store UTC in database, convert to browser timezone only for display
2. **Notification permission**: Request permission before scheduling notifications, handle denial gracefully
3. **APScheduler jobstore**: Use PostgreSQL jobstore (not in-memory) for stateless backend
4. **Recurring task edge cases**: Use dateutil.relativedelta for smart month handling (Jan 31 → Feb 28/29)
5. **History immutability**: TaskHistory records are write-once, never updated

### Performance Tips

1. **Database indexes**: Verify indexes on due_date, action_date, user_id exist after migrations
2. **History pagination**: Always use 50 entries per page to prevent large result sets
3. **Full-text search**: Use PostgreSQL GIN index for history title search
4. **Service worker**: Register only once on app startup, avoid re-registration on every render

### Debugging Tips

1. **Date parsing issues**: Test DateTimeParser.parse() independently with print statements
2. **Notification not appearing**: Check browser console for permission errors, verify service worker registered
3. **Recurring tasks not creating**: Check APScheduler logs, verify next_occurrence calculated correctly
4. **History not showing**: Verify HistoryService.create_history_entry() called on task completion/deletion

---

**End of Task Breakdown**

**Total**: 83 tasks | **Est. Duration**: 18-24 hours | **MVP**: ~8 hours (Phases 1-3)
