# Tasks: Phase I Complete Task Management System

**Feature**: Phase I Complete Task Management System
**Branch**: `003-phase1-task-mgmt`
**Created**: 2025-12-27
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

---

## Overview

This task breakdown implements Phase I Complete Task Management System with 6 user stories (P1-P6), prioritized for independent delivery. Voice input (US5) uses multi-turn conversation with state machine for error recovery.

**Total Tasks**: 120
**MVP Scope**: Phase 3 only (User Story 1 - Core Task Management)
**Recommended Delivery**: Phase-by-phase incremental delivery

---

## Implementation Strategy

1. **MVP First**: Deliver US1 (Core Task Management) as minimal viable product
2. **Incremental**: Add US2-US6 independently after MVP validation
3. **Parallel Opportunities**: Tasks marked [P] can run concurrently
4. **Independent Testing**: Each user story has clear test criteria

---

## Phase 1: Setup and Project Initialization

**Goal**: Initialize project structure, install dependencies, configure development environment

- [ ] T001 Initialize project with UV package manager in root directory
- [ ] T002 [P] Create src/ directory structure per plan.md
- [ ] T003 [P] Create tests/ directory structure per plan.md
- [ ] T004 Install Rich 13.0+ for terminal formatting via `uv add rich`
- [ ] T005 [P] Install python-dateutil 2.8+ for date parsing via `uv add python-dateutil`
- [ ] T006 [P] Install pytest 8.0+ for testing via `uv add --dev pytest pytest-cov`
- [ ] T007 [P] Install mypy 1.8+ and pylint 3.0+ via `uv add --dev mypy pylint`
- [ ] T008 Add optional voice dependencies group in pyproject.toml with SpeechRecognition>=3.10.0 and PyAudio>=0.2.13
- [ ] T009 Create .gitignore file with Python, IDE, and tasks.json entries
- [ ] T010 Run `uv sync` to install all dependencies

**Acceptance**: Project structure matches plan.md, all dependencies installed, uv sync succeeds

---

## Phase 2: Foundational Models and Infrastructure

**Goal**: Build core data models and enums needed by all user stories

- [ ] T011 [P] Create Priority enum (HIGH, MEDIUM, LOW, NONE) in src/models/enums.py
- [ ] T012 [P] Create Recurrence enum (NONE, DAILY, WEEKLY, MONTHLY) in src/models/enums.py
- [ ] T013 [P] Create Status enum (PENDING, COMPLETED, OVERDUE) in src/models/enums.py
- [ ] T014 Extend Task model with priority field (Priority enum, default NONE) in src/models/task.py
- [ ] T015 Extend Task model with due_date field (Optional[date], default None) in src/models/task.py
- [ ] T016 Extend Task model with recurrence field (Recurrence enum, default NONE) in src/models/task.py
- [ ] T017 Add computed status property to Task model in src/models/task.py
- [ ] T018 Update Task.to_dict() to serialize priority, due_date, recurrence in src/models/task.py
- [ ] T019 Update Task.from_dict() to deserialize priority, due_date, recurrence in src/models/task.py
- [ ] T020 [P] Create date parser utility with parse_date() function in src/lib/date_parser.py
- [ ] T021 [P] Create validators utility module in src/lib/validators.py
- [ ] T022 [P] Create custom exceptions module in src/lib/exceptions.py

**Acceptance**: All enums importable, Task model has new fields with validation, date parser handles "tomorrow"/"2025-12-31"

---

## Phase 3: User Story 1 - Core Task Management (Priority: P1)

**Story Goal**: Create and manage tasks with priority levels, due dates, and completion tracking

**Independent Test**: Add tasks with different priorities and due dates, mark complete, verify status display (pending/completed/overdue)

- [ ] T023 [US1] Update TaskService.create_task() to accept priority, due_date, recurrence in src/services/task_service.py
- [ ] T024 [US1] Update TaskService.update_task() to accept priority, due_date, recurrence in src/services/task_service.py
- [ ] T025 [US1] Implement status calculation logic in TaskService.get_all_tasks() in src/services/task_service.py
- [ ] T026 [US1] Update PersistenceService to save/load priority, due_date, recurrence in src/services/persistence_service.py
- [ ] T027 [US1] Create add task flow with priority prompt in src/cli/prompts.py
- [ ] T028 [US1] Create add task flow with due date prompt (natural language) in src/cli/prompts.py
- [ ] T029 [US1] Create add task flow with recurrence prompt in src/cli/prompts.py
- [ ] T030 [US1] Update edit task flow to allow editing priority, due_date, recurrence in src/cli/prompts.py
- [ ] T031 [US1] Implement priority color coding (Red=High, Yellow=Medium, Green=Low) in src/cli/formatter.py
- [ ] T032 [US1] Implement status color coding (Red=Overdue, Cyan=Pending, Green=Completed) in src/cli/formatter.py
- [ ] T033 [US1] Add emoji status indicators (⏳ Pending, ✓ Complete, 🔴 Overdue) in src/cli/formatter.py
- [ ] T034 [US1] Update task table display with Priority, Due Date, Status, Recurrence columns in src/cli/formatter.py
- [ ] T035 [US1] Implement overdue auto-sort to top of list in src/cli/menu.py
- [ ] T036 [US1] Wire up new fields in main menu add/edit/view flows in src/main.py

**Acceptance**: Users can create/edit/view tasks with priority, due dates, recurrence. Overdue tasks display at top in red. Color coding works.

---

## Phase 4: User Story 2 - Advanced Filtering and Search (Priority: P2)

**Story Goal**: Filter tasks by status, priority, date range and search by keywords

**Independent Test**: Create 20+ tasks, filter by High priority, verify only high-priority tasks shown. Search "meeting", verify correct results.

- [ ] T037 [P] [US2] Create FilterState dataclass in src/models/filter.py
- [ ] T038 [P] [US2] Create SortOption enum in src/models/sort_option.py
- [ ] T039 [US2] Implement FilterService.apply_filters() for status filtering in src/services/filter_service.py
- [ ] T040 [US2] Implement FilterService.apply_filters() for priority filtering in src/services/filter_service.py
- [ ] T041 [US2] Implement FilterService.apply_filters() for date range filtering in src/services/filter_service.py
- [ ] T042 [US2] Implement FilterService.apply_filters() for keyword search in src/services/filter_service.py
- [ ] T043 [US2] Add FilterState.is_active() method in src/models/filter.py
- [ ] T044 [US2] Add FilterState.describe() method for human-readable filter description in src/models/filter.py
- [ ] T045 [US2] Create filter menu UI with options (Status, Priority, Date Range, Clear) in src/cli/menu.py
- [ ] T046 [US2] Implement filter by status flow in src/cli/menu.py
- [ ] T047 [US2] Implement filter by priority flow in src/cli/menu.py
- [ ] T048 [US2] Implement filter by date range flow (Today, This Week, This Month, Overdue, Custom) in src/cli/menu.py
- [ ] T049 [US2] Implement clear filters flow in src/cli/menu.py
- [ ] T050 [US2] Create search menu option in main menu in src/cli/menu.py
- [ ] T051 [US2] Implement search flow with keyword prompt in src/cli/menu.py
- [ ] T052 [US2] Display filtered count "Showing X of Y tasks" in src/cli/formatter.py
- [ ] T053 [US2] Persist FilterState across operations (module-level variable) in src/main.py
- [ ] T054 [US2] Display active filters above task list in src/cli/formatter.py

**Acceptance**: Users can filter by status/priority/date range, search by keyword. Filters persist across operations. Count shows filtered results.

---

## Phase 5: User Story 3 - Recurring Tasks (Priority: P3)

**Story Goal**: Create recurring tasks that auto-generate next occurrence when completed

**Independent Test**: Create task with Daily recurrence, mark complete, verify new instance created with tomorrow's due date

- [ ] T055 [US3] Implement RecurringService.create_next_occurrence() in src/services/recurring_service.py
- [ ] T056 [US3] Calculate next due date for DAILY (+1 day) in src/services/recurring_service.py
- [ ] T057 [US3] Calculate next due date for WEEKLY (+7 days) in src/services/recurring_service.py
- [ ] T058 [US3] Calculate next due date for MONTHLY (+30 days) in src/services/recurring_service.py
- [ ] T059 [US3] Update TaskService.toggle_completion() to detect recurring tasks in src/services/task_service.py
- [ ] T060 [US3] Call RecurringService when recurring task completed in src/services/task_service.py
- [ ] T061 [US3] Display recurrence indicator "↻ Daily" in task list in src/cli/formatter.py
- [ ] T062 [US3] Validate recurring tasks have due dates in add/edit flows in src/cli/prompts.py

**Acceptance**: Marking recurring task complete creates next occurrence with correct due date. Recurrence indicator shows in list.

---

## Phase 6: User Story 4 - Sort and Display Options (Priority: P4)

**Story Goal**: Sort tasks by priority, due date, or creation date

**Independent Test**: Create tasks with varied priorities/dates, cycle through sort options, verify correct reordering each time

- [ ] T063 [P] [US4] Create SortBy enum (DEFAULT, PRIORITY, DUE_DATE, CREATED_DATE) in src/models/enums.py
- [ ] T064 [US4] Implement sort_tasks() with overdue-first logic in src/services/task_service.py
- [ ] T065 [US4] Implement DEFAULT sort (overdue by due_date, then created_at desc) in src/services/task_service.py
- [ ] T066 [US4] Implement PRIORITY sort (overdue first, then High→Medium→Low→None) in src/services/task_service.py
- [ ] T067 [US4] Implement DUE_DATE sort (overdue first, then earliest due date) in src/services/task_service.py
- [ ] T068 [US4] Implement CREATED_DATE sort (overdue first, then newest first) in src/services/task_service.py
- [ ] T069 [US4] Create sort menu UI in src/cli/menu.py
- [ ] T070 [US4] Implement sort selection flow in src/cli/menu.py
- [ ] T071 [US4] Persist sort preference across operations (module-level) in src/main.py
- [ ] T072 [US4] Combine filters and sort (filter first, then sort) in src/main.py
- [ ] T073 [US4] Display current sort order above task list in src/cli/formatter.py

**Acceptance**: Users can sort by Priority/DueDate/CreatedDate. Overdue always at top. Sort persists. Filters+sort work together.

---

## Phase 7: User Story 5 - Optional Voice Input (Priority: P5)

**Story Goal**: Use voice input with multi-turn conversation to create tasks hands-free

**Independent Test**: Say "add task" → "buy milk" → "high" → "tomorrow" → "none", verify confirmation summary, create task

- [ ] T074 [P] [US5] Create ConversationStep enum in src/models/voice_state.py
- [ ] T075 [P] [US5] Create VoiceState dataclass with current_step, collected_data, step_history in src/models/voice_state.py
- [ ] T076 [US5] Implement VoiceService.start_conversation() in src/services/voice_service.py
- [ ] T077 [US5] Implement VoiceService.listen() with microphone recording in src/services/voice_service.py
- [ ] T078 [US5] Implement VoiceService.transcribe() with Google Speech API in src/services/voice_service.py
- [ ] T079 [US5] Implement VoiceService.collect_title() with sequential prompt in src/services/voice_service.py
- [ ] T080 [US5] Implement VoiceService.collect_priority() with normalization in src/services/voice_service.py
- [ ] T081 [US5] Implement VoiceNormalizer.normalize_priority() with flexible patterns in src/services/voice_normalizer.py
- [ ] T082 [US5] Implement VoiceService.collect_due_date() in src/services/voice_service.py
- [ ] T083 [US5] Implement VoiceService.collect_recurrence() in src/services/voice_service.py
- [ ] T084 [US5] Implement VoiceService.check_for_correction() for "go back" command in src/services/voice_service.py
- [ ] T085 [US5] Implement VoiceService.show_confirmation() with summary in src/services/voice_service.py
- [ ] T086 [US5] Handle low confidence transcriptions (<70%) in src/services/voice_service.py
- [ ] T087 [US5] Create voice menu option (conditional on SpeechRecognition availability) in src/cli/voice_menu.py
- [ ] T088 [US5] Wire up voice flow in main menu in src/main.py
- [ ] T089 [US5] Add graceful degradation if microphone unavailable in src/services/voice_service.py

**Acceptance**: Voice input guides through fields sequentially. "Go back" works. Flexible normalization ("high priority"→HIGH). Graceful errors.

---

## Phase 8: User Story 6 - Visual Enhancements (Priority: P6)

**Story Goal**: Visually appealing interface with colors, icons, clear formatting

**Independent Test**: Launch app, verify ASCII art, colors, emoji, Rich tables display correctly

- [ ] T090 [P] [US6] Verify ASCII art title displays on launch in src/main.py
- [ ] T091 [P] [US6] Verify Rich table formatting with borders in src/cli/formatter.py
- [ ] T092 [P] [US6] Verify emoji status indicators display in src/cli/formatter.py
- [ ] T093 [P] [US6] Create Theme dataclass in src/models/theme.py
- [ ] T094 [US6] Implement theme switching (Dark, Light, Hacker) in src/cli/menu.py
- [ ] T095 [US6] Test graceful fallback for no-color terminals in src/cli/formatter.py
- [ ] T096 [US6] Add progress indicators for save/load operations in src/cli/formatter.py

**Acceptance**: ASCII art shows, Rich tables formatted, emojis display, themes switchable, color fallback works

---

## Phase 9: Polish, Testing, and Documentation

**Goal**: Comprehensive testing, documentation, final polish

- [ ] T097 [P] Create unit tests for enums in tests/unit/test_enums.py
- [ ] T098 [P] Create unit tests for Task model extensions in tests/unit/test_task_model.py
- [ ] T099 [P] Create unit tests for FilterState in tests/unit/test_filter_model.py
- [ ] T100 [P] Create unit tests for VoiceState in tests/unit/test_voice_state.py
- [ ] T101 [P] Create unit tests for TaskService in tests/unit/test_task_service.py
- [ ] T102 [P] Create unit tests for RecurringService in tests/unit/test_recurring_service.py
- [ ] T103 [P] Create unit tests for VoiceNormalizer in tests/unit/test_voice_normalizer.py
- [ ] T104 [P] Create unit tests for date parser in tests/unit/test_date_parser.py
- [ ] T105 [P] Create unit tests for validators in tests/unit/test_validators.py
- [ ] T106 [P] Create integration test for CLI menu flows in tests/integration/test_cli_menu.py
- [ ] T107 [P] Create integration test for voice conversation flow in tests/integration/test_voice_flow.py
- [ ] T108 [P] Create integration test for persistence in tests/integration/test_persistence.py
- [ ] T109 [P] Create contract test for CLI interface in tests/contract/test_cli_interface.py
- [ ] T110 [P] Create contract test for voice interface in tests/contract/test_voice_interface.py
- [ ] T111 Run full test suite with `pytest tests/ --cov=src --cov-report=term-missing`
- [ ] T112 Verify test coverage ≥80% per constitution
- [ ] T113 Run mypy type checking with `mypy src/` and fix all errors
- [ ] T114 Run pylint with `pylint src/` and achieve score ≥8.0
- [ ] T115 Update README.md with complete feature list, installation, usage
- [ ] T116 Document voice input setup in README.md
- [ ] T117 Create quickstart guide in specs/003-phase1-task-mgmt/quickstart.md
- [ ] T118 Run performance test with 1000 tasks, verify <200ms list render
- [ ] T119 Manual integration test: full workflow from add to filter to sort to complete recurring
- [ ] T120 Create demo script showcasing all features

**Acceptance**: All tests pass, coverage ≥80%, no type/lint errors, documentation complete, performance targets met

---

## Dependencies and Execution Order

### Story Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundation) → Phase 3 (US1) ──┐
                                                           ├→ Phase 4 (US2) [depends on US1]
                                                           ├→ Phase 5 (US3) [depends on US1]
                                                           ├→ Phase 6 (US4) [depends on US1]
                                                           ├→ Phase 7 (US5) [depends on US1]
                                                           └→ Phase 8 (US6) [depends on US1]

All user stories → Phase 9 (Polish & Testing)
```

**Critical Path**: Phase 1 → Phase 2 → Phase 3 (US1) must complete sequentially. US2-US6 can be implemented in parallel after US1.

### Parallel Execution Examples

**Phase 2 Parallelization** (Foundation):
- Run T011, T012, T013 (enums) in parallel
- Run T020, T021, T022 (utilities) in parallel after enums

**Phase 3 Parallelization** (US1):
- After T023-T026 (services) complete, run T027-T029 (prompts) and T031-T033 (formatting) in parallel

**Phase 4-8 Parallelization** (US2-US6):
- After Phase 3 complete, all user stories US2-US6 can start in parallel
- Within US2: T037-T038 (models) parallel, then T039-T042 (services) parallel

**Phase 9 Parallelization** (Testing):
- All T097-T110 (tests) can run in parallel as they're independent

---

## MVP Scope Recommendation

**Minimum Viable Product**: **Phase 3 only (User Story 1)**

Delivers:
- Create/read/update/delete tasks
- Priority levels with color coding
- Due dates with overdue detection
- Status tracking (pending/completed/overdue)
- Rich terminal UI with tables and colors
- JSON persistence

**MVP Validation**: Can fully test US1 independently. Delivers immediate value as functional task manager.

**Post-MVP**: Add US2-US6 incrementally based on user feedback.

---

## Task Count Summary

| Phase | Tasks | Parallel | Story Dependencies |
|-------|-------|----------|-------------------|
| Phase 1: Setup | 10 | 5 | None |
| Phase 2: Foundation | 12 | 6 | Phase 1 |
| Phase 3: US1 Core | 14 | 0 | Phase 2 |
| Phase 4: US2 Filter/Search | 18 | 6 | Phase 3 (US1) |
| Phase 5: US3 Recurring | 8 | 0 | Phase 3 (US1) |
| Phase 6: US4 Sorting | 11 | 1 | Phase 3 (US1) |
| Phase 7: US5 Voice Input | 16 | 3 | Phase 3 (US1) |
| Phase 8: US6 Visual | 7 | 4 | Phase 3 (US1) |
| Phase 9: Polish & Test | 24 | 18 | All stories |
| **TOTAL** | **120** | **43** | - |

**Parallel Opportunities**: 43 tasks (36%) can run concurrently with proper coordination

**Estimated Effort**:
- Setup & Foundation: 1-2 hours
- US1 (MVP): 3-4 hours
- US2-US6: 2-3 hours each
- Testing & Polish: 3-4 hours
- **Total: 15-20 hours** for complete implementation

---

## Format Validation

✅ All tasks follow checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
✅ Sequential task IDs (T001-T120)
✅ [P] marker on parallelizable tasks
✅ [US#] labels on user story tasks
✅ Clear file paths specified
✅ Independent test criteria per story
✅ Dependency graph provided
✅ MVP scope identified

**Status**: Tasks.md ready for implementation via `/sp.implement`
