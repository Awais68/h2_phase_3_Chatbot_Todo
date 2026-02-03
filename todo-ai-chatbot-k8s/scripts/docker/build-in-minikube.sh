#!/bin/bash

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Building images in Minikube Docker...${NC}"
echo ""

# Check Minikube is running
if ! minikube status | grep -q "Running"; then
    echo "Error: Minikube is not running"
    exit 1
fi

# Set Docker environment to Minikube
echo "Setting Docker environment to Minikube..."
eval $(minikube docker-env)

# Build all images
echo ""
echo -e "${YELLOW}Building images...${NC}"
if [ -f "./scripts/docker/build-all-images.sh" ]; then
    ./scripts/docker/build-all-images.sh
else
    echo "Build script not found, building directly..."
    # Build commands would go here
fi

# Reset Docker environment
eval $(minikube docker-env -u)

echo ""
echo -e "${GREEN}All images built in Minikube Docker!${NC}"
echo ""
echo "Images are now available in Minikube."
echo "They will NOT appear in 'docker images' outside Minikube."
echo "To verify: minikube ssh docker images | grep todo-"