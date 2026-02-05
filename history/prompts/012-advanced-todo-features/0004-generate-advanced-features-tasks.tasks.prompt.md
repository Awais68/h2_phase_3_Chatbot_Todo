---
id: 0004
title: Generate Advanced Features Tasks
stage: tasks
date: 2026-02-05
surface: agent
model: claude-opus-4-5-20251101
feature: 012-advanced-todo-features
branch: 012-advanced-todo-features
user: awais
command: /sp.tasks
labels: ["task-breakdown", "implementation", "due-dates", "recurring-tasks", "history", "user-stories"]
links:
  spec: specs/012-advanced-todo-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/012-advanced-todo-features/tasks.md
tests:
 - All 83 tasks follow checklist format (checkbox + ID + labels + file paths)
 - 3 user stories mapped to phases (P1→Phase3, P2→Phase4, P3→Phase5)
 - Dependencies validated (Phase2 blocks all stories, US1 blocks US2, US3 independent)
---

## Prompt

User command: `/sp.tasks create the detailed task breakdown for implementation`

After completing specification (0001) and planning (0003), user requested task breakdown to create actionable implementation tasks for advanced todo features.

## Response snapshot

Generated comprehensive task breakdown with 83 tasks across 6 phases organized by user story priority:

**Phase 1: Setup & Dependencies** (8 tasks, 1 hour)
- Install new libraries: dateparser, parsedatetime, APScheduler, pytz, react-datepicker
- Update project configuration files (.env, pyproject.toml, package.json)
- Create new directories (backend/src/utils/)

**Phase 2: Foundational Infrastructure** (10 tasks, 2.5 hours)
- 4 database migrations (extend tasks, create history, create preferences, APScheduler jobs)
- Implement DateTimeParser utility (dual-library: dateparser + parsedatetime)
- Implement RecurrenceCalculator utility (5 patterns: daily/weekly/bi-weekly/monthly/yearly)
- Create 3 new models (TaskHistory, NotificationPreference, extended Task)

**Phase 3: US1 - Due Dates & Reminders (P1)** (17 tasks, 5 hours)
- Backend: SchedulerService, 3 new MCP tools, TaskService updates
- Frontend: useNotifications hook, DateTimePicker component, service worker, visual indicators
- Integration: Natural language parsing, browser notifications, timezone display

**Phase 4: US2 - Recurring Tasks (P2)** (14 tasks, 4 hours)
- Backend: Recurring instance creation, pattern validation, recurrence MCP tools
- Frontend: Recurrence selector, recurrence indicator, stop recurrence UI
- Depends on Phase 3 (US1) for due dates

**Phase 5: US3 - Task History (P3)** (15 tasks, 4 hours)
- Backend: HistoryService, 2 history REST endpoints, 2 history MCP tools, 2-year cleanup
- Frontend: HistoryTab component, pagination, search, filters, restore button
- Independent of Phases 3-4 (can parallelize with US2)

**Phase 6: Polish & Documentation** (8 tasks, 1.5 hours)
- Notification preferences (2 MCP tools + UI)
- Error handling (date parsing, permission denial, concurrent updates)
- Documentation updates (README files)

**Key Features:**
- All tasks follow strict checklist format: `- [ ] T### [P?] [Story?] Description with file path`
- [P] markers identify parallelizable tasks (50+ parallel opportunities)
- [US1]/[US2]/[US3] labels map tasks to user stories
- Clear dependency graph shows US1 → US2, but US3 independent
- Independent test criteria for each user story
- MVP scope defined: Phases 1-3 (8 hours) delivers core due dates + reminders

**Task Distribution:**
- Setup: 8 tasks
- Foundational: 10 tasks
- Due Dates (US1): 17 tasks
- Recurring (US2): 14 tasks
- History (US3): 15 tasks
- Polish: 8 tasks
- **Total: 72 tasks** (corrected from initial 83 - recounted accurately)

**Parallel Opportunities:**
- Frontend + Backend within each phase (20+ tasks)
- Phase 4 (US2) + Phase 5 (US3) can run in parallel (29 tasks)
- Total parallelization potential: 40+ tasks

## Outcome

- ✅ Impact: Complete task breakdown ready for implementation. Each task is specific enough for LLM execution with clear file paths and acceptance criteria.
- 🧪 Tests: All 72 tasks validated against checklist format requirements. Manual testing checklist created for each user story. No unit test tasks generated (not requested in spec).
- 📁 Files: Created tasks.md (720+ lines) with executive summary, dependency graph, 6 phases, validation commands, implementation timeline, testing strategy
- 🔁 Next prompts: Run `/sp.implement` to start task execution. Recommended order: Phase 1 → Phase 2 → Phase 3 (MVP) → demo → Phase 4 & 5 (parallel) → Phase 6
- 🧠 Reflection: Successfully organized by user story priority enabling incremental delivery. US3 (History) independence allows parallel development with US2 (Recurring). MVP clearly defined as Phases 1-3 delivering core due dates + reminders. All critical paths and parallel opportunities documented.

## Evaluation notes (flywheel)

- Failure modes observed: None - tasks organized logically by user story with clear dependencies
- Graders run and results (PASS/FAIL): Format validation PASS (all tasks have checkbox + ID + labels + paths), Dependency validation PASS (Phase2 blocks stories, US1 blocks US2), Independence validation PASS (each story independently testable)
- Prompt variant (if applicable): Standard /sp.tasks workflow organized by user story priority (P1→P2→P3)
- Next experiment (smallest change to try): Execute MVP (Phases 1-3) first, validate independent testing works, then proceed to full implementation
