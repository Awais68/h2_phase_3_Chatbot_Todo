<!--
SYNC IMPACT REPORT
==================
Version Change: 1.0.0
Date: 2026-01-01

Initial Version Rationale:
- New constitution for Phase II: Full-Stack Web Application
- Major evolution from Phase I (console app) to modern web architecture
- Complete technology stack transformation (Python CLI → Next.js + FastAPI)
- Addition of 17 comprehensive principles for full-stack development
- Multi-user support, authentication, and persistent storage requirements

Modified Principles:
- None (initial version for Phase II)

Added Sections:
- Project Identity & Phase II Overview
- Complete Technology Stack (Frontend, Backend, Database, Deployment)
- Monorepo Architecture with detailed structure
- Subagents Specification (9 specialized agents)
- Skills Specification (19 skills across frontend, backend, and deployment)
- API Design Principles (RESTful endpoints, JWT authentication)
- Security Best Practices (JWT management, user isolation, CORS)
- Testing Strategy (Unit, Integration, E2E, API testing)
- Deployment Guide (Vercel, Railway/Render, Neon Cloud)
- Multi-language Implementation (i18next, Urdu support)
- Voice Commands Foundation (Web Speech API preparation)
- Quality Standards (Code quality, performance, documentation)
- Success Criteria (Phase II specific deliverables)
- Transition Plan (Phase I → Phase II migration path)
- Preparation for Phase III (AI chatbot foundation)

Template Consistency:
✅ spec-template.md - Aligned with user story format and priorities
✅ plan-template.md - Constitution Check references updated
✅ tasks-template.md - Task organization aligned with subagent workflows
✅ phr-template.prompt.md - No changes needed (generic)

Follow-up TODOs:
- Create subagent files in .claude/subagents/ directory
- Create skill files in .claude/skills/ directory
- Initialize monorepo structure (frontend/, backend/, specs/phase2/)
- Set up Neon PostgreSQL database
- Configure Better Auth for frontend
- Create initial API routes in FastAPI
-->

# Todo Evolution - Phase II Constitution

**Project**: Hackathon II - The Evolution of Todo (Phase II)
**Phase**: II - Full-Stack Web Application with Multi-User Support
**Technology**: Next.js 16+ | React 19 | FastAPI | SQLModel | Neon PostgreSQL
**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01

---

## 1. Project Identity & Phase II Overview

### 1.1 Mission Statement

Transform the Phase I console application into a modern, full-stack web application with multi-user support, demonstrating mastery of full-stack development, RESTful API design, authentication, and cloud deployment. This phase builds on the solid foundation of Phase I while introducing web technologies, persistent storage, and user management.

### 1.2 Phase II Objectives

1. **Full-Stack Transformation**: Evolve from CLI to modern web architecture (Next.js + FastAPI)
2. **Multi-User Support**: Implement user authentication and data isolation
3. **Persistent Storage**: Migrate from in-memory to Neon PostgreSQL database
4. **API-First Design**: Build RESTful API with JWT authentication
5. **Responsive UI**: Create mobile-first, touch-optimized interface
6. **Cloud Deployment**: Deploy frontend (Vercel) and backend (Railway/Render)
7. **Bonus Features**: Multi-language support (Urdu) and voice commands foundation

### 1.3 Success Metrics

- All 5 CRUD operations functional via web UI and API
- JWT authentication working with user data isolation
- Responsive design passing mobile/desktop tests
- Deployed to production (accessible URLs)
- Lighthouse score ≥85
- Bonus: Urdu language support (+100 points)
- Bonus: Voice input capability (+200 points)
- Deadline: December 14, 2025 (150 base points + bonuses)

### 1.4 Phase Transition (Phase I → Phase II)

**What Changes**:
- **Platform**: CLI → Web Browser
- **Architecture**: Single Python file → Full-stack monorepo
- **Storage**: In-memory → PostgreSQL database
- **Users**: Single user → Multi-user with authentication
- **Deployment**: Local execution → Cloud deployment
- **Language**: Python only → TypeScript + Python

**What Stays**:
- Core task management functionality (CRUD)
- Data model structure (Task entity)
- Quality standards (type checking, testing)
- Spec-driven development methodology
- Clean architecture principles

---

## 2. Core Principles

### I. Spec-Driven Development First (NON-NEGOTIABLE)

**Rule**: Every feature MUST have a detailed specification written BEFORE any code is generated.

**Requirements**:
- Write specifications in `/specs/phase2/` directory
- Include: user stories, acceptance criteria, API contracts, UI mockups
- Submit specifications to Claude Code for implementation
- NEVER write code manually - all code must be Claude Code generated
- If generated code is incorrect, refine the specification, not the code
- Iterate on specs until Claude Code produces correct output
- Document all spec changes with rationale in spec file

**Rationale**: Spec-driven development forces architectural thinking and precise requirements definition. Manual coding is prohibited to maintain the learning methodology established in Phase I.

### II. Monorepo Architecture

**Rule**: Maintain a single monorepo containing both frontend and backend with shared configurations.

**Requirements**:
- Root-level configuration (tsconfig, package.json, .env.example)
- Separate `frontend/` and `backend/` directories
- Shared documentation (README, CLAUDE.md)
- Shared specs directory (`specs/phase2/`)
- Git submodules NOT allowed
- Independent deployment pipelines (frontend → Vercel, backend → Railway/Render)

**Rationale**: Monorepo simplifies shared configuration, documentation, and coordination between frontend and backend teams (even if you're the sole developer).

### III. RESTful API Design

**Rule**: API endpoints MUST follow RESTful conventions and be resource-oriented.

**Requirements**:
- Use nouns for resources: `/tasks`, `/users`
- Use HTTP verbs for actions: GET, POST, PUT, PATCH, DELETE
- Include user_id in URL path: `/api/{user_id}/tasks`
- Use proper HTTP status codes:
  - 200 OK, 201 Created, 204 No Content
  - 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
  - 500 Internal Server Error
- Return JSON for all responses
- Version API: `/api/v1/{user_id}/tasks` (v1 initially)
- Use query parameters for filtering: `?status=completed`

**Rationale**: RESTful APIs are standard, predictable, and easy to consume. Clear conventions make the API self-documenting.

### IV. JWT Authentication & User Isolation

**Rule**: All API requests must be authenticated with JWT tokens, and user data MUST be strictly isolated.

**Requirements**:
- Better Auth issues JWT on successful login/signup
- JWT contains: user_id, email, issued_at, expires_at
- Frontend stores JWT in httpOnly cookie (NOT localStorage)
- All API requests include JWT in Authorization header: `Bearer <token>`
- Backend validates JWT on every request
- Backend extracts user_id from JWT and verifies it matches URL user_id
- Reject requests with mismatched user_id (403 Forbidden)
- Token expiry: 7 days
- Shared secret between frontend and backend (JWT_SECRET_KEY in .env)

**Rationale**: JWT authentication is stateless and scalable. User isolation prevents data leakage between users—a critical security requirement.

### V. Mobile-First Design

**Rule**: UI MUST be designed for mobile devices first, then enhanced for desktop.

**Requirements**:
- Use Tailwind CSS mobile-first approach (no `md:` prefix for base styles)
- Touch-optimized buttons (min 44x44px, easy to tap)
- Readable text without zooming (16px base font size)
- Responsive layouts that adapt to screen sizes
- Test on actual mobile devices (Chrome DevTools mobile emulation at minimum)
- Loading states and spinners for slow connections
- Offline capability (PWA foundation)
- Avoid hover-dependent interactions (use focus/tap instead)

**Rationale**: Mobile usage exceeds desktop globally. Mobile-first design ensures the app is usable everywhere, not just on large screens.

### VI. Database Schema Evolution

**Rule**: Database changes MUST be versioned with Alembic migrations and backward compatible when possible.

**Requirements**:
- Use Alembic for all database migrations
- Never manually modify database schema in production
- Create migration for every schema change: `alembic revision --autogenerate -m "description"`
- Test migrations on development database before production
- Migrations MUST be reversible (downgrade possible)
- Document breaking changes in migration descriptions
- Use SQLAlchemy/SQLModel for type-safe database access
- Connection pooling with Neon PostgreSQL

**Rationale**: Versioned migrations prevent schema drift, enable rollbacks, and keep development/staging/production in sync.

### VII. Type Safety Across Stack

**Rule**: Both frontend (TypeScript) and backend (Python type hints) MUST enforce type safety.

**Requirements**:
- **Frontend**: TypeScript strict mode enabled, no `any` types
- **Backend**: All functions have type hints, use mypy for checking
- **API Contracts**: Shared type definitions (optional: use OpenAPI schema)
- **Validation**: Pydantic for backend, Zod for frontend
- No runtime type coercion errors
- Zero type errors in CI/CD pipeline
- Zod schemas for frontend form validation match Pydantic models

**Rationale**: Type safety catches bugs at compile time, not runtime. Shared type definitions prevent API contract mismatches.

### VIII. Security First

**Rule**: Security MUST be considered from day one, not bolted on later.

**Requirements**:
- **JWT Security**: httpOnly cookies, secure flag, same-site policy
- **CORS**: Restrict to allowed origins (frontend URL only in production)
- **Input Validation**: Validate ALL user inputs on both frontend and backend
- **SQL Injection**: Use parameterized queries (SQLModel handles this)
- **Rate Limiting**: Limit API calls per user (100 req/min, implement with middleware)
- **Password Hashing**: Use bcrypt or Argon2 (Better Auth handles this)
- **HTTPS Only**: Deploy with TLS/SSL (Vercel/Railway handle this)
- **Environment Variables**: Never commit secrets, use .env.example
- **Audit Logging**: Log authentication events, failed attempts (for debugging)

**Rationale**: Security vulnerabilities are expensive to fix later. Security-by-design prevents common web vulnerabilities (OWASP Top 10).

### IX. Performance & Monitoring

**Rule**: Application MUST meet performance targets and be observable in production.

**Performance Targets**:
- Page load (Time to Interactive): <3 seconds
- API response time (p95): <500ms
- Lighthouse Performance score: >85
- First Contentful Paint: <1.5 seconds
- Time to Interactive: <3 seconds

**Observability**:
- **Logs**: Structured JSON logs with timestamp, level, context
- **Metrics**: API latency, error rates, user counts (optional: use Prometheus)
- **Tracing**: Request ID passed through frontend → backend → database
- **Error Tracking**: Log errors with stack traces (use Sentry or simple logging)

**Rationale**: Performance and monitoring are critical for user experience. You can't improve what you don't measure.

### X. Testing Pyramid

**Rule**: Tests MUST cover unit, integration, and E2E scenarios with 80%+ coverage.

**Testing Levels**:
1. **Unit Tests** (70% of tests):
   - Frontend: React components, custom hooks, utilities
   - Backend: Service layer, validation, business logic
   - Fast to run, mock external dependencies

2. **Integration Tests** (20% of tests):
   - API endpoint tests (FastAPI TestClient)
   - Database operations (test with test database)
   - Frontend-Backend integration (msw for API mocking)

3. **E2E Tests** (10% of tests):
   - Playwright for browser automation
   - Critical user journeys (signup, login, CRUD operations)
   - Test on multiple viewports (mobile, desktop)

**Coverage Requirements**:
- Backend: ≥80% code coverage (pytest --cov)
- Frontend: ≥70% code coverage (Jest/Vitest coverage)
- All tests MUST pass in CI/CD pipeline

**Rationale**: The testing pyramid ensures confidence in code changes without slowing development. Unit tests catch bugs early; E2E tests catch integration issues.

### XI. Deployment Automation

**Rule**: Deployment MUST be automated with zero-downtime deployments.

**Requirements**:
- **Frontend (Vercel)**:
  - Automatic deployment on push to main branch
  - Preview deployments for pull requests
  - Environment variables configured in Vercel dashboard
  - Custom domain (optional but recommended)

- **Backend (Railway/Render)**:
  - Automatic deployment on push to main branch
  - Health checks configured (`/health` endpoint)
  - Environment variables managed in Railway/Render dashboard
  - Zero-downtime deploys (use rolling updates)

- **Database (Neon)**:
  - Automated backups enabled (daily)
  - Read replicas (optional for scaling)
  - Connection pooling configured

- **CI/CD**:
  - GitHub Actions for testing on every push
  - Deploy only after all tests pass
  - Rollback procedure documented (revert commit, redeploy previous)

**Rationale**: Automated deployments reduce human error, enable frequent releases, and make rollbacks safe and fast.

### XII. Multi-Language Support (Bonus +100 pts)

**Rule**: Application MUST support English (default) and Urdu with language switching.

**Requirements**:
- Use i18next for internationalization
- Store translations in JSON files: `public/locales/en/translation.json`, `public/locales/ur/translation.json`
- Urdu translations for all UI text (buttons, labels, error messages)
- Language switcher component in header
- RTL (Right-to-Left) support for Urdu (`dir="rtl"` on `<html>` tag)
- Persist language preference in localStorage
- Format dates/numbers per locale (use Intl API)
- Translate API error messages (backend sends error codes, frontend translates)

**Urdu Translation Coverage**:
- ✅ Navigation labels (Home, Tasks, Profile)
- ✅ Task CRUD actions (Add, View, Update, Delete)
- ✅ Form labels and placeholders
- ✅ Success and error messages
- ✅ Loading states
- ✅ Empty states

**Rationale**: Multi-language support demonstrates internationalization skills and makes the app accessible to Urdu-speaking users—a bonus feature worth 100 points.

### XIII. Voice Commands Foundation (Bonus +200 pts)

**Rule**: Application MUST support voice input for task creation using Web Speech API.

**Requirements**:
- Use Web Speech API (SpeechRecognition) for voice input
- Voice input button in task creation form
- Browser compatibility: Chrome/Edge (Web Speech API support)
- Fallback: Show error if browser doesn't support speech recognition
- Simple commands: "Create task [task title]" or just "[task title]"
- Visual feedback: Microphone animation when listening
- Error handling: Timeout after 10 seconds of silence
- Audio feedback: Optional beep on start/stop recording

**Phase III Preparation**:
- Foundation for more complex voice commands (Phase III)
- Support for: "Delete task [number]", "Mark task [number] complete"
- Store voice transcripts for analytics (optional, with consent)

**Rationale**: Voice commands prepare for Phase III AI chatbot and demonstrate cutting-edge browser capabilities. Worth 200 bonus points.

### XIV. Error Handling & User Feedback

**Rule**: All errors MUST be handled gracefully with user-friendly messages.

**Requirements**:
- **Frontend**:
  - Try-catch around all async operations
  - Display toast notifications for errors (shadcn/ui toast)
  - Retry buttons for failed API calls
  - Empty states with helpful messages
  - Loading spinners for async operations
  - Form validation errors shown inline

- **Backend**:
  - Custom exception classes for domain errors
  - HTTPException for API errors (FastAPI)
  - Detailed error messages in dev, generic in production
  - Log all errors with stack traces (structured logging)
  - Return error codes for frontend translation

**Error Messages**:
- Generic: "Something went wrong. Please try again."
- Specific: "Task not found" (404), "Title is required" (400)
- Network: "Check your internet connection"
- Auth: "Session expired. Please login again."

**Rationale**: Good error handling reduces user frustration and helps with debugging. Never expose stack traces to users in production.

### XV. Accessibility (a11y)

**Rule**: Application MUST be accessible to users with disabilities.

**Requirements**:
- **Keyboard Navigation**: All interactive elements focusable with Tab
- **Screen Readers**: ARIA labels for buttons without text, alt text for images
- **Color Contrast**: WCAG AA compliance (4.5:1 for normal text)
- **Focus Indicators**: Visible focus rings on all focusable elements
- **Semantic HTML**: Use `<button>`, `<input>`, `<label>` properly
- **Forms**: Label-input associations, error messages announced
- **Testing**: Run Lighthouse accessibility audit (score >90)

**Bonus**: Implement keyboard shortcuts (e.g., "N" for new task, "D" for delete)

**Rationale**: Accessibility is a legal requirement in many jurisdictions and ensures everyone can use the app.

### XVI. Documentation & Knowledge Transfer

**Rule**: All code, APIs, and workflows MUST be documented.

**Requirements**:
- **API Documentation**: OpenAPI/Swagger UI (`/docs` endpoint in FastAPI)
- **Component Documentation**: Comments for complex components
- **README.md**: Setup instructions, deployment guide, feature list
- **CLAUDE.md**: Instructions for Claude Code, constitution reference
- **Inline Comments**: Explain non-obvious logic (don't comment the obvious)
- **Architecture Diagrams**: Use Mermaid for system architecture (in docs)
- **Changelog**: Track version changes and migrations

**Documentation Quality**:
- Clear, concise, and up-to-date
- Includes code examples
- Screenshots for UI components (optional)
- Troubleshooting section for common issues

**Rationale**: Good documentation makes the project maintainable and helps others (and future-you) understand the codebase.

### XVII. Continuous Improvement & Learning

**Rule**: Regularly refactor and improve code based on feedback and metrics.

**Requirements**:
- **Code Review**: Review your own code (or get peer reviews)
- **Refactoring**: Dedicate time to technical debt reduction
- **Learning**: Experiment with new tools/libraries (in side branches)
- **Metrics**: Track performance, error rates, user feedback
- **Retrospectives**: After each phase, document lessons learned

**Refactoring Guidelines**:
- Fix code smells (long functions, duplicate code)
- Improve test coverage
- Update dependencies (security patches)
- Optimize slow code (profile before optimizing)

**Rationale**: Software evolves. Continuous improvement prevents technical debt and keeps the codebase healthy.

---

## 3. Technology Stack

### 3.1 Frontend Stack

| Technology | Version | Purpose | Required |
|------------|---------|---------|----------|
| **Framework** | Next.js 16+ | React framework with App Router | ✅ Yes |
| **UI Library** | React 19 | Component library | ✅ Yes |
| **Language** | TypeScript | Type-safe JavaScript | ✅ Yes |
| **Styling** | Tailwind CSS | Utility-first CSS | ✅ Yes |
| **Components** | shadcn/ui | Pre-built accessible components | ✅ Yes |
| **Auth** | Better Auth | Authentication library | ✅ Yes |
| **Forms** | React Hook Form + Zod | Form handling and validation | ✅ Yes |
| **HTTP Client** | Axios | API requests | ✅ Yes |
| **i18n** | i18next | Multi-language support | ⭕ Bonus |
| **Testing** | Jest + React Testing Library | Unit/integration tests | ✅ Yes |
| **E2E Testing** | Playwright | Browser automation | ✅ Yes |

### 3.2 Backend Stack

| Technology | Version | Purpose | Required |
|------------|---------|---------|----------|
| **Framework** | FastAPI | Python web framework | ✅ Yes |
| **Language** | Python 3.13+ | Core backend language | ✅ Yes |
| **ORM** | SQLModel | Database ORM (Type-safe SQLAlchemy) | ✅ Yes |
| **Validation** | Pydantic v2 | Data validation | ✅ Yes |
| **Auth** | JWT (python-jose) | Token generation/validation | ✅ Yes |
| **Database** | Neon PostgreSQL | Serverless PostgreSQL | ✅ Yes |
| **Migrations** | Alembic | Database versioning | ✅ Yes |
| **Testing** | pytest | Python testing framework | ✅ Yes |
| **Type Checking** | mypy | Static type analysis | ✅ Yes |
| **Linting** | Black, isort, pylint | Code quality | ✅ Yes |
| **Package Manager** | UV | Fast Python dependency manager | ✅ Yes |

### 3.3 Deployment Stack

| Technology | Purpose | Required |
|------------|---------|----------|
| **Frontend** | Vercel | Serverless deployment (Next.js) | ✅ Yes |
| **Backend** | Railway/Render | Backend API deployment | ✅ Yes |
| **Database** | Neon Cloud | PostgreSQL hosting | ✅ Yes |
| **CI/CD** | GitHub Actions | Automated testing & deployment | ✅ Yes |
| **Domain** | Vercel/Railway subdomain | Public URL | ⭕ Optional |
| **Monitoring** | LogTail/Sentry (optional) | Error tracking and logging | ⭕ Optional |

### 3.4 Development Tools

| Tool | Purpose | Required |
|------|---------|----------|
| **Claude Code** | AI code generation from specs | ✅ Yes |
| **Spec-Kit Plus** | Spec-driven development framework | ✅ Yes |
| **Git** | Version control | ✅ Yes |
| **VS Code** | Code editor (with extensions) | ⭕ Recommended |
| **Chrome DevTools** | Browser debugging | ⭕ Recommended |

---

## 4. Repository Structure (Monorepo)

```
todo-phase2/
│
├── .specify/                          # Spec-Kit Plus configuration
│   ├── memory/
│   │   └── constitution-phase2.md    # This constitution file
│   ├── templates/
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   ├── tasks-template.md
│   │   ├── phr-template.prompt.md
│   │   └── adr-template.md
│   └── scripts/
│       └── bash/
│           ├── create-phr.sh
│           └── create-adr.sh
│
├── .claude/                           # Claude Code configuration
│   ├── subagents/                     # Specialized subagents
│   │   ├── frontend-architecture.md
│   │   ├── backend-api.md
│   │   ├── database-schema.md
│   │   ├── authentication.md
│   │   ├── api-integration.md
│   │   ├── ui-ux.md
│   │   ├── deployment.md
│   │   ├── multi-language.md          # Bonus
│   │   └── voice-interface.md         # Bonus
│   └── skills/                        # Reusable skills
│       ├── nextjs-app-router.md
│       ├── react-component.md
│       ├── tailwind-css.md
│       ├── better-auth.md
│       ├── api-client.md
│       ├── fastapi-application.md
│       ├── sqlmodel-crud.md
│       ├── jwt-auth.md
│       ├── api-route-design.md
│       ├── database-migration.md
│       ├── env-config.md
│       ├── error-handling.md
│       ├── data-validation.md
│       ├── api-testing.md
│       ├── vercel-deploy.md
│       ├── database-connection.md
│       ├── i18next-integration.md     # Bonus
│       ├── voice-recognition.md       # Bonus
│       └── pwa-setup.md               # Bonus
│
├── specs/                             # Specifications
│   └── phase2/
│       ├── overview.md
│       ├── architecture.md
│       ├── features/
│       │   ├── authentication.md
│       │   ├── task-crud.md
│       │   └── ui-responsive.md
│       ├── api/
│       │   ├── endpoints.md
│       │   └── auth-flow.md
│       ├── database/
│       │   ├── schema.md
│       │   └── migrations.md
│       └── ui/
│           ├── components.md
│           └── pages.md
│
├── frontend/                          # Next.js frontend
│   ├── CLAUDE.md
│   ├── app/
│   │   ├── layout.tsx                 # Root layout
│   │   ├── page.tsx                   # Landing page
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx
│   │   │   └── signup/page.tsx
│   │   ├── (dashboard)/
│   │   │   ├── layout.tsx             # Protected layout
│   │   │   ├── page.tsx               # Task list
│   │   │   └── tasks/
│   │   │       ├── new/page.tsx       # Create task
│   │   │       └── [id]/
│   │   │           └── page.tsx       # Task details
│   │   └── api/                       # API routes (if needed)
│   ├── components/
│   │   ├── ui/                        # shadcn/ui components
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   └── SignupForm.tsx
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── DeleteTaskDialog.tsx
│   │   ├── common/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Toast.tsx
│   │   ├── LanguageSwitcher.tsx       # Bonus
│   │   └── VoiceInput.tsx             # Bonus
│   ├── lib/
│   │   ├── api-client.ts              # Axios instance with JWT
│   │   ├── auth.ts                    # Better Auth configuration
│   │   ├── validations.ts             # Zod schemas
│   │   └── i18n.ts                    # i18next config (bonus)
│   ├── hooks/
│   │   ├── useAuth.ts                 # Auth hook
│   │   ├── useTasks.ts                # Tasks hook
│   │   └── useLocalStorage.ts         # Local storage hook
│   ├── types/
│   │   └── index.ts                   # TypeScript types
│   ├── public/
│   │   └── locales/
│   │       ├── en/
│   │       │   └── translation.json
│   │       └── ur/
│   │           └── translation.json   # Bonus
│   ├── tests/
│   │   ├── components/
│   │   └── e2e/
│   ├── .env.example
│   ├── .eslintrc.json
│   ├── next.config.js
│   ├── package.json
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── backend/                           # FastAPI backend
│   ├── CLAUDE.md
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app
│   │   ├── config.py                  # Settings (Pydantic Settings)
│   │   ├── dependencies.py            # Dependency injection
│   │   ├── database.py                # Database session
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py                # User model
│   │   │   ├── task.py                # Task model
│   │   │   └── base.py                # Base model
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py                # User schemas
│   │   │   ├── task.py                # Task schemas
│   │   │   └── auth.py                # Auth schemas
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                # Auth endpoints
│   │   │   └── tasks.py               # Task endpoints
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── cors.py                # CORS middleware
│   │   │   ├── rate_limit.py          # Rate limiting
│   │   │   └── auth.py                # JWT authentication
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py        # Auth logic
│   │   │   └── task_service.py        # Task logic
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py                 # JWT utilities
│   │   │   └── password.py            # Password hashing
│   │   └── api/
│   │       ├── v1/
│   │       │   └── router.py          # v1 API router
│   │       └── health.py              # Health check
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py                # Pytest fixtures
│   │   ├── test_auth.py
│   │   ├── test_tasks.py
│   │   └── test_api.py
│   ├── .env.example
│   ├── alembic.ini
│   ├── pyproject.toml
│   └── requirements.txt
│
├── history/                           # Development history
│   ├── prompts/
│   │   ├── constitution/
│   │   ├── phase2/
│   │   └── general/
│   └── adr/
│       ├── 001-jwt-auth-selection.md
│       ├── 002-monorepo-structure.md
│       └── 003-postgresql-choice.md
│
├── docs/                              # Additional documentation
│   ├── api.md                         # API documentation
│   ├── architecture.md                # Architecture diagrams
│   └── deployment.md                  # Deployment guide
│
├── .gitignore
├── README.md                          # Root README
├── CLAUDE.md                          # Claude Code instructions (root)
└── LICENSE
```

---

## 5. API Architecture

### 5.1 API Endpoints

**Base URL**: `https://<backend-url>/api/v1`

#### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/signup` | Create new user account | ❌ No |
| POST | `/auth/login` | Login with email/password | ❌ No |
| POST | `/auth/logout` | Logout (invalidate session) | ✅ Yes |
| GET | `/auth/me` | Get current user profile | ✅ Yes |

#### Task Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users/{user_id}/tasks` | List all user's tasks | ✅ Yes |
| POST | `/users/{user_id}/tasks` | Create new task | ✅ Yes |
| GET | `/users/{user_id}/tasks/{task_id}` | Get task details | ✅ Yes |
| PUT | `/users/{user_id}/tasks/{task_id}` | Update task | ✅ Yes |
| DELETE | `/users/{user_id}/tasks/{task_id}` | Delete task | ✅ Yes |
| PATCH | `/users/{user_id}/tasks/{task_id}/complete` | Toggle completion | ✅ Yes |

#### Health Check

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/health` | Service health status | ❌ No |

### 5.2 API Request/Response Examples

#### POST /auth/signup

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "created_at": "2026-01-01T10:00:00Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Response** (400 Bad Request):
```json
{
  "success": false,
  "error": {
    "code": "EMAIL_ALREADY_EXISTS",
    "message": "User with this email already exists"
  }
}
```

#### GET /users/{user_id}/tasks

**Request**:
```
GET /api/v1/users/1/tasks
Authorization: Bearer <JWT_TOKEN>
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": false,
        "created_at": "2026-01-01T10:00:00Z",
        "updated_at": "2026-01-01T10:00:00Z"
      },
      {
        "id": 2,
        "title": "Call dentist",
        "description": "",
        "completed": true,
        "created_at": "2026-01-01T11:00:00Z",
        "updated_at": "2026-01-01T12:00:00Z"
      }
    ],
    "count": 2,
    "completed_count": 1
  }
}
```

#### POST /users/{user_id}/tasks

**Request**:
```json
{
  "title": "New task",
  "description": "Task description"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": 3,
    "title": "New task",
    "description": "Task description",
    "completed": false,
    "created_at": "2026-01-01T13:00:00Z",
    "updated_at": "2026-01-01T13:00:00Z"
  }
}
```

#### Error Response (401 Unauthorized)
```json
{
  "success": false,
  "error": {
    "code": "INVALID_TOKEN",
    "message": "Authentication token is invalid or expired"
  }
}
```

#### Error Response (403 Forbidden)
```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "You don't have permission to access this resource"
  }
}
```

### 5.3 Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Database

    User->>Frontend: Enter email/password
    Frontend->>Backend: POST /auth/signup
    Backend->>Backend: Hash password (bcrypt)
    Backend->>Database: Create user record
    Database-->>Backend: User created
    Backend->>Backend: Generate JWT token
    Backend-->>Frontend: Return token + user data
    Frontend->>Frontend: Store token in httpOnly cookie

    Note over Frontend,Backend: Subsequent requests

    Frontend->>Backend: GET /users/{id}/tasks<br/>Authorization: Bearer <token>
    Backend->>Backend: Verify JWT signature
    Backend->>Backend: Extract user_id from JWT
    Backend->>Database: Query user's tasks
    Database-->>Backend: Task list
    Backend-->>Frontend: Return tasks
```

### 5.4 Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `EMAIL_ALREADY_EXISTS` | 400 | Email already registered |
| `INVALID_CREDENTIALS` | 401 | Wrong email or password |
| `INVALID_TOKEN` | 401 | JWT token is invalid or expired |
| `TOKEN_EXPIRED` | 401 | JWT token has expired |
| `FORBIDDEN` | 403 | User cannot access requested resource |
| `USER_NOT_FOUND` | 404 | User does not exist |
| `TASK_NOT_FOUND` | 404 | Task does not exist |
| `VALIDATION_ERROR` | 400 | Input validation failed |
| `INTERNAL_ERROR` | 500 | Server error |

---

## 6. Database Schema

### 6.1 Entity Relationship Diagram

```mermaid
erDiagram
    User ||--o{ Task : "has many"

    User {
        int id PK
        string email UK
        string password_hash
        datetime created_at
        datetime updated_at
    }

    Task {
        int id PK
        int user_id FK
        string title
        text description
        boolean completed
        datetime created_at
        datetime updated_at
    }
```

### 6.2 User Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique user ID |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Account creation time |
| `updated_at` | TIMESTAMP | DEFAULT NOW(), ON UPDATE | Last update time |

**Indexes**:
- `idx_email` on `email` (for fast login lookup)

### 6.3 Task Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique task ID |
| `user_id` | INTEGER | FOREIGN KEY → User.id, NOT NULL | Owner of task |
| `title` | VARCHAR(200) | NOT NULL | Task title |
| `description` | TEXT | NULLABLE | Task description |
| `completed` | BOOLEAN | DEFAULT FALSE | Completion status |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation time |
| `updated_at` | TIMESTAMP | DEFAULT NOW(), ON UPDATE | Last update time |

**Indexes**:
- `idx_user_id` on `user_id` (for user task queries)
- `idx_user_completed` on `user_id, completed` (for filtered queries)

**Foreign Keys**:
- `fk_task_user` → `user_id` REFERENCES `User(id)` ON DELETE CASCADE

**Constraints**:
- Title length: 1-200 characters
- Description: max 1000 characters

### 6.4 Migration Files

#### Initial Migration (001_initial_schema)

```python
"""Initial database schema

Revision ID: 001
Revises:
Create Date: 2026-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_email', 'users', ['email'], unique=True)

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_user_id', 'tasks', ['user_id'])
    op.create_index('idx_user_completed', 'tasks', ['user_id', 'completed'])

def downgrade():
    op.drop_index('idx_user_completed', 'tasks')
    op.drop_index('idx_user_id', 'tasks')
    op.drop_table('tasks')
    op.drop_index('idx_email', 'users')
    op.drop_table('users')
```

---

## 7. Security Best Practices

### 7.1 JWT Token Management

**Token Structure**:
```python
{
  "user_id": 1,
  "email": "user@example.com",
  "iat": 1609459200,  # Issued at
  "exp": 1610064000   # Expires at (7 days)
}
```

**Security Measures**:
1. **Shared Secret**: `JWT_SECRET_KEY` in .env (min 32 characters, random)
2. **Algorithm**: HS256 (HMAC-SHA256)
3. **Expiry**: 7 days (configurable)
4. **Storage**: httpOnly cookie on frontend (NOT localStorage)
5. **Transmission**: Always over HTTPS

**Token Refresh** (Phase III):
- Implement refresh tokens for long-lived sessions
- Optional for Phase II (simplified flow)

### 7.2 User Data Isolation

**Backend Validation**:
```python
async def get_user_tasks(user_id: int, current_user_id: int):
    # Verify user_id matches authenticated user
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    # Query only returns user's tasks
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks
```

**Database-Level Protection**:
- Foreign key constraints prevent orphaned tasks
- CASCADE DELETE removes tasks when user is deleted

### 7.3 Environment Variables

**Required Variables** (frontend/.env):
```
NEXT_PUBLIC_API_BASE_URL=https://<backend-url>/api/v1
NEXT_PUBLIC_APP_URL=https://<frontend-url>
BETTER_AUTH_SECRET=<random-32-chars>
JWT_SECRET_KEY=<shared-with-backend>
```

**Required Variables** (backend/.env):
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
JWT_SECRET_KEY=<shared-with-frontend>
CORS_ORIGINS=https://<frontend-url>
```

**Never Commit**:
- .env files
- Secrets
- API keys
- Passwords

### 7.4 CORS Configuration

**Development**:
```python
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production**:
```python
origins = [
    "https://<frontend-url>.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### 7.5 Input Validation

**Backend (Pydantic)**:
```python
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()
```

**Frontend (Zod)**:
```typescript
import { z } from 'zod';

export const taskSchema = z.object({
  title: z.string().min(1).max(200).transform((val) => val.trim()),
  description: z.string().max(1000).optional(),
});
```

### 7.6 Rate Limiting

**Implementation**:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/auth/login")
@limiter.limit("5 per minute")
async def login(request: Request, credentials: LoginSchema):
    # Login logic
```

**Limits**:
- Login/signup: 5 requests per minute
- Task CRUD: 100 requests per minute per user

---

## 8. Testing Strategy

### 8.1 Frontend Testing

#### Unit Tests (Jest + React Testing Library)

```typescript
// components/tasks/TaskCard.test.tsx
import { render, screen } from '@testing-library/react';
import { TaskCard } from './TaskCard';

describe('TaskCard', () => {
  it('renders task title and description', () => {
    render(<TaskCard task={{ id: 1, title: 'Test', description: 'Desc', completed: false }} />);
    expect(screen.getByText('Test')).toBeInTheDocument();
    expect(screen.getByText('Desc')).toBeInTheDocument();
  });

  it('shows completed badge when task is done', () => {
    render(<TaskCard task={{ id: 1, title: 'Test', completed: true }} />);
    expect(screen.getByText('Completed')).toBeInTheDocument();
  });
});
```

#### Integration Tests (MSW for API mocking)

```typescript
// tests/integration/task-flow.test.tsx
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('/api/v1/users/1/tasks', (req, res, ctx) => {
    return res(ctx.json({ success: true, data: { tasks: [] } }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

#### E2E Tests (Playwright)

```typescript
// tests/e2e/task-crud.spec.ts
test('complete task flow', async ({ page }) => {
  // Login
  await page.goto('/login');
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');

  // Create task
  await page.click('button:has-text("Add Task")');
  await page.fill('input[name="title"]', 'New task');
  await page.click('button:has-text("Save")');

  // Verify task appears
  await expect(page.locator('text=New task')).toBeVisible();
});
```

### 8.2 Backend Testing

#### Unit Tests (pytest)

```python
# tests/test_task_service.py
import pytest
from app.services.task_service import TaskService
from app.models.task import Task

def test_create_task(db_session):
    service = TaskService(db_session)
    task = service.create_task(user_id=1, title="Test task")
    assert task.id is not None
    assert task.title == "Test task"
    assert task.completed is False

def test_create_task_empty_title(db_session):
    service = TaskService(db_session)
    with pytest.raises(ValueError):
        service.create_task(user_id=1, title="")
```

#### Integration Tests (FastAPI TestClient)

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_task():
    # Login first to get token
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password"}
    )
    token = response.json()["data"]["token"]

    # Create task
    response = client.post(
        "/api/v1/users/1/tasks",
        json={"title": "New task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["data"]["title"] == "New task"
```

### 8.3 Test Coverage Requirements

| Component | Coverage Target | Tool |
|-----------|----------------|------|
| Backend Services | ≥90% | pytest --cov |
| Backend Routes | ≥80% | pytest --cov |
| Frontend Components | ≥80% | Jest coverage |
| Frontend Hooks | ≥85% | Jest coverage |
| API Endpoints | 100% (E2E) | Playwright |

---

## 9. Deployment Guide

### 9.1 Frontend Deployment (Vercel)

**Step 1: Install Vercel CLI**
```bash
npm install -g vercel
```

**Step 2: Deploy**
```bash
cd frontend
vercel
```

**Step 3: Configure Environment Variables in Vercel Dashboard**
```
NEXT_PUBLIC_API_BASE_URL=https://your-backend.railway.app
NEXT_PUBLIC_APP_URL=https://your-frontend.vercel.app
BETTER_AUTH_SECRET=<your-secret>
JWT_SECRET_KEY=<your-secret>
```

**Step 4: Custom Domain (Optional)**
- Add domain in Vercel dashboard
- Update DNS records

### 9.2 Backend Deployment (Railway)

**Step 1: Create Railway Account**
- Sign up at railway.app
- Connect GitHub repository

**Step 2: Configure Railway Project**
```bash
# In railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 300
```

**Step 3: Set Environment Variables**
```
DATABASE_URL=<neon-postgres-url>
JWT_SECRET_KEY=<your-secret>
CORS_ORIGINS=https://your-frontend.vercel.app
```

**Step 4: Run Migrations**
```bash
railway run alembic upgrade head
```

### 9.3 Database Deployment (Neon)

**Step 1: Create Neon Project**
- Sign up at neon.tech
- Create new PostgreSQL database

**Step 2: Get Connection String**
```
postgresql://user:password@ep-name.aws.region.aws.neon.tech/dbname?sslmode=require
```

**Step 3: Configure Connection Pooling**
```python
# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

### 9.4 CI/CD Pipeline (GitHub Actions)

**Workflow: .github/workflows/ci.yml**

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  frontend-test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./frontend
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
      - run: npm run build

  backend-test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./backend
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - run: uv sync
      - run: uv run pytest
      - run: uv run mypy app/
      - run: uv run pylint app/

  deploy:
    needs: [frontend-test, backend-test]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      # Vercel and Railway auto-deploy on push
```

---

## 10. Multi-Language Implementation (Bonus +100 pts)

### 10.1 i18next Setup

**Installation**:
```bash
npm install i18next react-i18next next-i18next
```

**Configuration: frontend/lib/i18n.ts**:
```typescript
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from '../public/locales/en/translation.json';
import ur from '../public/locales/ur/translation.json';

i18n.use(initReactI18next).init({
  resources: { en, ur },
  lng: 'en',
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
});

export default i18n;
```

### 10.2 Translation Files

**public/locales/en/translation.json**:
```json
{
  "nav": {
    "home": "Home",
    "tasks": "Tasks",
    "profile": "Profile",
    "logout": "Logout"
  },
  "tasks": {
    "add": "Add Task",
    "edit": "Edit Task",
    "delete": "Delete Task",
    "complete": "Mark Complete",
    "title": "Task Title",
    "description": "Description",
    "save": "Save",
    "cancel": "Cancel"
  },
  "auth": {
    "login": "Login",
    "signup": "Sign Up",
    "email": "Email",
    "password": "Password"
  }
}
```

**public/locales/ur/translation.json**:
```json
{
  "nav": {
    "home": "ہوم",
    "tasks": "ٹاسکس",
    "profile": "پروفائل",
    "logout": "لاگ آؤٹ"
  },
  "tasks": {
    "add": "ٹاسک شامل کریں",
    "edit": "ٹاسک ترمیم کریں",
    "delete": "ٹاسک حذف کریں",
    "complete": "مکمل کے طور پر نشان زد کریں",
    "title": "ٹاسک کا عنوان",
    "description": "تفصیل",
    "save": "محفوظ کریں",
    "cancel": "منسوخ کریں"
  },
  "auth": {
    "login": "لاگ ان",
    "signup": "سائن اپ",
    "email": "ای میل",
    "password": "پاس ورڈ"
  }
}
```

### 10.3 RTL Support

**Layout with RTL**:
```tsx
// app/layout.tsx
import { useTranslation } from 'react-i18next';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const { i18n } = useTranslation();
  const dir = i18n.language === 'ur' ? 'rtl' : 'ltr';

  return (
    <html lang={i18n.language} dir={dir}>
      <body>{children}</body>
    </html>
  );
}
```

### 10.4 Language Switcher Component

```tsx
// components/LanguageSwitcher.tsx
import { useTranslation } from 'react-i18next';

export function LanguageSwitcher() {
  const { i18n } = useTranslation();

  const changeLanguage = (lang: string) => {
    i18n.changeLanguage(lang);
    localStorage.setItem('language', lang);
  };

  return (
    <select
      value={i18n.language}
      onChange={(e) => changeLanguage(e.target.value)}
    >
      <option value="en">English</option>
      <option value="ur">اردو (Urdu)</option>
    </select>
  );
}
```

---

## 11. Voice Commands Foundation (Bonus +200 pts)

### 11.1 Web Speech API Setup

**components/VoiceInput.tsx**:
```tsx
'use client';

import { useState, useEffect, useRef } from 'react';

export function VoiceInput({ onTranscript }: { onTranscript: (text: string) => void }) {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;

      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        onTranscript(transcript);
        setIsListening(false);
      };

      recognitionRef.current.onerror = () => {
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
    };
  }, [onTranscript]);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition not supported in this browser');
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
    } else {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  return (
    <button
      onClick={toggleListening}
      className={`p-2 rounded-full ${isListening ? 'bg-red-500 animate-pulse' : 'bg-blue-500'}`}
    >
      {isListening ? '🎤 Listening...' : '🎤 Speak'}
    </button>
  );
}
```

### 11.2 Integration with Task Form

```tsx
// components/tasks/TaskForm.tsx
import { useState } from 'react';
import { VoiceInput } from '../VoiceInput';

export function TaskForm() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleVoiceTranscript = (transcript: string) => {
    // Simple parsing: "Create task [title]" or just "[title]"
    const lower = transcript.toLowerCase();
    if (lower.startsWith('create task')) {
      setTitle(transcript.replace('create task', '').trim());
    } else {
      setTitle(transcript);
    }
  };

  return (
    <form>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Task title"
      />
      <VoiceInput onTranscript={handleVoiceTranscript} />
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Description"
      />
      <button type="submit">Create Task</button>
    </form>
  );
}
```

### 11.3 Browser Compatibility

**Supported Browsers**:
- Chrome 25+
- Edge 79+
- Safari 14.1+
- Firefox (limited, requires configuration)

**Fallback UI**:
```tsx
if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
  return <button disabled>Voice not supported</button>;
}
```

---

## 12. Quality Standards

### 12.1 Code Quality

**Frontend**:
- TypeScript strict mode
- ESLint configuration
- Prettier for formatting
- No `any` types
- Component naming: PascalCase
- File naming: PascalCase (components), kebab-case (utilities)

**Backend**:
- Python type hints on all functions
- Black formatter (consistent style)
- isort (import sorting)
- pylint (code quality, score ≥8.0)
- mypy (type checking, zero errors)

### 12.2 Performance Standards

| Metric | Target | Tool |
|--------|--------|------|
| Page Load (TTFB) | <500ms | Lighthouse |
| First Contentful Paint | <1.5s | Lighthouse |
| Time to Interactive | <3s | Lighthouse |
| API Response (p95) | <500ms | Server logs |
| Lighthouse Performance | >85 | Lighthouse |
| Lighthouse Accessibility | >90 | Lighthouse |
| Lighthouse Best Practices | >90 | Lighthouse |
| Lighthouse SEO | >80 | Lighthouse |

### 12.3 Documentation Standards

**API Documentation**:
- Auto-generated with FastAPI OpenAPI
- Accessible at `/docs` (Swagger UI)
- Include all endpoints with request/response examples
- Document authentication requirements

**Code Documentation**:
- Docstrings for all backend functions
- JSDoc comments for complex frontend functions
- Comments explain "why", not "what"
- README with setup, deployment, and feature list

### 12.4 Accessibility Standards

- WCAG 2.1 Level AA compliance
- Keyboard navigation support
- Screen reader compatibility
- Color contrast ratio ≥4.5:1
- ARIA labels for icon-only buttons
- Focus indicators visible
- Form error announcements

---

## 13. Success Criteria

### 13.1 Must-Have (150 points)

- [ ] User signup works with email/password
- [ ] User login works with JWT authentication
- [ ] JWT token stored in httpOnly cookie
- [ ] All 5 CRUD operations functional via UI
- [ ] All 5 CRUD operations functional via API
- [ ] Tasks are user-specific (data isolation)
- [ ] Responsive on mobile devices (tested)
- [ ] Responsive on desktop (tested)
- [ ] Frontend deployed to Vercel (accessible URL)
- [ ] Backend deployed to Railway (accessible URL)
- [ ] Database on Neon PostgreSQL
- [ ] All API endpoints documented (/docs)
- [ ] All specs in `specs/phase2/`
- [ ] Subagents created in `.claude/subagents/`
- [ ] Skills created in `.claude/skills/`
- [ ] Unit tests pass (≥80% coverage)
- [ ] E2E tests pass (critical flows)
- [ ] Demo video (<90 seconds)

### 13.2 Bonus Features

**Multi-Language Support (+100 points)**:
- [ ] i18next configured
- [ ] English and Urdu translations complete
- [ ] Language switcher in UI
- [ ] RTL layout for Urdu
- [ ] Language preference persisted

**Voice Commands (+200 points)**:
- [ ] Web Speech API integration
- [ ] Voice input for task creation
- [ ] Visual feedback when listening
- [ ] Error handling for unsupported browsers
- [ ] Audio feedback (beep on start/stop)

**Additional Bonuses**:
- [ ] PWA installable (+50 points)
- [ ] Offline capability (+50 points)
- [ ] 90+ Lighthouse score (+50 points)

### 13.3 Definition of Done

A feature is complete when:
- [ ] Specification written and approved
- [ ] Code generated by Claude Code
- [ ] All tests pass (unit, integration, E2E)
- [ ] Manual testing against acceptance criteria
- [ ] API documented (if applicable)
- [ ] Performance meets targets
- [ ] Deployed to staging/production
- [ ] PHR created
- [ ] Code reviewed

---

## 14. Transition Plan: Phase I → Phase II

### 14.1 Data Migration

**Phase I Data Structure**:
```python
Task {
  id: int
  title: str
  description: str
  completed: bool
  created_at: datetime
  updated_at: datetime
}
```

**Phase II Data Structure**:
```python
Task {
  id: int
  user_id: int  # NEW
  title: str
  description: str
  completed: bool
  created_at: datetime
  updated_at: datetime
}

User {
  id: int  # NEW
  email: str  # NEW
  password_hash: str  # NEW
  created_at: datetime
  updated_at: datetime
}
```

**Migration Strategy**:
1. Create new PostgreSQL database with Phase II schema
2. Create a default user for migrating Phase I tasks
3. Import Phase I tasks (manually or via script)
4. Assign all tasks to default user

### 14.2 API Migration

**Phase I (CLI)**:
```python
# Direct function calls
task = service.create_task(title="Buy groceries")
tasks = service.list_tasks()
```

**Phase II (Web API)**:
```typescript
// HTTP requests
const response = await fetch('/api/v1/users/1/tasks', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: JSON.stringify({ title: 'Buy groceries' })
});
const task = await response.json();
```

### 14.3 UI Migration

| Phase I CLI | Phase II Web UI |
|-------------|----------------|
| "Enter task title: " | Input field with placeholder |
| "Task created successfully!" | Toast notification |
| ASCII table output | Card-based task list |
| Numeric menu (1-6) | Button navigation |

---

## 15. Preparation for Phase III

### 15.1 AI Chatbot Foundation

Phase II lays groundwork for Phase III AI integration:

**Current Implementation**:
- RESTful API (can be extended for chat)
- Task CRUD operations
- User authentication
- Voice input capability (bonus)

**Phase III Requirements**:
- WebSocket or Server-Sent Events for real-time chat
- AI model integration (OpenAI API or similar)
- Natural language processing for task commands
- Voice output (text-to-speech)

**Phase II Preparations**:
- Design API with extensibility in mind
- Store user preferences (for AI personalization)
- Implement voice input (prepare for voice output)
- Document API contracts for AI integration

### 15.2 Recommended ADRs

Document these decisions in Phase II to aid Phase III:

1. **API Versioning Strategy**: How to handle breaking changes?
2. **Authentication Method**: JWT vs OAuth 2.0 vs Session
3. **Database Scaling**: When to add caching (Redis)?
4. **Real-time Communication**: WebSocket vs SSE vs Polling

---

## 16. Development Workflow

### 16.1 Spec-Driven Development Cycle

```
1. Write Specification (specs/phase2/feature.md)
   ↓
2. Generate Plan (/sp.plan)
   ↓
3. Create Tasks (/sp.tasks)
   ↓
4. Invoke Subagent for Implementation
   ↓
5. Review Generated Code
   ↓
6. Run Quality Checks (type check, lint, test)
   ↓
7. Manual Testing (acceptance criteria)
   ↓
8. Create PHR
   ↓
9. Commit and Push
   ↓
10. Deploy (CI/CD auto-deploys)
```

### 16.2 Quality Gates

| Gate | Command | Threshold |
|------|---------|-----------|
| Type Check (Frontend) | `npm run type-check` | 0 errors |
| Lint (Frontend) | `npm run lint` | 0 errors |
| Type Check (Backend) | `uv run mypy app/` | 0 errors |
| Lint (Backend) | `uv run pylint app/` | Score ≥8.0 |
| Tests (Backend) | `uv run pytest` | 100% pass |
| Tests (Frontend) | `npm test` | 100% pass |
| Coverage | `pytest --cov=app` | ≥80% |
| E2E | `npx playwright test` | 100% pass |

### 16.3 Feature Implementation Order

1. **Project Setup** (Day 1-2)
   - Initialize monorepo
   - Set up Next.js frontend
   - Set up FastAPI backend
   - Configure Neon PostgreSQL
   - Create base structure

2. **Database & Models** (Day 2-3)
   - Define SQLModel schemas
   - Create Alembic migrations
   - Write model tests

3. **Authentication** (Day 3-4)
   - Implement user signup/login
   - JWT token generation
   - Better Auth integration
   - Auth middleware

4. **Task CRUD API** (Day 4-5)
   - Implement task endpoints
   - User data isolation
   - API tests

5. **Frontend UI** (Day 5-7)
   - Task list page
   - Task create/edit forms
   - Delete confirmation
   - Mobile responsive design

6. **Integration** (Day 7-8)
   - API client setup
   - Connect frontend to backend
   - Error handling
   - Loading states

7. **Testing & Polish** (Day 8-9)
   - E2E tests
   - Accessibility audit
   - Performance optimization
   - Bug fixes

8. **Bonus Features** (Day 9-10)
   - Multi-language support
   - Voice commands
   - PWA setup

9. **Deployment** (Day 10-11)
   - Deploy to Vercel
   - Deploy to Railway
   - Configure environment variables
   - Run migrations

10. **Demo & Documentation** (Day 11-12)
    - Record demo video
    - Write README
    - Final testing
    - Submit for review

---

## 17. Governance

### 17.1 Constitution Authority

This constitution is the governing document for Phase II. All implementation decisions must align with these principles.

**Hierarchy**:
1. Constitution (this document)
2. Feature specifications (`specs/phase2/`)
3. Implementation plans
4. Generated code

### 17.2 Amendment Process

**Minor Amendments** (1.0.0 → 1.0.1):
- Clarifications, typo fixes
- No principle changes
- Document in commit message

**Major Amendments** (1.0.0 → 1.1.0):
- Add new principles or sections
- Update version number
- Create ADR
- Update dependent templates

**Breaking Changes** (1.0.0 → 2.0.0):
- Remove or redefine principles
- Requires migration plan
- Explicit approval needed

### 17.3 Compliance Review

Before any feature is complete, verify:
- [ ] Specification written
- [ ] Code generated by Claude Code
- [ ] All principles followed
- [ ] Quality gates passed
- [ ] Tests pass (≥80% coverage)
- [ ] Manual testing complete
- [ ] PHR created
- [ ] Committed and documented

---

## 18. Summary

This constitution establishes the foundation for Phase II of the Todo Evolution project. By following these principles, specifications, and workflows, you will:

1. **Master Full-Stack Development** - Build modern web apps with Next.js + FastAPI
2. **Implement Security Best Practices** - JWT auth, user isolation, CORS
3. **Deploy to Cloud** - Production-grade deployment with Vercel and Railway
4. **Deliver Quality Software** - Type-safe, tested, documented, and performant
5. **Prepare for Phase III** - Foundation for AI chatbot integration

**Remember**:
- Spec-driven development is non-negotiable
- Quality gates must pass before proceeding
- Security is priority from day one
- Test thoroughly at all levels

**Next Steps**:
1. Create subagents in `.claude/subagents/`
2. Create skills in `.claude/skills/`
3. Write feature specifications in `specs/phase2/`
4. Generate plans and tasks
5. Implement with Claude Code
6. Test and deploy
7. Deliver by December 14, 2025

---

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01

*This constitution governs Phase II exclusively. Phase III will introduce AI chatbot capabilities and advanced features.*
