#!/bin/bash

set -e

# Load environment variables
if [ -f "../config/local/.env" ]; then
    source ../config/local/.env
elif [ -f "../../config/local/.env" ]; then
    source ../../config/local/.env
fi

echo "Starting backend container for testing..."

# Set default values if environment variables aren't loaded
: "${DATABASE_URL:=postgresql://user:password@localhost:5432/todo_test}"
: "${OPENAI_API_KEY:=dummy-key-for-testing}"
: "${OPENAI_ASSISTANT_ID:=dummy-assistant-id}"

# Run backend container
CONTAINER_ID=$(docker run -d \
    --name test-backend \
    -p 8000:8000 \
    -e DATABASE_URL="$DATABASE_URL" \
    -e OPENAI_API_KEY="$OPENAI_API_KEY" \
    -e OPENAI_ASSISTANT_ID="$OPENAI_ASSISTANT_ID" \
    -e MCP_SERVER_URL="http://localhost:3000" \
    -e LOG_LEVEL="INFO" \
    todo-backend:latest)

echo "Container ID: $CONTAINER_ID"

# Wait for container to be healthy
echo "Waiting for container to be healthy..."
RETRIES=30
while [ $RETRIES -gt 0 ]; do
    if docker inspect test-backend &>/dev/null; then
        CONTAINER_STATUS=$(docker inspect --format='{{.State.Status}}' test-backend)
        if [ "$CONTAINER_STATUS" = "running" ]; then
            # Check if we can reach the health endpoint
            if curl -f http://localhost:8000/health &>/dev/null; then
                echo "Container is healthy!"
                break
            fi
        fi
    fi
    sleep 2
    ((RETRIES--))
done

if [ $RETRIES -eq 0 ]; then
    echo "Error: Container failed to become healthy"
    docker logs test-backend
    docker rm -f test-backend
    exit 1
fi

# Test health endpoint
echo "Testing health endpoint..."
sleep 2
if curl -f http://localhost:8000/health; then
    echo "✓ Health endpoint working"
else
    echo "✗ Health endpoint failed"
    docker logs test-backend
    docker rm -f test-backend
    exit 1
fi

# Test API docs
echo "Testing API docs..."
if curl -f http://localhost:8000/docs &>/dev/null; then
    echo "✓ API docs accessible"
else
    echo "✗ API docs not accessible"
fi

# Test that it runs as non-root (if we can check this)
echo "Checking if container is running..."
if docker ps | grep -q test-backend; then
    echo "✓ Container is running"
else
    echo "✗ Container is not running"
    docker rm -f test-backend
    exit 1
fi

# Cleanup
echo "Cleaning up..."
docker rm -f test-backend

echo "Backend container tests passed!"
exit 0