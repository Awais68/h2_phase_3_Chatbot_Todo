#!/bin/bash
# Script to load environment variables from .env files

set -e

# Function to load environment variables from a file
load_env_file() {
    local file_path=$1

    if [[ -f "$file_path" ]]; then
        echo "Loading environment variables from: $file_path"
        export $(grep -v '^#' "$file_path" | xargs)
        return 0
    else
        echo "⚠️  Environment file $file_path does not exist"
        return 1
    fi
}

# Determine environment from argument
ENVIRONMENT=${1:-local}

echo "Loading $ENVIRONMENT environment variables..."

case $ENVIRONMENT in
    "local")
        load_env_file "../config/local/.env" || echo "Using default local values"
        ;;
    "prod")
        load_env_file "../config/prod/.env" || echo "Using default production values"
        ;;
    "docker")
        load_env_file "../docker/.env.docker" || echo "Using default Docker values"
        ;;
    "k8s")
        load_env_file "../k8s/.env.k8s" || echo "Using default Kubernetes values"
        ;;
    *)
        echo "Usage: $0 [local|prod|docker|k8s]"
        echo "Loading local environment as default..."
        load_env_file "../config/local/.env" || echo "Using default local values"
        ;;
esac

echo "Environment variables loaded successfully"
echo "Current environment: $ENVIRONMENT"

# Show loaded variables (excluding sensitive ones)
echo "Loaded variables:"
env | grep -E '^(APP_|BACKEND_|FRONTEND_|NEXT_PUBLIC_|ENABLE_|LOG_|CORS_|SECURE_)' | head -10
if env | grep -q "APP_NAME"; then
    echo "APP_NAME: $APP_NAME"
fi
if env | grep -q "APP_ENV"; then
    echo "APP_ENV: $APP_ENV"
fi