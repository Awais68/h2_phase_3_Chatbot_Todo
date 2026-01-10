# 404 Error Fix - Vercel Signup Issue

## Problem
When trying to signup on deployed Vercel frontend, getting **404 error**.

## Root Cause
Better-auth requires a DATABASE_URL to initialize. Without it:
- Auth API routes (`/api/auth/*`) return 404
- Signup/Login don't work
- Local works because you have `DATABASE_URL` in `.env.local`

## Solution - Add Environment Variables to Vercel

### Step 1: Get PostgreSQL Database URL

**Option A: Use Vercel Postgres (Recommended - Easiest!)**

1. Go to your Vercel project dashboard
2. Click **"Storage"** tab
3. Click **"Create Database"**
4. Select **"Postgres"**
5. Click **"Continue"**
6. Connect to your project
7. **Done!** DATABASE_URL is automatically added ✅

**Option B: Use Neon PostgreSQL**

1. Go to https://console.neon.tech/
2. Create a new project (or use existing)
3. Copy the connection string (looks like):
   ```
   postgresql://username:password@ep-xxx.neon.tech/neondb?sslmode=require
   ```

### Step 2: Add Environment Variables to Vercel

Go to: **Vercel Dashboard → Your Project → Settings → Environment Variables**

Add these variables:

```bash
# 1. Database URL (from Step 1)
DATABASE_URL=postgresql://username:password@host/database?sslmode=require

# 2. Auth Secret (use the same one from your local .env.local)
BETTER_AUTH_SECRET=Ikns5R4zC2bdlj+83nblBOMlL+jKa9wXdVkfviQDRuQ=

# 3. Backend API URL (your Render backend)
NEXT_PUBLIC_API_URL=https://hackathon-2-phase-ii-full-stack-web-app-1.onrender.com

# 4. Frontend URL (your Vercel deployment URL)
NEXT_PUBLIC_APP_URL=https://hackathon-2-phase-ii-full-stack-web-app.vercel.app
```

**Important**: Make sure to select **"Production"**, **"Preview"**, and **"Development"** for each variable.

### Step 3: Update Build Command

In Vercel Dashboard:
- Go to **Settings → General → Build & Development Settings**
- Change **Build Command** to:
  ```bash
  npx prisma generate && npx prisma db push && npm run build
  ```

This ensures:
- Prisma client is generated
- Database tables are created
- Build succeeds

### Step 4: Redeploy

1. Go to **Deployments** tab
2. Click the **"•••"** menu on latest deployment
3. Click **"Redeploy"**
4. Wait for build to complete

### Step 5: Test

1. Open your Vercel URL
2. Go to `/api/health` to check environment:
   ```
   https://your-project.vercel.app/api/health
   ```
   Should show:
   ```json
   {
     "status": "ok",
     "env": {
       "hasDatabase": true,
       "databaseType": "postgresql",
       "hasAuthSecret": true,
       ...
     }
   }
   ```

3. Try signup again - should work now! ✅

## Quick Verification Checklist

Before redeploying, verify in Vercel environment variables:

- [ ] `DATABASE_URL` is set (PostgreSQL connection string)
- [ ] `BETTER_AUTH_SECRET` is set
- [ ] `NEXT_PUBLIC_API_URL` points to Render backend
- [ ] `NEXT_PUBLIC_APP_URL` matches Vercel URL
- [ ] Build command includes `npx prisma generate && npx prisma db push`
- [ ] All variables applied to Production, Preview, Development

## If Still Getting 404

1. Check Vercel build logs for errors
2. Visit `/api/health` to verify environment variables
3. Check browser console for actual error message
4. Verify DATABASE_URL format is correct (must be PostgreSQL, not SQLite)

## Common Mistakes

❌ **Forgot to redeploy after adding variables**
→ Variables only apply to new deployments

❌ **DATABASE_URL is SQLite (file:...)**
→ Must be PostgreSQL for Vercel

❌ **Build command doesn't include prisma generate**
→ Prisma client won't be generated

❌ **DATABASE_URL has no SSL mode**
→ Add `?sslmode=require` at the end

## Why Local Works but Vercel Doesn't?

| Environment | Database | Why It Works |
|------------|----------|--------------|
| Local | SQLite (`file:./prisma/dev.db`) | File-based, stored locally ✅ |
| Vercel | None (if not configured) | Serverless - can't use file system ❌ |
| Vercel | PostgreSQL | Hosted database, accessible via URL ✅ |

---

**TL;DR**: Add `DATABASE_URL` (PostgreSQL) to Vercel environment variables, then redeploy.
