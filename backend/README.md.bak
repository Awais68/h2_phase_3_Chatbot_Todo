# Todo Evolution API - Backend

FastAPI-based REST API with PostgreSQL (Neon) database for the Todo Evolution application.

## Features

- JWT-based authentication
- RESTful task CRUD operations
- Offline sync support with conflict resolution
- Push notification subscription management
- PostgreSQL database with SQLModel ORM
- Type-safe API with Pydantic schemas
- Automatic API documentation (OpenAPI/Swagger)

## Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLModel**: SQL database ORM with Pydantic integration
- **PostgreSQL**: Neon serverless PostgreSQL database
- **Alembic**: Database migrations
- **JWT**: Stateless authentication
- **Uvicorn**: ASGI server

## Prerequisites

- Python 3.13+
- UV package manager
- Neon PostgreSQL account (https://neon.tech)

## Quick Start

```bash
cd backend
cp .env.example .env
# Edit .env with your Neon DATABASE_URL
uv run uvicorn src.main:app --reload
```

Access API docs at: http://localhost:8000/docs

## Complete Setup Guide

### 1. Install Dependencies

```bash
cd backend
uv sync
```

### 2. Configure Environment

Create `.env` file from template:

```bash
cp .env.example .env
```

Edit `.env` and update:
- `DATABASE_URL`: Your Neon PostgreSQL connection string
- `SECRET_KEY`: Generate with `openssl rand -hex 32`

### 3. Run Database Migrations

```bash
# Initialize Alembic (if not done)
uv add alembic
uv run alembic init src/db/migrations

# Configure alembic.ini with your DATABASE_URL
# Generate initial migration
uv run alembic revision --autogenerate -m "Initial migration"

# Apply migrations
uv run alembic upgrade head
```

### 4. Start Server

```bash
# Development mode (auto-reload)
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Tasks
- `POST /tasks/` - Create new task
- `GET /tasks/` - Get all user tasks (paginated)
- `GET /tasks/{task_id}` - Get specific task
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task

### Sync
- `POST /sync/` - Synchronize offline changes

### Push Notifications
- `POST /push/subscribe` - Register push subscription
- `DELETE /push/unsubscribe/{endpoint}` - Unsubscribe

## Project Structure

```
backend/
├── src/
│   ├── api/              # API endpoints
│   │   ├── auth.py       # Authentication routes
│   │   ├── tasks.py      # Task CRUD routes
│   │   ├── sync.py       # Offline sync route
│   │   └── push.py       # Push notification routes
│   ├── core/             # Core configuration
│   │   ├── config.py     # Settings
│   │   └── security.py   # JWT, password hashing
│   ├── db/               # Database configuration
│   │   ├── session.py    # DB session management
│   │   └── migrations/   # Alembic migrations
│   ├── middleware/       # Middleware components
│   │   ├── auth.py       # JWT verification
│   │   ├── cors.py       # CORS configuration
│   │   └── error_handler.py  # Global error handling
│   ├── models/           # Database models
│   │   ├── user.py       # User model
│   │   ├── task.py       # Task model
│   │   ├── sync_operation.py  # Sync tracking
│   │   └── push_subscription.py  # Push subscriptions
│   ├── services/         # Business logic
│   │   ├── user_service.py    # User operations
│   │   ├── task_service.py    # Task operations
│   │   └── sync_service.py    # Sync logic
│   └── main.py           # Application entry point
├── .env.example          # Environment template
├── pyproject.toml        # Dependencies
└── README.md             # This file
```

## Authentication Example

```bash
# 1. Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"user","password":"password123"}'

# 2. Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"password123"}'
# Returns: {"access_token":"<JWT>","token_type":"bearer",...}

# 3. Use token in subsequent requests
curl -X GET http://localhost:8000/tasks/ \
  -H "Authorization: Bearer <JWT>"
```

## Offline Sync Architecture

The API supports offline-first PWA architecture:

1. **Client offline**: Creates/updates/deletes tasks locally (IndexedDB)
2. **Each task gets**: Unique `client_id` for tracking
3. **When online**: Client sends batch of operations to `/sync/`
4. **Server processes**: Applies operations, detects conflicts
5. **Response includes**:
   - Successfully synced operations
   - Conflicts (version mismatches)
   - Server updates since last sync

### Conflict Resolution Strategy

- **Version-based**: Each task has a `version` number (increments on update)
- **Conflict detection**: Server compares client version vs server version
- **Resolution**:
  - If `client_version <= server_version`: Conflict (server wins)
  - Client must reconcile or accept server version
  - Manual resolution UI shows both versions

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `APP_NAME` | Application name | "Todo Evolution API" | No |
| `DEBUG` | Enable debug mode | false | No |
| `DATABASE_URL` | PostgreSQL connection string | - | **Yes** |
| `SECRET_KEY` | JWT secret key | - | **Yes** |
| `ALGORITHM` | JWT algorithm | "HS256" | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | 30 | No |
| `CORS_ORIGINS` | Allowed CORS origins | ["http://localhost:3000"] | No |

## Development Commands

### Run Tests

```bash
uv add --dev pytest pytest-asyncio httpx
uv run pytest
```

### Code Quality

```bash
# Type checking
uv run mypy src/

# Linting
uv run pylint src/

# Formatting
uv run black src/
```

### Database Migrations

```bash
# Create new migration
uv run alembic revision --autogenerate -m "Migration description"

# Apply migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# Show migration history
uv run alembic history
```

## Troubleshooting

### Database Connection Issues

```bash
# Test database connection
uv run python -c "from src.db.session import engine; engine.connect(); print('Connected!')"
```

### Alembic Not Initialized

```bash
cd backend
uv add alembic
uv run alembic init src/db/migrations
# Edit alembic.ini and set sqlalchemy.url = <your DATABASE_URL>
```

### Import Errors

Ensure you're running commands from the `backend/` directory with `uv run`.

## Deployment

### Docker

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync --no-dev
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t todo-api .
docker run -p 8000:8000 --env-file .env todo-api
```

### Neon PostgreSQL Setup

1. Sign up at https://console.neon.tech
2. Create new project: "todo-evolution"
3. Copy connection string (format: `postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require`)
4. Paste into `.env` as `DATABASE_URL`
5. Run migrations: `uv run alembic upgrade head`

## Performance

- **Target API latency**: < 200ms (p95)
- **Database connection pooling**: 10 connections, 20 max overflow
- **Async request handling**: Non-blocking I/O with FastAPI
- **Optimized queries**: Selective loading, pagination, indexing

## Security

- Passwords hashed with **bcrypt** (salted, adaptive)
- JWT tokens with **expiration** (30 min default)
- **CORS configured** for frontend origins only
- **Input validation** with Pydantic schemas
- **SQL injection protection** via SQLModel ORM
- **No secrets in code** - all in environment variables

## API Rate Limiting (TODO)

To add rate limiting in production:

```bash
uv add slowapi
```

Then add to `main.py`:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/tasks/")
@limiter.limit("100/minute")
async def get_tasks(...):
    ...
```

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- See [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md)
- Check API docs at `/docs` endpoint
- Review constitution at `.specify/memory/constitution.md`
