# Kubernetes Deployment Quick Start Guide

## Prerequisites

- Docker Desktop with Kubernetes enabled OR Minikube
- kubectl
- Helm 3+
- Git

## Setup Minikube (if using)

```bash
# Start Minikube with adequate resources
minikube start --cpus=2 --memory=4096

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server

# Verify cluster
kubectl cluster-info
kubectl get nodes
```

## Clone and Prepare Repository

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd <repository-directory>

# Build Docker images
docker build -t todo-frontend:v1 frontend/
docker build -t todo-backend:v1 backend/

# Load images to Minikube
minikube image load todo-frontend:v1
minikube image load todo-backend:v1
```

## Deploy with Helm

```bash
# Create namespace
kubectl create namespace todo-app

# Deploy application
helm upgrade --install todo-app todo-chatbot/ \
  --namespace todo-app \
  --values todo-chatbot/values-dev.yaml

# Wait for all pods to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/component=backend -n todo-app
kubectl wait --for=condition=ready pod -l app.kubernetes.io/component=frontend -n todo-app
kubectl wait --for=condition=ready pod -l app.kubernetes.io/component=postgres -n todo-app
```

## Verify Deployment

```bash
# Check all resources
kubectl get all -n todo-app

# Check pod status
kubectl get pods -n todo-app -o wide

# Check logs
kubectl logs -f deployment/todo-app-todo-chatbot-backend -n todo-app
kubectl logs -f deployment/todo-app-todo-chatbot-frontend -n todo-app

# Test connectivity
kubectl run test-connectivity --image=curlimages/curl:latest -n todo-app --rm -it --restart=Never -- \
  curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://todo-app-todo-chatbot-backend:8000/health
```

## Access the Application

### For Minikube

```bash
# Get Minikube IP
minikube ip

# Add to /etc/hosts
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts

# Access application at
# Frontend: http://todo.local
```

### For Port Forwarding (alternative)

```bash
# Forward frontend port
kubectl port-forward -n todo-app service/todo-app-todo-chatbot-frontend 3000:3000

# Forward backend port
kubectl port-forward -n todo-app service/todo-app-todo-chatbot-backend 8000:8000
```

## Useful Commands

```bash
# Check deployment status
helm status todo-app -n todo-app

# Get all resources
kubectl get all -n todo-app

# Check resource usage
kubectl top pods -n todo-app

# View deployment history
helm history todo-app -n todo-app

# Rollback deployment
helm rollback todo-app -n todo-app

# Upgrade with new values
helm upgrade todo-app todo-chatbot/ --namespace todo-app --values todo-chatbot/values-dev.yaml

# Uninstall
helm uninstall todo-app -n todo-app
```

## Troubleshooting

### Common Issues

1. **Pods stuck in Pending state**:
   ```bash
   kubectl describe pods -n todo-app
   ```

2. **Image pull errors**:
   ```bash
   # Ensure images are built and loaded to Minikube
   docker build -t todo-frontend:v1 frontend/
   minikube image load todo-frontend:v1
   ```

3. **Service connectivity issues**:
   ```bash
   # Test connectivity between services
   kubectl run test --image=curlimages/curl:latest -n todo-app --rm -it --restart=Never -- \
     curl -s http://todo-app-todo-chatbot-backend:8000/health
   ```

4. **Database connection issues**:
   ```bash
   # Check database logs
   kubectl logs -f statefulset/todo-app-todo-chatbot-postgres -n todo-app
   ```

### Debug Commands

```bash
# Get detailed pod information
kubectl describe pod <pod-name> -n todo-app

# Check events
kubectl get events -n todo-app --sort-by='.lastTimestamp'

# Exec into a pod
kubectl exec -it <pod-name> -n todo-app -- /bin/sh

# Check service endpoints
kubectl get endpoints -n todo-app
```

## Development Workflow

### Making Changes

1. Update your application code
2. Rebuild Docker images:
   ```bash
   docker build -t todo-frontend:v1 frontend/
   docker build -t todo-backend:v1 backend/
   minikube image load todo-frontend:v1
   minikube image load todo-backend:v1
   ```
3. Update image tags in values file or use `--set` flag:
   ```bash
   helm upgrade todo-app todo-chatbot/ --namespace todo-app \
     --values todo-chatbot/values-dev.yaml \
     --set backend.image.tag=v1 \
     --set frontend.image.tag=v1
   ```

### Scaling Applications

```bash
# Scale deployments
kubectl scale deployment/todo-app-todo-chatbot-frontend -n todo-app --replicas=3
kubectl scale deployment/todo-app-todo-chatbot-backend -n todo-app --replicas=2

# Check HPA status (if enabled)
kubectl get hpa -n todo-app
```

## Production Deployment

For production deployment, use the production values file:

```bash
helm upgrade --install todo-app todo-chatbot/ \
  --namespace todo-app \
  --values todo-chatbot/values-prod.yaml \
  --set backend.apiKeys.openaiApiKey=<your-production-key>
```

## Cleanup

```bash
# Uninstall Helm release
helm uninstall todo-app -n todo-app

# Delete namespace
kubectl delete namespace todo-app

# Stop Minikube (if using)
minikube stop
```

## Next Steps

- Configure proper domain and TLS certificates
- Set up monitoring and logging
- Implement backup and recovery procedures
- Configure CI/CD pipeline
- Set up proper security scanning