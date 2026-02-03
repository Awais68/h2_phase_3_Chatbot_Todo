# Directory Structure Documentation

## Overview
This document describes the directory structure for the Todo AI Chatbot Kubernetes deployment project.

## Project Structure
```
todo-ai-chatbot-k8s/
├── docker/
│   ├── backend/
│   ├── mcp-server/
│   ├── frontend/
│   └── docker-compose.yml
├── k8s/
│   ├── base/
│   ├── backend/
│   ├── mcp-server/
│   ├── frontend/
│   ├── ingress/
│   └── network/
├── helm/
│   └── todo-chatbot/
│       └── templates/
├── scripts/
│   ├── setup/
│   ├── docker/
│   ├── k8s/
│   ├── helm/
│   ├── testing/
│   └── monitoring/
├── docs/
│   ├── setup/
│   ├── deployment/
│   ├── operations/
│   └── architecture/
├── config/
│   ├── local/
│   └── prod/
└── tests/
```

## Directory Purposes

### `docker/`
Contains all Docker-related files including Dockerfiles for each service:
- `backend/` - Dockerfile and configs for the backend service
- `mcp-server/` - Dockerfile and configs for the MCP server
- `frontend/` - Dockerfile and configs for the frontend service
- `docker-compose.yml` - Local development orchestration

### `k8s/`
Contains all Kubernetes manifest files:
- `base/` - Base kustomize configurations
- `backend/` - Backend-specific Kubernetes resources
- `mcp-server/` - MCP server-specific Kubernetes resources
- `frontend/` - Frontend-specific Kubernetes resources
- `ingress/` - Ingress configurations
- `network/` - Network policies and configurations

### `helm/`
Contains Helm chart for the application:
- `todo-chatbot/` - Main Helm chart
  - `templates/` - Helm templates for all resources

### `scripts/`
Contains utility scripts for various operations:
- `setup/` - Environment setup scripts
- `docker/` - Docker-related scripts
- `k8s/` - Kubernetes deployment scripts
- `helm/` - Helm-related scripts
- `testing/` - Testing scripts
- `monitoring/` - Monitoring and observability scripts

### `docs/`
Contains documentation files:
- `setup/` - Setup and installation guides
- `deployment/` - Deployment procedures
- `operations/` - Day-2 operations guides
- `architecture/` - Architecture documentation

### `config/`
Contains configuration files for different environments:
- `local/` - Local development configurations
- `prod/` - Production configurations

### `tests/`
Contains test files for the application:
- Unit tests
- Integration tests
- End-to-end tests