#!/bin/bash
set -e

# Final validation script for Todo AI Chatbot Kubernetes deployment

echo "🔍 Starting final validation of Todo AI Chatbot Kubernetes deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    log_error "kubectl is not installed or not in PATH"
    exit 1
fi

# Check if Helm is available
if ! command -v helm &> /dev/null; then
    log_error "Helm is not installed or not in PATH"
    exit 1
fi

# Check if namespace exists
if ! kubectl get namespace todo-chatbot &> /dev/null; then
    log_error "Namespace 'todo-chatbot' does not exist"
    exit 1
fi
log_success "Namespace 'todo-chatbot' exists"

# Check deployments
deployments=("frontend-deployment" "backend-deployment" "mcp-deployment")
for deployment in "${deployments[@]}"; do
    if ! kubectl get deployment "$deployment" -n todo-chatbot &> /dev/null; then
        log_error "Deployment '$deployment' does not exist"
        exit 1
    fi

    # Check if deployment is ready
    ready_replicas=$(kubectl get deployment "$deployment" -n todo-chatbot -o jsonpath='{.status.readyReplicas}')
    desired_replicas=$(kubectl get deployment "$deployment" -n todo-chatbot -o jsonpath='{.spec.replicas}')

    if [ "$ready_replicas" != "$desired_replicas" ] || [ "$ready_replicas" -eq 0 ]; then
        log_error "Deployment '$deployment' is not ready ($ready_replicas/$desired_replicas ready)"
        exit 1
    fi
    log_success "Deployment '$deployment' is ready ($ready_replicas/$desired_replicas)"
done

# Check services
services=("frontend-service" "backend-service" "mcp-service")
for service in "${services[@]}"; do
    if ! kubectl get service "$service" -n todo-chatbot &> /dev/null; then
        log_error "Service '$service' does not exist"
        exit 1
    fi
    log_success "Service '$service' exists"
done

# Check ingress
if kubectl get ingress todo-chatbot-ingress -n todo-chatbot &> /dev/null; then
    log_success "Ingress 'todo-chatbot-ingress' exists"
else
    log_warn "Ingress 'todo-chatbot-ingress' does not exist"
fi

# Check HPA if enabled
hpas=("frontend-hpa" "backend-hpa" "mcp-hpa")
for hpa in "${hpas[@]}"; do
    if kubectl get hpa "$hpa" -n todo-chatbot &> /dev/null; then
        log_success "HPA '$hpa' exists"
    else
        log_warn "HPA '$hpa' does not exist (autoscaling may be disabled)"
    fi
done

# Check pods status
log_info "Checking pod status..."
pods=$(kubectl get pods -n todo-chatbot -o jsonpath='{.items[*].metadata.name}')
for pod in $pods; do
    status=$(kubectl get pod "$pod" -n todo-chatbot -o jsonpath='{.status.phase}')
    if [ "$status" != "Running" ]; then
        log_error "Pod '$pod' is not running (status: $status)"
        exit 1
    fi

    # Check if all containers in pod are ready
    ready_containers=$(kubectl get pod "$pod" -n todo-chatbot -o jsonpath='{.status.containerStatuses[*].ready}' | tr ' ' '\n' | grep -c true)
    total_containers=$(kubectl get pod "$pod" -n todo-chatbot -o jsonpath='{.spec.containers[*].name}' | wc -w)

    if [ "$ready_containers" -ne "$total_containers" ]; then
        log_error "Pod '$pod' has unready containers ($ready_containers/$total_containers ready)"
        exit 1
    fi
done
log_success "All pods are running and ready"

# Check Helm release
if helm status todo-chatbot -n todo-chatbot &> /dev/null; then
    log_success "Helm release 'todo-chatbot' is deployed"
else
    log_warn "Helm release 'todo-chatbot' not found"
fi

# Display summary
log_info "📋 Deployment Summary:"
echo ""
kubectl get all -n todo-chatbot
echo ""

# Display ingress info if available
if kubectl get ingress todo-chatbot-ingress -n todo-chatbot &> /dev/null; then
    log_info "🌐 Ingress Information:"
    kubectl get ingress todo-chatbot-ingress -n todo-chatbot -o wide
    echo ""
fi

log_success "🎉 All validation checks passed!"
log_success "Todo AI Chatbot is successfully deployed to Kubernetes!"

echo ""
echo "🚀 Next Steps:"
echo "1. Add ingress IP to /etc/hosts: <INGRESS_IP> todo-chatbot.local api.todo-chatbot.local mcp.todo-chatbot.local"
echo "2. Access frontend at: https://todo-chatbot.local"
echo "3. Access API at: https://api.todo-chatbot.local"
echo "4. Access MCP at: https://mcp.todo-chatbot.local"
echo ""
echo "🔧 For operations, refer to docs/KUBERNETES_DEPLOYMENT_GUIDE.md"
echo "📊 For completion summary, see docs/KUBERNETES_DEPLOYMENT_COMPLETION_SUMMARY.md"