# Quickstart Guide: Todo AI Chatbot

**Feature**: 001-todo-ai-chatbot | **Date**: 2026-01-10
**Purpose**: Get the Todo AI Chatbot running locally in under 15 minutes

## Prerequisites

Before you begin, ensure you have:

- **Python 3.13+** installed
- **Node.js 18+** and npm/yarn installed
- **Git** for version control
- **OpenAI API key** (for Agents SDK)
- **Neon PostgreSQL** database (free tier available)
- **Better Auth** credentials (or use local setup)

## Quick Setup (15 minutes)

### Step 1: Clone and Setup (2 minutes)

```bash
# Clone the repository
git clone <repository-url>
cd todo-ai-chatbot

# Checkout the feature branch
git checkout 001-todo-ai-chatbot
```

### Step 2: Backend Setup (5 minutes)

```bash
# Navigate to backend directory
cd backend

# Install UV package manager (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install fastapi uvicorn sqlmodel psycopg2-binary python-dotenv openai better-auth mcp-sdk

# Install dev dependencies
uv pip install pytest pytest-cov mypy pylint black
```

### Step 3: Environment Configuration (3 minutes)

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

**Required Environment Variables**:
```bash
# Database
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# OpenAI
OPENAI_API_KEY=sk-...

# Better Auth
AUTH_SECRET=your-secret-key-here
AUTH_DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Application
DEBUG=true
LOG_LEVEL=info
```

### Step 4: Database Setup (2 minutes)

```bash
# Run database migrations
python -m src.database.migrations.init_db

# Verify connection
python -c "from src.database.connection import engine; print('✓ Database connected')"
```

### Step 5: Start Backend Server (1 minute)

```bash
# Start FastAPI server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Server should be running at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### Step 6: Frontend Setup (2 minutes)

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or: yarn install

# Copy environment template
cp .env.example .env.local

# Edit .env.local
nano .env.local
```

**Frontend Environment Variables**:
```bash
VITE_API_URL=http://localhost:8000
VITE_AUTH_URL=http://localhost:8000/auth
```

### Step 7: Start Frontend (1 minute)

```bash
# Start development server
npm run dev
# or: yarn dev

# Frontend should be running at http://localhost:5173
```

### Step 8: Test the Application (2 minutes)

1. Open browser to `http://localhost:5173`
2. Sign up or log in (Better Auth)
3. Try these commands in the chat:
   - "Add a task to buy groceries"
   - "Show me all my tasks"
   - "Mark task 1 as complete"
   - "Delete task 1"

## Project Structure

```
todo-ai-chatbot/
├── backend/
│   ├── src/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── models/              # SQLModel database models
│   │   ├── services/            # Business logic
│   │   ├── mcp/                 # MCP tools
│   │   ├── api/                 # API routes
│   │   └── database/            # DB connection & migrations
│   ├── tests/                   # Backend tests
│   ├── pyproject.toml           # Python dependencies
│   └── .env                     # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Main React component
│   │   ├── components/          # React components
│   │   ├── services/            # API client
│   │   └── types/               # TypeScript types
│   ├── package.json             # Node dependencies
│   └── .env.local               # Frontend environment
└── specs/
    └── 001-todo-ai-chatbot/     # Feature specifications
```

## Development Workflow

### Running Tests

**Backend Tests**:
```bash
cd backend

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_models.py

# Run with verbose output
pytest tests/ -v
```

**Frontend Tests**:
```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

### Code Quality Checks

**Backend**:
```bash
cd backend

# Type checking
mypy src/

# Linting
pylint src/

# Code formatting
black src/ tests/

# Run all checks
./scripts/check-quality.sh
```

**Frontend**:
```bash
cd frontend

# Type checking
npm run type-check

# Linting
npm run lint

# Code formatting
npm run format
```

### Database Migrations

**Create Migration**:
```bash
cd backend

# Generate migration from model changes
alembic revision --autogenerate -m "Add new field to Task"

# Review generated migration in alembic/versions/
```

**Apply Migration**:
```bash
# Apply all pending migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# View migration history
alembic history
```

## Common Tasks

### Adding a New MCP Tool

1. Define tool in `backend/src/mcp/tools.py`:
```python
@mcp_server.tool()
def my_new_tool(user_id: int, param: str) -> Dict[str, Any]:
    """Tool description for the AI agent."""
    # Implementation
    pass
```

2. Add tool to OpenAI function definitions in `backend/src/services/agent_service.py`

3. Write tests in `backend/tests/unit/test_mcp_tools.py`

4. Update `specs/001-todo-ai-chatbot/contracts/mcp-tools.json`

### Adding a New API Endpoint

1. Create route in `backend/src/api/`:
```python
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/my-endpoint")
async def my_endpoint(current_user = Depends(get_current_user)):
    # Implementation
    pass
```

2. Register router in `backend/src/main.py`:
```python
from src.api.my_endpoint import router as my_router
app.include_router(my_router, prefix="/api")
```

3. Write tests in `backend/tests/integration/`

4. Update OpenAPI spec in `specs/001-todo-ai-chatbot/contracts/chat-api.yaml`

### Debugging Tips

**Backend Debugging**:
```bash
# Enable debug logging
export LOG_LEVEL=debug

# Run with debugger
python -m debugpy --listen 5678 --wait-for-client -m uvicorn src.main:app --reload

# View SQL queries
export DATABASE_ECHO=true
```

**Frontend Debugging**:
```bash
# Enable verbose logging
export VITE_LOG_LEVEL=debug

# Use React DevTools in browser
# Use Network tab to inspect API calls
```

**Database Debugging**:
```bash
# Connect to database
psql $DATABASE_URL

# View tables
\dt

# View table schema
\d tasks

# Query data
SELECT * FROM tasks WHERE user_id = 123;
```

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`
```bash
# Solution: Ensure you're in the backend directory and virtual environment is activated
cd backend
source .venv/bin/activate
```

**Issue**: `Database connection failed`
```bash
# Solution: Check DATABASE_URL in .env
# Verify Neon database is running
# Check SSL mode is set to 'require'
```

**Issue**: `OpenAI API rate limit exceeded`
```bash
# Solution: Implement rate limiting or upgrade OpenAI plan
# Add retry logic with exponential backoff
```

### Frontend Issues

**Issue**: `CORS error when calling API`
```bash
# Solution: Add CORS middleware in backend/src/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Issue**: `ChatKit component not rendering`
```bash
# Solution: Verify OpenAI ChatKit is installed
npm install @openai/chatkit

# Check import statement
import { ChatKit } from '@openai/chatkit';
```

### Database Issues

**Issue**: `Too many database connections`
```bash
# Solution: Use connection pooling with NullPool for Neon
from sqlalchemy.pool import NullPool

engine = create_engine(DATABASE_URL, poolclass=NullPool)
```

**Issue**: `Migration conflicts`
```bash
# Solution: Resolve conflicts manually
alembic history
alembic downgrade <revision>
# Fix migration file
alembic upgrade head
```

## Performance Optimization

### Backend Optimization

1. **Database Query Optimization**:
```python
# Use indexes for frequent queries
# Limit result sets with pagination
# Use eager loading for relationships

tasks = session.query(Task)\
    .filter(Task.user_id == user_id)\
    .order_by(Task.created_at.desc())\
    .limit(50)\
    .all()
```

2. **Caching** (optional):
```python
# Cache frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=100)
def get_user_tasks(user_id: int):
    # Implementation
    pass
```

3. **Async Operations**:
```python
# Use async/await for I/O operations
async def fetch_conversation_history(conversation_id: int):
    # Async database query
    pass
```

### Frontend Optimization

1. **Code Splitting**:
```typescript
// Lazy load components
const ChatInterface = lazy(() => import('./components/ChatInterface'));
```

2. **Memoization**:
```typescript
// Memoize expensive computations
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
```

3. **Debouncing**:
```typescript
// Debounce API calls
const debouncedSearch = debounce(searchTasks, 300);
```

## Next Steps

1. ✅ **Development Environment Ready** - Backend and frontend running locally
2. → **Implement Core Features** - Follow `/sp.tasks` to break down implementation
3. → **Write Tests** - Achieve ≥80% code coverage
4. → **Deploy to Production** - Use Vercel (frontend) + Railway/Render (backend)
5. → **Monitor and Iterate** - Add logging, monitoring, and user feedback

## Additional Resources

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Feature Specification**: `specs/001-todo-ai-chatbot/spec.md`
- **Data Model**: `specs/001-todo-ai-chatbot/data-model.md`
- **API Contracts**: `specs/001-todo-ai-chatbot/contracts/`
- **Research Notes**: `specs/001-todo-ai-chatbot/research.md`

## Getting Help

- Check the troubleshooting section above
- Review error logs in `backend/logs/` and browser console
- Consult the specification documents in `specs/001-todo-ai-chatbot/`
- Test API endpoints using Swagger UI at http://localhost:8000/docs

---

**Estimated Setup Time**: 15 minutes
**Difficulty**: Intermediate
**Prerequisites**: Python, Node.js, PostgreSQL knowledge
