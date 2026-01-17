# Environment Setup Guide

## Overview

This guide explains how to configure environment variables for both backend and frontend applications.

## Backend Environment Variables

### Location
Create a `.env` file in the `backend/` directory.

### Required Variables

```bash
# Copy the example file
cp backend/.env.example backend/.env
```

#### 1. Database Configuration

```bash
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
```

**Neon PostgreSQL Format**:
```bash
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
```

**How to get**:
1. Log in to Neon Console (https://console.neon.tech)
2. Select your project
3. Go to "Connection Details"
4. Copy the connection string
5. Paste into `.env` file

#### 2. OpenAI API Key

```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**How to get**:
1. Log in to OpenAI Platform (https://platform.openai.com)
2. Go to "API Keys" section
3. Click "Create new secret key"
4. Copy the key (you won't see it again!)
5. Paste into `.env` file

**Important**: Never commit this key to version control!

#### 3. Server Configuration

```bash
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

- `HOST`: Server bind address (0.0.0.0 for all interfaces)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Enable debug mode (True for development, False for production)

#### 4. CORS Configuration

```bash
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

- Add all frontend URLs that need to access the API
- Separate multiple origins with commas
- No spaces between URLs

#### 5. Logging

```bash
LOG_LEVEL=INFO
```

Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

### Optional Variables (Future)

```bash
# Better Auth (when implemented)
AUTH_SECRET=your-auth-secret-here
AUTH_URL=http://localhost:8000
```

---

## Frontend Environment Variables

### Location
Create a `.env.local` file in the `frontend/` directory.

### Required Variables

```bash
# Copy the example file
cp frontend/.env.local.example frontend/.env.local
```

#### 1. Backend API URL

```bash
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

- Points to your FastAPI backend
- Must include protocol (http:// or https://)
- No trailing slash

**Production**: Update to your deployed backend URL:
```bash
NEXT_PUBLIC_BACKEND_URL=https://api.yourdomain.com
```

#### 2. User Configuration (Development Only)

```bash
NEXT_PUBLIC_USER_ID=1
```

- Temporary user ID for development
- **TODO**: Replace with Better Auth integration
- Will be removed when authentication is implemented

#### 3. Feature Flags

```bash
NEXT_PUBLIC_ENABLE_VOICE=true
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_RECURRING=true
```

- Enable/disable features without code changes
- Set to `false` to disable a feature
- Useful for testing and gradual rollout

#### 4. Analytics Configuration

```bash
NEXT_PUBLIC_ANALYTICS_DEFAULT_DAYS=30
```

- Default number of days for timeline analytics
- Used in "Tasks Over Time" chart
- Can be overridden by user in UI

#### 5. Voice Configuration

```bash
NEXT_PUBLIC_VOICE_LANG=en-US
NEXT_PUBLIC_VOICE_AUTO_SPEAK=true
```

- `NEXT_PUBLIC_VOICE_LANG`: Language for speech recognition/synthesis
  - Options: `en-US`, `en-GB`, `es-ES`, `fr-FR`, etc.
- `NEXT_PUBLIC_VOICE_AUTO_SPEAK`: Auto-speak assistant responses
  - Set to `false` to disable auto-speak

### Optional Variables (Future)

```bash
# OpenAI ChatKit (if using ChatKit instead of custom chat)
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-chatkit-domain-key-here
```

---

## Environment Variable Naming Conventions

### Backend (Python/FastAPI)
- Use UPPERCASE_WITH_UNDERSCORES
- No prefix needed
- Example: `DATABASE_URL`, `OPENAI_API_KEY`

### Frontend (Next.js)
- Use `NEXT_PUBLIC_` prefix for client-side variables
- Use UPPERCASE_WITH_UNDERSCORES
- Example: `NEXT_PUBLIC_BACKEND_URL`

**Important**: Only variables with `NEXT_PUBLIC_` prefix are exposed to the browser!

---

## Security Best Practices

### 1. Never Commit Secrets

Add to `.gitignore`:
```
.env
.env.local
.env.*.local
```

### 2. Use Different Keys for Environments

- **Development**: Use test API keys
- **Staging**: Use staging API keys
- **Production**: Use production API keys

### 3. Rotate Keys Regularly

- Change API keys every 90 days
- Immediately rotate if compromised
- Use key management services for production

### 4. Validate Environment Variables

Backend validation (add to `src/config.py`):
```python
import os
from typing import Optional

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    def __init__(self):
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is required")
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")

settings = Settings()
```

---

## Verification

### Backend Verification

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -c "import os; print('DATABASE_URL:', os.getenv('DATABASE_URL')[:20] + '...')"
python -c "import os; print('OPENAI_API_KEY:', 'sk-' in os.getenv('OPENAI_API_KEY', ''))"
```

Expected output:
```
DATABASE_URL: postgresql://user:pa...
OPENAI_API_KEY: True
```

### Frontend Verification

```bash
cd frontend
npm run dev
```

Open browser console and check:
```javascript
console.log('Backend URL:', process.env.NEXT_PUBLIC_BACKEND_URL);
console.log('User ID:', process.env.NEXT_PUBLIC_USER_ID);
```

---

## Troubleshooting

### Issue: "DATABASE_URL not found"

**Solution**:
1. Verify `.env` file exists in `backend/` directory
2. Check file name is exactly `.env` (not `.env.txt`)
3. Restart the backend server after creating `.env`

### Issue: "OPENAI_API_KEY invalid"

**Solution**:
1. Verify key starts with `sk-`
2. Check for extra spaces or newlines
3. Regenerate key from OpenAI Platform
4. Ensure key has not expired

### Issue: "CORS error in browser"

**Solution**:
1. Add frontend URL to `CORS_ORIGINS` in backend `.env`
2. Restart backend server
3. Clear browser cache
4. Check browser console for exact error

### Issue: "Frontend can't connect to backend"

**Solution**:
1. Verify `NEXT_PUBLIC_BACKEND_URL` is correct
2. Ensure backend is running (`uvicorn src.main:app --reload`)
3. Test backend directly: `curl http://localhost:8000/docs`
4. Check for firewall blocking port 8000

### Issue: "Voice features not working"

**Solution**:
1. Check browser compatibility (Chrome/Edge recommended)
2. Grant microphone permissions
3. Verify `NEXT_PUBLIC_ENABLE_VOICE=true`
4. Test in HTTPS environment (required for some browsers)

---

## Production Deployment

### Backend (Render/Railway/Fly.io)

1. Set environment variables in platform dashboard
2. Use production database URL
3. Set `DEBUG=False`
4. Add production frontend URL to `CORS_ORIGINS`

### Frontend (Vercel/Netlify)

1. Set environment variables in platform dashboard
2. Update `NEXT_PUBLIC_BACKEND_URL` to production backend
3. Remove or update `NEXT_PUBLIC_USER_ID` (use auth instead)
4. Verify all `NEXT_PUBLIC_` variables are set

---

## Environment Variable Checklist

### Backend Setup
- [ ] `.env` file created in `backend/` directory
- [ ] `DATABASE_URL` configured with Neon PostgreSQL connection string
- [ ] `OPENAI_API_KEY` configured with valid API key
- [ ] `CORS_ORIGINS` includes frontend URL
- [ ] Backend starts without errors
- [ ] Database connection successful

### Frontend Setup
- [ ] `.env.local` file created in `frontend/` directory
- [ ] `NEXT_PUBLIC_BACKEND_URL` points to backend
- [ ] `NEXT_PUBLIC_USER_ID` set for development
- [ ] Feature flags configured
- [ ] Frontend starts without errors
- [ ] Can connect to backend API

### Security
- [ ] `.env` and `.env.local` added to `.gitignore`
- [ ] No secrets committed to version control
- [ ] Different keys for dev/staging/production
- [ ] API keys validated and working

---

**Last Updated**: 2026-01-10
**Version**: 1.0
**Status**: Production Ready
