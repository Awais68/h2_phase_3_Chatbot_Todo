---
description: "Task list for Phase II Deployment: Vercel frontend, Render backend, Neon database"
---

# Tasks: Phase II Deployment

**Input**: Design documents from `/specs/011-phase2-deploy/`
**Prerequisites**: plan.md (complete), spec.md (complete)
**Branch**: `011-phase2-deploy`

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each deployment target.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- Include exact file paths in descriptions

---

## Phase 1: Pre-Deployment Setup

**Purpose**: Verify project structure and prepare deployment artifacts

- [x] T001 [P] Verify project structure has `frontend/` and `backend/` directories per plan.md
- [x] T002 [P] Create `frontend/vercel.json` with Next.js build and CORS configuration (from plan.md 1.1)
- [x] T003 [P] Create `backend/render.yaml` with Docker configuration and health check path (from plan.md 1.2)
- [x] T004 [P] Create `backend/Dockerfile` for FastAPI container (from plan.md 1.2)
- [x] T005 [P] Create `frontend/.env.example` with required environment variables (from plan.md 1.4)
- [x] T006 [P] Create `backend/.env.example` with required environment variables (from plan.md 1.4)

**Checkpoint**: All configuration files created and ready for deployment platforms

---

## Phase 2: Database Setup (Neon)

**Purpose**: Create Neon PostgreSQL database and generate connection artifacts

### US3: Configure Database

- [x] T010 [P] [US3] Create Neon project at https://console.neon.tech
- [x] T011 [US3] Generate database schema SQL in `backend/migrations/001_initial_schema.sql` (from plan.md 1.3)
- [x] T012 [US3] Add PostgreSQL connection string to `backend/.env.example` (DATABASE_URL)
- [x] T013 [US3] Document database setup steps in `docs/database-setup.md`

**Checkpoint**: Neon database created and connection string available

---

## Phase 3: Backend Deployment (Render)

**Purpose**: Deploy FastAPI backend to Render with Docker

### US2: Deploy Backend to Container Platform

- [ ] T020 [P] [US2] Push backend code to GitHub repository
- [ ] T021 [US2] Create Render web service connected to GitHub repo
- [ ] T022 [US2] Configure environment variables in Render dashboard (from backend/.env.example):
  - DATABASE_URL (from Neon connection string)
  - SECRET_KEY (generate secure random string)
  - ALGORITHM=HS256
  - ACCESS_TOKEN_EXPIRE_MINUTES=30
  - CORS_ORIGINS
- [ ] T023 [US2] Connect Render service to Neon database
- [ ] T024 [US2] Deploy backend and verify health check endpoint at `/health`
- [ ] T025 [US2] Test API endpoints via curl or Postman:
  - `GET /health` - Verify status 200
  - `GET /docs` - Verify Swagger UI accessible

**Checkpoint**: Backend deployed and responding at https://todo-backend.onrender.com

---

## Phase 4: Frontend Deployment (Vercel)

**Purpose**: Deploy Next.js frontend to Vercel

### US1: Deploy Frontend to Cloud Platform

- [ ] T030 [P] [US1] Push frontend code to GitHub repository
- [ ] T031 [US1] Import project in Vercel dashboard
- [ ] T032 [US1] Configure environment variables in Vercel:
  - NEXT_PUBLIC_API_URL (Render backend URL)
  - NEXT_PUBLIC_APP_URL (Vercel frontend URL)
- [ ] T033 [US1] Trigger deployment and verify build succeeds
- [ ] T034 [US1] Test frontend loads at Vercel URL
- [ ] T035 [US1] Verify CORS headers allow communication with backend

**Checkpoint**: Frontend deployed and accessible at Vercel URL

---

## Phase 5: Environment Configuration

**Purpose**: Configure all environment variables and secrets across platforms

### US4: Configure Environment Variables

- [ ] T040 [P] [US4] Generate secure SECRET_KEY for JWT authentication
- [ ] T041 [US4] Verify DATABASE_URL format for Neon (sslmode=require)
- [ ] T042 [US4] Configure CORS_ORIGINS in Render to allow Vercel frontend
- [ ] T043 [US4] Test environment variable loading in both deployments
- [ ] T044 [US4] Document all required environment variables in DEPLOYMENT.md

**Checkpoint**: All environment variables configured and application starts successfully

---

## Phase 6: Monitoring Setup

**Purpose**: Enable logging and monitoring for deployed services

### US5: Set Up Monitoring and Logging

- [ ] T050 [P] [US5] Verify Vercel build and runtime logs accessible in dashboard
- [ ] T051 [US5] Verify Render application logs visible in real-time
- [ ] T052 [US5] Check Neon dashboard for connection metrics and storage usage
- [ ] T053 [US5] Test health check endpoint monitoring
- [ ] T054 [US5] Document log access procedures in docs/monitoring.md

**Checkpoint**: Logs and monitoring accessible for all three services

---

## Phase 7: Custom Domain (Optional)

**Purpose**: Configure custom domain for production URL

### US6: Configure Custom Domain

- [ ] T060 [P] [US6] Add custom domain to Vercel project settings
- [ ] T061 [US6] Configure DNS records for custom domain
- [ ] T062 [US6] Verify SSL certificate issued and renewed automatically
- [ ] T063 [US6] Update CORS_ORIGINS to include custom domain
- [ ] T064 [US6] Test application accessibility via custom domain

**Checkpoint**: Custom domain configured and SSL certificate active

---

## Phase 8: Final Verification

**Purpose**: Verify all acceptance criteria from spec.md

- [ ] T070 Verify FR-001: Frontend accessible via public URL
- [ ] T071 Verify FR-002: Backend API accessible via public URL
- [ ] T072 Verify FR-003: Data persists in PostgreSQL database
- [ ] T073 Verify FR-004: Automatic deployments trigger on push to main
- [ ] T074 Verify FR-005: Preview deployments available for pull requests
- [ ] T075 Verify FR-006: Environment variables validated at startup
- [ ] T076 Verify FR-007: Health check endpoint responding
- [ ] T077 Verify FR-008: CORS configured for frontend-backend communication
- [ ] T078 Verify FR-009: Logs accessible through platform dashboards
- [ ] T079 Verify FR-010: Custom domain works (if configured)
- [ ] T080 Verify FR-011: No credentials hardcoded in repository
- [ ] T081 Verify FR-012: Database migrations run automatically

- [ ] T090 Create comprehensive DEPLOYMENT.md with:
  - Platform account setup instructions
  - Deployment step-by-step
  - Environment variable reference
  - Troubleshooting guide
  - Rollback procedures

**Checkpoint**: All success criteria from spec.md verified

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|------------|--------|
| Phase 1: Pre-Deployment | None | All subsequent phases |
| Phase 2: Database Setup | Phase 1 | Phase 3 (backend needs DB) |
| Phase 3: Backend | Phase 2 (DATABASE_URL) | Phase 4 (frontend needs API URL) |
| Phase 4: Frontend | Phase 3 (API URL for env vars) | Phase 5 |
| Phase 5: Environment | Phases 3, 4 | Phase 6 |
| Phase 6: Monitoring | Phase 3 | Phase 8 |
| Phase 7: Custom Domain | Phase 4 | Phase 8 |
| Phase 8: Final Verification | Phases 3-7 | END |

### Critical Path

Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 8

### Parallel Opportunities

- Tasks within Phase 1 marked [P] can run in parallel
- Phase 5 environment tasks marked [P] can run in parallel
- Phase 6 monitoring tasks marked [P] can run in parallel
- Phase 7 custom domain tasks marked [P] can run in parallel

---

## Implementation Strategy

### Quick Start (MVP)

1. Complete Phase 1: Pre-Deployment Setup
2. Complete Phase 2: Database Setup
3. Complete Phase 3: Backend Deployment
4. Complete Phase 4: Frontend Deployment
5. **STOP and VALIDATE**: Basic deployment working
6. Continue to Phases 5-8 for full feature completion

### Task Execution Commands

```bash
# Verify project structure
ls -la frontend/ backend/

# Create configuration files
cat > frontend/vercel.json << 'EOF'
{ ... }
EOF

# Build and test backend locally
cd backend && docker build -t todo-backend . && docker run -p 8000:8000 todo-backend

# Test health endpoint
curl http://localhost:8000/health
```

---

## Verification Checklist

### Per Task Verification

- [ ] File created at specified path
- [ ] File content matches specification from plan.md
- [ ] No hardcoded credentials
- [ ] File follows project coding standards

### Per Phase Verification

- [ ] All tasks in phase complete
- [ ] Phase checkpoint criteria met
- [ ] Integration tested with dependent phases

### Final Verification

- [ ] All 12 functional requirements verified (FR-001 to FR-012)
- [ ] All 10 success criteria met (SC-001 to SC-010)
- [ ] DEPLOYMENT.md created and complete
- [ ] Documentation updated
- [ ] PHR created for deployment

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each phase should be independently completable and verifiable
- Rollback procedures documented for each platform
- Free tier limits documented to prevent unexpected charges
