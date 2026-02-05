# Feature Specification: Advanced Todo Features

**Feature Branch**: `012-advanced-todo-features`
**Created**: 2026-02-05
**Status**: Draft
**Input**: User description: "Implement Advanced Todo Features: Recurring Tasks, Due Dates & Reminders, and History Tab"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Set Due Dates and Receive Reminders (Priority: P1)

Users can set deadlines for their tasks using natural language or a date/time picker, and receive browser notifications when tasks are due or approaching their deadline. This ensures users never miss important deadlines.

**Why this priority**: This is the most critical feature because it directly addresses the core problem of time management. Without due dates and reminders, users can easily forget tasks. This delivers immediate value and is the foundation for the other features.

**Independent Test**: Can be fully tested by creating a task with "due tomorrow at 3pm", verifying the due date is stored, and confirming a browser notification appears 15 minutes before and at the due time.

**Acceptance Scenarios**:

1. **Given** a user creates a task with "buy groceries tomorrow at 3pm", **When** the natural language is parsed, **Then** the system sets the due date to tomorrow at 3:00 PM in the user's timezone
2. **Given** a user opens the task form, **When** they select a date/time using the picker, **Then** the due date is set and displayed with visual indicators (due today, overdue, upcoming)
3. **Given** a task is due in 15 minutes, **When** the reminder time is reached, **Then** the user receives a browser notification with the task title
4. **Given** a task is overdue, **When** the user views their task list, **Then** the overdue task is highlighted with a red indicator
5. **Given** a user hasn't granted notification permission, **When** they try to set a reminder, **Then** the system prompts for permission and gracefully handles denial

---

### User Story 2 - Create and Manage Recurring Tasks (Priority: P2)

Users can create tasks that automatically reschedule themselves after completion, such as "weekly team meeting" or "monthly rent payment". When a recurring task is marked complete, a new instance is automatically created with the next due date.

**Why this priority**: Recurring tasks save significant time for users with repetitive responsibilities. However, users must first have due dates working (P1) since recurring tasks depend on calculating next due dates. This is P2 because it builds on P1 functionality.

**Independent Test**: Can be fully tested by creating a task "weekly standup every Monday at 9am", completing it, and verifying a new task is automatically created for the following Monday at 9am.

**Acceptance Scenarios**:

1. **Given** a user creates a task "weekly team meeting", **When** they specify "recurring weekly", **Then** the system stores the recurrence pattern and displays it in task details
2. **Given** a recurring task is completed, **When** the completion is saved, **Then** a new task instance is automatically created with the next occurrence date
3. **Given** a user has a "monthly rent payment" task, **When** they complete it on Jan 15, **Then** a new task is created for Feb 15 at the same time
4. **Given** a user wants to stop a recurrence, **When** they edit the recurring task and select "stop recurrence", **Then** future instances are not created
5. **Given** a user updates a recurring task's details, **When** they choose "apply to all future instances", **Then** the recurrence pattern is updated for subsequent tasks

---

### User Story 3 - View Task History and Restore Deleted Tasks (Priority: P3)

Users can access a dedicated "History" tab in the dashboard to view all completed and deleted tasks from the past 2 years. They can search, filter by date range or status, and optionally restore deleted tasks.

**Why this priority**: History provides valuable record-keeping and accountability, but users can function without it. This is P3 because it's a convenience feature that enhances the experience but isn't critical for daily task management.

**Independent Test**: Can be fully tested by completing 5 tasks, deleting 3 tasks, navigating to the History tab, and verifying all 8 actions are displayed with correct metadata (completion date, deletion date, timestamps).

**Acceptance Scenarios**:

1. **Given** a user completes a task, **When** they navigate to the History tab, **Then** the completed task appears with completion date and timestamp
2. **Given** a user deletes a task, **When** they view History, **Then** the deleted task appears with deletion date and is marked as "deleted"
3. **Given** a user opens History, **When** they apply filters (completed/deleted, date range), **Then** only matching history entries are displayed
4. **Given** a user searches in History for "groceries", **When** the search executes, **Then** all historical tasks containing "groceries" are shown
5. **Given** a user finds a deleted task in History, **When** they click "restore", **Then** the task is moved back to the active task list with its original details
6. **Given** tasks are older than 2 years, **When** the automatic cleanup runs, **Then** old history entries are archived and no longer visible in the History tab

---

### Edge Cases

- What happens when a user sets a due date in the past? System should accept it but immediately mark it as overdue with appropriate visual indicators.
- How does the system handle recurring tasks when the user completes multiple instances at once? Only the oldest incomplete instance should trigger creation of the next occurrence.
- What happens when a user's browser doesn't support notifications or they deny permission? System should store reminder preferences but display a warning that notifications are unavailable, offering alternative reminder methods.
- How does the system handle timezone changes (e.g., user travels)? All due dates are stored in UTC and displayed in the user's current browser timezone.
- What happens when a recurring task lands on a non-working day (e.g., "monthly report on 31st" in February)? System should use the last day of the month (e.g., Feb 31st becomes Feb 28/29), ensuring the task always occurs monthly even if on a different day.
- How does the system handle very long task titles in notifications? Notifications should truncate titles to 50 characters with "..." to fit notification space.
- What happens when a user deletes a recurring task? Deletion stops all future recurrences - the entire recurring series is ended. This is the most intuitive behavior for users who want to cancel a recurring commitment.
- How does the system handle concurrent updates to the same task from multiple browser tabs? Use last-write-wins with optimistic locking and display a warning if conflicts are detected.
- What happens when the History tab has thousands of entries? Implement pagination with 50 entries per page and optimize database queries with indexes.
- How does the system handle restoring a deleted task that had a due date in the past? Restore with the original due date but mark it as overdue.

## Requirements *(mandatory)*

### Functional Requirements

**Due Dates & Reminders:**
- **FR-001**: System MUST allow users to set due dates for tasks using natural language input (e.g., "tomorrow at 3pm", "next Friday", "in 2 hours")
- **FR-002**: System MUST provide a date/time picker UI component for precise due date selection
- **FR-003**: System MUST store all due dates in UTC and display them in the user's browser timezone
- **FR-004**: System MUST support tasks without due dates (optional deadline field)
- **FR-005**: System MUST calculate and display task status: overdue, due today, due this week, upcoming, no deadline
- **FR-006**: System MUST request browser notification permission when a user sets their first reminder
- **FR-007**: System MUST send browser notifications at the exact due time for tasks
- **FR-008**: System MUST support reminder notifications before the due time (default: 15 minutes before, configurable)
- **FR-009**: System MUST display visual indicators for task urgency in the task list (red for overdue, yellow for due today, blue for upcoming)
- **FR-010**: System MUST handle notification permission denial gracefully and inform users

**Recurring Tasks:**
- **FR-011**: System MUST support standard recurrence patterns: daily, weekly, bi-weekly, monthly, yearly
- **FR-012**: System MUST allow users to specify recurrence when creating tasks via natural language (e.g., "weekly meeting")
- **FR-013**: System MUST display recurrence information in task details (e.g., "Repeats: Weekly on Monday")
- **FR-014**: System MUST automatically create the next task instance when a recurring task is completed
- **FR-015**: System MUST calculate the next due date based on the recurrence pattern (e.g., weekly = 7 days from current due date)
- **FR-016**: System MUST allow users to modify recurrence patterns on existing recurring tasks
- **FR-017**: System MUST allow users to stop recurrence (convert to one-time task)
- **FR-018**: System MUST allow users to choose whether updates apply to current instance only or all future instances
- **FR-019**: System MUST prevent completion of future recurring task instances (only the current/overdue instance can be completed)

**History Tab:**
- **FR-020**: System MUST provide a "History" tab in the dashboard navigation
- **FR-021**: System MUST store all completed tasks in history with completion date and timestamp
- **FR-022**: System MUST store all deleted tasks in history with deletion date and timestamp
- **FR-023**: System MUST retain history entries for 2 years from the action date
- **FR-024**: System MUST automatically archive or purge history entries older than 2 years
- **FR-025**: System MUST allow filtering history by status (completed, deleted, all)
- **FR-026**: System MUST allow filtering history by date range (from/to dates)
- **FR-027**: System MUST provide search functionality within history (search by task title)
- **FR-028**: System MUST display history entries as read-only (no editing)
- **FR-029**: System MUST allow users to restore deleted tasks from history
- **FR-030**: System MUST move restored tasks back to the active task list with original details preserved
- **FR-031**: System MUST implement pagination for history entries (50 per page)

**Cross-Cutting:**
- **FR-032**: System MUST integrate due dates and recurrence with the existing AI chatbot (allow natural language task creation with these features)
- **FR-033**: System MUST update existing Task model to include due_date, recurrence_pattern, next_occurrence, and reminder_time fields
- **FR-034**: System MUST create a TaskHistory entity to track completed and deleted tasks separately from active tasks
- **FR-035**: System MUST ensure all user data remains isolated (users can only see their own history)
- **FR-036**: System MUST validate due dates are in the future when creating new tasks (past dates are allowed but marked overdue)
- **FR-037**: System MUST handle background notification scheduling using a job scheduler
- **FR-038**: System MUST persist notification preferences per user

### Key Entities

- **Task (extended)**: Represents a todo item with new fields for due_date (optional timestamp in UTC), recurrence_pattern (nullable string: daily/weekly/bi-weekly/monthly/yearly), next_occurrence (calculated timestamp for recurring tasks), reminder_time (minutes before due time for notification), and is_recurring (boolean flag)

- **TaskHistory**: Represents a historical record of completed or deleted tasks. Attributes include: history_id (unique identifier), user_id (foreign key), original_task_id (reference to original task), title, description, completed status, due_date, action_type (completed or deleted), action_date (timestamp when completed/deleted), action_by (user who performed action), can_restore (boolean, true for deleted tasks). Retained for 2 years from action_date.

- **NotificationPreference**: Represents user's notification settings. Attributes include: user_id (foreign key), notification_enabled (boolean), reminder_minutes_before (integer, default 15), browser_permission_granted (boolean), timezone (string, user's timezone for display purposes).

- **RecurrencePattern**: Represents the recurrence configuration for recurring tasks. Attributes include: pattern_type (daily/weekly/bi-weekly/monthly/yearly), interval (integer, e.g., every 2 weeks), day_of_week (for weekly patterns), day_of_month (for monthly patterns), end_date (optional, when to stop creating instances).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can set a due date and receive a notification within 1 second of the scheduled time with 99% reliability
- **SC-002**: Users can create a recurring task and verify automatic rescheduling within 5 seconds of marking it complete
- **SC-003**: Users can access History tab and view all entries from the past 2 years within 2 seconds, even with 1000+ historical tasks
- **SC-004**: 95% of natural language due date inputs ("tomorrow at 3pm", "next Friday") are correctly parsed and set
- **SC-005**: System handles 1000 concurrent users with active notifications without performance degradation
- **SC-006**: Zero instances of notifications being sent to wrong users (100% data isolation)
- **SC-007**: Users can complete the full workflow (create task with due date, set reminder, receive notification, complete task, view in history) in under 2 minutes
- **SC-008**: 90% of users successfully grant notification permission on first prompt
- **SC-009**: Recurring task instances are created within 1 second of the previous instance being completed
- **SC-010**: History search returns results within 1 second for datasets up to 10,000 entries per user
- **SC-011**: Task restoration from History succeeds 100% of the time with all original data preserved
- **SC-012**: System automatically purges history entries older than 2 years within 24 hours of the 2-year mark

## Assumptions *(mandatory)*

- Users have modern browsers that support the Notification API (Chrome 50+, Firefox 52+, Safari 16+, Edge 79+)
- Users understand that browser notifications require explicit permission and may not work if denied
- Users will primarily use natural language for setting due dates, with the date/time picker as a secondary option
- Each user will have a reasonable number of active recurring tasks (< 50 simultaneous recurring patterns)
- History retention of 2 years is sufficient for most users' audit and record-keeping needs
- Users expect recurring tasks to reschedule based on the original due date, not the completion date (e.g., weekly Monday task completed on Tuesday still rescues for next Monday)
- Notification reminders default to 15 minutes before due time unless users customize it
- The existing Task entity can be extended with new fields without breaking existing functionality
- Background job scheduling for recurring tasks and notifications can be implemented using the existing backend infrastructure
- Users access the application primarily through web browsers (not mobile apps) for notification functionality
- Timezones are handled automatically based on browser settings; users don't need to manually configure timezone preferences
- For recurring patterns, "monthly" means same day of month (e.g., 15th of every month), and "weekly" means same day of week
- History pagination with 50 entries per page provides good balance between performance and usability
- Database indexes on due_date and action_date fields will maintain query performance as data grows
