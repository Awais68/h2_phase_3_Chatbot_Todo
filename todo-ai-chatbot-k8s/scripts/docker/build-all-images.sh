#!/bin/bash

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "====================================="
echo "Building All Docker Images"
echo "====================================="
echo ""

# Build backend image
echo -e "${YELLOW}Building backend image...${NC}"
if [ -d "../backend" ]; then
    docker build -t todo-backend:latest ../backend
    echo -e "${GREEN}✓ Backend image built${NC}"
else
    echo "Backend directory not found, skipping backend build"
fi
echo ""

# Build MCP server image
echo -e "${YELLOW}Building MCP server image...${NC}"
if [ -f "docker/mcp-server/Dockerfile" ]; then
    # Copy backend directory to a temporary location and build MCP server from it
    TEMP_MCP_DIR=$(mktemp -d)
    cp -r ../backend/* $TEMP_MCP_DIR/
    cp -r docker/mcp-server/Dockerfile $TEMP_MCP_DIR/
    docker build -t todo-mcp-server:latest -f $TEMP_MCP_DIR/Dockerfile $TEMP_MCP_DIR
    rm -rf $TEMP_MCP_DIR
    echo -e "${GREEN}✓ MCP server image built${NC}"
else
    echo "MCP server Dockerfile not found, skipping MCP server build"
fi
echo ""

# Build frontend image
echo -e "${YELLOW}Building frontend image...${NC}"
if [ -d "../frontend" ]; then
    docker build -t todo-frontend:latest ../frontend
    echo -e "${GREEN}✓ Frontend image built${NC}"
else
    echo "Frontend directory not found, skipping frontend build"
fi
echo ""

echo -e "${GREEN}All images built successfully!${NC}"
echo ""
echo "Built images:"
docker images | grep todo- | grep latest