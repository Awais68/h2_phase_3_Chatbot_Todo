# End-to-End Test Scenarios

## Overview

This document provides comprehensive end-to-end test scenarios for the Todo AI Chatbot. Each scenario tests multiple features working together to ensure the system functions correctly as a whole.

## Test Environment Setup

**Prerequisites**:
- Backend running on http://localhost:8000
- Frontend running on http://localhost:3000
- Database connected (Neon PostgreSQL)
- OpenAI API key configured
- Clean database state (or known test data)

**Test User**:
- User ID: 1 (or configured test user)
- Clean slate: No existing tasks

## Scenario 1: Voice-Based Task Management

**Objective**: Complete full task lifecycle using voice commands

**Duration**: 5 minutes

**Steps**:

1. **Setup**:
   - Open http://localhost:3000/chatbot
   - Navigate to Chat tab
   - Ensure microphone permissions granted

2. **Create Task via Voice**:
   - Click microphone button (🎤)
   - Speak: "Add a task to call mom tomorrow"
   - Wait for transcription
   - Click Send
   - **Verify**:
     - ✅ Task created with title "Call mom tomorrow"
     - ✅ Assistant confirms creation
     - ✅ Response is spoken aloud

3. **List Tasks via Voice**:
   - Click microphone button
   - Speak: "Show me all my pending tasks"
   - **Verify**:
     - ✅ Task list displayed
     - ✅ "Call mom tomorrow" appears in list
     - ✅ Response is spoken aloud

4. **Complete Task via Voice**:
   - Click microphone button
   - Speak: "Mark task 1 as done"
   - **Verify**:
     - ✅ Task marked as completed
     - ✅ Confirmation message displayed
     - ✅ Response is spoken aloud

5. **Verify Completion**:
   - Click microphone button
   - Speak: "Show me completed tasks"
   - **Verify**:
     - ✅ Completed task appears
     - ✅ Task shows completed status

6. **Delete Task via Voice**:
   - Click microphone button
   - Speak: "Delete task 1"
   - **Verify**:
     - ✅ Task deleted
     - ✅ Confirmation message
     - ✅ Task no longer in list

**Expected Outcome**:
- ✅ All voice commands recognized correctly
- ✅ All operations completed successfully
- ✅ All responses spoken aloud
- ✅ No manual typing required

**Failure Scenarios**:
- ❌ Voice not recognized → Check microphone
- ❌ Task not created → Check backend logs
- ❌ No voice output → Check browser audio

---

## Scenario 2: Recurring Task Workflow

**Objective**: Create and manage recurring tasks

**Duration**: 7 minutes

**Steps**:

1. **Create Daily Recurring Task**:
   - Navigate to Recurring tab
   - Click "+ New Recurring Task"
   - Fill form:
     - Title: "Review emails"
     - Description: "Check and respond to emails"
     - Frequency: Daily
   - Click "Create Recurring Task"
   - **Verify**:
     - ✅ Task appears in recurring list
     - ✅ Status shows "Active"
     - ✅ Frequency shows "Daily"

2. **Create Weekly Recurring Task**:
   - Click "+ New Recurring Task"
   - Fill form:
     - Title: "Team meeting"
     - Description: "Weekly standup"
     - Frequency: Weekly
     - Day: Monday
   - Click "Create Recurring Task"
   - **Verify**:
     - ✅ Task appears in list
     - ✅ Frequency shows "Weekly (Monday)"

3. **Create Monthly Recurring Task**:
   - Click "+ New Recurring Task"
   - Fill form:
     - Title: "Monthly report"
     - Frequency: Monthly
     - Day: 1
   - Click "Create Recurring Task"
   - **Verify**:
     - ✅ Task appears in list
     - ✅ Frequency shows "Monthly (Day 1)"

4. **Pause Recurring Task**:
   - Find "Review emails" task
   - Click "Pause" button
   - **Verify**:
     - ✅ Status changes to "Paused"
     - ✅ Badge color changes to gray

5. **Resume Recurring Task**:
   - Find "Review emails" task
   - Click "Resume" button
   - **Verify**:
     - ✅ Status changes to "Active"
     - ✅ Badge color changes to green

6. **Delete Recurring Task**:
   - Find "Monthly report" task
   - Click "Delete" button
   - Confirm deletion
   - **Verify**:
     - ✅ Task removed from list
     - ✅ Confirmation message shown

7. **Verify via Chat**:
   - Navigate to Chat tab
   - Type: "Show me my recurring tasks"
   - **Verify**:
     - ✅ Lists active recurring tasks
     - ✅ Shows correct frequencies

**Expected Outcome**:
- ✅ All recurring tasks created successfully
- ✅ Pause/resume functionality works
- ✅ Delete removes task permanently
- ✅ Chat interface can query recurring tasks

---

## Scenario 3: Analytics Viewing

**Objective**: Verify analytics display accurate data

**Duration**: 5 minutes

**Setup**:
- Create test data: 10 tasks (6 completed, 4 pending)

**Steps**:

1. **Create Test Tasks**:
   - Navigate to Chat tab
   - Create 10 tasks via chat:
     - "Add task 1", "Add task 2", ... "Add task 10"
   - Complete 6 tasks:
     - "Complete task 1", "Complete task 2", ... "Complete task 6"

2. **View Analytics Overview**:
   - Navigate to Analytics tab
   - **Verify Statistics Cards**:
     - ✅ Total Tasks: 10
     - ✅ Completed: 6
     - ✅ Pending: 4
     - ✅ Completion Rate: 60%

3. **View Pie Chart**:
   - Locate "Task Status Distribution" chart
   - **Verify**:
     - ✅ Green slice: 60% (Completed)
     - ✅ Yellow slice: 40% (Pending)
     - ✅ Legend shows correct labels

4. **View Line Chart**:
   - Locate "Tasks Over Time" chart
   - **Verify**:
     - ✅ Shows last 30 days
     - ✅ Blue line: Created tasks
     - ✅ Green line: Completed tasks
     - ✅ Data points match task creation dates

5. **View Bar Chart**:
   - Locate "Productivity by Hour" chart
   - **Verify**:
     - ✅ Shows 24 hours (0-23)
     - ✅ Bars show task completion by hour
     - ✅ Matches actual completion times

6. **Refresh Analytics**:
   - Click "Refresh Analytics" button
   - **Verify**:
     - ✅ Data updates
     - ✅ Charts re-render
     - ✅ No errors

7. **Create More Tasks**:
   - Navigate to Chat tab
   - Create 2 more tasks
   - Complete 1 task
   - Return to Analytics tab
   - **Verify**:
     - ✅ Total Tasks: 12
     - ✅ Completed: 7
     - ✅ Pending: 5
     - ✅ Completion Rate: 58.33%

**Expected Outcome**:
- ✅ All statistics accurate
- ✅ All charts display correctly
- ✅ Data updates in real-time
- ✅ No rendering errors

---

## Scenario 4: Multi-Tab Workflow

**Objective**: Test seamless navigation between tabs

**Duration**: 5 minutes

**Steps**:

1. **Chat → Analytics**:
   - Start in Chat tab
   - Create 3 tasks
   - Switch to Analytics tab
   - **Verify**: Data reflects new tasks

2. **Analytics → Recurring**:
   - From Analytics tab
   - Switch to Recurring tab
   - Create recurring task
   - **Verify**: Tab switches smoothly

3. **Recurring → Chat**:
   - From Recurring tab
   - Switch to Chat tab
   - Ask: "Show my recurring tasks"
   - **Verify**: Lists recurring tasks

4. **Rapid Tab Switching**:
   - Quickly switch: Chat → Analytics → Recurring → Chat
   - **Verify**:
     - ✅ No lag or freezing
     - ✅ Data persists across switches
     - ✅ No errors in console

**Expected Outcome**:
- ✅ Smooth tab transitions
- ✅ Data consistency across tabs
- ✅ No performance issues

---

## Scenario 5: Error Handling

**Objective**: Test system behavior with errors

**Duration**: 5 minutes

**Steps**:

1. **Invalid Task Creation**:
   - Type: "Add a task with a title that is way too long and exceeds the maximum character limit of 200 characters which should trigger a validation error from the backend API and return an appropriate error message to the user"
   - **Verify**:
     - ✅ Error message displayed
     - ✅ Task not created
     - ✅ User can retry

2. **Non-Existent Task**:
   - Type: "Complete task 999"
   - **Verify**:
     - ✅ Error: "Task not found"
     - ✅ Helpful message displayed

3. **Empty Message**:
   - Try to send empty message
   - **Verify**:
     - ✅ Send button disabled
     - ✅ No API call made

4. **Network Error Simulation**:
   - Stop backend server
   - Try to send message
   - **Verify**:
     - ✅ Error message: "Failed to send message"
     - ✅ User can retry
   - Restart backend
   - Retry message
   - **Verify**:
     - ✅ Message sends successfully

5. **Voice Recognition Error**:
   - Click microphone
   - Don't speak (timeout)
   - **Verify**:
     - ✅ Graceful timeout
     - ✅ No error thrown
     - ✅ Can retry

**Expected Outcome**:
- ✅ All errors handled gracefully
- ✅ Clear error messages
- ✅ System remains stable
- ✅ User can recover from errors

---

## Scenario 6: Performance Under Load

**Objective**: Test system with many tasks

**Duration**: 10 minutes

**Steps**:

1. **Create 50 Tasks**:
   - Use chat to create 50 tasks
   - **Verify**:
     - ✅ All tasks created
     - ✅ No performance degradation
     - ✅ Response times < 3 seconds

2. **List All Tasks**:
   - Type: "Show me all my tasks"
   - **Verify**:
     - ✅ All 50 tasks listed
     - ✅ Response time acceptable
     - ✅ UI remains responsive

3. **View Analytics with Large Dataset**:
   - Navigate to Analytics tab
   - **Verify**:
     - ✅ Charts render correctly
     - ✅ No lag or freezing
     - ✅ Data accurate

4. **Complete Many Tasks**:
   - Complete 30 tasks
   - **Verify**:
     - ✅ All completions processed
     - ✅ Analytics update correctly

5. **Delete Many Tasks**:
   - Delete 20 tasks
   - **Verify**:
     - ✅ All deletions processed
     - ✅ List updates correctly

**Expected Outcome**:
- ✅ System handles 50+ tasks
- ✅ No performance issues
- ✅ All operations complete successfully

---

## Scenario 7: Conversation Context

**Objective**: Test conversation memory

**Duration**: 5 minutes

**Steps**:

1. **Create Task**:
   - Type: "Add a task to buy milk"
   - **Verify**: Task created

2. **Reference Previous Context**:
   - Type: "Actually, make that 2 gallons"
   - **Verify**:
     - ✅ System understands "that" refers to milk task
     - ✅ Task updated to "Buy 2 gallons of milk"

3. **Multi-Turn Conversation**:
   - Type: "Add a task to call dentist"
   - Type: "When should I do that?"
   - **Verify**:
     - ✅ System understands "that" refers to dentist task
     - ✅ Provides relevant response

4. **Context Across Operations**:
   - Type: "Show me my tasks"
   - Type: "Complete the first one"
   - **Verify**:
     - ✅ System completes first task from list
     - ✅ Maintains context

**Expected Outcome**:
- ✅ Conversation context maintained
- ✅ References resolved correctly
- ✅ Natural conversation flow

---

## Test Results Summary Template

```markdown
## E2E Test Results: [Date]

**Tester**: [Name]
**Environment**: [Local/Staging/Production]
**Duration**: [Total time]

### Scenario Results

| Scenario | Status | Duration | Issues |
|----------|--------|----------|--------|
| 1. Voice-Based Task Management | PASS/FAIL | Xm | [Issues] |
| 2. Recurring Task Workflow | PASS/FAIL | Xm | [Issues] |
| 3. Analytics Viewing | PASS/FAIL | Xm | [Issues] |
| 4. Multi-Tab Workflow | PASS/FAIL | Xm | [Issues] |
| 5. Error Handling | PASS/FAIL | Xm | [Issues] |
| 6. Performance Under Load | PASS/FAIL | Xm | [Issues] |
| 7. Conversation Context | PASS/FAIL | Xm | [Issues] |

### Overall Assessment

**Pass Rate**: X/7 (XX%)
**Critical Issues**: [Count]
**Minor Issues**: [Count]

### Issues Found

1. **[Issue Title]**
   - Severity: Critical/Major/Minor
   - Scenario: [Which scenario]
   - Description: [Details]
   - Steps to Reproduce: [Steps]
   - Expected: [Expected behavior]
   - Actual: [Actual behavior]

### Recommendations

- [Recommendation 1]
- [Recommendation 2]

### Sign-off

**Tested By**: [Name]
**Date**: [Date]
**Status**: APPROVED / NEEDS WORK
```

---

## Automated E2E Testing (Future)

Consider implementing automated E2E tests using:
- **Playwright**: For browser automation
- **Cypress**: For frontend testing
- **pytest**: For backend API testing
- **Newman**: For API contract testing

---

**Last Updated**: 2026-01-10
**Version**: 1.0
**Status**: Ready for Testing
