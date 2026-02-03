#!/bin/bash

set -e

# Load environment variables
if [ -f "../config/local/.env" ]; then
    source ../config/local/.env
elif [ -f "../../config/local/.env" ]; then
    source ../../config/local/.env
fi

echo "Starting MCP server container for testing..."

# Set default values if environment variables aren't loaded
: "${DATABASE_URL:=postgresql://user:password@localhost:5432/todo_test}"

# Run MCP container
CONTAINER_ID=$(docker run -d \
    --name test-mcp \
    -p 3000:3000 \
    -e DATABASE_URL="$DATABASE_URL" \
    -e MCP_SERVER_PORT="3000" \
    -e LOG_LEVEL="INFO" \
    todo-mcp-server:latest)

echo "Container ID: $CONTAINER_ID"

# Wait for container to start
echo "Waiting for MCP server to start..."
sleep 5

# Check if container is running
if ! docker ps | grep -q test-mcp; then
    echo "Error: MCP container not running"
    docker logs test-mcp
    docker rm -f test-mcp
    exit 1
fi

# Test port is open
echo "Testing TCP connection..."
if timeout 5 bash -c "</dev/tcp/localhost/3000" &>/dev/null; then
    echo "✓ MCP server port is open"
else
    echo "✗ Cannot connect to MCP server"
    docker logs test-mcp
    docker rm -f test-mcp
    exit 1
fi

# Check logs for successful startup
echo "Checking logs..."
docker logs test-mcp

# Test that container is running
if docker ps | grep -q test-mcp; then
    echo "✓ MCP container is running"
else
    echo "✗ MCP container is not running"
    docker rm -f test-mcp
    exit 1
fi

# Cleanup
echo "Cleaning up..."
docker rm -f test-mcp

echo "MCP container tests passed!"
exit 0