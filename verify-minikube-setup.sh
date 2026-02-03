#!/bin/bash

echo "=========================================="
echo "Minikube Verification Script"
echo "=========================================="

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Checking Minikube Installation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v minikube &> /dev/null; then
    MINIKUBE_VERSION=$(minikube version | grep -o "v[0-9.]*")
    echo "✓ Minikube is installed: $MINIKUBE_VERSION"
    if [[ $(echo $MINIKUBE_VERSION | cut -d. -f2) -ge 32 ]]; then
        echo "✓ Minikube version is adequate (${MINIKUBE_VERSION})"
    else
        echo "⚠ Minikube version is older than recommended (1.32.0+)"
    fi
else
    echo "❌ Minikube is not installed"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. Checking Cluster Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if minikube status | grep -q "Running"; then
    echo "✓ Minikube cluster is running"
    minikube status
else
    echo "❌ Minikube cluster is not running"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. Checking kubectl Connection"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if kubectl cluster-info &> /dev/null; then
    echo "✓ kubectl can connect to cluster"
    echo "ℹ Kubernetes control plane is running at $(kubectl cluster-info | grep 'is running at' | head -1)"
else
    echo "❌ kubectl cannot connect to cluster"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. Checking Nodes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
NODE_COUNT=$(kubectl get nodes | grep -c Ready || echo 0)
if [ $NODE_COUNT -ge 1 ]; then
    echo "✓ Found $NODE_COUNT node(s) in Ready status"
    kubectl get nodes
else
    echo "❌ No nodes in Ready status"
    kubectl get nodes
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. Checking System Pods"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
SYSTEM_PODS=$(kubectl get pods --all-namespaces | grep -c Running || echo 0)
if [ $SYSTEM_PODS -gt 0 ]; then
    echo "✓ Found $SYSTEM_PODS system pods running"
else
    echo "ℹ No system pods found (this may be normal depending on cluster state)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. Checking Metrics Server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if kubectl get pods -n kube-system | grep -q metrics-server; then
    METRICS_READY=$(kubectl get pods -n kube-system | grep metrics-server | awk '{print $2}' | cut -d'/' -f1)
    TOTAL_METRICS=$(kubectl get pods -n kube-system | grep metrics-server | awk '{print $2}' | cut -d'/' -f2)
    if [ "$METRICS_READY" = "$TOTAL_METRICS" ] && [ "$METRICS_READY" != "" ]; then
        echo "✓ Metrics server is running ($METRICS_READY/$TOTAL_METRICS ready)"
    else
        echo "⚠ Metrics server may not be fully ready ($METRICS_READY/$TOTAL_METRICS)"
    fi
else
    echo "❌ Metrics server not found"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. Checking Dashboard"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if kubectl get pods -n kubernetes-dashboard &> /dev/null; then
    DASHBOARD_READY=$(kubectl get pods -n kubernetes-dashboard | grep -c Running || echo 0)
    TOTAL_DASHBOARD=$(kubectl get pods -n kubernetes-dashboard | grep -c kubernetes-dashboard || echo 0)
    if [ $DASHBOARD_READY -ge 1 ]; then
        echo "✓ Dashboard is running ($DASHBOARD_READY/$TOTAL_DASHBOARD ready)"
    else
        echo "⚠ Dashboard pods exist but none are ready"
    fi
else
    echo "ℹ Dashboard may not be actively monitored"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "8. Checking Minikube IP"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
MINIKUBE_IP=$(minikube ip 2>/dev/null || echo "unknown")
if [ "$MINIKUBE_IP" != "unknown" ]; then
    echo "✓ Minikube IP: $MINIKUBE_IP"
else
    echo "⚠ Could not get Minikube IP"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "9. Testing DNS Resolution"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if kubectl run test-dns --image=busybox:1.28 --rm -it --restart=Never -- nslookup kubernetes.default &> /dev/null; then
    echo "✓ DNS resolution test passed"
else
    echo "⚠ DNS resolution test failed"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "10. Testing Metrics (if available)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if kubectl top nodes &> /dev/null; then
    echo "✓ Metrics API is working"
    kubectl top nodes 2>/dev/null | head -5
else
    echo "ℹ Metrics API may not be ready yet (this can take a few minutes)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Final Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

CRITICAL_CHECKS=0
if command -v minikube &> /dev/null; then ((CRITICAL_CHECKS++)); fi
if minikube status | grep -q "Running"; then ((CRITICAL_CHECKS++)); fi
if kubectl cluster-info &> /dev/null; then ((CRITICAL_CHECKS++)); fi
if [ $NODE_COUNT -ge 1 ]; then ((CRITICAL_CHECKS++)); fi

if [ $CRITICAL_CHECKS -eq 4 ]; then
    echo "✅ Minikube cluster is ready for Kubernetes deployment!"
    echo ""
    echo "Next steps:"
    echo "1. Build Docker images for your application"
    echo "2. Load images to Minikube"
    echo "3. Deploy your application using Kubernetes manifests or Helm"
    echo ""
    echo "Minikube IP: $MINIKUBE_IP"
    echo "To access the dashboard: minikube dashboard"
    exit 0
else
    echo "❌ Minikube cluster is not fully ready"
    echo "Critical checks passed: $CRITICAL_CHECKS/4"
    exit 1
fi