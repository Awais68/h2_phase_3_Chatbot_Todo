#!/bin/bash

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "====================================="
echo "Docker Image Security Scan"
echo "====================================="
echo ""

# Images to scan
IMAGES=("todo-backend:latest" "todo-mcp-server:latest" "todo-frontend:latest")

# Check if docker scan is available
if docker scan --help &> /dev/null 2>&1; then
    SCANNER="docker scan"
elif command -v trivy &> /dev/null; then
    SCANNER="trivy"
else
    echo -e "${YELLOW}No security scanner found${NC}"
    echo "Install Trivy: brew install trivy"
    echo "Or use Docker scan (requires Docker Scout)"
    exit 1
fi

for IMAGE in "${IMAGES[@]}"; do
    echo -e "${YELLOW}Scanning $IMAGE...${NC}"
    echo ""

    if [ "$SCANNER" = "docker scan" ]; then
        docker scan $IMAGE || true
    else
        trivy image $IMAGE || true
    fi

    echo ""
    echo "-----------------------------------"
    echo ""
done

echo -e "${GREEN}Security scan complete!${NC}"