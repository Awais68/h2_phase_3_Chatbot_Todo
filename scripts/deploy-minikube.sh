#!/bin/bash

# Script to deploy the Todo Chatbot application to Minikube
# Uses the Helm chart created for the application

set -e  # Exit on any error

echo "=========================================="
echo "Todo Chatbot Deployment to Minikube"
echo "=========================================="

echo ""
echo "Step 1: Verify Minikube is running"
if ! minikube status | grep -q "Running"; then
    echo "❌ Minikube is not running. Please start Minikube first."
    echo "Run: minikube start --cpus=2 --memory=4096"
    exit 1
fi
echo "✅ Minikube is running"

echo ""
echo "Step 2: Verify kubectl can connect to cluster"
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ kubectl cannot connect to cluster"
    exit 1
fi
echo "✅ kubectl connected to cluster"

echo ""
echo "Step 3: Verify Helm is available"
if ! command -v helm &> /dev/null; then
    echo "❌ Helm is not installed"
    exit 1
fi
echo "✅ Helm is available"

echo ""
echo "Step 4: Verify Docker images are available in Minikube"
if ! docker images | grep -q "todo-frontend" || ! docker images | grep -q "todo-backend"; then
    echo "⚠️  Docker images not found locally. Building them now..."

    echo "Building frontend image..."
    docker build -t todo-frontend:v1 frontend/

    echo "Building backend image..."
    docker build -t todo-backend:v1 backend/

    echo "Loading images into Minikube..."
    minikube image load todo-frontend:v1
    minikube image load todo-backend:v1
    echo "✅ Images built and loaded"
else
    echo "✅ Docker images are available"
fi

echo ""
echo "Step 5: Create namespace if it doesn't exist"
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

echo ""
echo "Step 6: Deploy application using Helm"
echo "Installing/upgrading todo-chatbot release..."

helm upgrade --install todo-app todo-chatbot/ \
    --namespace todo-app \
    --values todo-chatbot/values-dev.yaml \
    --timeout=10m

echo ""
echo "Step 7: Wait for deployments to be ready"
echo "Waiting for backend deployment..."
kubectl rollout status deployment/todo-app-todo-chatbot-backend -n todo-app --timeout=5m

echo "Waiting for frontend deployment..."
kubectl rollout status deployment/todo-app-todo-chatbot-frontend -n todo-app --timeout=5m

echo "Waiting for database to be ready..."
kubectl rollout status statefulset/todo-app-todo-chatbot-postgres -n todo-app --timeout=5m

echo ""
echo "Step 8: Show deployment status"
echo "Deployments:"
kubectl get deployments -n todo-app
echo ""
echo "StatefulSets:"
kubectl get statefulsets -n todo-app
echo ""
echo "Services:"
kubectl get services -n todo-app
echo ""
echo "Pods:"
kubectl get pods -n todo-app

echo ""
echo "Step 9: Show ingress if available"
kubectl get ingress -n todo-app || echo "No ingress found (may be disabled)"

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "To access the application:"
echo "1. Add to /etc/hosts: $(minikube ip) todo.local"
echo "2. Access frontend at: http://todo.local"
echo ""
echo "To check logs:"
echo "kubectl logs -f deployment/todo-app-todo-chatbot-backend -n todo-app"
echo "kubectl logs -f deployment/todo-app-todo-chatbot-frontend -n todo-app"
echo ""
echo "To check status anytime:"
echo "kubectl get all -n todo-app"