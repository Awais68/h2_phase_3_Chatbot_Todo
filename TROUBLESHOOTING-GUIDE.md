# Todo Evolution - Troubleshooting Guide

**Project**: Todo Evolution - Multi-Phase Progressive Application
**Version**: 1.0.0
**Last Updated**: December 26, 2025

---

## Table of Contents

1. [Phase 1: CLI Issues](#phase-1-cli-issues)
2. [Phase 2: Backend API Issues](#phase-2-backend-api-issues)
3. [Phase 3: Frontend PWA Issues](#phase-3-frontend-pwa-issues)
4. [Phase 4: Voice Interface Issues](#phase-4-voice-interface-issues)
5. [Phase 5: AI Optimization Issues](#phase-5-ai-optimization-issues)
6. [Phase 6: Kubernetes Deployment Issues](#phase-6-kubernetes-deployment-issues)
7. [Common Issues Across All Phases](#common-issues-across-all-phases)

---

## Phase 1: CLI Issues

### Issue: CLI Won't Start - Import Error

**Symptoms**:
```
ModuleNotFoundError: No module named 'rich'
```

**Cause**: Dependencies not installed

**Solution**:
```bash
# Install dependencies
uv sync

# Or with pip
pip install -r requirements.txt

# Verify installation
python -c "import rich; print('Rich installed')"
```

---

### Issue: ASCII Art Not Displaying

**Symptoms**:
- Garbled characters instead of ASCII art
- Box-drawing characters appear as question marks

**Cause**: Terminal encoding not set to UTF-8

**Solution**:

**Linux/macOS**:
```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
python main.py
```

**Windows**:
```powershell
# PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
python main.py
```

**Alternative**: Use terminal that supports UTF-8 (iTerm2, Windows Terminal, GNOME Terminal)

---

### Issue: Colors Not Showing

**Symptoms**:
- Plain text without colors
- ANSI codes visible as raw text (e.g., `\033[32m`)

**Cause**: Terminal doesn't support 256 colors

**Solution**:
```bash
# Check terminal color support
echo $TERM

# Should be: xterm-256color or similar

# Set terminal to support colors
export TERM=xterm-256color
python main.py
```

Rich library handles graceful degradation automatically.

---

### Issue: Menu Options Not Working

**Symptoms**:
- Arrow keys don't navigate menu
- Only raw characters displayed

**Cause**: Questionary not compatible with terminal

**Solution**:
```bash
# Verify questionary installed
python -c "import questionary; print('Installed')"

# If issue persists, use numeric input mode
# (Already supported - just type numbers 1-6)
```

---

## Phase 2: Backend API Issues

### Issue: Backend Won't Start - Database Connection Error

**Symptoms**:
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Cause**: Database URL incorrect or database not accessible

**Solution**:

1. **Check DATABASE_URL in .env**:
```bash
# Correct format for Neon:
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require

# Correct format for local PostgreSQL:
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

2. **Test database connection**:
```bash
psql "postgresql://user:password@host:5432/dbname"
```

3. **Check firewall/network**:
- Ensure database port (5432) is accessible
- Check security groups (AWS) or firewall rules

---

### Issue: JWT Authentication Failing

**Symptoms**:
```json
{"detail": "Could not validate credentials"}
```

**Cause**: JWT_SECRET not set or token expired

**Solution**:

1. **Generate new JWT_SECRET**:
```bash
openssl rand -hex 32
```

2. **Update .env**:
```bash
JWT_SECRET=your-newly-generated-secret-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. **Restart backend**:
```bash
uv run uvicorn src.main:app --reload
```

4. **Get new token**:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

---

### Issue: CORS Errors

**Symptoms**:
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Cause**: Frontend origin not in CORS_ORIGINS

**Solution**:

1. **Update .env**:
```bash
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

2. **Restart backend**

3. **Verify CORS middleware**:
```bash
# Check backend logs on startup
# Should see: "CORS middleware configured with origins: ..."
```

---

### Issue: Slow API Response

**Symptoms**:
- API requests take >1 second
- Backend logs show slow database queries

**Cause**: Missing database indexes or N+1 queries

**Solution**:

1. **Check database indexes**:
```sql
-- Connect to database
psql $DATABASE_URL

-- Check indexes on tasks table
\d tasks

-- Create missing indexes if needed
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
```

2. **Enable query logging**:
```python
# backend/src/main.py
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

3. **Optimize queries**:
- Use eager loading: `.options(joinedload())`
- Add pagination: `.limit(50).offset(0)`
- Cache frequently accessed data (Redis)

---

## Phase 3: Frontend PWA Issues

### Issue: PWA Won't Install

**Symptoms**:
- No "Add to Home Screen" prompt
- Browser doesn't recognize PWA

**Cause**: PWA requirements not met

**Solution**:

1. **Verify HTTPS** (PWA requires HTTPS except localhost):
```bash
# Check URL scheme
echo $NEXT_PUBLIC_API_URL
# Should be https:// for production
```

2. **Check Service Worker registration**:
```javascript
// Open browser console
navigator.serviceWorker.getRegistrations().then(regs => console.log(regs))

// Should show registered service worker
```

3. **Validate manifest.json**:
```bash
# Open browser DevTools → Application → Manifest
# Check for errors
```

4. **Verify manifest fields**:
```json
{
  "name": "Todo Evolution",
  "short_name": "Todo",
  "start_url": "/",
  "display": "standalone",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

---

### Issue: Offline Mode Not Working

**Symptoms**:
- App shows blank page when offline
- Tasks don't save while offline

**Cause**: Service Worker not caching properly or IndexedDB error

**Solution**:

1. **Check Service Worker status**:
```javascript
// Browser console
navigator.serviceWorker.controller
// Should return ServiceWorker object
```

2. **Verify IndexedDB**:
```javascript
// Browser console
indexedDB.databases().then(dbs => console.log(dbs))
// Should show 'todo-app-db'
```

3. **Clear cache and re-register**:
```javascript
// Browser console
caches.keys().then(keys => Promise.all(keys.map(k => caches.delete(k))))
navigator.serviceWorker.getRegistrations().then(regs => regs.forEach(reg => reg.unregister()))
location.reload()
```

4. **Check Service Worker logs**:
```javascript
// In sw.js, add console.log statements
self.addEventListener('fetch', event => {
  console.log('Fetching:', event.request.url);
});
```

---

### Issue: Swipe Gestures Not Working

**Symptoms**:
- Swiping task cards does nothing
- No animation on swipe

**Cause**: Touch events not enabled or react-swipeable not configured

**Solution**:

1. **Verify react-swipeable installed**:
```bash
cd frontend
npm list react-swipeable
```

2. **Check touchscreen support**:
```javascript
// Browser console
'ontouchstart' in window
// Should return true on touch devices
```

3. **Test on real device** (not desktop emulator):
- Desktop Chrome DevTools touch emulation is limited
- Use actual phone or tablet for accurate testing

4. **Check swipe configuration**:
```tsx
<Swipeable
  onSwipedLeft={handleDelete}
  onSwipedRight={handleComplete}
  preventDefaultTouchmoveEvent
  trackMouse  // Enable for desktop testing
>
  {/* Task card content */}
</Swipeable>
```

---

### Issue: Push Notifications Not Working

**Symptoms**:
- Permission prompt doesn't appear
- Notifications not received

**Cause**: HTTPS required or permissions denied

**Solution**:

1. **Verify HTTPS** (required for push notifications):
```bash
# Check URL in browser address bar
# Must be https:// (or localhost)
```

2. **Check notification permission**:
```javascript
// Browser console
Notification.permission
// Should be "granted" or "default"
// If "denied", user must manually reset in browser settings
```

3. **Reset notification permission**:
- **Chrome**: Settings → Privacy → Site Settings → Notifications → Remove site
- **Firefox**: Address bar → ⓘ → Permissions → Receive Notifications → Reset
- **Safari**: Safari → Preferences → Websites → Notifications → Remove site

4. **Test notification API**:
```javascript
// Browser console
new Notification("Test", { body: "Testing notifications" })
// Should show notification if permission granted
```

---

## Phase 4: Voice Interface Issues

### Issue: Microphone Access Denied

**Symptoms**:
```
NotAllowedError: Permission denied
```

**Cause**: User denied microphone permission

**Solution**:

1. **Check permission status**:
```javascript
// Browser console
navigator.permissions.query({ name: 'microphone' }).then(result => console.log(result.state))
// Returns: "granted", "denied", or "prompt"
```

2. **Reset microphone permission**:
- **Chrome**: Settings → Privacy → Site Settings → Microphone → Remove site
- **Firefox**: Address bar → ⓘ → Permissions → Use the Microphone → Reset
- **Safari**: Safari → Preferences → Websites → Microphone → Remove site

3. **Grant permission**:
- Reload page
- Click voice button
- Allow microphone when prompted

---

### Issue: Voice Commands Not Recognized

**Symptoms**:
- Transcript shows gibberish
- Commands not parsed correctly

**Cause**: Low microphone quality or background noise

**Solution**:

1. **Test microphone**:
- Use system sound settings to test mic
- Ensure mic is not muted
- Check mic volume level (should be 70-90%)

2. **Reduce background noise**:
- Move to quieter location
- Close apps making noise
- Use headset microphone (better quality)

3. **Check language setting**:
```javascript
// Verify correct language
const recognition = new webkitSpeechRecognition();
console.log(recognition.lang);  // Should be 'en-US' or 'ur-PK'
```

4. **Speak clearly**:
- Moderate pace (not too fast)
- Clear pronunciation
- Pause between commands

5. **Check confidence score**:
- Low confidence (<0.7) indicates poor recognition
- App should show confidence score
- Try rephrasing command

---

### Issue: Urdu Commands Not Working

**Symptoms**:
- Urdu speech not recognized
- Transcript shows English instead

**Cause**: Browser doesn't support Urdu or language not set

**Solution**:

1. **Check browser support**:
```javascript
// Test Urdu support
const recognition = new webkitSpeechRecognition();
recognition.lang = 'ur-PK';
recognition.start();
// If error, browser doesn't support Urdu
```

2. **Use Azure Speech Services fallback**:
```bash
# Set in .env.local
NEXT_PUBLIC_AZURE_SPEECH_KEY=your-key
NEXT_PUBLIC_AZURE_SPEECH_REGION=your-region
```

3. **Switch browser**:
- Chrome: Good Urdu support
- Edge: Good Urdu support
- Firefox: Limited Urdu support
- Safari: Fair Urdu support

---

### Issue: Voice Feedback Not Speaking

**Symptoms**:
- No audio response after command
- SpeechSynthesis not working

**Cause**: Browser bug or voices not loaded

**Solution**:

1. **Check SpeechSynthesis support**:
```javascript
// Browser console
'speechSynthesis' in window
// Should return true
```

2. **Load voices**:
```javascript
// Voices load asynchronously
speechSynthesis.getVoices()
// Returns array of voices (may be empty initially)

// Wait for voices to load
speechSynthesis.onvoiceschanged = () => {
  console.log(speechSynthesis.getVoices());
};
```

3. **Test manual speech**:
```javascript
const utterance = new SpeechSynthesisUtterance("Test");
utterance.lang = 'en-US';
speechSynthesis.speak(utterance);
```

4. **Restart browser** (Firefox specific issue):
- SpeechSynthesis sometimes stops working
- Full browser restart fixes it

---

## Phase 5: AI Optimization Issues

### Issue: Task Optimizer Not Finding Duplicates

**Symptoms**:
- Obvious duplicates not detected
- Similarity score too low

**Cause**: Duplicate detection threshold too strict

**Solution**:

1. **Lower similarity threshold**:
```python
# In task optimizer code
SIMILARITY_THRESHOLD = 0.80  # Lower from 0.90 to 0.80
```

2. **Normalize task titles**:
- Remove punctuation
- Convert to lowercase
- Trim whitespace

3. **Use fuzzy matching**:
```python
from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()
```

---

### Issue: Priority Recommendations Incorrect

**Symptoms**:
- Low-priority tasks marked high
- Important tasks marked low

**Cause**: Keyword matching insufficient

**Solution**:

1. **Expand keyword lists**:
```python
HIGH_PRIORITY_KEYWORDS = ['urgent', 'critical', 'asap', 'emergency', 'production', 'bug', 'fix', 'broken']
LOW_PRIORITY_KEYWORDS = ['someday', 'maybe', 'eventually', 'cleanup', 'organize', 'sort']
```

2. **Add context analysis**:
- Check due dates
- Check user's historical priorities
- Use ML model for better prediction

---

## Phase 6: Kubernetes Deployment Issues

### Issue: Pods Stuck in Pending State

**Symptoms**:
```
NAME                         READY   STATUS    RESTARTS
todo-backend-xxx-yyy         0/1     Pending   0
```

**Cause**: Insufficient cluster resources

**Solution**:

1. **Check pod events**:
```bash
kubectl describe pod todo-backend-xxx-yyy -n todo-app
# Look for: "0/3 nodes are available: insufficient cpu"
```

2. **Check cluster resources**:
```bash
kubectl top nodes
kubectl describe nodes
```

3. **Reduce resource requests**:
```yaml
# values.yaml
resources:
  requests:
    memory: "128Mi"  # Reduce from 256Mi
    cpu: "50m"       # Reduce from 100m
```

4. **Scale up cluster** (if cloud):
```bash
# AWS EKS
eksctl scale nodegroup --cluster=my-cluster --nodes=3

# GCP GKE
gcloud container clusters resize my-cluster --num-nodes=3

# Azure AKS
az aks scale --resource-group myResourceGroup --name myAKSCluster --node-count 3
```

---

### Issue: Pods Crash Looping

**Symptoms**:
```
NAME                         READY   STATUS             RESTARTS
todo-backend-xxx-yyy         0/1     CrashLoopBackOff   5
```

**Cause**: Application startup error

**Solution**:

1. **Check pod logs**:
```bash
kubectl logs todo-backend-xxx-yyy -n todo-app
# Look for error messages
```

2. **Check previous logs** (if pod restarted):
```bash
kubectl logs todo-backend-xxx-yyy -n todo-app --previous
```

3. **Common causes**:
- **Missing environment variables**: Check ConfigMap and Secrets
- **Database connection failed**: Verify DATABASE_URL
- **Missing dependencies**: Check Docker image build
- **Port already in use**: Check containerPort configuration

4. **Exec into container** (if running):
```bash
kubectl exec -it todo-backend-xxx-yyy -n todo-app -- bash
# Debug inside container
```

---

### Issue: Service Not Accessible

**Symptoms**:
- `curl` to service fails
- Frontend can't reach backend

**Cause**: Service not properly exposed

**Solution**:

1. **Check service exists**:
```bash
kubectl get svc -n todo-app
```

2. **Check service endpoints**:
```bash
kubectl get endpoints todo-backend -n todo-app
# Should show pod IPs
```

3. **Test service from within cluster**:
```bash
kubectl run -it --rm debug --image=busybox --restart=Never -- \
  wget -O- http://todo-backend:8000/health
```

4. **Check service selector**:
```bash
kubectl describe svc todo-backend -n todo-app
# Selector should match pod labels
```

---

### Issue: Ingress Not Working

**Symptoms**:
- Domain not accessible
- 404 errors
- SSL certificate errors

**Cause**: Ingress misconfiguration

**Solution**:

1. **Check Ingress resource**:
```bash
kubectl get ingress -n todo-app
kubectl describe ingress todo-ingress -n todo-app
```

2. **Verify Ingress Controller running**:
```bash
kubectl get pods -n ingress-nginx
# Should see ingress-nginx-controller pod
```

3. **Check DNS resolution**:
```bash
nslookup todo.yourdomain.com
# Should resolve to LoadBalancer IP
```

4. **Verify TLS secret**:
```bash
kubectl get secret todo-tls-secret -n todo-app
# Should exist if TLS enabled
```

5. **Test without Ingress** (port-forward):
```bash
kubectl port-forward svc/todo-frontend 8080:80 -n todo-app
# Access at http://localhost:8080
```

---

### Issue: Kafka Events Not Flowing

**Symptoms**:
- Tasks created but no events in analytics
- Event logs show no messages

**Cause**: Kafka or Dapr misconfiguration

**Solution**:

1. **Check Kafka pods running**:
```bash
kubectl get pods -n todo-app | grep kafka
# Should see: kafka-0, kafka-1, kafka-2 all Running
```

2. **Check Kafka topics**:
```bash
kubectl exec -it kafka-0 -n todo-app -- \
  kafka-topics --bootstrap-server localhost:9092 --list

# Expected topics:
# task.created
# task.updated
# task.deleted
# task.completed
```

3. **Check Dapr sidecar**:
```bash
kubectl logs todo-backend-xxx-yyy -c daprd -n todo-app
# Look for pub/sub initialization logs
```

4. **Verify Dapr component**:
```bash
kubectl get component pubsub -n todo-app
# Should show Kafka pubsub component
```

5. **Test publishing manually**:
```bash
# Exec into backend pod
kubectl exec -it todo-backend-xxx-yyy -n todo-app -- bash

# Publish test event
curl -X POST http://localhost:3500/v1.0/publish/pubsub/task.created \
  -H "Content-Type: application/json" \
  -d '{"test": "event"}'
```

---

### Issue: Horizontal Pod Autoscaler Not Scaling

**Symptoms**:
- CPU exceeds 70% but pods don't scale
- HPA shows "unknown" metrics

**Cause**: Metrics Server not installed

**Solution**:

1. **Install Metrics Server**:
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

2. **Check Metrics Server running**:
```bash
kubectl get pods -n kube-system | grep metrics-server
```

3. **Verify metrics available**:
```bash
kubectl top pods -n todo-app
# Should show CPU and memory usage
```

4. **Check HPA status**:
```bash
kubectl get hpa -n todo-app
kubectl describe hpa backend-hpa -n todo-app
```

5. **Test scaling manually**:
```bash
# Generate load
kubectl run -it --rm load-generator --image=busybox --restart=Never -- \
  /bin/sh -c "while true; do wget -q -O- http://todo-backend:8000/health; done"

# Watch HPA
kubectl get hpa backend-hpa -n todo-app --watch
```

---

## Common Issues Across All Phases

### Issue: "Permission Denied" Errors

**Symptoms**:
- Docker: `permission denied while trying to connect to the Docker daemon socket`
- Kubernetes: `error: You must be logged in to the server (Unauthorized)`

**Solution**:

**Docker**:
```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
newgrp docker

# Restart Docker (macOS)
docker-machine restart

# Windows: Run Docker Desktop as Administrator
```

**Kubernetes**:
```bash
# Check kubectl config
kubectl config view

# Set correct context
kubectl config use-context <context-name>

# Get credentials (cloud specific)
aws eks update-kubeconfig --name my-cluster  # AWS
gcloud container clusters get-credentials my-cluster  # GCP
az aks get-credentials --resource-group myRG --name myAKS  # Azure
```

---

### Issue: Environment Variables Not Loading

**Symptoms**:
- `undefined` or `null` values for environment variables
- App uses default values instead of configured

**Solution**:

1. **Check .env file exists**:
```bash
# Backend
ls backend/.env

# Frontend
ls frontend/.env.local
```

2. **Verify variable names**:
```bash
# Backend (.env)
DATABASE_URL=...

# Frontend (.env.local) - must start with NEXT_PUBLIC_
NEXT_PUBLIC_API_URL=...
```

3. **Restart application** (env changes require restart):
```bash
# Backend
# Stop (Ctrl+C) and restart

# Frontend
# Stop (Ctrl+C) and restart
npm run dev
```

4. **Check variable in app**:
```python
# Backend - Python
import os
print(os.getenv('DATABASE_URL'))
```

```javascript
// Frontend - Next.js
console.log(process.env.NEXT_PUBLIC_API_URL)
```

---

### Issue: Slow Performance

**Symptoms**:
- Application feels sluggish
- Long load times

**Solution**:

1. **Check network latency**:
```bash
# Test API response time
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health

# curl-format.txt:
#     time_total:  %{time_total}s\n
```

2. **Enable production mode**:
```bash
# Frontend
npm run build
npm start  # Production server

# Backend
# Use gunicorn instead of uvicorn --reload
```

3. **Check database performance**:
```sql
-- Find slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

4. **Add caching** (Redis):
```python
# Cache frequently accessed data
from redis import Redis
cache = Redis(host='localhost', port=6379)
```

5. **Optimize bundle size** (Frontend):
```bash
# Analyze bundle
npm run build
npx @next/bundle-analyzer
```

---

## Getting Help

### Official Documentation
- **Todo Evolution**: [README.md](./README.md)
- **Deployment**: [DEPLOYMENT-RUNBOOK.md](./DEPLOYMENT-RUNBOOK.md)
- **Audits**: [PHASE8-AUDIT-REPORTS.md](./PHASE8-AUDIT-REPORTS.md)

### External Resources
- **FastAPI**: https://fastapi.tiangolo.com/
- **Next.js**: https://nextjs.org/docs
- **Kubernetes**: https://kubernetes.io/docs/
- **Helm**: https://helm.sh/docs/
- **Dapr**: https://docs.dapr.io/

### Issue Reporting
- **GitHub Issues**: [Create an issue](https://github.com/your-repo/issues/new)
- **Email Support**: support@example.com

---

**Document Maintained By**: Engineering Team
**Last Updated**: December 26, 2025
**Version**: 1.0.0
