#!/bin/bash

# scripts/create-directory-structure.sh
# Creates all required directories for the project

set -e

echo "Creating Kubernetes project directory structure..."

# Create main project directory
mkdir -p todo-ai-chatbot-k8s
cd todo-ai-chatbot-k8s

# Create Docker directories
mkdir -p docker/backend
mkdir -p docker/mcp-server
mkdir -p docker/frontend
touch docker/.gitkeep
touch docker/backend/.gitkeep
touch docker/mcp-server/.gitkeep
touch docker/frontend/.gitkeep

# Create K8s directories
mkdir -p k8s/base
mkdir -p k8s/backend
mkdir -p k8s/mcp-server
mkdir -p k8s/frontend
mkdir -p k8s/ingress
mkdir -p k8s/network
touch k8s/.gitkeep
touch k8s/base/.gitkeep
touch k8s/backend/.gitkeep
touch k8s/mcp-server/.gitkeep
touch k8s/frontend/.gitkeep
touch k8s/ingress/.gitkeep
touch k8s/network/.gitkeep

# Create Helm directories
mkdir -p helm/todo-chatbot/templates
touch helm/.gitkeep
touch helm/todo-chatbot/.gitkeep
touch helm/todo-chatbot/templates/.gitkeep

# Create Scripts directories
mkdir -p scripts/setup
mkdir -p scripts/docker
mkdir -p scripts/k8s
mkdir -p scripts/helm
mkdir -p scripts/testing
mkdir -p scripts/monitoring
touch scripts/.gitkeep
touch scripts/setup/.gitkeep
touch scripts/docker/.gitkeep
touch scripts/k8s/.gitkeep
touch scripts/helm/.gitkeep
touch scripts/testing/.gitkeep
touch scripts/monitoring/.gitkeep

# Create Docs directories
mkdir -p docs/setup
mkdir -p docs/deployment
mkdir -p docs/operations
mkdir -p docs/architecture
touch docs/.gitkeep
touch docs/setup/.gitkeep
touch docs/deployment/.gitkeep
touch docs/operations/.gitkeep
touch docs/architecture/.gitkeep

# Create Config directories
mkdir -p config/local
mkdir -p config/prod
touch config/.gitkeep
touch config/local/.gitkeep
touch config/prod/.gitkeep

# Create tests directory
mkdir -p tests
touch tests/.gitkeep

# Create placeholder README files
echo "# Docker Files" > docker/README.md
echo "# Backend Docker Configuration" > docker/backend/README.md
echo "# MCP Server Docker Configuration" > docker/mcp-server/README.md
echo "# Frontend Docker Configuration" > docker/frontend/README.md
echo "# Kubernetes Manifests" > k8s/README.md
echo "# Helm Charts" > helm/README.md
echo "# Project Scripts" > scripts/README.md
echo "# Documentation" > docs/README.md
echo "# Configuration Files" > config/README.md
echo "# Test Files" > tests/README.md

# Create root README
cat > README.md << 'EOF'
# Todo AI Chatbot Kubernetes Deployment

This repository contains the Kubernetes deployment configuration for the Todo AI Chatbot application.

## Structure
- `docker/` - Dockerfiles and build configurations
- `k8s/` - Kubernetes manifests
- `helm/` - Helm charts
- `scripts/` - Utility scripts
- `docs/` - Documentation
- `config/` - Configuration files
- `tests/` - Test files

## Quick Start
Follow the documentation in the docs/ directory to set up and deploy the application.
EOF

echo "Directory structure created successfully!"