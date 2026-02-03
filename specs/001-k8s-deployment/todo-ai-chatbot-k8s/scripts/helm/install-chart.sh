#!/bin/bash

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Installing Helm chart for Todo AI Chatbot...${NC}"
echo ""

# Check if Helm is available
if ! command -v helm &> /dev/null; then
    echo -e "${RED}Helm is not installed or not in PATH${NC}"
    exit 1
fi

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

RELEASE_NAME=${1:-"todo-chatbot"}
NAMESPACE=${2:-"todo-chatbot"}

echo -e "${YELLOW}Using release name: $RELEASE_NAME${NC}"
echo -e "${YELLOW}Using namespace: $NAMESPACE${NC}"

# Create namespace if it doesn't exist
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Install the Helm chart
echo -e "${YELLOW}Installing Helm chart...${NC}"
helm install $RELEASE_NAME helm/todo-chatbot/ \
    --namespace $NAMESPACE \
    --values helm/todo-chatbot/values.yaml \
    --wait \
    --timeout=10m

echo ""
echo -e "${GREEN}Helm chart installed successfully!${NC}"
echo ""
echo "Check the release status with:"
echo "helm status $RELEASE_NAME -n $NAMESPACE"
echo ""
echo "View deployed resources with:"
echo "kubectl get all -n $NAMESPACE"
echo "kubectl get ingress -n $NAMESPACE"