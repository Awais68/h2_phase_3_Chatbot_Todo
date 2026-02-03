#!/bin/bash

# scripts/verify-directory-structure.sh
# Verifies all required directories exist

set -e

echo "Verifying directory structure..."

PROJECT_ROOT="todo-ai-chatbot-k8s"
if [[ ! -d "$PROJECT_ROOT" ]]; then
    echo "❌ Project root directory $PROJECT_ROOT does not exist"
    echo "💡 Run create-directory-structure.sh first"
    exit 1
fi

cd "$PROJECT_ROOT"

# List of required directories
DIRECTORIES=(
    "docker"
    "docker/backend"
    "docker/mcp-server"
    "docker/frontend"
    "k8s"
    "k8s/base"
    "k8s/backend"
    "k8s/mcp-server"
    "k8s/frontend"
    "k8s/ingress"
    "k8s/network"
    "helm"
    "helm/todo-chatbot"
    "helm/todo-chatbot/templates"
    "scripts"
    "scripts/setup"
    "scripts/docker"
    "scripts/k8s"
    "scripts/helm"
    "scripts/testing"
    "scripts/monitoring"
    "docs"
    "docs/setup"
    "docs/deployment"
    "docs/operations"
    "docs/architecture"
    "config"
    "config/local"
    "config/prod"
    "tests"
)

MISSING_DIRS=()
for dir in "${DIRECTORIES[@]}"; do
    if [[ ! -d "$dir" ]]; then
        MISSING_DIRS+=("$dir")
        echo "❌ Missing directory: $dir"
    else
        echo "✅ Found directory: $dir"
    fi
done

# Check for required README files
README_FILES=(
    "docker/README.md"
    "docker/backend/README.md"
    "docker/mcp-server/README.md"
    "docker/frontend/README.md"
    "k8s/README.md"
    "helm/README.md"
    "scripts/README.md"
    "docs/README.md"
    "config/README.md"
    "tests/README.md"
    "README.md"
)

for readme in "${README_FILES[@]}"; do
    if [[ ! -f "$readme" ]]; then
        echo "❌ Missing README: $readme"
        MISSING_DIRS+=("$readme")
    else
        echo "✅ Found README: $readme"
    fi
done

if [[ ${#MISSING_DIRS[@]} -eq 0 ]]; then
    echo "🎉 All required directories and files exist!"
    echo "✅ Directory structure verification passed"
else
    echo "❌ Missing ${#MISSING_DIRS[@]} directories/files"
    exit 1
fi