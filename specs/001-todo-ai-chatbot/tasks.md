# Task Breakdown: Todo AI Chatbot

**Feature**: 001-todo-ai-chatbot | **Branch**: `001-todo-ai-chatbot` | **Date**: 2026-01-10

## Executive Summary

This document provides a comprehensive, actionable task breakdown for implementing the Todo AI Chatbot. The implementation is organized by user story priority to enable incremental delivery and independent testing of each feature.

**Total Tasks**: 58 tasks across 9 phases
**Estimated Duration**: 15-20 hours
**MVP Scope**: Phase 1-4 (Setup + US1 + US2) = ~8 hours

### Task Distribution by Phase

| Phase | Description | Tasks | Est. Time |
|-------|-------------|-------|-----------|
| Phase 1 | Setup & Configuration | 7 tasks | 1.5 hours |
| Phase 2 | Foundational Infrastructure | 8 tasks | 2 hours |
| Phase 3 | US1: Create Tasks (P1) | 8 tasks | 2 hours |
| Phase 4 | US2: View Tasks (P1) | 6 tasks | 1.5 hours |
| Phase 5 | US6: Conversation Context (P2) | 6 tasks | 1.5 hours |
| Phase 6 | US3: Complete Tasks (P2) | 5 tasks | 1 hour |
| Phase 7 | US4: Update Tasks (P3) | 5 tasks | 1 hour |
| Phase 8 | US5: Delete Tasks (P3) | 5 tasks | 1 hour |
| Phase 9 | Polish & Documentation | 8 tasks | 2 hours |

### Technology Stack

**Backend**:
- Python 3.13+
- FastAPI (web framework)
- SQLModel (ORM)
-  Agents SDK (natural language)
- MCP SDK (tool definitions)
- Better Auth (authentication)
- Neon PostgreSQL (database)

**Frontend**:
- TypeScript/React
- OpenAI ChatKit (chat UI)
- Vite (build tool)

**Testing**:
- pytest (backend)
- Jest/Vitest (frontend)

---

## Dependency Graph

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ← Must complete before any user stories
    ↓
    ├─→ Phase 3 (US1: Create Tasks) ← MVP Core
    │       ↓
    ├─→ Phase 4 (US2: View Tasks) ← MVP Core
    │       ↓
    ├─→ Phase 5 (US6: Conversation Context) ← Enhances all stories
    │       ↓
    ├─→ Phase 6 (US3: Complete Tasks)
    │       ↓
    ├─→ Phase 7 (US4: Update Tasks) ← Can be parallel with Phase 8
    │       ↓
    └─→ Phase 8 (US5: Delete Tasks) ← Can be parallel with Phase 7
            ↓
        Phase 9 (Polish)
```

**Parallel Opportunities**:
- Phase 7 and Phase 8 can be developed in parallel (different MCP tools)
- Frontend and backend tasks within each phase can be parallel (marked with [P])
- Testing tasks can be parallel with implementation

---

## Phase 1: Setup & Configuration

**Goal**: Initialize project structure and development environment

**Independent Test**: Run `tree` command to verify directory structure exists

### Tasks

- [ ] T001 Initialize project directory structure per plan.md
- [ ] T002 [P] Setup backend Python environment with uv in backend/
- [ ] T003 [P] Setup frontend Node.js environment in frontend/
- [ ] T004 [P] Create backend/.env.example with required environment variables
- [ ] T005 [P] Create frontend/.env.example with API URL configuration
- [ ] T006 Create root README.md with project overview and setup instructions
- [ ] T007 Initialize git repository and create .gitignore for Python and Node.js

**Validation**:
```bash
# Verify structure
tree -L 2

# Verify Python environment
cd backend && uv --version

# Verify Node environment
cd frontend && npm --version

# Verify git
git status
```

---

## Phase 2: Foundational Infrastructure

**Goal**: Implement core infrastructure required by all user stories

**Independent Test**: Database connection successful, models can be imported, FastAPI app starts

### Tasks

- [ ] T008 [P] Implement Task model in backend/src/models/task.py per data-model.md
- [ ] T009 [P] Implement Conversation model in backend/src/models/conversation.py per data-model.md
- [ ] T010 [P] Implement Message model in backend/src/models/message.py per data-model.md
- [ ] T011 Create database connection module in backend/src/database/connection.py for Neon PostgreSQL
- [ ] T012 Create database migration script in backend/src/database/migrations/init_db.py
- [ ] T013 Setup Better Auth integration in backend/src/api/auth.py
- [ ] T014 Create FastAPI application structure in backend/src/main.py with CORS and auth middleware
- [ ] T015 Create configuration module in backend/src/config/settings.py for environment variables

**Validation**:
```bash
# Test database connection
cd backend
python -c "from src.database.connection import engine; print('✓ Connected')"

# Test models import
python -c "from src.models.task import Task; print('✓ Models OK')"

# Start FastAPI
uvicorn src.main:app --reload
# Visit http://localhost:8000/docs
```

---

## Phase 3: User Story 1 - Create Tasks via Natural Language (P1)

**Story Goal**: Users can create todo tasks by typing natural language requests

**Independent Test**: Send "Add a task to buy groceries" → Task created in database with title "Buy groceries"

**Why P1**: Core value proposition - without task creation, the chatbot has no purpose

### Tasks

- [ ] T016 [US1] Implement add_task MCP tool in backend/src/mcp/tools.py per mcp-tools.json
- [ ] T017 [US1] Implement TaskService.create_task() in backend/src/services/task_service.py
- [ ] T018 [US1] Setup MCP server configuration in backend/src/mcp/server.py
- [ ] T019 [US1] Create agent system prompt in backend/src/services/agent_service.py with task creation intent
- [ ] T020 [US1] Implement OpenAI agent integration in backend/src/services/agent_service.py
- [ ] T021 [US1] Implement POST /api/{user_id}/chat endpoint in backend/src/api/chat.py (initial version)
- [ ] T022 [P] [US1] Create ChatInterface component in frontend/src/components/ChatInterface.tsx using ChatKit
- [ ] T023 [P] [US1] Implement API client in frontend/src/services/chat.ts for chat endpoint

**Validation**:
```bash
# Backend test
curl -X POST http://localhost:8000/api/1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'

# Expected: {"conversation_id": 1, "response": "✓ Task created...", "tool_calls": [...]}

# Database verification
psql $DATABASE_URL -c "SELECT * FROM tasks WHERE user_id=1;"

# Frontend test
# Open http://localhost:5173
# Type: "Add a task to buy groceries"
# Verify: Task creation confirmation appears
```

**Acceptance Criteria**:
- [ ] User can type natural language task creation request
- [ ] System extracts title from natural language
- [ ] Task is stored in database with user_id
- [ ] System responds with friendly confirmation
- [ ] Frontend displays assistant response

---

## Phase 4: User Story 2 - View and Query Tasks (P1)

**Story Goal**: Users can ask about their tasks and receive organized responses

**Independent Test**: Create 3 tasks, ask "What are my tasks?" → Receive list of all 3 tasks

**Why P1**: Users need to see tasks before managing them - essential for usefulness

### Tasks

- [ ] T024 [US2] Implement list_tasks MCP tool in backend/src/mcp/tools.py per mcp-tools.json
- [ ] T025 [US2] Implement TaskService.list_tasks() in backend/src/services/task_service.py with status filtering
- [ ] T026 [US2] Update agent system prompt in backend/src/services/agent_service.py with list intent patterns
- [ ] T027 [US2] Implement response formatting for task lists in backend/src/services/agent_service.py
- [ ] T028 [P] [US2] Create TaskList component in frontend/src/components/TaskList.tsx for displaying tasks
- [ ] T029 [P] [US2] Add task list formatting in frontend/src/utils/formatters.ts

**Validation**:
```bash
# Backend test
curl -X POST http://localhost:8000/api/1/chat \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": 1, "message": "Show me all my tasks"}'

# Expected: List of tasks with status indicators

# Test filtering
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"conversation_id": 1, "message": "What'\''s pending?"}'

# Frontend test
# Type: "Show me all my tasks"
# Verify: Tasks displayed with status (✓ or •)
```

**Acceptance Criteria**:
- [ ] User can request task list with natural language
- [ ] System returns all tasks for the user
- [ ] System supports status filtering (all/pending/completed)
- [ ] Empty list handled gracefully
- [ ] Tasks formatted clearly with status indicators

---

## Phase 5: User Story 6 - Maintain Conversation Context (P2)

**Story Goal**: Chatbot maintains conversation history for natural multi-turn conversations

**Independent Test**: Say "Add milk", then "Actually, make that 2 gallons" → System updates the just-created task

**Why P2**: Significantly improves UX by enabling natural conversation flow

### Tasks

- [ ] T030 [US6] Implement ConversationService.create_conversation() in backend/src/services/conversation_service.py
- [ ] T031 [US6] Implement ConversationService.get_history() in backend/src/services/conversation_service.py
- [ ] T032 [US6] Implement message storage in backend/src/services/conversation_service.py
- [ ] T033 [US6] Update chat endpoint to fetch and use conversation history in backend/src/api/chat.py
- [ ] T034 [US6] Implement conversation context management in agent service in backend/src/services/agent_service.py
- [ ] T035 [P] [US6] Add conversation state management in frontend/src/components/ChatInterface.tsx

**Validation**:
```bash
# Test multi-turn conversation
# Turn 1
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"message": "Add a task to buy milk"}'
# Save conversation_id from response

# Turn 2 (reference previous context)
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"conversation_id": 1, "message": "Actually, make that 2 gallons"}'

# Verify: System understands "that" refers to milk task

# Database verification
psql $DATABASE_URL -c "SELECT * FROM messages WHERE conversation_id=1 ORDER BY created_at;"
```

**Acceptance Criteria**:
- [ ] New conversation created if no conversation_id provided
- [ ] Conversation history fetched from database
- [ ] Messages stored with role (user/assistant)
- [ ] Agent receives full conversation context
- [ ] System handles context references correctly

---

## Phase 6: User Story 3 - Complete Tasks Conversationally (P2)

**Story Goal**: Users can mark tasks complete using natural language

**Independent Test**: Create task, say "Mark task 1 as done" → Task status changes to completed

**Why P2**: Core workflow, but requires task creation and viewing first

### Tasks

- [ ] T036 [US3] Implement complete_task MCP tool in backend/src/mcp/tools.py per mcp-tools.json
- [ ] T037 [US3] Implement TaskService.complete_task() in backend/src/services/task_service.py
- [ ] T038 [US3] Update agent system prompt with complete intent patterns in backend/src/services/agent_service.py
- [ ] T039 [US3] Add error handling for non-existent task IDs in backend/src/services/task_service.py
- [ ] T040 [P] [US3] Update TaskList component to show completion status in frontend/src/components/TaskList.tsx

**Validation**:
```bash
# Create a task first
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"message": "Add a task to call dentist"}'

# Complete the task
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"conversation_id": 1, "message": "Mark task 1 as complete"}'

# Verify in database
psql $DATABASE_URL -c "SELECT id, title, completed FROM tasks WHERE id=1;"

# Test error case
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"message": "Complete task 999"}'
# Expected: Helpful error message
```

**Acceptance Criteria**:
- [ ] User can complete task by ID
- [ ] User can complete task by description
- [ ] System updates completed status in database
- [ ] System updates updated_at timestamp
- [ ] Non-existent task IDs handled gracefully

---

## Phase 7: User Story 4 - Update Task Details (P3)

**Story Goal**: Users can modify existing tasks using natural language

**Independent Test**: Create task, say "Change task 1 to 'Call mom tomorrow'" → Task title updated

**Why P3**: Convenience feature - users can work around by delete/recreate

### Tasks

- [ ] T041 [US4] Implement update_task MCP tool in backend/src/mcp/tools.py per mcp-tools.json
- [ ] T042 [US4] Implement TaskService.update_task() in backend/src/services/task_service.py
- [ ] T043 [US4] Update agent system prompt with update intent patterns in backend/src/services/agent_service.py
- [ ] T044 [US4] Add validation for title and description updates in backend/src/services/task_service.py
- [ ] T045 [P] [US4] Add task editing UI feedback in frontend/src/components/TaskList.tsx

**Validation**:
```bash
# Create a task
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"message": "Add a task to call mom"}'

# Update title
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"message": "Change task 1 to '\''Call mom tomorrow'\''"}'

# Update description
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"message": "Update task 1 description to include phone number"}'

# Verify
psql $DATABASE_URL -c "SELECT * FROM tasks WHERE id=1;"
```

**Acceptance Criteria**:
- [ ] User can update task title
- [ ] User can update task description
- [ ] System validates new title/description
- [ ] System updates updated_at timestamp
- [ ] Partial updates supported (title only or description only)

---

## Phase 8: User Story 5 - Delete Tasks (P3)

**Story Goal**: Users can remove tasks using natural language

**Independent Test**: Create task, say "Delete task 1" → Task removed from database

**Why P3**: Maintenance feature - users can ignore unwanted tasks

### Tasks

- [ ] T046 [US5] Implement delete_task MCP tool in backend/src/mcp/tools.py per mcp-tools.json
- [ ] T047 [US5] Implement TaskService.delete_task() in backend/src/services/task_service.py
- [ ] T048 [US5] Update agent system prompt with delete intent patterns in backend/src/services/agent_service.py
- [ ] T049 [US5] Add error handling for non-existent task deletion in backend/src/services/task_service.py
- [ ] T050 [P] [US5] Add task deletion feedback in frontend/src/components/TaskList.tsx

**Validation**:
```bash
# Create a task
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"message": "Add a task to test deletion"}'

# Delete the task
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"message": "Delete task 1"}'

# Verify deletion
psql $DATABASE_URL -c "SELECT * FROM tasks WHERE id=1;"
# Expected: No rows

# Test error case
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"message": "Delete task 999"}'
# Expected: Helpful error message
```

**Acceptance Criteria**:
- [ ] User can delete task by ID
- [ ] User can delete task by description
- [ ] Task removed from database
- [ ] Non-existent task IDs handled gracefully
- [ ] System confirms deletion

---

## Phase 9: Polish & Cross-Cutting Concerns

**Goal**: Add error handling, logging, documentation, and testing

### Tasks

- [ ] T051 [P] Add comprehensive error handling middleware in backend/src/main.py
- [ ] T052 [P] Implement logging throughout backend in backend/src/services/
- [ ] T053 [P] Add health check endpoint in backend/src/api/health.py
- [ ] T054 [P] Create API documentation in backend/README.md
- [ ] T055 [P] Add error handling UI in frontend/src/components/ChatInterface.tsx
- [ ] T056 [P] Create frontend setup guide in frontend/README.md
- [ ] T057 [P] Add performance monitoring for database queries in backend/src/database/connection.py
- [ ] T058 Update root README.md with complete setup and usage instructions

**Validation**:
```bash
# Test error handling
curl -X POST http://localhost:8000/api/1/chat \
  -d '{"message": ""}'
# Expected: 400 Bad Request with clear error

# Test health check
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Check logs
tail -f backend/logs/app.log

# Verify documentation
cat README.md
cat backend/README.md
cat frontend/README.md
```

---

## Implementation Timeline

### Week 1: MVP (Phases 1-4)

**Day 1-2**: Setup & Foundational (Phases 1-2)
- Complete project setup
- Implement database models
- Setup FastAPI and Better Auth

**Day 3-4**: Core Features (Phases 3-4)
- Implement task creation (US1)
- Implement task viewing (US2)
- Basic chat interface

**Day 5**: Testing & Refinement
- Test MVP end-to-end
- Fix bugs
- Prepare for demo

### Week 2: Full Feature Set (Phases 5-9)

**Day 6**: Conversation Context (Phase 5)
- Implement conversation management
- Test multi-turn conversations

**Day 7-8**: Task Management (Phases 6-8)
- Implement complete, update, delete
- Can work on Phase 7 and 8 in parallel

**Day 9**: Polish (Phase 9)
- Error handling
- Logging
- Documentation

**Day 10**: Final Testing & Deployment
- End-to-end testing
- Performance testing
- Deploy to production

---

## Quick Start Guide

### First 5 Tasks to Get Started

1. **T001**: Initialize project structure
   ```bash
   mkdir -p backend/src/{models,services,mcp,api,database,config}
   mkdir -p frontend/src/{components,services,types,utils}
   mkdir -p specs/001-todo-ai-chatbot
   ```

2. **T002**: Setup backend environment
   ```bash
   cd backend
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv venv
   source .venv/bin/activate
   uv pip install fastapi uvicorn sqlmodel psycopg2-binary python-dotenv openai
   ```

3. **T003**: Setup frontend environment
   ```bash
   cd frontend
   npm create vite@latest . -- --template react-ts
   npm install @openai/chatkit
   ```

4. **T004**: Create backend .env.example
   ```bash
   cat > backend/.env.example << 'EOF'
   DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
   OPENAI_API_KEY=sk-...
   AUTH_SECRET=your-secret-key
   DEBUG=true
   EOF
   ```

5. **T008**: Implement Task model
   - Copy SQLModel definition from data-model.md
   - Create backend/src/models/task.py
   - Add validation methods

---

## Parallel Execution Examples

### Within Phase 3 (US1: Create Tasks)

**Backend Team**:
- T016: Implement add_task MCP tool
- T017: Implement TaskService.create_task()
- T018: Setup MCP server
- T019-T021: Agent and API integration

**Frontend Team** (parallel):
- T022: Create ChatInterface component
- T023: Implement API client

**Timeline**: Both teams work simultaneously, integrate at end

### Phase 7 vs Phase 8

**Developer A** (Phase 7):
- T041-T045: Implement update_task feature

**Developer B** (Phase 8, parallel):
- T046-T050: Implement delete_task feature

**Timeline**: Both features developed in parallel, no dependencies

---

## Testing Strategy

### Unit Tests (Optional - if requested)

**Backend**:
```bash
# Test models
pytest backend/tests/unit/test_models.py

# Test services
pytest backend/tests/unit/test_services.py

# Test MCP tools
pytest backend/tests/unit/test_mcp_tools.py
```

**Frontend**:
```bash
# Test components
npm test -- components/

# Test services
npm test -- services/
```

### Integration Tests (Optional - if requested)

```bash
# Test chat endpoint
pytest backend/tests/integration/test_chat_api.py

# Test agent flow
pytest backend/tests/integration/test_agent_flow.py
```

### Manual Testing Checklist

- [ ] Create task: "Add a task to buy groceries"
- [ ] View tasks: "Show me all my tasks"
- [ ] Complete task: "Mark task 1 as done"
- [ ] Update task: "Change task 1 to 'Buy groceries and fruits'"
- [ ] Delete task: "Delete task 1"
- [ ] Multi-turn: "Add milk" → "Make that 2 gallons"
- [ ] Error handling: "Complete task 999"
- [ ] Empty list: "Show tasks" (when no tasks exist)

---

## Success Criteria

### MVP Success (Phases 1-4)

- [ ] User can create tasks via natural language
- [ ] User can view all tasks
- [ ] Tasks persist to database
- [ ] Chat interface is functional
- [ ] Authentication works

### Full Feature Success (All Phases)

- [ ] All 6 user stories implemented
- [ ] All MCP tools functional
- [ ] Conversation context maintained
- [ ] Error handling comprehensive
- [ ] Documentation complete
- [ ] Performance targets met (<3s response time)

---

## Notes & Tips

### General Guidelines

1. **Follow the spec**: Reference spec.md, plan.md, and data-model.md for all implementation details
2. **Test incrementally**: Test each task before moving to the next
3. **Use type hints**: All Python code must have type hints
4. **Document as you go**: Add docstrings to all functions
5. **Commit frequently**: Commit after each completed task

### Common Pitfalls

1. **Database connection**: Ensure Neon PostgreSQL uses NullPool for serverless
2. **CORS**: Configure CORS in FastAPI for frontend origin
3. **Authentication**: Verify user_id matches authenticated user in all endpoints
4. **Conversation history**: Limit history to last 50 messages to avoid token limits
5. **MCP tools**: Ensure tool definitions match OpenAI function calling format

### Performance Tips

1. **Database indexes**: Ensure indexes on user_id and conversation_id
2. **Connection pooling**: Use NullPool for Neon serverless
3. **Caching**: Consider caching frequently accessed data
4. **Pagination**: Implement pagination for large task lists

### Debugging Tips

1. **Enable debug logging**: Set DEBUG=true in .env
2. **Use FastAPI docs**: Visit /docs for interactive API testing
3. **Check database**: Use psql to verify data
4. **Monitor logs**: tail -f backend/logs/app.log
5. **Test MCP tools**: Test tools independently before agent integration

---

## Appendix: Claude Code Prompts

### Example Prompt for T008 (Task Model)

```
I'm implementing the Task model for a Todo AI Chatbot using SQLModel.

Context:
- Feature: Todo AI Chatbot with natural language interface
- Database: Neon PostgreSQL
- ORM: SQLModel
- File: backend/src/models/task.py

Requirements from data-model.md:
- Fields: id, user_id, title, description, completed, created_at, updated_at
- Validation: title 1-200 chars, description max 1000 chars
- Indexes: user_id, (user_id, completed)
- Type hints required
- Docstrings required

Please generate:
1. Complete Task model class with SQLModel
2. Validation methods for title and description
3. Proper type hints and docstrings
4. Table name and field constraints

Expected output: Complete task.py file ready to use
```

### Example Prompt for T016 (MCP Tool)

```
I'm implementing the add_task MCP tool for the Todo AI Chatbot.

Context:
- Feature: Natural language task creation
- Framework: MCP SDK
- File: backend/src/mcp/tools.py
- Tool definition: specs/001-todo-ai-chatbot/contracts/mcp-tools.json

Requirements:
- Tool name: add_task
- Parameters: user_id (int), title (str), description (str, optional)
- Returns: {task_id, status, title}
- Validation: title 1-200 chars, description max 1000 chars
- Error handling: INVALID_TITLE, INVALID_DESCRIPTION

Please generate:
1. MCP tool decorator and function
2. Parameter validation
3. Call to TaskService.create_task()
4. Error handling with proper error codes
5. Type hints and docstrings

Expected output: Complete add_task tool implementation
```

---

**End of Task Breakdown**

Total: 58 tasks | Est. Duration: 15-20 hours | MVP: 8 hours (Phases 1-4)
