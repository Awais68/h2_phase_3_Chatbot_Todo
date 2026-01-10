# Frontend Deployment Guide - Vercel

This guide walks through deploying the MissionImpossible frontend to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Backend API**: The backend should be deployed and accessible (see `backend/RENDER_DEPLOYMENT.md`)

## Deployment Steps

### 1. Connect GitHub Repository

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Project"
3. Select your GitHub repository
4. Vercel will automatically detect Next.js

### 2. Configure Project Settings

#### Root Directory
Set the root directory to: `frontend`

#### Framework Preset
- Framework: **Next.js**
- Build Command: `npm run build`
- Output Directory: `.next`
- Install Command: `npm install`

### 3. Environment Variables

Add the following environment variables in Vercel dashboard:

```bash
# Backend API URL (from your Render deployment)
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com

# Frontend App URL (will be your Vercel URL)
NEXT_PUBLIC_APP_URL=https://your-project.vercel.app

# Application Name
NEXT_PUBLIC_APP_NAME=MissionImpossible

# Feature Flags
NEXT_PUBLIC_ENABLE_VOICE_COMMANDS=true
NEXT_PUBLIC_ENABLE_MULTI_LANGUAGE=true
```

**Note**: After first deployment, update `NEXT_PUBLIC_APP_URL` with your actual Vercel URL.

### 4. Deploy

1. Click **"Deploy"**
2. Wait for the build to complete (usually 2-5 minutes)
3. Vercel will provide you with a deployment URL

### 5. Post-Deployment Configuration

#### Update Backend CORS Settings

After deployment, you need to update your backend's CORS configuration:

1. Go to your Render dashboard
2. Navigate to your backend service
3. Add an environment variable:
   ```bash
   FRONTEND_URL=https://your-project.vercel.app
   ```
4. Redeploy the backend service

#### Update Frontend Environment Variable

1. In Vercel dashboard, update `NEXT_PUBLIC_APP_URL` with your actual deployment URL
2. Trigger a new deployment

### 6. Custom Domain (Optional)

1. Go to your project settings in Vercel
2. Navigate to "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions
5. Update both `NEXT_PUBLIC_APP_URL` and backend `FRONTEND_URL` with your custom domain

## Vercel Configuration

The project includes a `vercel.json` file with optimized settings:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["iad1"],
  "env": {
    "NEXT_PUBLIC_API_URL": "@api-url",
    "NEXT_PUBLIC_APP_URL": "@app-url"
  }
}
```

## Features Enabled

✅ **Progressive Web App (PWA)**
- Offline support
- Install prompt
- Service worker caching

✅ **Multi-Language Support**
- English and Urdu
- RTL layout for Urdu
- Language detection and persistence

✅ **Voice Commands**
- Speech recognition
- Voice navigation
- Hands-free operation

✅ **Responsive Design**
- Mobile-first approach
- Touch gestures
- Adaptive layouts

## Testing the Deployment

After deployment, test these critical features:

1. **Homepage Load**: Visit your Vercel URL
2. **Authentication**: Test login/register flows
3. **API Connection**: Verify tasks load from backend
4. **Language Switch**: Test English ↔ Urdu switching
5. **Voice Commands**: Test microphone permissions and recognition
6. **PWA Install**: Test "Add to Home Screen" on mobile
7. **Offline Mode**: Disable network and verify cached content works

## Monitoring

### Vercel Analytics
1. Enable Vercel Analytics in project settings
2. Monitor performance metrics
3. Track Core Web Vitals

### Error Tracking
Check Vercel deployment logs for errors:
```bash
vercel logs <deployment-url>
```

## Troubleshooting

### Build Failures

**Issue**: TypeScript errors during build
```bash
# Solution: Run type-check locally
npm run type-check
```

**Issue**: Missing dependencies
```bash
# Solution: Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Runtime Errors

**Issue**: API connection fails (CORS errors)
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend `FRONTEND_URL` matches your Vercel URL
- Ensure backend CORS middleware is configured correctly

**Issue**: Environment variables not loading
- Verify variables are set in Vercel dashboard
- Redeploy after adding variables
- Check variable names have `NEXT_PUBLIC_` prefix for client-side access

**Issue**: Language detection not working
- Clear browser cache and localStorage
- Check translation files are included in build
- Verify i18n configuration

### Performance Issues

**Issue**: Slow initial load
- Enable Vercel Edge Network
- Check image optimization settings
- Review bundle size: `npm run build` shows bundle analysis

**Issue**: PWA not caching properly
- Check service worker registration
- Verify `next-pwa` configuration
- Clear service worker cache and re-register

## Deployment Checklist

- [ ] Backend deployed and accessible
- [ ] Environment variables configured in Vercel
- [ ] CORS configured on backend
- [ ] First deployment successful
- [ ] NEXT_PUBLIC_APP_URL updated with actual URL
- [ ] Backend FRONTEND_URL updated
- [ ] Authentication tested
- [ ] API connection verified
- [ ] Language switching tested
- [ ] Voice commands tested
- [ ] PWA installation tested
- [ ] Mobile responsiveness verified
- [ ] Custom domain configured (if applicable)
- [ ] Analytics enabled

## Continuous Deployment

Vercel automatically deploys:
- **Production**: Commits to `main` branch
- **Preview**: Pull requests and other branches

Each deployment gets a unique URL for testing.

## Rollback

If issues occur:
1. Go to Vercel dashboard
2. Navigate to "Deployments"
3. Find a previous working deployment
4. Click "Promote to Production"

## Support Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [Vercel Support](https://vercel.com/support)

## Notes

- **Build Time**: ~2-5 minutes
- **Region**: Defaults to US East (iad1)
- **SSL**: Automatic HTTPS
- **Edge Network**: Global CDN included
- **Serverless**: Functions automatically deployed

