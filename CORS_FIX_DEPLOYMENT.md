# CORS Configuration Fix - Deployment Guide

## Changes Made

### 1. Backend CORS Enhancement (`backend/main.py`)

**Updated:**
- ✅ Added explicit CORS headers including `Accept`, `Origin`, etc.
- ✅ Added `max_age=3600` to cache preflight requests
- ✅ Added `HEAD` method support
- ✅ Added wildcard for Vercel preview URLs: `https://*.vercel.app`
- ✅ Exposed necessary response headers

**Configuration:**
```python
allow_origins=["*"]  # Allows all origins
allow_credentials=True
allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"]
max_age=3600  # Cache preflight for 1 hour
```

### 2. Frontend API Client Enhancement (`frontend/src/lib/api.ts`)

**Updated:**
- ✅ Added `mode: 'cors'` to explicitly enable CORS
- ✅ Set `credentials: 'omit'` (no cookies needed for Render API)
- ✅ Added `Accept: application/json` header

### 3. Next.js CORS Headers (`frontend/next.config.mjs`)

**Added:**
- ✅ CORS headers for all `/api/*` routes
- ✅ Allows cross-origin requests to Next.js API routes

## For Render Backend Deployment

### Option 1: Current Configuration (Already Applied ✅)
Your backend already has `allow_origins=["*"]` which allows all origins.

### Option 2: Restrict to Specific Origins (More Secure)

If you want to restrict CORS to only your Vercel frontend:

1. Go to Render Dashboard → Your Backend Service
2. Add Environment Variable:
   ```
   CORS_ORIGINS=https://hackathon-2-phase-ii-full-stack-web-app.vercel.app
   ```
3. The backend will automatically add this to allowed origins

## For Vercel Frontend Deployment

### Required Environment Variables

Make sure these are set in Vercel:

```bash
NEXT_PUBLIC_API_URL=https://hackathon-2-phase-ii-full-stack-web-app-1.onrender.com
NEXT_PUBLIC_APP_URL=https://hackathon-2-phase-ii-full-stack-web-app.vercel.app
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=Ikns5R4zC2bdlj+83nblBOMlL+jKa9wXdVkfviQDRuQ=
```

## Testing CORS

### 1. Test Backend CORS

Open browser console on Vercel deployment and run:

```javascript
fetch('https://hackathon-2-phase-ii-full-stack-web-app-1.onrender.com/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

Should return health check data without CORS error.

### 2. Test API Call

```javascript
fetch('https://hackathon-2-phase-ii-full-stack-web-app-1.onrender.com/tasks/')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

Should work without CORS errors.

### 3. Check Network Tab

1. Open DevTools → Network tab
2. Reload page
3. Look for API calls to Render backend
4. Check Response Headers should include:
   - `Access-Control-Allow-Origin: *`
   - `Access-Control-Allow-Methods: ...`

## Common CORS Issues & Solutions

### Issue: "No 'Access-Control-Allow-Origin' header"

**Solution:**
- Backend `allow_origins=["*"]` is set ✅
- Render backend needs to be redeployed after changes

### Issue: "CORS preflight request failed"

**Solution:**
- Backend now includes OPTIONS method ✅
- `max_age=3600` caches preflight requests ✅

### Issue: "Credentials mode is 'include'"

**Solution:**
- Frontend now uses `credentials: 'omit'` ✅
- No cookies needed for API calls

## Deployment Checklist

### Backend (Render)
- [x] CORS middleware configured with `allow_origins=["*"]`
- [x] All HTTP methods allowed including OPTIONS
- [x] Preflight caching enabled
- [ ] Redeploy backend if needed

### Frontend (Vercel)
- [x] `NEXT_PUBLIC_API_URL` points to Render backend
- [x] API client uses `mode: 'cors'`
- [x] Next.js config has CORS headers for `/api/*`
- [ ] Redeploy frontend
- [ ] Test API calls from Vercel deployment

## Redeploy Instructions

### 1. Commit Changes
```bash
git add .
git commit -m "Fix: Enhanced CORS configuration for deployment"
git push origin main
```

### 2. Render Backend
- Should auto-deploy from GitHub
- Or manually redeploy from Render dashboard

### 3. Vercel Frontend
- Should auto-deploy from GitHub
- Or manually redeploy from Vercel dashboard

### 4. Verify
- Visit Vercel URL
- Open DevTools → Console
- Check for CORS errors (should be none)
- Try creating a task
- Check Network tab for successful API calls

## Quick Verification

Run this in browser console on your Vercel deployment:

```javascript
// Test 1: Health Check
fetch('https://hackathon-2-phase-ii-full-stack-web-app-1.onrender.com/health', {
  mode: 'cors'
}).then(r => r.json()).then(d => console.log('✅ Health:', d))

// Test 2: Tasks List
fetch('https://hackathon-2-phase-ii-full-stack-web-app-1.onrender.com/tasks/', {
  mode: 'cors'
}).then(r => r.json()).then(d => console.log('✅ Tasks:', d))
```

Both should succeed without CORS errors.

## Summary

**Changes Applied:**
1. ✅ Backend: Enhanced CORS with all headers, methods, and Vercel wildcard
2. ✅ Frontend: Explicit CORS mode and proper headers
3. ✅ Next.js: CORS headers for API routes

**Current Status:**
- Backend CORS: `allow_origins=["*"]` ✅ (Most permissive)
- Frontend API: Properly configured for CORS ✅
- Ready for deployment ✅

**Next Steps:**
1. Push changes to GitHub
2. Wait for auto-deployment (Render + Vercel)
3. Test on deployed URLs
4. Should work smoothly! 🚀
