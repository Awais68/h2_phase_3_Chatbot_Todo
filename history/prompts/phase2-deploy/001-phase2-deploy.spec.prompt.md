---
id: 001
title: Phase II deployment specification
stage: spec
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: phase2-deploy
branch: 011-phase2-deploy
user: claude
command: /sp.specify PHASE II DEPLOYMENT SPECIFICATION...
labels: [deployment, vercel, render, neon]
links:
  spec: specs/011-phase2-deploy/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/011-phase2-deploy/spec.md
  - specs/011-phase2-deploy/checklists/requirements.md
tests: []
---

## Prompt

PHASE II DEPLOYMENT SPECIFICATION

DEPLOYMENT TARGETS:

- Frontend: Vercel (Recommended) or Netlify
- Backend: Render
- Database: Neon Serverless PostgreSQL

---

FRONTEND DEPLOYMENT (Vercel)

Prerequisites:
- Vercel account (free tier)
- GitHub repository
- Project pushed to GitHub

Steps:

1. Install Vercel CLI:
```bash
npm i -g vercel
```
Login to Vercel:

```bash
vercel login
```
Deploy from project root:

```bash
cd frontend
vercel
```
Answer prompts:

```
? Set up and deploy "frontend"? Y
? Which scope? [Your Account]
? Link to existing project? N
? What's your project's name? hackathon-todo
? In which directory is your code located? ./
? Want to override settings? N
```
Set environment variables in Vercel Dashboard:

```bash
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_URL=https://your-app.vercel.app
```
Redeploy after setting env vars:

```bash
vercel --prod
```
Vercel configuration file:

```json
// vercel.json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["iad1"]
}
```
Automatic deployments:

Connect GitHub repository in Vercel Dashboard

Every push to main branch triggers production deployment

Every PR creates preview deployment

Environment variables inherited

BACKEND DEPLOYMENT (Render)

Prerequisites:

Render account (free tier / trial)

Dockerized backend

GitHub repository

Create Dockerfile:

```dockerfile
# backend/Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
Create render.yaml (recommended for Render Infra-as-Code):

```yaml
# render.yaml
services:
  - type: web
    name: hackathon-todo-backend
    env: docker
    plan: free
    dockerfilePath: ./backend/Dockerfile
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: JWT_SECRET_KEY
        sync: false
      - key: JWT_ALGORITHM
        value: HS256
      - key: JWT_EXPIRE_MINUTES
        value: 10080
      - key: CORS_ORIGINS
        sync: false
      - key: PORT
        value: 8000
    healthCheckPath: /health
    autoDeploy: true
```
Or render.toml (if you prefer):

```toml
# backend/render.toml
[build]
builder = "dockerfile"
dockerfilePath = "Dockerfile"

[service]
name = "hackathon-todo-backend"
env = "docker"
autoDeploy = true

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```
Deploy to Render (Dashboard – recommended):

Push your code to GitHub.

Go to https://dashboard.render.com.

Click "New" → "Web Service".

"Build & deploy from a Git repository".

Connect your GitHub and select your repo.

Root directory:

If Dockerfile is at backend/Dockerfile, set:

Root directory: backend

Environment:

Runtime: Docker.

Build command: leave default (Render uses Dockerfile).

Start command: uvicorn main:app --host 0.0.0.0 --port $PORT (or leave empty if in Dockerfile/CMD).

Set environment variables (see section below).

Click "Create Web Service" to deploy.

Optional: Render CLI:

```bash
npm i -g @render/cli
render login
cd backend
render init
render up
```
Environment variables in Render:

In Render Dashboard → your service → Environment:

```bash
DATABASE_URL=postgresql://user:pass@ep-xyz.us-east-2.aws.neon.tech/dbname?sslmode=require
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080
CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000
PORT=8000
```
Health Check endpoint:

```python
# backend/main.py
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
```
Render health check path:

Set to /health in service settings.

After first successful deploy, you'll get a backend URL like:
https://hackathon-todo-backend.onrender.com

Use this in frontend NEXT_PUBLIC_API_URL.

DATABASE SETUP (Neon)

Prerequisites:

Neon account (free tier: 3GB storage)

Create Neon project:

Go to https://neon.tech

Click "Create Project"

Name: hackathon-todo

Region: closest to Render region

PostgreSQL version: 16

Get connection string:

Copy connection string from Neon dashboard.

Example:
postgresql://user:pass@ep-xyz.us-east-2.aws.neon.tech/dbname?sslmode=require

Add to backend environment:

```bash
DATABASE_URL=postgresql://user:pass@ep-xyz.us-east-2.aws.neon.tech/dbname?sslmode=require
```
Run migrations:

```bash
# Locally first
cd backend
alembic upgrade head
```
For production, you can:

Run migrations on startup, or

Trigger an ad-hoc migration job after each deploy.

Enable Neon features:

Connection pooling: enable pgBouncer.

Autosuspend: enable (e.g., 5 mins inactivity).

Backups: confirm daily automatic backups.

ENVIRONMENT VARIABLES SUMMARY

Frontend (frontend/.env.local):

```bash
# API
NEXT_PUBLIC_API_URL=https://hackathon-todo-backend.onrender.com

# Authentication
BETTER_AUTH_SECRET=generate-32-char-secret
BETTER_AUTH_URL=https://your-app.vercel.app

# Optional
NEXT_PUBLIC_APP_NAME=Todo App
NEXT_PUBLIC_APP_VERSION=1.0.0
```
Backend (backend/.env for local dev):

```bash
# Database
DATABASE_URL=postgresql://user:pass@host/db

# JWT
JWT_SECRET_KEY=same-as-better-auth-secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080

# CORS
CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000

# Server
PORT=8000
```
Generating secrets:

```bash
# Generate secure secret (32 characters)
openssl rand -hex 32

# Or in Python
python -c "import secrets; print(secrets.token_hex(32))"
```
CUSTOM DOMAIN (Optional)

Vercel:

Go to Project Settings → Domains.

Add your domain.

Update DNS records at your registrar.

Wait for automatic SSL.

Render:

Go to your backend service → "Custom Domains".

Add your custom domain.

Follow Render instructions to add CNAME in your DNS.

SSL certificate is issued automatically.

MONITORING & LOGS

Vercel logs:

```bash
# View logs
vercel logs

# Stream logs
vercel logs --follow
```
Render logs:

View in Render Dashboard → Logs tab.

Or use CLI:

```bash
render logs <service-name>
```
Neon monitoring:

View query statistics in Neon dashboard.

Check connection pool metrics.

Monitor storage usage.

## Response snapshot

Created feature branch `011-phase2-deploy` with comprehensive deployment specification covering:
- 6 prioritized user stories (P1-P3) for frontend, backend, database, env vars, monitoring, custom domain
- 12 functional requirements for deployment and operations
- 10 measurable success criteria (technology-agnostic)
- Clear assumptions, dependencies, and out-of-scope items
- Edge cases for error handling
- Quality checklist validated with all items passing

## Outcome

- ✅ Impact: Defined deployment specification for Phase II covering Vercel frontend, Render backend, and Neon database
- 🧪 Tests: N/A (specification phase)
- 📁 Files: specs/011-phase2-deploy/spec.md, specs/011-phase2-deploy/checklists/requirements.md
- 🔁 Next prompts: `/sp.plan` for architecture decisions
- 🧠 Reflection: Specification is complete with no clarification needed. All requirements are testable and success criteria are measurable.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS): All quality checklist items passed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
