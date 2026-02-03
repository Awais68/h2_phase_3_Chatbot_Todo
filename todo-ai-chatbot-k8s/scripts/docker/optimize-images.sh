#!/bin/bash

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "====================================="
echo "Docker Image Optimization"
echo "====================================="
echo ""

# Images to analyze
IMAGES=("todo-backend:latest" "todo-mcp-server:latest" "todo-frontend:latest")

# Check if Gordon is available
if command -v docker &> /dev/null && docker ai --help &> /dev/null 2>&1; then
    echo -e "${GREEN}Docker AI available - using for optimization${NC}"
    USE_AI=true
else
    echo -e "${YELLOW}Docker AI not available - using manual tools${NC}"
    USE_AI=false
fi

echo ""

for IMAGE in "${IMAGES[@]}"; do
    echo -e "${YELLOW}Analyzing $IMAGE...${NC}"

    # Get current size
    if command -v docker &> /dev/null && docker images --format "{{.Size}}" $IMAGE &> /dev/null; then
        SIZE=$(docker images --format "{{.Size}}" $IMAGE)
        echo "Current size: $SIZE"
    else
        echo "Could not get image size"
    fi

    if [ "$USE_AI" = true ]; then
        # Use Docker AI for recommendations if available
        echo ""
        echo "Getting Docker AI recommendations..."
        docker ai "analyze $IMAGE and suggest optimizations" 2>/dev/null || true
    else
        # Manual analysis
        echo ""
        echo "Running manual analysis..."

        # Check for common issues
        echo "Checking for optimization opportunities..."

        # List layers
        if command -v docker &> /dev/null; then
            docker history $IMAGE --no-trunc | head -20
        fi
    fi

    echo ""
    echo "-----------------------------------"
    echo ""
done

echo -e "${GREEN}Optimization analysis complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Review recommendations"
echo "2. Update Dockerfiles with optimizations"
echo "3. Rebuild images"
echo "4. Compare sizes"