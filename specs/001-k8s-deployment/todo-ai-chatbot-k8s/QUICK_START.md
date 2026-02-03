# Quick Start Guide: Todo AI Chatbot on Kubernetes

This guide provides step-by-step instructions to deploy the Todo AI Chatbot to your local Kubernetes cluster using Minikube.

## Prerequisites

Before starting, ensure you have the following installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop) with Kubernetes enabled, OR [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm 3](https://helm.sh/docs/intro/install/)
- [OpenAI API Key](https://platform.openai.com/api-keys)
- [Neon PostgreSQL](https://neon.tech/) database credentials

## Step 1: Set up Kubernetes Cluster

### Option A: Using Minikube (Recommended for local development)

```bash
# Start Minikube with adequate resources
minikube start --cpus=4 --memory=8192

# Enable ingress addon
minikube addons enable ingress

# Verify cluster is running
kubectl cluster-info
```

### Option B: Using Docker Desktop with Kubernetes

```bash
# Enable Kubernetes in Docker Desktop settings
# Verify cluster is running
kubectl cluster-info
```

## Step 2: Prepare Environment

### Clone the Repository

```bash
git clone <repository-url>
cd todo-ai-chatbot-k8s
```

### Configure Environment Variables

Copy the environment template and fill in your credentials:

```bash
# Create environment files from templates
cp config/local/.env.example config/local/.env
cp config/prod/.env.example config/prod/.env

# Edit the .env file with your actual credentials
# - OpenAI API Key
# - Neon PostgreSQL credentials
# - Better Auth secret
nano config/local/.env
```

## Step 3: Build Docker Images

### Build Images Locally

```bash
# Build all images in Minikube Docker environment
eval $(minikube docker-env)

# Build backend image
docker build -t todo-backend:latest -f docker/backend/Dockerfile docker/backend/.

# Build MCP server image
docker build -t todo-mcp-server:latest -f docker/mcp-server/Dockerfile docker/mcp-server/.

# Build frontend image
docker build -t todo-frontend:latest -f docker/frontend/Dockerfile docker/frontend/.

# Reset Docker environment
eval $(minikube docker-env -u)
```

### Alternative: Load Pre-built Images

If you have images built in your local Docker:

```bash
# Load images to Minikube
minikube image load todo-backend:latest
minikube image load todo-mcp-server:latest
minikube image load todo-frontend:latest
```

## Step 4: Deploy with Helm (Recommended)

### Install the Helm Chart

```bash
# Navigate to the Helm directory
cd helm

# Install the chart
./install-chart.sh

# Or install with custom values
helm install todo-chatbot todo-chatbot/ \
    --namespace todo-chatbot \
    --create-namespace \
    --values todo-chatbot/values.yaml
```

### Verify Installation

```bash
# Check release status
helm status todo-chatbot -n todo-chatbot

# Check all resources
kubectl get all -n todo-chatbot
kubectl get ingress -n todo-chatbot
```

## Step 5: Deploy with Raw Kubernetes Manifests (Alternative)

### Apply All Manifests

```bash
# Create namespace
kubectl apply -f k8s/base/namespace.yaml

# Apply base configurations
kubectl apply -f k8s/base/configmap.yaml
kubectl apply -f k8s/base/secrets.yaml

# Apply deployments and services
kubectl apply -f k8s/backend/deployment.yaml
kubectl apply -f k8s/backend/service.yaml
kubectl apply -f k8s/mcp-server/deployment.yaml
kubectl apply -f k8s/mcp-server/service.yaml
kubectl apply -f k8s/frontend/deployment.yaml
kubectl apply -f k8s/frontend/service.yaml

# Apply ingress
kubectl apply -f k8s/ingress/ingress.yaml

# Apply network policies
kubectl apply -f k8s/network/network-policy.yaml
kubectl apply -f k8s/network/pdb.yaml
```

## Step 6: Verify the Deployment

### Check Deployment Status

```bash
# Run the verification script
./scripts/k8s/verify-deployment.sh

# Or manually check:
kubectl get pods -n todo-chatbot
kubectl get services -n todo-chatbot
kubectl get ingress -n todo-chatbot
```

### Check Application Health

```bash
# Run the health check script
./scripts/monitoring/check-health.sh

# Check logs for each component
kubectl logs -l app=backend -n todo-chatbot
kubectl logs -l app=mcp-server -n todo-chatbot
kubectl logs -l app=frontend -n todo-chatbot
```

## Step 7: Access the Application

### Using NodePort Service

```bash
# Get the NodePort address
minikube service frontend-service -n todo-chatbot --url

# Or get the Minikube IP
minikube ip
# Then access: http://<minikube-ip>:<nodeport>
```

### Using Ingress (Recommended)

```bash
# Add host entry to /etc/hosts
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts

# Access the application
# Frontend: http://todo.local
# Backend API: http://todo-api.local
```

### Using Port Forwarding (Development)

```bash
# Forward frontend port
kubectl port-forward -n todo-chatbot service/frontend-service 3000:3000

# Forward backend port
kubectl port-forward -n todo-chatbot service/backend-service 8000:8000
```

## Step 8: Monitor and Scale

### Check Resource Usage

```bash
# View resource usage
kubectl top nodes
kubectl top pods -n todo-chatbot

# Check monitoring
kubectl get hpa -n todo-chatbot
```

### Scale Applications

```bash
# Scale backend manually
kubectl scale deployment backend-deployment -n todo-chatbot --replicas=3

# Or update values and upgrade Helm chart
helm upgrade todo-chatbot todo-chatbot/ \
    --namespace todo-chatbot \
    --set replicaCount.backend=3
```

## Troubleshooting

### Common Issues

1. **Images not found**: Make sure images are loaded to Minikube
   ```bash
   # Check images in Minikube
   minikube ssh docker images | grep todo-
   ```

2. **Pods not starting**: Check pod status and logs
   ```bash
   kubectl get pods -n todo-chatbot
   kubectl describe pod <pod-name> -n todo-chatbot
   kubectl logs <pod-name> -n todo-chatbot
   ```

3. **Service not accessible**: Verify service configuration
   ```bash
   kubectl get services -n todo-chatbot
   kubectl describe service frontend-service -n todo-chatbot
   ```

4. **Ingress not working**: Check ingress controller and rules
   ```bash
   kubectl get ingress -n todo-chatbot
   kubectl describe ingress todo-chatbot-ingress -n todo-chatbot
   minikube addons list | grep ingress
   ```

### Useful Commands

```bash
# Get all resources in todo-chatbot namespace
kubectl get all -n todo-chatbot

# Watch pods status
kubectl get pods -n todo-chatbot -w

# Check events
kubectl get events -n todo-chatbot --sort-by='.lastTimestamp'

# Debug a pod
kubectl run debug --image=curlimages/curl -it --rm --restart=Never -n todo-chatbot -- sh
```

## Next Steps

1. **Configure Production Values**: Update `values-prod.yaml` with production settings
2. **Set up Monitoring**: Configure Prometheus and Grafana
3. **Configure SSL/TLS**: Set up certificates for ingress
4. **Set up CI/CD**: Implement automated deployment pipeline
5. **Backup Strategy**: Implement database and application backups

## Uninstall

### Using Helm

```bash
# Uninstall the release
helm uninstall todo-chatbot -n todo-chatbot

# Delete the namespace
kubectl delete namespace todo-chatbot
```

### Using Raw Manifests

```bash
# Delete all resources (in reverse order)
kubectl delete -f k8s/ingress/ingress.yaml
kubectl delete -f k8s/network/pdb.yaml
kubectl delete -f k8s/network/network-policy.yaml
kubectl delete -f k8s/frontend/service.yaml
kubectl delete -f k8s/frontend/deployment.yaml
kubectl delete -f k8s/mcp-server/service.yaml
kubectl delete -f k8s/mcp-server/deployment.yaml
kubectl delete -f k8s/backend/service.yaml
kubectl delete -f k8s/backend/deployment.yaml
kubectl delete -f k8s/base/secrets.yaml
kubectl delete -f k8s/base/configmap.yaml
kubectl delete -f k8s/base/namespace.yaml
```

Congratulations! You now have the Todo AI Chatbot running on Kubernetes.