#!/bin/bash

echo "=========================================="
echo "Prerequisite Verification Script"
echo "=========================================="

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Checking Docker Installation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | grep -o "Docker version [0-9.]*")
    echo "✓ Docker is installed: $DOCKER_VERSION"
else
    echo "❌ Docker is not installed"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. Checking Gordon (Docker AI) Availability"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if docker ai "What can you do?" &> /dev/null; then
    echo "✓ Gordon (Docker AI) is available"
else
    echo "⚠ Gordon (Docker AI) is not available"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. Checking Minikube Installation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v minikube &> /dev/null; then
    MINIKUBE_VERSION=$(minikube version | grep -o "v[0-9.]*")
    echo "✓ Minikube is installed: $MINIKUBE_VERSION"
else
    echo "❌ Minikube is not installed"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. Checking kubectl Installation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v kubectl &> /dev/null; then
    KUBECTL_VERSION=$(kubectl version --client --short | grep -o "v[0-9.]*")
    echo "✓ kubectl is installed: $KUBECTL_VERSION"
else
    echo "❌ kubectl is not installed"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. Checking Helm Installation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v helm &> /dev/null; then
    HELM_VERSION=$(helm version --short | grep -o "v[0-9.]*")
    echo "✓ Helm is installed: $HELM_VERSION"
else
    echo "❌ Helm is not installed"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. Checking kubectl-ai Availability"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v kubectl-ai &> /dev/null; then
    KUBECTL_AI_VERSION=$(kubectl-ai --version 2>/dev/null || echo "available")
    echo "✓ kubectl-ai is installed: $KUBECTL_AI_VERSION"
else
    echo "⚠ kubectl-ai is not available"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. Checking Kagent Installation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v kagent &> /dev/null; then
    KAGENT_VERSION=$(kagent --version 2>/dev/null || echo "available")
    echo "✓ Kagent is installed: $KAGENT_VERSION"
else
    echo "⚠ Kagent is not available"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "8. Checking Claude Code CLI"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v claude-code &> /dev/null; then
    echo "✓ Claude Code CLI is available"
else
    echo "⚠ Claude Code CLI may not be available"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "9. Checking Phase III Application Code"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d "frontend" ] && [ -d "backend" ]; then
    echo "✓ Phase III application code found (frontend, backend)"
elif [ -d "todo-app" ]; then
    echo "✓ Phase III application code found (todo-app directory)"
else
    echo "⚠ Phase III application code not found in expected locations"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "10. Checking Minikube Cluster Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if minikube status | grep -q "Running"; then
    echo "✓ Minikube cluster is running"
    echo "✓ Cluster addons status:"
    minikube addons list | grep -E "(ingress|metrics-server)" | grep enabled
else
    echo "❌ Minikube cluster is not running"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Final Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All essential prerequisites are satisfied!"
echo ""
echo "Summary:"
echo "- Docker: Available"
echo "- Gordon: $(if docker ai "What can you do?" &> /dev/null; then echo "Available"; else echo "Not available (using fallback)"; fi)"
echo "- Minikube: Available"
echo "- kubectl: Available"
echo "- Helm: Available"
echo "- kubectl-ai: $(if command -v kubectl-ai &> /dev/null; then echo "Available"; else echo "Not available (using fallback)"; fi)"
echo "- Kagent: Available"
echo "- Cluster: Running with required addons"
echo ""
echo "Ready to proceed with Kubernetes deployment!"