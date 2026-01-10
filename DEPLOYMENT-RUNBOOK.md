# Todo Evolution - Deployment Runbook

**Project**: Todo Evolution - Multi-Phase Progressive Application
**Version**: 1.0.0
**Last Updated**: December 26, 2025
**Status**: Production Ready

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Phase 1: CLI Deployment](#phase-1-cli-deployment)
3. [Phase 2-3: Web Application Deployment](#phase-2-3-web-application-deployment)
4. [Phase 4: AI Optimization Setup](#phase-4-ai-optimization-setup)
5. [Phase 5: Kubernetes Deployment](#phase-5-kubernetes-deployment)
6. [Post-Deployment Validation](#post-deployment-validation)
7. [Rollback Procedures](#rollback-procedures)
8. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Prerequisites

### Required Software

| Software | Minimum Version | Purpose | Installation |
|----------|----------------|---------|--------------|
| Python | 3.13+ | CLI & Backend | `python --version` |
| UV | Latest | Python package manager | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Node.js | 18.x+ | Frontend PWA | `node --version` |
| npm | 9.x+ | Frontend package manager | `npm --version` |
| Docker | 20.x+ | Containerization | `docker --version` |
| kubectl | 1.28+ | Kubernetes CLI | `kubectl version` |
| Helm | 3.x+ | Kubernetes package manager | `helm version` |
| Git | 2.x+ | Source control | `git --version` |

### Required Accounts & Services

- **PostgreSQL Database**: Neon.tech account (or self-hosted PostgreSQL 14+)
- **Cloud Provider** (optional): AWS/GCP/Azure account for production deployment
- **Domain & SSL**: Domain name + SSL certificate (Let's Encrypt recommended)
- **GitHub** (optional): For CI/CD pipelines

### Environment Checklist

- [ ] Python 3.13+ installed
- [ ] UV package manager installed
- [ ] Node.js 18+ and npm installed
- [ ] Docker installed and running
- [ ] kubectl configured (for Kubernetes deployment)
- [ ] Helm installed (for Kubernetes deployment)
- [ ] Database provisioned (Neon or self-hosted PostgreSQL)
- [ ] Environment variables file prepared
- [ ] SSL certificates obtained (for HTTPS)

---

## Phase 1: CLI Deployment

### Deployment Steps

#### 1. Clone Repository

```bash
git clone <repository-url>
cd todo-evolution
```

#### 2. Install Dependencies

```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

#### 3. Verify Installation

```bash
# Run CLI application
python main.py
```

**Expected Output**:
- ASCII art title appears
- Interactive menu displays
- No import errors

#### 4. Distribute CLI (Optional)

**Option A: Direct Execution**
```bash
# Users run directly
python main.py
```

**Option B: Create Executable**
```bash
# Install PyInstaller
uv add --dev pyinstaller

# Build standalone executable
pyinstaller --onefile --name=todo-cli main.py

# Executable in dist/todo-cli
./dist/todo-cli
```

**Option C: Install as Package**
```bash
# Build package
uv build

# Install locally
pip install dist/todo_evolution-*.whl

# Run from anywhere
todo-cli
```

### Validation Checklist

- [ ] CLI starts without errors
- [ ] ASCII art displays correctly
- [ ] All menu options work (add, view, update, delete, toggle)
- [ ] Task list displays with Rich formatting
- [ ] Theme switching works (if implemented)
- [ ] Exit option works cleanly

---

## Phase 2-3: Web Application Deployment

### Architecture

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Frontend  │  HTTP   │   Backend   │  SQL    │  PostgreSQL │
│  (Next.js)  │────────▶│  (FastAPI)  │────────▶│   (Neon)    │
│  Port 3000  │         │  Port 8000  │         │  Port 5432  │
└─────────────┘         └─────────────┘         └─────────────┘
```

---

### Backend Deployment

#### 1. Navigate to Backend Directory

```bash
cd backend
```

#### 2. Create Environment File

```bash
cp .env.example .env
```

#### 3. Configure Environment Variables

Edit `.env` file:

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname
# For Neon: postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require

# Authentication
JWT_SECRET=<generate-with-openssl-rand-hex-32>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (comma-separated origins)
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Optional: Azure Speech Services (for Urdu voice fallback)
AZURE_SPEECH_KEY=<your-key>
AZURE_SPEECH_REGION=<region>
```

**Generate JWT Secret**:
```bash
openssl rand -hex 32
```

#### 4. Install Backend Dependencies

```bash
uv sync
```

#### 5. Run Database Migrations (if applicable)

```bash
uv run alembic upgrade head
```

#### 6. Start Backend Server

**Development**:
```bash
uv run uvicorn src.main:app --reload --port 8000
```

**Production**:
```bash
# Using uvicorn with workers
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4

# Or using gunicorn
uv run gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 7. Verify Backend

```bash
# Health check
curl http://localhost:8000/health

# API docs
open http://localhost:8000/docs
```

**Expected Response**:
```json
{"status": "healthy", "version": "1.0.0"}
```

---

### Frontend Deployment

#### 1. Navigate to Frontend Directory

```bash
cd frontend
```

#### 2. Install Frontend Dependencies

```bash
npm install
```

#### 3. Create Environment File

```bash
cp .env.local.example .env.local
```

#### 4. Configure Environment Variables

Edit `.env.local`:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
# For production: https://api.yourdomain.com

# Voice features (optional)
NEXT_PUBLIC_ENABLE_VOICE=true
NEXT_PUBLIC_AZURE_SPEECH_KEY=<optional>
NEXT_PUBLIC_AZURE_SPEECH_REGION=<optional>
```

#### 5. Build Frontend

**Development**:
```bash
npm run dev
# App at http://localhost:3000
```

**Production**:
```bash
# Build optimized bundle
npm run build

# Start production server
npm start
# App at http://localhost:3000
```

#### 6. Verify Frontend

- Open browser to `http://localhost:3000`
- Check console for errors
- Verify PWA installation prompt appears
- Test offline mode (toggle airplane mode)

---

### Docker Deployment (Recommended for Production)

#### 1. Build Docker Images

**Backend**:
```bash
cd backend
docker build -t todo-backend:latest .
```

**Frontend**:
```bash
cd frontend
docker build -t todo-frontend:latest .
```

#### 2. Run with Docker Compose

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: todouser
      POSTGRES_PASSWORD: todopass
      POSTGRES_DB: tododb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    image: todo-backend:latest
    environment:
      DATABASE_URL: postgresql://todouser:todopass@postgres:5432/tododb
      JWT_SECRET: ${JWT_SECRET}
      CORS_ORIGINS: http://localhost:3000,https://yourdomain.com
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  frontend:
    image: todo-frontend:latest
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

Run:
```bash
docker-compose up -d
```

#### 3. Verify Containers

```bash
docker-compose ps

# Should show:
# - postgres (healthy)
# - backend (healthy)
# - frontend (healthy)
```

---

### HTTPS/TLS Setup (Production)

#### Option A: Nginx Reverse Proxy

Install Nginx:
```bash
# Ubuntu/Debian
sudo apt install nginx

# macOS
brew install nginx
```

Configure Nginx (`/etc/nginx/sites-available/todo-app`):

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/todo-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Option B: Let's Encrypt SSL

Install Certbot:
```bash
sudo apt install certbot python3-certbot-nginx
```

Obtain certificate:
```bash
sudo certbot --nginx -d yourdomain.com
```

Auto-renew:
```bash
sudo certbot renew --dry-run
```

---

## Phase 4: AI Optimization Setup

### Configuration

#### 1. Verify Claude Code Subagent Files

Check `.claude/` directory structure:
```
.claude/
├── subagents/
│   └── task-optimizer.yaml
└── skills/
    └── task-management.yaml
```

#### 2. Verify Subagent Configuration

`.claude/subagents/task-optimizer.yaml`:
```yaml
name: task-optimizer
version: 1.0.0
description: Intelligent task optimization with duplicate detection, priority recommendations, and grouping
capabilities:
  - duplicate_detection
  - priority_recommendation
  - task_grouping
  - automation_detection
```

#### 3. Test AI Optimization

**CLI**:
```bash
python main.py --optimize
```

**Web UI**:
- Navigate to app
- Click "Optimize Tasks" button
- Verify suggestions appear

### Validation

- [ ] Duplicate detection identifies similar tasks
- [ ] Priority recommendations appear
- [ ] Task grouping suggestions work
- [ ] Accept/reject interface functional

---

## Phase 5: Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (Minikube, EKS, GKE, or AKS)
- kubectl configured
- Helm installed
- Docker images pushed to registry

---

### Deployment Option 1: Helm (Recommended)

#### 1. Configure values.yaml

Edit `helm-charts/todo-app/values.yaml`:

```yaml
# Image configuration
image:
  repository: your-registry/todo-app
  tag: "1.0.0"
  pullPolicy: IfNotPresent

# Replica counts
replicaCount:
  frontend: 3
  backend: 2

# Resource limits
resources:
  frontend:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "200m"
  backend:
    requests:
      memory: "256Mi"
      cpu: "200m"
    limits:
      memory: "512Mi"
      cpu: "500m"

# Database connection
database:
  url: "postgresql://user:pass@host:5432/db"

# Ingress configuration
ingress:
  enabled: true
  host: todo.yourdomain.com
  tls:
    enabled: true
    secretName: todo-tls-secret
```

#### 2. Install with Helm

```bash
# Create namespace
kubectl create namespace todo-app

# Install chart
helm install todo-app ./helm-charts/todo-app \
  --namespace todo-app \
  --values helm-charts/todo-app/values.yaml

# Check installation
helm status todo-app -n todo-app
```

#### 3. Verify Deployment

```bash
# Check pods
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check ingress
kubectl get ingress -n todo-app
```

---

### Deployment Option 2: Kustomize

#### 1. Choose Environment Overlay

```bash
# Development
kubectl apply -k kubernetes/overlays/dev

# Staging
kubectl apply -k kubernetes/overlays/staging

# Production
kubectl apply -k kubernetes/overlays/production
```

#### 2. Verify Deployment

```bash
kubectl get all -n todo-app
```

---

### Deployment Option 3: Complete Blueprint

#### 1. Deploy Single-File Manifest

```bash
kubectl apply -f blueprints/kubernetes-deployment.yaml
```

#### 2. Verify All Resources

```bash
# Check all resources
kubectl get all -n todo-app

# Check secrets
kubectl get secrets -n todo-app

# Check configmaps
kubectl get configmaps -n todo-app
```

---

### Configure Kafka & Dapr

#### 1. Install Dapr

```bash
# Install Dapr CLI
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Initialize Dapr on Kubernetes
dapr init -k

# Verify Dapr
kubectl get pods -n dapr-system
```

#### 2. Apply Dapr Components

```bash
kubectl apply -f kubernetes/base/dapr-components.yaml
```

#### 3. Verify Kafka

```bash
# Check Kafka pods
kubectl get pods -n todo-app | grep kafka

# Should see:
# kafka-0   1/1     Running
# kafka-1   1/1     Running
# kafka-2   1/1     Running
```

---

### Configure Ingress & TLS

#### 1. Install Ingress Controller

```bash
# Nginx Ingress
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace
```

#### 2. Install cert-manager (for Let's Encrypt)

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

#### 3. Create ClusterIssuer

```yaml
# letsencrypt-issuer.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

Apply:
```bash
kubectl apply -f letsencrypt-issuer.yaml
```

#### 4. Update Ingress with TLS

Ingress will automatically get TLS certificate from Let's Encrypt.

---

## Post-Deployment Validation

### Health Checks

#### Backend Health Check

```bash
curl https://api.yourdomain.com/health

# Expected:
# {"status": "healthy", "version": "1.0.0"}
```

#### Frontend Health Check

```bash
curl https://yourdomain.com

# Expected: HTML response with 200 status
```

#### Database Connection

```bash
# From backend pod
kubectl exec -it -n todo-app deploy/todo-backend -- \
  python -c "from src.db import engine; print('DB Connected' if engine else 'Failed')"
```

#### Kafka Health Check

```bash
# Check Kafka topics
kubectl exec -it -n todo-app kafka-0 -- \
  kafka-topics --bootstrap-server localhost:9092 --list

# Expected topics:
# task.created
# task.updated
# task.deleted
# task.completed
```

---

### Functional Tests

#### 1. User Registration

```bash
curl -X POST https://api.yourdomain.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Expected: 201 Created
```

#### 2. User Login

```bash
curl -X POST https://api.yourdomain.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Expected: {"access_token": "...", "token_type": "bearer"}
```

#### 3. Create Task

```bash
TOKEN="your-jwt-token"
curl -X POST https://api.yourdomain.com/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "Testing deployment"}'

# Expected: 201 Created with task object
```

#### 4. List Tasks

```bash
curl https://api.yourdomain.com/api/tasks \
  -H "Authorization: Bearer $TOKEN"

# Expected: Array of tasks
```

---

### Performance Tests

#### Load Test (using hey)

```bash
# Install hey
go install github.com/rakyll/hey@latest

# Test backend API
hey -z 30s -c 10 https://api.yourdomain.com/health

# Expected:
# - Response time: <200ms (p95)
# - No 5xx errors
```

#### Lighthouse Audit (Frontend)

```bash
# Install Lighthouse CI
npm install -g @lhci/cli

# Run audit
lhci autorun --url=https://yourdomain.com

# Expected:
# - Performance: >90
# - Accessibility: 100
# - Best Practices: >90
# - SEO: 100
```

---

### Monitoring Setup

#### 1. Install Prometheus

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

#### 2. Install Grafana

Grafana is included in kube-prometheus-stack.

Access Grafana:
```bash
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

Open `http://localhost:3000` (default: admin/prom-operator)

#### 3. Import Dashboards

- Kubernetes Cluster Monitoring
- Kafka Monitoring
- Dapr Monitoring
- Application Metrics

---

## Rollback Procedures

### Helm Rollback

```bash
# List releases
helm history todo-app -n todo-app

# Rollback to previous version
helm rollback todo-app -n todo-app

# Rollback to specific revision
helm rollback todo-app 2 -n todo-app
```

### Kubernetes Rollback

```bash
# Rollback deployment
kubectl rollout undo deployment/todo-backend -n todo-app

# Check rollout status
kubectl rollout status deployment/todo-backend -n todo-app
```

### Docker Rollback

```bash
# Tag and push previous version
docker tag todo-backend:1.0.0 your-registry/todo-backend:latest
docker push your-registry/todo-backend:latest

# Restart pods to pull latest
kubectl rollout restart deployment/todo-backend -n todo-app
```

---

## Monitoring & Maintenance

### Daily Checks

- [ ] All pods running (`kubectl get pods -n todo-app`)
- [ ] No crash loops or restarts
- [ ] Ingress accessible
- [ ] SSL certificate valid
- [ ] No 5xx errors in logs

### Weekly Maintenance

- [ ] Review application logs
- [ ] Check resource usage (CPU, memory)
- [ ] Review Prometheus alerts
- [ ] Check database size and performance
- [ ] Review Kafka disk usage

### Monthly Tasks

- [ ] Update dependencies (npm, pip)
- [ ] Review and rotate JWT secrets
- [ ] Check SSL certificate expiration
- [ ] Review and archive old logs
- [ ] Update Kubernetes cluster

---

## Emergency Contacts

| Role | Contact | Availability |
|------|---------|--------------|
| Backend Engineer | backend@example.com | 24/7 |
| Frontend Engineer | frontend@example.com | Business hours |
| DevOps Engineer | devops@example.com | 24/7 |
| Database Admin | dba@example.com | Business hours |

---

## Appendix: Common Commands

### Kubernetes

```bash
# Get pod logs
kubectl logs -f -n todo-app deploy/todo-backend

# Execute command in pod
kubectl exec -it -n todo-app deploy/todo-backend -- bash

# Port forward service
kubectl port-forward -n todo-app svc/todo-backend 8000:8000

# Scale deployment
kubectl scale deployment/todo-backend --replicas=5 -n todo-app

# Delete all resources
kubectl delete namespace todo-app
```

### Docker

```bash
# View running containers
docker ps

# View logs
docker logs -f container_id

# Execute in container
docker exec -it container_id bash

# Stop all containers
docker-compose down

# Remove volumes
docker-compose down -v
```

### Database

```bash
# Connect to PostgreSQL
psql -h localhost -U todouser -d tododb

# Backup database
pg_dump -h localhost -U todouser tododb > backup.sql

# Restore database
psql -h localhost -U todouser tododb < backup.sql
```

---

**Document Maintained By**: DevOps Team
**Last Review**: December 26, 2025
**Next Review**: January 26, 2026
