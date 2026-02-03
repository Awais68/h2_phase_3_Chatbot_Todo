# Quickstart Guide: Todo AI Chatbot on Kubernetes

## Overview
This guide provides a rapid setup process to deploy the Todo AI Chatbot application to a local Minikube Kubernetes cluster using AI-powered DevOps tools.

## Prerequisites

### System Requirements
- Docker Desktop installed and running
- Minikube installed (v1.20+)
- kubectl installed
- Helm 3.x installed
- Gordon (Docker AI Agent) available
- kubectl-ai (optional, for AI-assisted operations)

### Environment Setup
```bash
# Verify prerequisites
docker --version
minikube version
kubectl version --client
helm version
```

## Quick Deployment Steps

### 1. Start Minikube Cluster
```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192

# Enable ingress addon
minikube addons enable ingress

# Verify cluster status
minikube status
```

### 2. Set Up Docker Environment for Minikube
```bash
# Point Docker client to Minikube's Docker daemon
eval $(minikube docker-env)

# Verify Docker is pointing to Minikube
docker images
```

### 3. Build Application Images (using Gordon)
```bash
# Create Dockerfiles using Gordon AI
docker ai "create an optimized Dockerfile for a Next.js ChatKit frontend"
docker ai "create a production Dockerfile for FastAPI with SQLModel and MCP SDK"

# Build frontend image
docker build -f docker/Dockerfile.frontend -t todo-frontend:v1.0.0 .

# Build backend image
docker build -f docker/Dockerfile.backend -t todo-backend:v1.0.0 .

# Build MCP server image
docker build -f docker/Dockerfile.mcp -t todo-mcp:v1.0.0 .

# Verify images were built
docker images | grep todo-
```

### 4. Deploy Using Helm
```bash
# Navigate to helm charts directory
cd helm-charts/todo-chatbot

# Install the Todo AI Chatbot using Helm
helm install todo-chatbot . \
  --namespace todo-chatbot \
  --create-namespace \
  --set frontend.image.repository=todo-frontend \
  --set frontend.image.tag=v1.0.0 \
  --set backend.image.repository=todo-backend \
  --set backend.image.tag=v1.0.0 \
  --set mcp.image.repository=todo-mcp \
  --set mcp.image.tag=v1.0.0

# Verify installation
helm list -n todo-chatbot
```

### 5. Configure Secrets (Required)
```bash
# Create secrets for the application
kubectl create secret generic todo-secrets \
  --namespace todo-chatbot \
  --from-literal=DATABASE_URL="your-neon-db-url" \
  --from-literal=OPENAI_API_KEY="your-openai-key" \
  --from-literal=OPENAI_DOMAIN_KEY="your-openai-domain" \
  --from-literal=BETTER_AUTH_SECRET="your-auth-secret"
```

### 6. Verify Deployment
```bash
# Check all resources are running
kubectl get all -n todo-chatbot

# Wait for all pods to be ready
kubectl wait --for=condition=ready pod -l app=frontend -n todo-chatbot --timeout=300s
kubectl wait --for=condition=ready pod -l app=backend -n todo-chatbot --timeout=300s
kubectl wait --for=condition=ready pod -l app=mcp -n todo-chatbot --timeout=300s

# Check service endpoints
kubectl get svc -n todo-chatbot
```

### 7. Access the Application
```bash
# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

# Access frontend via NodePort (find the NodePort from service output)
echo "Frontend: http://$MINIKUBE_IP:<NODEPORT>"

# Or use minikube service to open in browser
minikube service frontend-service -n todo-chatbot

# Test backend health endpoint
kubectl port-forward -n todo-chatbot svc/backend-service 8000:8000 &
curl http://localhost:8000/health
```

## AI-Assisted Operations (Optional)

### Using kubectl-ai for Management
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"

# Ask kubectl-ai for help
kubectl-ai "show me all pods in todo-chatbot namespace"

# Scale deployments
kubectl-ai "scale the backend deployment to 3 replicas in todo-chatbot namespace"

# Debug issues
kubectl-ai "why are the frontend pods not starting in todo-chatbot namespace"
```

### Using Gordon for Image Optimization
```bash
# Analyze images for optimization
docker ai "analyze the todo-backend:v1.0.0 image for optimization"

# Get build recommendations
docker ai "how can I reduce the size of my Python FastAPI image"
```

## Troubleshooting Quick Fixes

### Common Issues and Solutions
```bash
# 1. Pods stuck in Pending state
kubectl describe pods -n todo-chatbot
# Check if resources are available

# 2. ImagePullBackOff errors
kubectl describe pod <pod-name> -n todo-chatbot
# Ensure images exist in Minikube's registry

# 3. Service not accessible
kubectl get endpoints -n todo-chatbot
# Verify pods are ready and service selectors match

# 4. Check logs for issues
kubectl logs -n todo-chatbot -l app=frontend
kubectl logs -n todo-chatbot -l app=backend
kubectl logs -n todo-chatbot -l app=mcp
```

## Cleanup
```bash
# Uninstall the Helm release
helm uninstall todo-chatbot -n todo-chatbot

# Delete the namespace
kubectl delete namespace todo-chatbot

# Stop Minikube
minikube stop
```

## Next Steps
- Explore the comprehensive deployment guide for advanced configurations
- Set up monitoring and observability
- Configure persistent storage for production use
- Implement CI/CD pipeline for automated deployments