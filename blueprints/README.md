# Todo Evolution - Kubernetes Deployment Blueprint

Complete cloud-native deployment blueprint for Todo Evolution application on Kubernetes.

## Quick Start

Deploy the entire application stack with a single command:

```bash
kubectl apply -f kubernetes-deployment.yaml
```

That's it! The complete Todo Evolution application with all components (frontend, backend, database, cache, messaging) will be deployed.

## What Gets Deployed

### Core Components
- **Frontend** (Next.js 15 PWA): 3 replicas with auto-scaling (3-15 pods)
- **Backend** (FastAPI): 2 replicas with auto-scaling (2-10 pods)
- **PostgreSQL**: 1 replica with 50Gi persistent storage
- **Redis**: 1 replica for caching with 10Gi storage
- **Kafka**: 3 brokers for event streaming with 50Gi storage each
- **ZooKeeper**: 3 nodes for Kafka coordination

### Infrastructure
- **Namespace**: `todo-app` for resource isolation
- **ConfigMap**: Application configuration
- **Secrets**: Sensitive credentials (requires manual configuration)
- **Services**: ClusterIP services for internal communication
- **Ingress**: nginx-ingress with TLS/HTTPS support
- **HPA**: Horizontal Pod Autoscaler for frontend and backend
- **PDB**: Pod Disruption Budgets for high availability
- **Dapr**: Service mesh components for microservices communication

### Features Deployed
- Progressive Web App (PWA) with offline support
- Voice interface (English & Urdu)
- AI-powered task optimization
- Event-driven architecture with Kafka
- Service-to-service communication via Dapr
- Auto-scaling based on CPU/memory usage
- TLS/HTTPS with Let's Encrypt certificates
- Rate limiting and CORS protection
- Health checks and readiness probes
- Prometheus metrics exposure
- Distributed tracing with Jaeger

## Prerequisites

### Required Components
1. **Kubernetes Cluster** (v1.28+)
   - AWS EKS, GCP GKE, Azure AKS, or self-hosted
   - Minimum: 3 nodes with 4 CPU and 8GB RAM each
   - Recommended: 5 nodes with 8 CPU and 16GB RAM each

2. **kubectl** (v1.28+)
   ```bash
   kubectl version --client
   ```

3. **nginx-ingress-controller**
   ```bash
   helm install ingress-nginx ingress-nginx/ingress-nginx \
     --namespace ingress-nginx \
     --create-namespace
   ```

4. **cert-manager** (for TLS certificates)
   ```bash
   kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
   ```

5. **Dapr** (v1.12+) - Optional but recommended
   ```bash
   dapr init --kubernetes --wait
   ```

### Storage Requirements
- Storage class `standard` or modify `storageClassName` in the YAML
- Total storage needed: ~250Gi
  - PostgreSQL: 50Gi
  - Redis: 10Gi
  - Kafka (3 brokers): 150Gi
  - ZooKeeper (3 nodes): 30Gi

## Pre-Deployment Configuration

### 1. Update Secrets

**CRITICAL**: Update secrets before deployment!

Edit the `secret.yaml` section in `kubernetes-deployment.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-app-secrets
stringData:
  DATABASE_PASSWORD: "your-secure-database-password"
  REDIS_PASSWORD: "your-secure-redis-password"
  JWT_SECRET_KEY: "your-secure-jwt-secret-key"
  OPENAI_API_KEY: "your-openai-api-key"
  AZURE_SPEECH_KEY: "your-azure-speech-key"
  # ... other secrets
```

### 2. Update Domain

Replace `todo-app.example.com` with your actual domain:

```bash
# On Linux/Mac
sed -i 's/todo-app.example.com/your-domain.com/g' kubernetes-deployment.yaml

# On Mac (alternative)
sed -i '' 's/todo-app.example.com/your-domain.com/g' kubernetes-deployment.yaml
```

### 3. Update Container Images

Update image repositories if using your own registry:

```yaml
# Frontend
image: your-registry.com/todo-app/frontend:latest

# Backend
image: your-registry.com/todo-app/backend:latest
```

## Deployment Steps

### Option 1: Single-File Deployment (Easiest)

```bash
# Deploy everything at once
kubectl apply -f kubernetes-deployment.yaml

# Wait for all pods to be ready (may take 5-10 minutes)
kubectl wait --for=condition=ready pod --all -n todo-app --timeout=600s

# Check deployment status
kubectl get pods -n todo-app
kubectl get svc -n todo-app
kubectl get ingress -n todo-app
```

### Option 2: Kustomize Deployment (Environment-Specific)

```bash
# Development
kubectl apply -k ../kubernetes/overlays/dev/

# Staging
kubectl apply -k ../kubernetes/overlays/staging/

# Production
kubectl apply -k ../kubernetes/overlays/production/
```

### Option 3: Helm Chart Deployment (Advanced)

```bash
# Using Helm chart
helm install todo-app ../helm-charts/todo-app \
  --namespace todo-app \
  --create-namespace \
  --set global.domain=your-domain.com \
  --set postgresql.auth.password=your-db-password \
  --set redis.auth.password=your-redis-password
```

## Post-Deployment Steps

### 1. Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n todo-app

# Expected output: All pods in "Running" or "Completed" status
# - backend-xxx (2/2 running)
# - frontend-xxx (1/1 running)
# - postgres-0 (2/2 running)
# - redis-0 (2/2 running)
# - kafka-0, kafka-1, kafka-2 (2/2 running each)
# - zookeeper-0, zookeeper-1, zookeeper-2 (1/1 running each)
```

### 2. Configure DNS

Get the ingress external IP:

```bash
kubectl get ingress -n todo-app

# Output:
# NAME               CLASS   HOSTS                   ADDRESS
# todo-app-ingress   nginx   todo-app.example.com    x.x.x.x
```

Create DNS A records:
- `todo-app.example.com` → `<EXTERNAL-IP>`
- `api.todo-app.example.com` → `<EXTERNAL-IP>`

### 3. Wait for TLS Certificate

```bash
# Check certificate status
kubectl get certificate -n todo-app

# Wait for "Ready" status (may take 1-2 minutes)
kubectl wait --for=condition=ready certificate/todo-app-tls -n todo-app --timeout=300s
```

### 4. Run Database Migrations

```bash
# Run migrations
kubectl exec -n todo-app deployment/backend -c backend -- alembic upgrade head
```

### 5. Access the Application

- **Frontend**: https://todo-app.example.com
- **Backend API**: https://api.todo-app.example.com
- **API Docs**: https://api.todo-app.example.com/docs

## Verification Checklist

- [ ] All pods are in `Running` state
- [ ] Services have `ClusterIP` assigned
- [ ] Ingress has external IP
- [ ] DNS records are configured
- [ ] TLS certificate is issued
- [ ] Database migrations completed
- [ ] Frontend is accessible via browser
- [ ] Backend API `/health` endpoint returns 200
- [ ] HPA is active and monitoring metrics
- [ ] Kafka topics are created

```bash
# Quick verification script
./verify-deployment.sh  # See below for script
```

## Monitoring

### View Logs

```bash
# Backend logs
kubectl logs -n todo-app -l component=backend -f

# Frontend logs
kubectl logs -n todo-app -l component=frontend -f

# Kafka logs
kubectl logs -n todo-app -l component=kafka -f

# All logs
kubectl logs -n todo-app --all-containers -f
```

### Check Metrics

```bash
# HPA status
kubectl get hpa -n todo-app

# Resource usage
kubectl top pods -n todo-app
kubectl top nodes
```

### Health Checks

```bash
# Backend health
kubectl exec -n todo-app deployment/backend -c backend -- curl localhost:8000/health

# Frontend health
kubectl exec -n todo-app deployment/frontend -- curl localhost:3000/api/health
```

## Scaling

### Manual Scaling

```bash
# Scale frontend
kubectl scale deployment/frontend -n todo-app --replicas=10

# Scale backend
kubectl scale deployment/backend -n todo-app --replicas=5
```

### Auto-Scaling Configuration

Auto-scaling is pre-configured with HPA:
- **Frontend**: 3-15 replicas (70% CPU, 80% memory)
- **Backend**: 2-10 replicas (70% CPU, 80% memory)

Modify HPA in the YAML to adjust thresholds.

## Undeployment

### Remove Application

```bash
# Delete all resources
kubectl delete -f kubernetes-deployment.yaml

# Or delete namespace (removes everything)
kubectl delete namespace todo-app
```

### Clean Up Persistent Volumes

```bash
# List PVCs
kubectl get pvc -n todo-app

# Delete PVCs (WARNING: This deletes all data!)
kubectl delete pvc -n todo-app --all

# Delete PVs if needed
kubectl get pv | grep todo-app
kubectl delete pv <pv-name>
```

## Troubleshooting

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for detailed troubleshooting guide.

### Quick Fixes

#### Pods Not Starting

```bash
# Describe pod to see events
kubectl describe pod <pod-name> -n todo-app

# Common issues:
# - Insufficient resources: Scale down or add nodes
# - Image pull errors: Check image names and registry access
# - Storage issues: Verify storage class exists
```

#### Database Connection Errors

```bash
# Check PostgreSQL status
kubectl logs -n todo-app statefulset/postgres -c postgres

# Test connection
kubectl run psql-test --rm -it --image=postgres:16 -n todo-app -- \
  psql -h postgres-service -U postgres -d todo_db
```

#### Ingress Not Working

```bash
# Check ingress controller
kubectl get pods -n ingress-nginx

# Check ingress resource
kubectl describe ingress todo-app-ingress -n todo-app

# Check service endpoints
kubectl get endpoints -n todo-app
```

## Cloud Provider Specific Notes

### AWS EKS

```bash
# Use GP3 storage class
storageClassName: gp3

# Use NLB for ingress
annotations:
  service.beta.kubernetes.io/aws-load-balancer-type: nlb
```

### GCP GKE

```bash
# Use PD-SSD storage class
storageClassName: pd-ssd

# Use GCE ingress
annotations:
  kubernetes.io/ingress.class: gce
```

### Azure AKS

```bash
# Use managed-premium storage class
storageClassName: managed-premium

# Use Azure ingress
annotations:
  kubernetes.io/ingress.class: azure/application-gateway
```

## Performance Tuning

### Resource Optimization

Based on actual usage, adjust resource requests/limits:

```yaml
resources:
  requests:
    cpu: 200m      # Adjust based on actual CPU usage
    memory: 512Mi  # Adjust based on actual memory usage
  limits:
    cpu: 1000m
    memory: 1Gi
```

### Database Tuning

For high-traffic deployments, adjust PostgreSQL settings:

```yaml
env:
- name: POSTGRES_MAX_CONNECTIONS
  value: "200"
- name: POSTGRES_SHARED_BUFFERS
  value: "256MB"
```

### Kafka Tuning

For high-throughput event processing:

```yaml
env:
- name: KAFKA_NUM_PARTITIONS
  value: "6"  # Double the partitions
- name: KAFKA_HEAP_OPTS
  value: "-Xmx1G -Xms1G"  # Increase heap
```

## Security Hardening

1. **Enable Network Policies**: Restrict pod-to-pod communication
2. **Use External Secrets**: Integrate with HashiCorp Vault or AWS Secrets Manager
3. **Enable Pod Security Standards**: Enforce restricted policy
4. **Scan Images**: Use Trivy or Snyk to scan for vulnerabilities
5. **Enable Audit Logging**: Configure Kubernetes audit logs
6. **Rotate Secrets**: Implement automatic secret rotation

## Backup and Recovery

### Database Backup

```bash
# Create backup
kubectl exec -n todo-app statefulset/postgres -c postgres -- \
  pg_dump -U postgres todo_db > backup-$(date +%Y%m%d).sql

# Restore backup
kubectl exec -i -n todo-app statefulset/postgres -c postgres -- \
  psql -U postgres todo_db < backup-20240101.sql
```

### Disaster Recovery

- Regular PVC snapshots (use VolumeSnapshot)
- Cross-region PostgreSQL replication
- Kafka topic backups to S3/GCS
- Terraform/Helm state backups

## Support

- **Documentation**: See `/docs` folder
- **Issues**: https://github.com/todo-app/todo-evolution/issues
- **Email**: admin@todo-app.example.com
- **Slack**: #todo-app-support

## License

MIT License - see LICENSE file

---

**Last Updated**: 2024-12-26
**Version**: 2.0.0
**Kubernetes Version**: 1.28+
