#!/bin/bash

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

NAMESPACE="todo-chatbot"

echo -e "${YELLOW}Verifying Todo AI Chatbot deployment...${NC}"
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}kubectl is not installed or not in PATH${NC}"
    exit 1
fi

# Check if namespace exists
if ! kubectl get namespace $NAMESPACE &> /dev/null; then
    echo -e "${RED}Namespace $NAMESPACE does not exist${NC}"
    exit 1
fi

# Check if all required deployments exist
REQUIRED_DEPLOYMENTS=("backend-deployment" "mcp-server-deployment" "frontend-deployment")

echo -e "${YELLOW}Checking required deployments...${NC}"
ALL_DEPLOYMENTS_EXIST=true

for deployment in "${REQUIRED_DEPLOYMENTS[@]}"; do
    if kubectl get deployment $deployment -n $NAMESPACE &> /dev/null; then
        echo -e "${GREEN}✓ $deployment exists${NC}"
    else
        echo -e "${RED}✗ $deployment does not exist${NC}"
        ALL_DEPLOYMENTS_EXIST=false
    fi
done

if [ "$ALL_DEPLOYMENTS_EXIST" = false ]; then
    echo -e "${RED}Some required deployments are missing${NC}"
    exit 1
fi

# Check if all required services exist
REQUIRED_SERVICES=("backend-service" "mcp-server-service" "frontend-service")

echo ""
echo -e "${YELLOW}Checking required services...${NC}"
ALL_SERVICES_EXIST=true

for service in "${REQUIRED_SERVICES[@]}"; do
    if kubectl get service $service -n $NAMESPACE &> /dev/null; then
        echo -e "${GREEN}✓ $service exists${NC}"
    else
        echo -e "${RED}✗ $service does not exist${NC}"
        ALL_SERVICES_EXIST=false
    fi
done

if [ "$ALL_SERVICES_EXIST" = false ]; then
    echo -e "${RED}Some required services are missing${NC}"
    exit 1
fi

# Check if ingress exists
echo ""
echo -e "${YELLOW}Checking ingress...${NC}"
if kubectl get ingress todo-chatbot-ingress -n $NAMESPACE &> /dev/null; then
    echo -e "${GREEN}✓ Ingress exists${NC}"
else
    echo -e "${YELLOW}~ Ingress does not exist${NC}"
fi

# Check if pods are running and ready
echo ""
echo -e "${YELLOW}Checking pod status...${NC}"
ALL_PODS_READY=true

for deployment in "${REQUIRED_DEPLOYMENTS[@]}"; do
    # Get the app label from deployment
    APP_LABEL=$(kubectl get deployment $deployment -n $NAMESPACE -o jsonpath='{.spec.selector.matchLabels.app}')

    # Get pods for this deployment
    PODS=$(kubectl get pods -n $NAMESPACE -l app=$APP_LABEL -o jsonpath='{.items[*].metadata.name}')

    if [ -z "$PODS" ]; then
        echo -e "${RED}✗ No pods found for $deployment (app=$APP_LABEL)${NC}"
        ALL_PODS_READY=false
        continue
    fi

    for pod in $PODS; do
        READY_STATUS=$(kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.status.containerStatuses[*].ready}' | tr ' ' '\n' | grep -c true)
        TOTAL_CONTAINERS=$(kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.status.containerStatuses[*]}' | wc -w)
        POD_STATUS=$(kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.status.phase}')

        if [ "$READY_STATUS" -eq "$TOTAL_CONTAINERS" ] && [ "$POD_STATUS" = "Running" ]; then
            echo -e "${GREEN}✓ $pod: $POD_STATUS ($READY_STATUS/$TOTAL_CONTAINERS ready)${NC}"
        else
            echo -e "${RED}✗ $pod: $POD_STATUS ($READY_STATUS/$TOTAL_CONTAINERS ready)${NC}"
            ALL_PODS_READY=false
        fi
    done
done

if [ "$ALL_PODS_READY" = false ]; then
    echo -e "${RED}Some pods are not ready${NC}"
    exit 1
fi

# Check if services are accessible
echo ""
echo -e "${YELLOW}Checking service accessibility...${NC}"
ALL_SERVICES_ACCESSIBLE=true

for service in "${REQUIRED_SERVICES[@]}"; do
    SERVICE_TYPE=$(kubectl get service $service -n $NAMESPACE -o jsonpath='{.spec.type}')
    SERVICE_PORT=$(kubectl get service $service -n $NAMESPACE -o jsonpath='{.spec.ports[0].port}')

    if [ "$SERVICE_TYPE" = "ClusterIP" ]; then
        # For ClusterIP services, just check if they're created with a valid IP
        SERVICE_IP=$(kubectl get service $service -n $NAMESPACE -o jsonpath='{.spec.clusterIP}')
        if [ "$SERVICE_IP" != "<none>" ] && [ -n "$SERVICE_IP" ]; then
            echo -e "${GREEN}✓ $service: $SERVICE_TYPE ($SERVICE_IP:$SERVICE_PORT)${NC}"
        else
            echo -e "${RED}✗ $service: $SERVICE_TYPE (invalid IP: $SERVICE_IP)${NC}"
            ALL_SERVICES_ACCESSIBLE=false
        fi
    elif [ "$SERVICE_TYPE" = "NodePort" ]; then
        # For NodePort services, check if they have a valid node port
        NODE_PORT=$(kubectl get service $service -n $NAMESPACE -o jsonpath='{.spec.ports[0].nodePort}')
        if [ "$NODE_PORT" != "<none>" ] && [ -n "$NODE_PORT" ]; then
            MINIKUBE_IP=$(minikube ip 2>/dev/null || echo "127.0.0.1")
            echo -e "${GREEN}✓ $service: $SERVICE_TYPE ($MINIKUBE_IP:$NODE_PORT)${NC}"
        else
            echo -e "${RED}✗ $service: $SERVICE_TYPE (invalid node port: $NODE_PORT)${NC}"
            ALL_SERVICES_ACCESSIBLE=false
        fi
    else
        echo -e "${YELLOW}~ $service: $SERVICE_TYPE (type not fully validated)${NC}"
    fi
done

if [ "$ALL_SERVICES_ACCESSIBLE" = false ]; then
    echo -e "${RED}Some services are not accessible${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ All verifications passed!${NC}"
echo ""
echo -e "${GREEN}Todo AI Chatbot deployment is ready.${NC}"
echo ""
echo "You can access the application via:"
echo "- Frontend: $(minikube ip):30080 (if NodePort service is used)"
echo "- Check all services with: kubectl get services -n $NAMESPACE"
echo "- Check all pods with: kubectl get pods -n $NAMESPACE"