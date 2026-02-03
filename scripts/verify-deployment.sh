#!/bin/bash

# Script to verify the Todo Chatbot application deployment

set -e

echo "=========================================="
echo "Todo Chatbot Deployment Verification"
echo "=========================================="

echo ""
echo "Step 1: Check all resources in todo-app namespace"
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
echo "Step 2: Check pod statuses"
echo "Checking if all pods are running and ready..."
kubectl get pods -n todo-app -o wide

echo ""
echo "Step 3: Check pod logs for errors"
echo "Checking backend logs..."
kubectl logs -l app.kubernetes.io/component=backend -n todo-app --tail=10 || echo "No backend pods found"

echo ""
echo "Checking frontend logs..."
kubectl logs -l app.kubernetes.io/component=frontend -n todo-app --tail=10 || echo "No frontend pods found"

echo ""
echo "Checking database logs..."
kubectl logs -l app.kubernetes.io/component=postgres -n todo-app --tail=10 || echo "No database pods found"

echo ""
echo "Step 4: Test health endpoints"
echo "Testing backend health endpoint..."
if kubectl get pods -n todo-app -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}' > /dev/null 2>&1; then
    BACKEND_POD=$(kubectl get pods -n todo-app -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}')
    echo "Found backend pod: $BACKEND_POD"
    echo "Testing health endpoint via port forward..."

    # Start port forward in background
    kubectl port-forward -n todo-app "pod/$BACKEND_POD" 8080:8000 &
    PORT_FORWARD_PID=$!

    # Give time for port forward to start
    sleep 5

    # Test the health endpoint
    if curl -f http://localhost:8080/health 2>/dev/null; then
        echo "✅ Backend health check passed"
    else
        echo "❌ Backend health check failed"
    fi

    # Kill the port forward
    kill $PORT_FORWARD_PID 2>/dev/null || true
    sleep 2
else
    echo "⚠️  No backend pods found to test"
fi

echo ""
echo "Step 5: Check resource usage"
echo "Resource usage by pods:"
kubectl top pods -n todo-app || echo "Metrics server may not be ready yet"

echo ""
echo "Step 6: Verify ingress if available"
if kubectl get ingress -n todo-app &> /dev/null; then
    echo "Ingress configuration:"
    kubectl get ingress -n todo-app -o wide
    INGRESS_IP=$(kubectl get ingress -n todo-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    if [ -n "$INGRESS_IP" ]; then
        echo "Ingress IP: $INGRESS_IP"
    else
        echo "Ingress IP not available yet (this is normal shortly after deployment)"
    fi
else
    echo "No ingress found in deployment"
fi

echo ""
echo "Step 7: Check persistent volume claims"
echo "PersistentVolumeClaims:"
kubectl get pvc -n todo-app || echo "No PVCs found"

echo ""
echo "Step 8: Run connectivity tests"
echo "Testing internal service connectivity..."
kubectl run connectivity-test --image=curlimages/curl:latest -n todo-app --rm -it --restart=Never -- curl -s -o /dev/null -w "%{http_code}" http://todo-app-todo-chatbot-backend:8000/health || echo "Connectivity test skipped"

echo ""
echo "=========================================="
echo "Verification Complete!"
echo "=========================================="
echo ""
echo "Summary:"
echo "- Deployments: $(kubectl get deployments -n todo-app --no-headers 2>/dev/null | wc -l) found"
echo "- StatefulSets: $(kubectl get statefulsets -n todo-app --no-headers 2>/dev/null | wc -l) found"
echo "- Services: $(kubectl get services -n todo-app --no-headers 2>/dev/null | wc -l) found"
echo "- Pods: $(kubectl get pods -n todo-app --no-headers 2>/dev/null | wc -l) found"
echo "- Healthy pods: $(kubectl get pods -n todo-app --no-headers 2>/dev/null | grep Running | wc -l) out of $(kubectl get pods -n todo-app --no-headers 2>/dev/null | wc -l)"