#!/bin/bash

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Starting Kubernetes deployment...${NC}"
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}kubectl is not installed or not in PATH${NC}"
    exit 1
fi

# Check if Minikube is running
if ! minikube status &> /dev/null; then
    echo -e "${RED}Minikube is not running. Start it with: minikube start${NC}"
    exit 1
fi

# Create namespace
echo -e "${YELLOW}Creating namespace...${NC}"
kubectl apply -f k8s/base/namespace.yaml

# Wait for namespace to be ready
sleep 2

# Apply base configurations
echo -e "${YELLOW}Applying base configurations...${NC}"
kubectl apply -f k8s/base/configmap.yaml
kubectl apply -f k8s/base/secrets.yaml

# Apply backend components
echo -e "${YELLOW}Deploying backend...${NC}"
kubectl apply -f k8s/backend/deployment.yaml
kubectl apply -f k8s/backend/service.yaml

# Apply MCP server components
echo -e "${YELLOW}Deploying MCP server...${NC}"
kubectl apply -f k8s/mcp-server/deployment.yaml
kubectl apply -f k8s/mcp-server/service.yaml

# Apply frontend components
echo -e "${YELLOW}Deploying frontend...${NC}"
kubectl apply -f k8s/frontend/deployment.yaml
kubectl apply -f k8s/frontend/service.yaml

# Apply ingress
echo -e "${YELLOW}Applying ingress...${NC}"
kubectl apply -f k8s/ingress/ingress.yaml

# Apply network policies
echo -e "${YELLOW}Applying network policies...${NC}"
kubectl apply -f k8s/network/network-policy.yaml
kubectl apply -f k8s/network/pdb.yaml

echo ""
echo -e "${GREEN}Deployment completed!${NC}"
echo ""
echo "Check deployment status with:"
echo "kubectl get pods -n todo-chatbot"
echo "kubectl get services -n todo-chatbot"
echo "kubectl get ingress -n todo-chatbot"