---
id: 0001
title: phase2-constitution
stage: constitution
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: awais
command: /sp.constitution
labels: ["constitution", "phase2", "full-stack"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution-phase2.md
tests:
  - No tests run (documentation only)
---

## Prompt

Create a comprehensive constitution for Phase II: Full-Stack Web Application

PROJECT CONTEXT:
- Phase: II - Full-Stack Web Application with Multi-User Support
- Previous Phase: Phase I Console App (completed)
- Evolution: Transform console app into modern web application
- Approach: Spec-Driven Development (No manual coding)
- Deadline: December 14, 2025
- Points: 150 base + bonuses

TECHNOLOGY STACK:

Frontend:
- Next.js 16+ (App Router)
- React 19
- TypeScript
- Tailwind CSS (Mobile-First)
- shadcn/ui components
- Better Auth (Authentication)

Backend:
- Python FastAPI
- SQLModel (ORM)
- Pydantic (Validation)
- JWT (Token handling)
- Python 3.13+

Database:
- Neon Serverless PostgreSQL
- Automated migrations

Authentication:
- Better Auth (Frontend)
- JWT tokens (Shared secret)
- User isolation

Development Tools:
- Claude Code (Code generation)
- Spec-Kit Plus (Specifications)
- UV (Python package manager)
- npm/pnpm (Node package manager)

Deployment:
- Frontend: Vercel
- Backend: Railway/Render
- Database: Neon Cloud

[... rest of user request with detailed requirements for subagents, skills, API architecture, security, testing, deployment, multi-language support, voice commands, and quality standards ...]

FORMAT:
Create the constitution as a comprehensive markdown document with:
- Clear section headers
- Tables for tech stack and skills
- Code examples where relevant
- Checklists for requirements
- Architecture diagrams (mermaid)
- Workflow diagrams
- API endpoint documentation
- Security guidelines
- Deployment procedures

Make it actionable, detailed, and ready for Claude Code to implement from!

## Response snapshot

Created comprehensive Phase II constitution (.specify/memory/constitution-phase2.md) with:

1. **17 Core Principles** covering spec-driven development, monorepo architecture, RESTful API design, JWT authentication, mobile-first design, database schema evolution, type safety, security, performance, testing pyramid, deployment automation, multi-language support, voice commands, error handling, accessibility, documentation, and continuous improvement.

2. **Complete Technology Stack** breakdown for frontend (Next.js 16+, React 19, TypeScript, Tailwind, shadcn/ui), backend (FastAPI, SQLModel, Pydantic, Python 3.13+), database (Neon PostgreSQL), and deployment (Vercel, Railway/Render).

3. **Monorepo Structure** with detailed directory tree showing frontend/, backend/, specs/phase2/, .claude/ subagents and skills, and history/ directories.

4. **9 Subagent Specifications** specialized for frontend architecture, backend API, database schema, authentication, API integration, UI/UX, deployment, multi-language, and voice interface.

5. **19 Skill Definitions** covering Next.js App Router, React components, Tailwind CSS, Better Auth, API client, FastAPI, SQLModel CRUD, JWT authentication, API routes, database migrations, environment config, error handling, data validation, API testing, Vercel deployment, database connection, i18next integration, voice recognition, and PWA setup.

6. **RESTful API Architecture** with all endpoints documented (auth, tasks, health), request/response examples, JWT authentication flow diagram, and error codes.

7. **Database Schema** with ER diagram (User, Task entities), complete table definitions, foreign keys, indexes, and initial Alembic migration.

8. **Security Best Practices** covering JWT token management, user data isolation, environment variables, CORS configuration, input validation, and rate limiting.

9. **Testing Strategy** with frontend unit/integration/E2E tests (Jest, React Testing Library, Playwright), backend unit/integration tests (pytest, FastAPI TestClient), and 80%+ coverage requirements.

10. **Deployment Guide** for Vercel (frontend), Railway (backend), Neon (database), GitHub Actions CI/CD pipeline, and environment variable configuration.

11. **Multi-Language Implementation** (Bonus +100 pts) with i18next setup, English/Urdu translation files, RTL support, and language switcher component.

12. **Voice Commands Foundation** (Bonus +200 pts) with Web Speech API setup, voice input component, integration with task forms, and browser compatibility handling.

13. **Quality Standards** for code quality (TypeScript strict, Python type hints, Black, pylint, mypy), performance (Lighthouse >85, API <500ms), documentation (OpenAPI/Swagger), and accessibility (WCAG AA).

14. **Success Criteria** with must-have checklist (150 points), bonus features (+100 Urdu, +200 voice), and definition of done.

15. **Transition Plan** (Phase I → Phase II) with data migration strategy, API migration examples, and UI migration mapping.

16. **Phase III Preparation** outlining AI chatbot foundation and recommended ADRs.

17. **Development Workflow** with 10-step spec-driven cycle, quality gates table, and 12-day implementation timeline.

Constitution version 1.0.0 ratified on 2026-01-01 with governance amendment process and compliance review checklist.

## Outcome

- ✅ Impact: Created comprehensive governing document for Phase II full-stack web application development
- 🧪 Tests: No tests run (documentation creation only)
- 📁 Files: Created .specify/memory/constitution-phase2.md (1 file, ~1800 lines)
- 🔁 Next prompts: Create subagents in .claude/subagents/, create skills in .claude/skills/, write feature specifications in specs/phase2/
- 🧠 Reflection: Constitution successfully captures all user requirements including technology stack, architecture, subagents, skills, security, testing, deployment, and bonus features (multi-language + voice commands)

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (documentation)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create subagent and skill files as specified in constitution
