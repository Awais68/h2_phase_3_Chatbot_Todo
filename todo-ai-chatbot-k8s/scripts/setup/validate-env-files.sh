#!/bin/bash
# Script to validate all required environment variables are set

set -e

echo "Validating environment variables..."

# Function to check if required variables are set in a file
validate_env_file() {
    local file_path=$1
    local required_vars=("${@:2}")

    if [[ ! -f "$file_path" ]]; then
        echo "❌ Environment file $file_path does not exist"
        return 1
    fi

    echo "🔍 Checking: $file_path"
    local missing_vars=()

    for var in "${required_vars[@]}"; do
        if ! grep -q "^${var}=" "$file_path" || grep "^${var}=" "$file_path" | grep -q "${var}=.*xxx"; then
            missing_vars+=("$var")
            echo "⚠️  Variable $var is missing or has placeholder value in $file_path"
        else
            echo "✅ Variable $var is set in $file_path"
        fi
    done

    if [[ ${#missing_vars[@]} -gt 0 ]]; then
        echo "❌ Found ${#missing_vars[@]} missing or placeholder variables in $file_path"
        return 1
    else
        echo "✅ All required variables are set in $file_path"
        return 0
    fi
}

# Define required variables for each environment
LOCAL_VARS=(
    "APP_NAME"
    "DATABASE_URL"
    "OPENAI_API_KEY"
    "BETTER_AUTH_SECRET"
    "BACKEND_URL"
    "NEXT_PUBLIC_API_URL"
)

PROD_VARS=(
    "APP_NAME"
    "DATABASE_URL"
    "OPENAI_API_KEY"
    "BETTER_AUTH_SECRET"
    "BACKEND_URL"
    "NEXT_PUBLIC_API_URL"
)

DOCKER_VARS=(
    "FRONTEND_IMAGE"
    "BACKEND_IMAGE"
    "MCP_SERVER_IMAGE"
    "POSTGRES_DB"
    "POSTGRES_USER"
    "POSTGRES_PASSWORD"
    "DATABASE_URL"
    "OPENAI_API_KEY"
    "BETTER_AUTH_SECRET"
)

K8S_VARS=(
    "K8S_NAMESPACE"
    "POSTGRES_DB"
    "POSTGRES_USER"
    "POSTGRES_PASSWORD"
    "DATABASE_URL"
    "OPENAI_API_KEY"
    "BETTER_AUTH_SECRET"
)

# Validate each environment file
echo "📋 Validating local environment file..."
validate_env_file "../config/local/.env" "${LOCAL_VARS[@]}"
LOCAL_VALID=$?

echo ""
echo "📋 Validating production environment file..."
validate_env_file "../config/prod/.env" "${PROD_VARS[@]}"
PROD_VALID=$?

echo ""
echo "📋 Validating Docker environment file..."
validate_env_file "../docker/.env.docker" "${DOCKER_VARS[@]}"
DOCKER_VALID=$?

echo ""
echo "📋 Validating Kubernetes environment file..."
validate_env_file "../k8s/.env.k8s" "${K8S_VARS[@]}"
K8S_VALID=$?

echo ""
if [[ $LOCAL_VALID -eq 0 && $PROD_VALID -eq 0 && $DOCKER_VALID -eq 0 && $K8S_VALID -eq 0 ]]; then
    echo "🎉 All environment files are properly configured!"
    echo "✅ Environment validation passed"
    exit 0
else
    echo "❌ Some environment files have missing or placeholder values"
    echo "🔧 Please update the .env files with your actual values before proceeding"
    exit 1
fi