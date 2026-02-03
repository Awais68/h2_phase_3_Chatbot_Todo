#!/bin/bash

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Loading images to Minikube...${NC}"
echo ""

# Check Minikube is running
if ! minikube status | grep -q "Running"; then
    echo "Error: Minikube is not running. Start it with: minikube start"
    exit 1
fi

# Images to load
IMAGES=(
    "todo-backend:latest"
    "todo-mcp-server:latest"
    "todo-frontend:latest"
)

# Load each image
for IMAGE in "${IMAGES[@]}"; do
    echo -e "${YELLOW}Loading $IMAGE...${NC}"
    minikube image load $IMAGE
    echo -e "${GREEN}✓ $IMAGE loaded${NC}"
    echo ""
done

echo -e "${GREEN}All images loaded to Minikube!${NC}"
echo ""
echo "Verify with: minikube ssh docker images | grep todo-"