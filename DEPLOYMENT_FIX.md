# Deployment Fix Guide - User Signup Issue

## Problem
Deployed frontend on Vercel cannot signup users because:
1. SQLite database doesn't work on Vercel (serverless)
2. Missing PostgreSQL connection for better-auth
3. CORS configuration needed

## Solution

### 1. Vercel Environment Variables

Go to your Vercel project settings → Environment Variables and add:

```bash
# Backend API URL (your Render backend)
NEXT_PUBLIC_API_URL=https://hackathon-2-phase-ii-full-stack-web-app-1.onrender.com

# Frontend URL (your Vercel deployment URL)
NEXT_PUBLIC_APP_URL=https://hackathon-2-phase-ii-full-stack-web-app.vercel.app

# PostgreSQL Database for better-auth (use Neon or Vercel Postgres)
DATABASE_URL=postgresql://username:password@host/database?sslmode=require

# Better Auth Secret (generate a random string)
BETTER_AUTH_SECRET=YOUR_SECRET_KEY_HERE
```

### 2. Get Neon PostgreSQL Database URL

**Option A: Create New Neon Database for Frontend Auth**

1. Go to https://console.neon.tech/
2. Create a new project called "todo-app-frontend-auth"
3. Copy the connection string
4. Add it to Vercel as `DATABASE_URL`

**Option B: Use Same Backend Neon Database**

You can use the same Neon database for both backend tasks and frontend auth.
Just add the same `DATABASE_URL` to Vercel.

### 3. Run Prisma Migration on Vercel

After adding DATABASE_URL to Vercel:

1. Go to Vercel Dashboard → Your Project
2. Settings → General → Build & Development Settings
3. Add to Build Command:
   ```bash
   npx prisma generate && npx prisma db push && npm run build
   ```

OR manually run on your local machine connected to the same database:

```bash
cd frontend
DATABASE_URL="postgresql://..." npx prisma db push
```

### 4. Backend CORS Update

Your backend already has `allow_origins=["*"]` which is fine for now.

For production, update `backend/main.py` to include your Vercel URL explicitly:

```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3005",
    "https://hackathon-2-phase-ii-full-stack-web-app.vercel.app",
    # ... existing origins
]
```

### 5. Redeploy

1. Commit and push the changes:
   ```bash
   git add .
   git commit -m "Fix: Update auth config for Vercel deployment with PostgreSQL"
   git push origin main
   ```

2. Vercel will automatically redeploy

3. Test signup on your Vercel URL

## Verification Checklist

- [ ] `DATABASE_URL` added to Vercel (PostgreSQL)
- [ ] `BETTER_AUTH_SECRET` added to Vercel
- [ ] `NEXT_PUBLIC_API_URL` points to Render backend
- [ ] `NEXT_PUBLIC_APP_URL` matches Vercel deployment URL
- [ ] Prisma schema uses `provider = "postgresql"`
- [ ] Build command includes `npx prisma generate`
- [ ] Redeployed on Vercel
- [ ] Signup works on deployed URL

## Quick Test

After deployment, open browser console on your Vercel URL and check:

1. Network tab → Any 401/403 errors?
2. Console → Any CORS errors?
3. Try signup → Does it create user?

## Troubleshooting

### "Cannot connect to database"
- Verify DATABASE_URL format includes `?sslmode=require`
- Check Neon database is accessible (not sleeping)

### "CORS error"
- Check backend logs on Render
- Verify `allow_origins=["*"]` in backend CORS middleware

### "Build failed"
- Check Vercel build logs
- Ensure `npx prisma generate` runs before build

## Alternative: Use Vercel Postgres

Instead of Neon, you can use Vercel's built-in Postgres:

1. Vercel Dashboard → Storage → Create Database → Postgres
2. Connect to your project
3. Vercel will automatically add `DATABASE_URL` environment variable
4. Redeploy

This is the easiest option for Vercel deployments!
