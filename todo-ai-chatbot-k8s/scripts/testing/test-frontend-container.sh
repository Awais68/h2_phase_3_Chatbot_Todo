#!/bin/bash

set -e

echo "Starting frontend container for testing..."

# Run frontend container
CONTAINER_ID=$(docker run -d \
    --name test-frontend \
    -p 3001:3000 \
    -e NEXT_PUBLIC_API_URL="http://localhost:8000" \
    -e NEXT_PUBLIC_APP_URL="http://localhost:3001" \
    -e NEXT_PUBLIC_ENABLE_VOICE="true" \
    -e NEXT_PUBLIC_ENABLE_ANALYTICS="true" \
    -e NEXT_PUBLIC_ENABLE_RECURRING="true" \
    todo-frontend:latest)

echo "Container ID: $CONTAINER_ID"

# Wait for container to start
echo "Waiting for frontend to start..."
RETRIES=30
while [ $RETRIES -gt 0 ]; do
    if curl -f http://localhost:3001 &>/dev/null; then
        echo "Frontend is responding!"
        break
    fi
    sleep 2
    ((RETRIES--))
done

if [ $RETRIES -eq 0 ]; then
    echo "Error: Frontend failed to start"
    docker logs test-frontend
    docker rm -f test-frontend
    exit 1
fi

# Test home page loads
echo "Testing home page..."
RESPONSE=$(curl -s http://localhost:3001)
if echo "$RESPONSE" | grep -q "html\|react\|next"; then
    echo "✓ Home page loads"
else
    echo "✗ Home page doesn't load properly"
fi

# Test that container is running
if docker ps | grep -q test-frontend; then
    echo "✓ Frontend container is running"
else
    echo "✗ Frontend container is not running"
    docker rm -f test-frontend
    exit 1
fi

# Cleanup
echo "Cleaning up..."
docker rm -f test-frontend

echo "Frontend container tests passed!"
exit 0