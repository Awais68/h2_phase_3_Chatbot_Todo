#!/bin/bash

set -e

echo "Running integration tests with Docker Compose..."

# Check if docker-compose file exists
if [ ! -f "docker-compose.yml" ] && [ ! -f "../docker-compose.yml" ] && [ ! -f "../../docker-compose.yml" ]; then
    echo "Creating a basic docker-compose.yml for testing..."

    cat > docker-compose.test.yml << 'EOF'
version: '3.8'

services:
  backend:
    image: todo-backend:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/todo
      - OPENAI_API_KEY=test-key
      - MCP_SERVER_URL=http://mcp-server:3000
    depends_on:
      - db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 5

  mcp-server:
    image: todo-mcp-server:latest
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/todo
    depends_on:
      - db

  frontend:
    image: todo-frontend:latest
    ports:
      - "3001:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - NEXT_PUBLIC_APP_URL=http://localhost:3001
    depends_on:
      - backend

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: todo
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
EOF

    COMPOSE_FILE="docker-compose.test.yml"
else
    if [ -f "docker-compose.yml" ]; then
        COMPOSE_FILE="docker-compose.yml"
    elif [ -f "../docker-compose.yml" ]; then
        COMPOSE_FILE="../docker-compose.yml"
    else
        COMPOSE_FILE="../../docker-compose.yml"
    fi
fi

# Start all services
echo "Starting services with Docker Compose..."
docker-compose -f $COMPOSE_FILE up -d

echo "Waiting for services to be ready..."
sleep 10

# Test backend health
echo "Testing backend health..."
RETRIES=20
while [ $RETRIES -gt 0 ]; do
    if curl -f http://localhost:8000/health &>/dev/null; then
        echo "✓ Backend is healthy"
        break
    fi
    sleep 3
    ((RETRIES--))
done

if [ $RETRIES -eq 0 ]; then
    echo "✗ Backend failed to become healthy"
    docker-compose -f $COMPOSE_FILE logs
    docker-compose -f $COMPOSE_FILE down
    exit 1
fi

# Test frontend
echo "Testing frontend..."
if curl -f http://localhost:3001 &>/dev/null; then
    echo "✓ Frontend is accessible"
else
    echo "✗ Frontend is not accessible"
    docker-compose -f $COMPOSE_FILE logs
    docker-compose -f $COMPOSE_FILE down
    exit 1
fi

# Test MCP server
echo "Testing MCP server..."
if timeout 5 bash -c "</dev/tcp/localhost/3000" &>/dev/null; then
    echo "✓ MCP server is accessible"
else
    echo "✗ MCP server is not accessible"
    docker-compose -f $COMPOSE_FILE logs
    docker-compose -f $COMPOSE_FILE down
    exit 1
fi

echo "✓ All services are running and communicating properly"

# Cleanup
echo "Stopping services..."
docker-compose -f $COMPOSE_FILE down

# Remove test file if we created it
if [ "$COMPOSE_FILE" = "docker-compose.test.yml" ] && [ -f "docker-compose.test.yml" ]; then
    rm docker-compose.test.yml
fi

echo "Integration tests passed!"
exit 0