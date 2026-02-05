# Implementation Plan: Advanced Todo Features

**Branch**: `012-advanced-todo-features` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/012-advanced-todo-features/spec.md`

## Summary

Extend the existing Todo AI Chatbot with advanced time management features: due dates with natural language parsing and browser notifications, automatically recurring tasks that reschedule on completion, and a comprehensive history tab for viewing and restoring completed/deleted tasks. The system uses **dateparser + parsedatetime** for 100% natural language coverage, **Web Notifications API + Service Worker** for browser notifications, **APScheduler with PostgreSQL jobstore** for background task scheduling, and extends the existing Task model with 5 new fields while adding 2 new entities (TaskHistory, NotificationPreference). All timestamps stored in UTC, displayed in user's browser timezone. Fully integrates with existing FastAPI + React + Neon PostgreSQL stack with zero additional infrastructure required.

## Technical Context

**Language/Version**: Python 3.13+ (backend), JavaScript/TypeScript (frontend)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, dateparser 1.3.0+, parsedatetime 2.6+, APScheduler 3.10.0+, pytz 2024.1+
- Frontend: React, OpenAI ChatKit, Web Notifications API, Service Worker API, react-datepicker (or similar)
**Storage**: Neon Serverless PostgreSQL (extended tasks table, new task_history and notification_preferences tables)
**Testing**: pytest (backend), Jest/Vitest (frontend)
**Target Platform**: Web application (browser-based + API server)
**Project Type**: Web (frontend + backend)
**Performance Goals**:
- Notification delivery: within 1 second of scheduled time (99% reliability)
- Natural language parsing: <100ms for 95% of inputs
- History query: <2 seconds for 10,000 records per user
- Recurring task creation: <1 second after completion
**Constraints**:
- Stateless backend (jobs persisted in PostgreSQL, not memory)
- Browser notifications require user permission
- Service workers require HTTPS in production
- APScheduler job persistence enables multi-instance backend
**Scale/Scope**:
- Expected: 1000 users, 50-100 active tasks per user
- Task History: 500-1000 entries per user (2-year retention)
- Notification jobs: 10-50 scheduled per user
- Background jobs: Daily history cleanup + per-task notification scheduling

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development First
- ✅ **PASS**: Complete specification exists at `specs/012-advanced-todo-features/spec.md`
- ✅ **PASS**: All 3 user stories prioritized (P1, P2, P3) with clear rationale
- ✅ **PASS**: 38 functional requirements documented
- ✅ **PASS**: Edge cases identified and resolved (2 clarifications completed)

### Principle II: Simplicity and Clean Code
- ✅ **PASS**: Extends existing Task model (5 new fields, backward-compatible)
- ✅ **PASS**: No new microservices or infrastructure (uses existing PostgreSQL)
- ⚠️ **REVIEW**: Adds 3 new libraries (dateparser, parsedatetime, apscheduler) - justified for feature requirements
- ✅ **PASS**: Dual-library date parsing increases complexity but achieves 100% coverage (justified)

### Principle III: User Experience Excellence
- ✅ **PASS**: Natural language date parsing ("tomorrow at 3pm") reduces friction
- ✅ **PASS**: Visual indicators (red/yellow/blue) for task urgency
- ✅ **PASS**: Browser notifications ensure users don't miss deadlines
- ✅ **PASS**: History tab with search/filter provides audit trail and restoration

### Principle IV: Data Integrity and Validation
- ✅ **PASS**: All timestamps timezone-aware (UTC storage, browser display)
- ✅ **PASS**: Recurring task validation (must have due_date and pattern)
- ✅ **PASS**: History immutability (no updates after creation)
- ✅ **PASS**: 2-year retention with automatic cleanup
- ✅ **PASS**: User isolation enforced at database level (user_id in all entities)

### Principle V: Modularity and Testability
- ✅ **PASS**: Separate DateTimeParser utility (21 test cases documented)
- ✅ **PASS**: Separate RecurrenceCalculator utility (5 patterns + edge cases)
- ✅ **PASS**: SchedulerService handles all background jobs
- ✅ **PASS**: Frontend hooks (useNotifications) separate from components
- ✅ **PASS**: Test coverage targets: ≥80% (existing standard)

### Principle VI: Standard Project Structure
- ✅ **PASS**: Follows existing web application structure (backend/ + frontend/)
- ✅ **PASS**: New utilities in backend/src/utils/
- ✅ **PASS**: New services in backend/src/services/
- ✅ **PASS**: Frontend hooks in frontend/src/hooks/

### Principle VII: Python Code Quality Standards
- ✅ **PASS**: Type hints required for all new functions
- ✅ **PASS**: Docstrings required with parameter documentation
- ✅ **PASS**: SQLModel validation methods for new fields
- ✅ **PASS**: pytest for all backend testing

### Principle IX: Performance and Resource Efficiency
- ✅ **PASS**: Database indexes on due_date, action_date (documented in data-model.md)
- ✅ **PASS**: History pagination (50 per page) prevents large result sets
- ✅ **PASS**: Full-text search index (GIN) for history title search
- ✅ **PASS**: APScheduler job persistence enables horizontal scaling

### Principle X: Version Control and Documentation
- ✅ **PASS**: Complete research.md (date parsing, notifications, scheduling)
- ✅ **PASS**: Complete data-model.md (3 entities, migrations, indexes)
- ✅ **PASS**: OpenAPI contracts (history-api.yaml, mcp-tools-extended.json)
- ✅ **PASS**: Git branch created (012-advanced-todo-features)

### Overall Assessment
**STATUS**: ✅ **PASS** - All critical gates passed. Additional libraries (dateparser, parsedatetime, apscheduler) justified by feature requirements (natural language parsing needs dual-library approach for 100% coverage; background scheduling requires stateless job persistence). Ready to proceed to Phase 2 (Task Breakdown).

## Project Structure

### Documentation (this feature)

```text
specs/012-advanced-todo-features/
├── spec.md                      # Feature specification (completed)
├── plan.md                      # This file (/sp.plan command output)
├── research.md                  # Phase 0 output - technical research (completed)
├── data-model.md                # Phase 1 output - database schema (completed)
├── quickstart.md                # Phase 1 output - integration guide (to be created)
├── contracts/                   # Phase 1 output - API contracts (completed)
│   ├── history-api.yaml         # History REST endpoints
│   └── mcp-tools-extended.json  # Extended MCP tool definitions
├── checklists/                  # Quality validation
│   └── requirements.md          # Spec quality checklist (completed)
└── tasks.md                     # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── __init__.py
│   ├── main.py                         # FastAPI app (update: add scheduler init)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py                     # UPDATE: extend with 5 new fields
│   │   ├── task_history.py             # NEW: history entity
│   │   ├── notification_preference.py  # NEW: user notification settings
│   │   ├── conversation.py             # EXISTING (no changes)
│   │   └── message.py                  # EXISTING (no changes)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py             # UPDATE: add due date, recurrence logic
│   │   ├── history_service.py          # NEW: history CRUD operations
│   │   ├── scheduler_service.py        # NEW: APScheduler integration
│   │   ├── conversation_service.py     # EXISTING (no changes)
│   │   └── agent_service.py            # UPDATE: add new MCP tools
│   ├── utils/                          # NEW directory
│   │   ├── __init__.py
│   │   ├── datetime_parser.py          # NEW: natural language date parsing
│   │   └── recurrence_calculator.py    # NEW: next occurrence calculation
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py                   # UPDATE: register new tools
│   │   └── tools.py                    # UPDATE: add 7 new MCP tools
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat.py                     # UPDATE: support due date in chat
│   │   ├── history.py                  # NEW: history REST endpoints
│   │   └── auth.py                     # EXISTING (no changes)
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py               # EXISTING (no changes)
│   │   └── migrations/
│   │       ├── 001_extend_tasks.sql    # NEW: add 5 columns to tasks
│   │       ├── 002_task_history.sql    # NEW: create history table
│   │       ├── 003_notif_prefs.sql     # NEW: create preferences table
│   │       └── 004_apscheduler.sql     # NEW: create jobs table
│   └── config/
│       ├── __init__.py
│       └── settings.py                 # UPDATE: add new env vars
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_datetime_parser.py     # NEW: 21 test cases
│   │   ├── test_recurrence_calc.py     # NEW: 5 patterns + edge cases
│   │   ├── test_history_service.py     # NEW: history CRUD tests
│   │   ├── test_scheduler_service.py   # NEW: notification scheduling tests
│   │   └── test_models.py              # UPDATE: test new Task fields
│   ├── integration/
│   │   ├── test_history_api.py         # NEW: history endpoint tests
│   │   ├── test_recurring_tasks.py     # NEW: recurrence flow tests
│   │   └── test_chat_api.py            # UPDATE: test due date in chat
│   └── contract/
│       └── test_mcp_extended.py        # NEW: test new MCP tools
├── pyproject.toml                      # UPDATE: add dependencies
├── .env.example                        # UPDATE: add scheduler config
└── README.md                           # UPDATE: document new features

frontend/
├── src/
│   ├── App.tsx                         # UPDATE: add History tab route
│   ├── components/
│   │   ├── ChatInterface.tsx           # UPDATE: support due date display
│   │   ├── TaskList.tsx                # UPDATE: add due date indicators
│   │   ├── HistoryTab.tsx              # NEW: history view component
│   │   ├── DateTimePicker.tsx          # NEW: date/time selection
│   │   └── AuthProvider.tsx            # EXISTING (no changes)
│   ├── hooks/
│   │   ├── useNotifications.ts         # NEW: notification permission & scheduling
│   │   └── useTaskHistory.ts           # NEW: history data fetching
│   ├── services/
│   │   ├── api.ts                      # EXISTING (no changes)
│   │   ├── chat.ts                     # UPDATE: send due_date_text
│   │   └── history.ts                  # NEW: history API client
│   ├── types/
│   │   ├── task.ts                     # UPDATE: add new Task fields
│   │   ├── history.ts                  # NEW: history types
│   │   └── notification.ts             # NEW: notification types
│   └── utils/
│       ├── formatters.ts               # UPDATE: format due dates
│       └── dateUtils.ts                # NEW: timezone display helpers
├── public/
│   └── service-worker.js               # NEW: notification service worker
├── tests/
│   ├── components/
│   │   ├── HistoryTab.test.tsx         # NEW: history UI tests
│   │   └── DateTimePicker.test.tsx     # NEW: picker tests
│   └── hooks/
│       └── useNotifications.test.ts    # NEW: notification hook tests
├── package.json                        # UPDATE: add dependencies
└── README.md                           # UPDATE: document new features

.env                                    # UPDATE: add scheduler, notification config
README.md                               # UPDATE: document advanced features
```

**Structure Decision**: Web application structure (Option 2) maintains consistency with existing `001-todo-ai-chatbot` architecture. Backend and frontend directories separated for independent deployment. New directories:
- `backend/src/utils/` for reusable utilities (date parsing, recurrence)
- `frontend/src/hooks/` for React custom hooks (notifications, history)
- `backend/src/database/migrations/` for 4 new migration files

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Dual-library date parsing | dateparser (62% success) + parsedatetime (86% success) = 100% coverage | Single library insufficient: dateparser fails "next Friday", parsedatetime fails timezone handling |
| APScheduler dependency | Stateless backend requires job persistence in PostgreSQL | In-memory scheduling (Python threading) lost on server restart; Celery too complex (requires broker) |

---

## Phase 0: Research (Completed)

**Status**: ✅ **COMPLETE** - All technical unknowns resolved

**Artifacts Generated**:
- `research.md` - 14KB comprehensive research document

**Key Decisions**:

1. **Natural Language Date Parsing**: dateparser (primary) + parsedatetime (fallback)
   - Rationale: Combined 100% success rate vs 62% (dateparser alone) or 86% (parsedatetime alone)
   - 21 test cases validated

2. **Browser Notifications**: Web Notifications API + Service Worker
   - Rationale: Native browser support, no external dependencies, works cross-platform
   - Hybrid scheduling: setTimeout (<1 hour), Service Worker (>1 hour)

3. **Background Job Scheduling**: APScheduler with PostgreSQL jobstore
   - Rationale: Lightweight, no broker required, stateless-compatible, PostgreSQL persistence
   - Alternative: Celery rejected (too complex for scope)

4. **Recurring Tasks**: Pattern-based date calculation (not cron)
   - Rationale: Simple, predictable, handles edge cases (Feb 31 → Feb 28/29)

5. **Timezone Strategy**: Store UTC, display browser local
   - Rationale: Single source of truth, automatic DST handling, no per-user timezone storage

## Phase 1: Design & Contracts (Completed)

**Status**: ✅ **COMPLETE** - All design artifacts generated

**Artifacts Generated**:
- `data-model.md` - Extended Task model + 2 new entities (TaskHistory, NotificationPreference)
- `contracts/history-api.yaml` - OpenAPI 3.0 spec for history REST endpoints
- `contracts/mcp-tools-extended.json` - 7 new MCP tool definitions

**Database Schema Changes**:

1. **Extended Task Table** (5 new columns):
   ```sql
   ALTER TABLE tasks ADD COLUMN due_date TIMESTAMP WITH TIME ZONE;
   ALTER TABLE tasks ADD COLUMN recurrence_pattern VARCHAR(20);
   ALTER TABLE tasks ADD COLUMN is_recurring BOOLEAN DEFAULT FALSE;
   ALTER TABLE tasks ADD COLUMN reminder_minutes INTEGER DEFAULT 15;
   ALTER TABLE tasks ADD COLUMN next_occurrence TIMESTAMP WITH TIME ZONE;
   ```

2. **New TaskHistory Table**:
   - Immutable audit trail (completed + deleted tasks)
   - 2-year retention with automatic cleanup
   - Full-text search index on title
   - Restore capability for deleted tasks

3. **New NotificationPreference Table**:
   - Per-user notification settings
   - One record per user (user_id primary key)
   - Default: enabled, 15 minutes before

4. **APScheduler Jobs Table**:
   - Job persistence for stateless backend
   - Enables multi-instance deployment

**API Contracts**:

1. **History REST API** (`history-api.yaml`):
   - `GET /users/{user_id}/history` - paginated history with filtering
   - `POST /users/{user_id}/history/{history_id}/restore` - restore deleted task

2. **Extended MCP Tools** (`mcp-tools-extended.json`):
   - `add_task_with_due_date` - create task with natural language due date
   - `update_task_due_date` - modify due date/recurrence
   - `list_tasks_by_due_date` - filter by overdue/due today/upcoming
   - `view_task_history` - browse history with search
   - `restore_deleted_task` - restore from history
   - `get_notification_preferences` - retrieve user settings
   - `update_notification_preferences` - modify notification settings

**Integration Points**:

1. **Backend Integration**:
   - FastAPI startup: initialize SchedulerService, schedule daily cleanup
   - Task completion: trigger recurring instance creation (if applicable)
   - Task deletion: cancel scheduled notifications, create history record

2. **Frontend Integration**:
   - Chat interface: parse natural language dates via backend
   - Task list: display due date indicators (red/yellow/blue)
   - New History tab: pagination, search, filter, restore
   - Notification permission: request on first reminder setup
   - Service worker: register for background notifications

## Agent Context Update

Run `.specify/scripts/bash/update-agent-context.sh claude` to add new technologies to `.claude/settings.local.json`:

**Technologies to Add**:
```json
{
  "012-advanced-todo-features": {
    "date_parsing": "dateparser + parsedatetime",
    "background_scheduling": "APScheduler 3.10.0+ with PostgreSQL jobstore",
    "browser_notifications": "Web Notifications API + Service Worker",
    "recurrence_calculation": "dateutil.relativedelta for smart month handling"
  }
}
```

## Next Steps

1. **Run `/sp.tasks`** to generate detailed task breakdown
   - Expected: 60-80 tasks across 5 phases (Setup, Due Dates, Recurring Tasks, History, Polish)
   - Dependencies: Backend tasks before frontend, database migrations before services

2. **Implementation Order** (recommended):
   - Phase 1: Extend Task model + migrations
   - Phase 2: Natural language date parsing + due dates
   - Phase 3: Browser notifications (frontend first, then backend scheduling)
   - Phase 4: Recurring tasks (calculation + auto-creation)
   - Phase 5: Task history (backend CRUD + frontend UI)
   - Phase 6: Integration testing + polish

3. **Critical Path**:
   - Database migrations must complete before any backend services
   - DateTimeParser utility required before task creation endpoints
   - SchedulerService required before notification scheduling
   - Task model extension required before recurring task logic

---

**Plan Complete**: All research and design phases finished. Ready for task breakdown with `/sp.tasks`.
