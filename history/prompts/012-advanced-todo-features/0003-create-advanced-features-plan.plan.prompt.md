---
id: 0003
title: Create Advanced Features Plan
stage: plan
date: 2026-02-05
surface: agent
model: claude-opus-4-5-20251101
feature: 012-advanced-todo-features
branch: 012-advanced-todo-features
user: awais
command: /sp.plan
labels: ["planning", "architecture", "due-dates", "recurring-tasks", "history", "research", "data-model"]
links:
  spec: specs/012-advanced-todo-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/012-advanced-todo-features/plan.md
 - specs/012-advanced-todo-features/research.md
 - specs/012-advanced-todo-features/data-model.md
 - specs/012-advanced-todo-features/contracts/history-api.yaml
 - specs/012-advanced-todo-features/contracts/mcp-tools-extended.json
tests:
 - Constitution Check: All gates passed (10 principles)
 - 21 date parsing test cases validated in research
 - 5 recurrence patterns + edge cases documented
---

## Prompt

User command: `/sp.plan Generate architectural plan create the technical architecture`

After completing specification (0001-create-advanced-todo-features-spec.spec.prompt.md), user requested architectural planning to create technical implementation plan for advanced todo features including:
1. Due dates with natural language parsing ("tomorrow at 3pm")
2. Browser notifications with reminders
3. Recurring tasks (daily/weekly/monthly/yearly auto-reschedule)
4. Task history with 2-year retention and restoration

## Response snapshot

Completed comprehensive architectural planning with Phase 0 (Research) and Phase 1 (Design & Contracts):

**Phase 0: Research** (research.md - 14KB)
- **Natural Language Date Parsing**: Selected dual-library approach (dateparser + parsedatetime) achieving 100% coverage
  - dateparser 1.3.0: 62% success rate (excellent for absolute dates, timezone handling)
  - parsedatetime 2.6: 86% success rate (excellent for relative dates like "next Friday")
  - Combined: 100% success on 21 test cases

- **Browser Notifications**: Web Notifications API + Service Worker
  - Hybrid scheduling: setTimeout for <1 hour, Service Worker for >1 hour
  - Native browser support, no external dependencies

- **Background Job Scheduling**: APScheduler 3.10.0+ with PostgreSQL jobstore
  - Stateless backend compatible (jobs persisted in database)
  - No broker required (vs Celery which needs Redis/RabbitMQ)

- **Recurring Tasks**: Pattern-based date calculation using dateutil.relativedelta
  - Handles edge cases gracefully (Feb 31 → Feb 28/29)

- **Timezone Strategy**: Store UTC, display browser local time
  - Single source of truth, automatic DST handling

**Phase 1: Design & Contracts** (data-model.md, contracts/)
- **Extended Task Model**: 5 new fields (due_date, recurrence_pattern, is_recurring, reminder_minutes, next_occurrence)
- **New TaskHistory Entity**: Immutable audit trail with 2-year retention, full-text search, restore capability
- **New NotificationPreference Entity**: Per-user settings (notification_enabled, reminder_minutes_before, browser_permission_granted)
- **Database Migrations**: 4 new SQL migrations (extend tasks, create history, create preferences, APScheduler jobs)
- **API Contracts**:
  - history-api.yaml: OpenAPI 3.0 spec with 2 endpoints (GET history, POST restore)
  - mcp-tools-extended.json: 7 new MCP tools for chatbot integration
- **Performance Optimizations**: 7 new database indexes documented

**Implementation Plan** (plan.md - 365 lines)
- Complete technical context and constitution check (all 10 principles passed)
- Project structure with NEW/UPDATE markers for all affected files
- Complexity tracking: Justified dual-library parsing and APScheduler dependency
- Clear integration points for backend (FastAPI startup) and frontend (History tab, notifications)
- Critical path defined: migrations → utilities → services → endpoints → frontend

## Outcome

- ✅ Impact: Complete architectural plan with all research decisions documented and design artifacts generated. Ready for task breakdown.
- 🧪 Tests: Constitution check passed (10/10 principles). Research validated 21 date parsing test cases. Performance indexes documented for query optimization.
- 📁 Files: Created 5 design artifacts (plan.md, research.md, data-model.md, history-api.yaml, mcp-tools-extended.json)
- 🔁 Next prompts: Run `/sp.tasks` to generate detailed task breakdown (expected 60-80 tasks across 6 phases)
- 🧠 Reflection: Successfully balanced complexity vs features - dual-library date parsing justified by 100% coverage requirement. APScheduler with PostgreSQL jobstore enables stateless backend. All design decisions traceable to functional requirements.

## Evaluation notes (flywheel)

- Failure modes observed: None - smooth research and design phases
- Graders run and results (PASS/FAIL): Constitution Check PASS (all 10 principles), Research decisions validated against requirements
- Prompt variant (if applicable): Standard /sp.plan workflow with Phase 0 research → Phase 1 design
- Next experiment (smallest change to try): Proceed to /sp.tasks for task breakdown, validate task dependencies match critical path
