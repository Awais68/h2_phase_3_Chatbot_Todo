# Render Backend Deployment Guide

This document provides step-by-step instructions for deploying the FastAPI backend to Render.

## Prerequisites

- GitHub account with repository access
- Render account (free tier is sufficient)
- Neon PostgreSQL database (created in Phase 2)

## Deployment Steps

### Step 1: Connect Repository to Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** and select **Web Service**
3. Under "GitHub", select your repository: `Awais68/hackathon-2-phase-ii-full-stack-web-app`
4. Select the branch: `011-phase2-deploy`
5. Render will auto-detect the `backend/render.yaml` configuration

### Step 2: Configure Service Settings

Render will pre-fill from `render.yaml`. Verify:

| Setting | Value |
|---------|-------|
| Name | `todo-backend` |
| Environment | `Docker` |
| Region | `Oregon (US West)` or closest to your users |
| Branch | `011-phase2-deploy` |
| Dockerfile Path | `backend/Dockerfile` |
| Health Check Path | `/health` |
| Plan | `Free` |

### Step 3: Configure Environment Variables

In the Environment Variables section, add the following:

**Critical Secrets (generate secure values):**

```bash
# Generate SECRET_KEY:
openssl rand -hex 32

# Or use Python:
python -c "import secrets; print(secrets.token_hex(32))"
```

**Environment Variables to Add:**

| Key | Value | Source |
|-----|-------|--------|
| `DATABASE_URL` | `postgres://user:password@ep-xxx.us-east-1.aws.neon.tech/neon?sslmode=require` | From Neon Console |
| `SECRET_KEY` | `(generated secure string)` | Generate with `openssl rand -hex 32` |
| `ALGORITHM` | `HS256` | Fixed value |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Fixed value |
| `CORS_ORIGINS` | `https://*.vercel.app,http://localhost:3000` | Adjust for your frontend |
| `LOG_LEVEL` | `INFO` | Options: DEBUG, INFO, WARNING, ERROR |
| `ENVIRONMENT` | `production` | Optional: set for production mode |

### Step 4: Connect Neon Database

**Option A: Use render.yaml database (Recommended)**

The `render.yaml` includes a database definition. Render will prompt to create it.

**Option B: Manual Connection**

1. In Render Dashboard, go to **Databases** → **New Database**
2. Select `todo-db` as the name
3. Choose **Free** plan
4. Once created, go to your web service → **Environment**
5. Add database connection:
   - Key: `DATABASE_URL`
   - Value: Click the "From Database" button and select `todo-db`

### Step 5: Deploy

1. Click **Create Web Service**
2. Render will:
   - Clone the repository
   - Build the Docker image (multi-stage build)
   - Start the container
   - Run health check at `/health`

**Expected Build Time:** 3-5 minutes on first deploy

### Step 6: Verify Deployment

Once deployment completes:

1. **Check Logs:** Dashboard → Logs tab
2. **Health Check:** Visit `https://todo-backend.onrender.com/health`
3. **API Docs:** Visit `https://todo-backend.onrender.com/docs`

### Step 7: Test Endpoints

```bash
# Health check
curl https://todo-backend.onrender.com/health

# Root endpoint
curl https://todo-backend.onrender.com/

# API documentation (in browser)
open https://todo-backend.onrender.com/docs
```

**Expected Health Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-02T12:00:00.000000",
  "version": "1.0.0",
  "environment": "production"
}
```

## Troubleshooting

### Build Fails

1. Check build logs in Render dashboard
2. Common issues:
   - Missing `pyproject.toml` in backend directory
   - Python version mismatch (Dockerfile uses 3.12)
   - Dependencies not in `pyproject.toml`

### Health Check Fails

1. Verify `/health` endpoint is implemented in `main.py`
2. Check container logs for startup errors
3. Ensure `PORT` environment variable is used (Render sets this)

### Database Connection Fails

1. Verify `DATABASE_URL` is correct and includes `?sslmode=require`
2. Check Neon firewall allows Render IPs
3. Verify database is in the same region as the web service

### CORS Errors

1. Verify `CORS_ORIGINS` includes your frontend URL
2. Check browser console for specific CORS errors
3. Ensure trailing slashes are consistent

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Neon PostgreSQL connection string |
| `SECRET_KEY` | Yes | JWT signing secret (generate with `openssl rand -hex 32`) |
| `ALGORITHM` | Yes | JWT algorithm (HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Yes | Token expiry time |
| `CORS_ORIGINS` | Yes | Comma-separated list of allowed origins |
| `LOG_LEVEL` | No | Logging level (default: INFO) |
| `ENVIRONMENT` | No | Environment name (development/production) |

## Rollback Procedure

1. Go to Render Dashboard → Your Service → **Deployments**
2. Select a previous successful deployment
3. Click **Redeploy** to roll back

## Scaling (Future)

- **Free Tier:** 1 instance, 750 hours/month
- **Paid Tier:** Auto-scaling, more hours, custom domains

## Next Steps

After successful backend deployment:

1. **Phase 4:** Deploy frontend to Vercel
2. **Set NEXT_PUBLIC_API_URL** in Vercel to your Render URL
3. **Test full-stack integration**
