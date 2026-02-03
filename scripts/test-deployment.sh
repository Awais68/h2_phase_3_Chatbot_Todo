#!/bin/bash

# Comprehensive test script for Todo Chatbot deployment

set -e

echo "=========================================="
echo "Todo Chatbot Deployment - Comprehensive Test"
echo "=========================================="

echo ""
echo "Test 1: Pre-deployment checks"
echo "Checking if Minikube is running..."
if minikube status | grep -q "Running"; then
    echo "✅ Minikube is running"
else
    echo "❌ Minikube is not running"
    exit 1
fi

echo "Checking if Helm chart exists..."
if [ -d "todo-chatbot/" ]; then
    echo "✅ Helm chart directory exists"
else
    echo "❌ Helm chart directory does not exist"
    exit 1
fi

echo "Checking if Docker images exist..."
if docker images | grep -q "todo-frontend:v1" && docker images | grep -q "todo-backend:v1"; then
    echo "✅ Docker images exist"
else
    echo "❌ Docker images do not exist"
    exit 1
fi

echo ""
echo "Test 2: Helm chart validation"
echo "Validating Helm chart..."
if helm lint todo-chatbot/; then
    echo "✅ Helm chart validates successfully"
else
    echo "❌ Helm chart validation failed"
    exit 1
fi

echo ""
echo "Test 3: Template rendering"
echo "Testing template rendering..."
if helm template test-release todo-chatbot/ --values todo-chatbot/values-dev.yaml > /tmp/rendered-templates.yaml; then
    echo "✅ Templates render successfully"
else
    echo "❌ Template rendering failed"
    exit 1
fi

echo ""
echo "Test 4: Deploy to Minikube"
echo "Starting deployment..."

# Create namespace
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

# Deploy with Helm
helm upgrade --install todo-app todo-chatbot/ \
    --namespace todo-app \
    --values todo-chatbot/values-dev.yaml \
    --timeout=10m

echo "✅ Deployment initiated successfully"

echo ""
echo "Test 5: Wait for all resources to be ready"
echo "Waiting for deployments to be ready..."

# Wait for backend deployment
echo "Waiting for backend deployment..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/component=backend -n todo-app --timeout=5m || {
    echo "❌ Backend deployment failed to become ready"
    kubectl get pods -n todo-app
    kubectl describe pods -n todo-app
    exit 1
}

# Wait for frontend deployment
echo "Waiting for frontend deployment..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/component=frontend -n todo-app --timeout=5m || {
    echo "❌ Frontend deployment failed to become ready"
    kubectl get pods -n todo-app
    kubectl describe pods -n todo-app
    exit 1
}

# Wait for database
echo "Waiting for database..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/component=postgres -n todo-app --timeout=5m || {
    echo "❌ Database failed to become ready"
    kubectl get pods -n todo-app
    kubectl describe pods -n todo-app
    exit 1
}

echo "✅ All deployments are ready"

echo ""
echo "Test 6: Verify all resources"
echo "Checking deployments..."
BACKEND_DEPLOY=$(kubectl get deployment todo-app-todo-chatbot-backend -n todo-app -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")
FRONTEND_DEPLOY=$(kubectl get deployment todo-app-todo-chatbot-frontend -n todo-app -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")

if [ "$BACKEND_DEPLOY" -ge 1 ] && [ "$FRONTEND_DEPLOY" -ge 1 ]; then
    echo "✅ Deployments have ready replicas (Backend: $BACKEND_DEPLOY, Frontend: $FRONTEND_DEPLOY)"
else
    echo "❌ Deployments don't have expected ready replicas"
    exit 1
fi

echo "Checking services..."
if kubectl get service todo-app-todo-chatbot-backend -n todo-app &> /dev/null && \
   kubectl get service todo-app-todo-chatbot-frontend -n todo-app &> /dev/null && \
   kubectl get service todo-app-todo-chatbot-postgres -n todo-app &> /dev/null; then
    echo "✅ All services exist"
else
    echo "❌ Some services are missing"
    exit 1
fi

echo "Checking StatefulSet..."
if kubectl get statefulset todo-app-todo-chatbot-postgres -n todo-app &> /dev/null; then
    echo "✅ Database StatefulSet exists"
else
    echo "❌ Database StatefulSet does not exist"
    exit 1
fi

echo ""
echo "Test 7: Check pod statuses and logs"
echo "Checking pod statuses..."
POD_COUNT=$(kubectl get pods -n todo-app --no-headers 2>/dev/null | wc -l)
READY_PODS=$(kubectl get pods -n todo-app --no-headers 2>/dev/null | grep Running | wc -l)

echo "Total pods: $POD_COUNT, Ready pods: $READY_PODS"

if [ "$POD_COUNT" -eq "$READY_PODS" ]; then
    echo "✅ All pods are in Running state"
else
    echo "❌ Some pods are not in Running state"
    kubectl get pods -n todo-app
    exit 1
fi

echo "Checking for pod restarts..."
RESTARTS=$(kubectl get pods -n todo-app -o jsonpath='{range .items[*]}{.status.containerStatuses[*].restartCount}{"\n"}{end}' | tr ' ' '\n' | sort -nr | head -1)

if [ "$RESTARTS" -lt 5 ]; then
    echo "✅ Pod restarts are reasonable (max: $RESTARTS)"
else
    echo "⚠️  High number of pod restarts detected (max: $RESTARTS)"
fi

echo ""
echo "Test 8: Test service connectivity"
echo "Testing internal service connectivity..."

# Create a test pod to check connectivity
kubectl run connectivity-test --image=curlimages/curl:latest -n todo-app --rm -it --restart=Never -- \
    sh -c 'echo "Testing backend health..." && curl -s -f http://todo-app-todo-chatbot-backend:8000/health && echo "Backend OK"' || {
    echo "❌ Backend connectivity test failed"
    exit 1
}

echo "✅ Service connectivity test passed"

echo ""
echo "Test 9: Check resource limits and requests"
echo "Checking resource configurations..."

BACKEND_RESOURCES=$(kubectl get deployment todo-app-todo-chatbot-backend -n todo-app -o jsonpath='{.spec.template.spec.containers[0].resources}' 2>/dev/null)
FRONTEND_RESOURCES=$(kubectl get deployment todo-app-todo-chatbot-frontend -n todo-app -o jsonpath='{.spec.template.spec.containers[0].resources}' 2>/dev/null)

if [ -n "$BACKEND_RESOURCES" ] && [ -n "$FRONTEND_RESOURCES" ]; then
    echo "✅ Resource configurations exist for deployments"
else
    echo "⚠️  Resource configurations may be missing"
fi

echo ""
echo "Test 10: Check Horizontal Pod Autoscaler (if enabled)"
if kubectl get hpa -n todo-app &> /dev/null; then
    echo "HPA configurations:"
    kubectl get hpa -n todo-app
    echo "✅ HPA resources exist"
else
    echo "ℹ️  HPA not enabled in this configuration"
fi

echo ""
echo "Test 11: Check Pod Disruption Budget (if enabled)"
if kubectl get pdb -n todo-app &> /dev/null; then
    echo "PDB configurations:"
    kubectl get pdb -n todo-app
    echo "✅ PDB resources exist"
else
    echo "ℹ️  PDB not enabled in this configuration"
fi

echo ""
echo "Test 12: Final status check"
echo "Final resource status:"
kubectl get all -n todo-app

echo ""
echo "=========================================="
echo "All tests passed! 🎉"
echo "=========================================="
echo ""
echo "Deployment Summary:"
echo "- Namespace: todo-app"
echo "- Backend: $(kubectl get deployment todo-app-todo-chatbot-backend -n todo-app -o jsonpath='{.status.readyReplicas}/{.spec.replicas}') replicas ready"
echo "- Frontend: $(kubectl get deployment todo-app-todo-chatbot-frontend -n todo-app -o jsonpath='{.status.readyReplicas}/{.spec.replicas}') replicas ready"
echo "- Database: $(kubectl get statefulset todo-app-todo-chatbot-postgres -n todo-app -o jsonpath='{.status.readyReplicas}/{.spec.replicas}') replicas ready"
echo "- Total pods: $(kubectl get pods -n todo-app --no-headers | wc -l)"
echo "- All pods running: Yes"
echo ""
echo "To access the application:"
echo "1. Add to /etc/hosts: $(minikube ip) todo.local"
echo "2. Access frontend at: http://todo.local"
echo ""
echo "To check logs:"
echo "kubectl logs -f deployment/todo-app-todo-chatbot-backend -n todo-app"
echo "kubectl logs -f deployment/todo-app-todo-chatbot-frontend -n todo-app"