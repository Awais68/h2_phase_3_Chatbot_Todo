#!/bin/bash
# Deploy Todo App to Kubernetes (minikube)

set -e

echo "=========================================="
echo "Deploying Todo App to Kubernetes"
echo "=========================================="

# Navigate to kubernetes/simple directory
cd "$(dirname "$0")"

# Apply manifests in order
echo "1. Creating namespace..."
kubectl apply -f namespace.yaml

echo "2. Creating secrets..."
kubectl apply -f secrets.yaml

echo "3. Creating configmap..."
kubectl apply -f configmap.yaml

echo "4. Deploying backend..."
kubectl apply -f backend-deployment.yaml

echo "5. Deploying frontend..."
kubectl apply -f frontend-deployment.yaml

echo "6. Creating services..."
kubectl apply -f services.yaml

echo ""
echo "=========================================="
echo "Deployment complete!"
echo "=========================================="
echo ""
echo "Wait for pods to be ready:"
echo "  kubectl get pods -n todo-app -w"
echo ""
echo "Access the app:"
echo "  Frontend: minikube service frontend-service -n todo-app"
echo "  Backend:  minikube service backend-service -n todo-app"
echo ""
echo "Or use NodePorts:"
echo "  Frontend: http://\$(minikube ip):30080"
echo "  Backend:  http://\$(minikube ip):30800"
