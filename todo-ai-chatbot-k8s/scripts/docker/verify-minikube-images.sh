#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "Verifying images in Minikube..."
echo ""

# Check Minikube is running
if ! minikube status | grep -q "Running"; then
    echo -e "${RED}Error: Minikube is not running${NC}"
    exit 1
fi

# Images to verify
IMAGES=(
    "todo-backend"
    "todo-mcp-server"
    "todo-frontend"
)

ALL_FOUND=true

for IMAGE in "${IMAGES[@]}"; do
    if minikube ssh docker images | grep -q "$IMAGE"; then
        echo -e "${GREEN}✓${NC} $IMAGE:latest found in Minikube"
    else
        echo -e "${RED}✗${NC} $IMAGE:latest NOT found in Minikube"
        ALL_FOUND=false
    fi
done

echo ""

if [ "$ALL_FOUND" = true ]; then
    echo -e "${GREEN}All images verified in Minikube!${NC}"
    echo ""
    echo "Full image list in Minikube:"
    minikube ssh docker images | grep todo-
    exit 0
else
    echo -e "${RED}Some images missing. Please load or build them.${NC}"
    exit 1
fi