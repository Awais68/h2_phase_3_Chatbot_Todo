# Implementation Plan: Phase II Deployment

**Branch**: `011-phase2-deploy` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification for Vercel frontend, Render backend, and Neon database deployment

## Summary

Deploy the Phase II Todo Web Application to production using cloud-native platforms:
- **Frontend**: Vercel (Next.js application)
- **Backend**: Render (Dockerized FastAPI application)
- **Database**: Neon (PostgreSQL)

This plan covers infrastructure configuration, environment management, and deployment automation through platform-native CI/CD features.

## Technical Context

**Deployment Platform**: Vercel + Render + Neon (free tier)
**Frontend Framework**: Next.js 14+ (App Router)
**Backend Framework**: FastAPI with SQLModel
**Database**: PostgreSQL 15+ (Neon serverless)
**Container Runtime**: Docker 24+
**Infrastructure as Code**: render.yaml (Render), vercel.json (Vercel)

**Primary Dependencies**:
- GitHub repository with connected deployment platforms
- Dockerized backend with health check endpoint
- Environment variable documentation for all required secrets
- Database migration scripts (Alembic/SQLModel)

**Target Performance Goals**:
- Frontend load time: <3 seconds (SC-001)
- Backend health check: <500ms (SC-002)
- Deployment time: <5 minutes (SC-003)
- Preview deployment: <10 minutes (SC-004)
- Database connection: <10 seconds (SC-005)

**Constraints**:
- Free tier resource limits (Vercel: 100GB bandwidth, Render: 750 hours, Neon: 10GB storage)
- No multi-region deployment (out of scope)
- No advanced monitoring tools (Datadog/New Relic) - use platform-native

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Requirement | Status | Notes |
|------|-------------|--------|-------|
| Spec-Driven Development | Deployment spec exists in `/specs/011-phase2-deploy/` | ✅ Pass | spec.md defines all 6 user stories with acceptance criteria |
| Project Structure | Monorepo has backend/ and frontend/ directories | ⚠️ Needs Verification | Verify existing project structure |
| Security | No hardcoded credentials in repository | ✅ Pass | Requirement FR-011 explicitly prohibits this |
| Documentation | README contains deployment instructions | ⚠️ Pending | Will be created during deployment |
| Monitoring | Logging strategy defined | ✅ Pass | Platform-native dashboards specified in FR-009 |

**Constitution Violations**: None identified for deployment phase.

## Project Structure

### Documentation (this feature)

```text
specs/011-phase2-deploy/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (platform-specific configs)
├── data-model.md        # N/A - data model in separate feature
├── quickstart.md        # Phase 1 output (deployment quickstart)
├── contracts/           # Phase 1 output (API contracts)
├── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
└── DEPLOYMENT.md        # Generated deployment guide
```

### Deployment Configuration (repository root)

```text
./
├── frontend/                    # Next.js application
│   ├── vercel.json             # Vercel deployment config
│   ├── .env.example            # Frontend environment template
│   └── src/...
│
├── backend/                     # FastAPI application
│   ├── Dockerfile              # Container definition
│   ├── render.yaml             # Render deployment config
│   ├── .env.example            # Backend environment template
│   └── src/...
│
├── .github/
│   └── workflows/              # GitHub Actions (optional)
│
├── specs/                       # Specifications
│   └── 011-phase2-deploy/
│
└── DEPLOYMENT.md               # Deployment guide (generated)
```

**Structure Decision**: Deploy frontend to Vercel, backend to Render as Docker container, database to Neon. Separation allows independent scaling and deployment of frontend/backend.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multi-platform deployment (3 platforms) | Frontend/serverless (Vercel) + Backend container (Render) + Database (Neon) | Single platform not optimal for this stack - Vercel best for Next.js, Render best for Docker, Neon best for PostgreSQL |

---

# Phase 0: Research

## Research Tasks

The following research tasks must be completed before design phase:

### R1: Vercel Configuration for Next.js
**Research**: Best practices for deploying Next.js 14+ to Vercel with environment variables
**Output**: `vercel.json` configuration and environment variable setup

### R2: Render Docker Configuration
**Research**: Optimal Dockerfile for FastAPI with health checks and Render-specific configurations
**Output**: `render.yaml` and `Dockerfile` specifications

### R3: Neon Database Connection
**Research**: Connection pooling, environment variable format, and migration handling for Neon PostgreSQL
**Output**: Database connection configuration and migration strategy

### R4: CORS and Domain Configuration
**Research**: CORS origins setup for cross-origin requests between Vercel frontend and Render backend
**Output**: CORS configuration for FastAPI and Vercel headers

### R5: Monitoring and Logging
**Research**: Platform-native logging/monitoring access and health check implementation
**Output**: Health check endpoint specification and log access strategy

---

# Phase 1: Design & Contracts

## 1.1 Vercel Configuration (`vercel.json`)

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_API_URL": "@api-url",
    "NEXT_PUBLIC_APP_URL": "@app-url"
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Credentials", "value": "true" },
        { "key": "Access-Control-Allow-Origin", "value": "@frontend-url" },
        { "key": "Access-Control-Allow-Methods", "value": "GET,POST,PUT,DELETE,OPTIONS" },
        { "key": "Access-Control-Allow-Headers", "value": "Content-Type,Authorization" }
      ]
    }
  ]
}
```

## 1.2 Render Configuration (`render.yaml`)

```yaml
services:
  - type: web
    name: todo-backend
    env: docker
    repo: https://github.com/owner/repo.git
    branch: main
    dockerfilePath: backend/Dockerfile
    dockerCommand: null
    healthCheckPath: /health
    numInstances: 1
    plan: free
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: todo-db
          property: connectionString
      - key: SECRET_KEY
        sync: false
      - key: ALGORITHM
        value: HS256
      - key: ACCESS_TOKEN_EXPIRE_MINUTES
        value: 30
      - key: CORS_ORIGINS
        value: https://*.vercel.app,http://localhost:3000
```

## 1.3 Database Schema (PostgreSQL via Neon)

```sql
-- Tasks table (matches SQLModel definition)
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id INTEGER REFERENCES users(id)
);

-- Users table (for Phase II authentication)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

## 1.4 Environment Variables

### Frontend (`.env.example`)
```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://todo-backend.onrender.com
NEXT_PUBLIC_APP_URL=https://todo-frontend.vercel.app

# Optional: Analytics and features
NEXT_PUBLIC_APP_NAME=Todo Evolution
```

### Backend (`.env.example`)
```bash
# Database
DATABASE_URL=postgres://user:password@ep-xxx.us-east-1.aws.neon.tech/neon?sslmode=require

# Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=https://*.vercel.app,http://localhost:3000

# Logging
LOG_LEVEL=INFO
```

## 1.5 Health Check Endpoint (FastAPI)

```python
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint for Render deployment"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
```

---

# Phase 2: Task Breakdown

> **Generated by `/sp.tasks` command after plan approval**

---

# Summary of Generated Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Implementation Plan | `/specs/011-phase2-deploy/plan.md` | ✅ Complete |
| Research Tasks | `/specs/011-phase2-deploy/research.md` | ⏳ Phase 0 |
| Quickstart Guide | `/specs/011-phase2-deploy/quickstart.md` | ⏳ Phase 1 |
| Vercel Config | `frontend/vercel.json` | ⏳ Phase 1 |
| Render Config | `backend/render.yaml` | ⏳ Phase 1 |
| Dockerfile | `backend/Dockerfile` | ⏳ Phase 1 |
| Environment Templates | `frontend/.env.example`, `backend/.env.example` | ⏳ Phase 1 |
| Deployment Guide | `/DEPLOYMENT.md` | ⏳ Phase 1 |
| Task Breakdown | `/specs/011-phase2-deploy/tasks.md` | ⏳ Phase 2 |

---

## Next Steps

1. **Phase 0**: Complete research tasks (R1-R5) and create `research.md`
2. **Phase 1**: Generate deployment configurations from research findings
3. **Phase 2**: Run `/sp.tasks` to create detailed task breakdown

**Report**: Branch `011-phase2-deploy`, IMPL_PLAN at `/specs/011-phase2-deploy/plan.md`
