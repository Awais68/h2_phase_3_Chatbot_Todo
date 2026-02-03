# Environment Variables Reference

## Overview

This document provides a comprehensive reference for all environment variables used in the Todo AI Chatbot Kubernetes deployment. Environment variables are organized by environment and purpose to facilitate proper configuration across different deployment scenarios.

## Table of Contents

1. [Local Development Environment](#local-development-environment)
2. [Production Environment](#production-environment)
3. [Docker Compose Environment](#docker-compose-environment)
4. [Kubernetes Environment](#kubernetes-environment)
5. [Security Best Practices](#security-best-practices)
6. [Validation and Troubleshooting](#validation-and-troubleshooting)

## Local Development Environment

Location: `config/local/.env.example`

### Application Configuration
- `APP_NAME`: Name of the application (default: `todo-ai-chatbot`)
- `APP_ENV`: Environment identifier (default: `local`)
- `APP_DEBUG`: Enable/disable debug mode (default: `true`)
- `APP_PORT`: Port on which the application runs (default: `3000`)

### Database Configuration (Neon PostgreSQL)
- `DATABASE_URL`: Full connection string to PostgreSQL database
- `DB_HOST`: Database host address
- `DB_PORT`: Database port (default: `5432`)
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_SSL_MODE`: SSL mode for database connections (default: `require`)

### OpenAI API Configuration
- `OPENAI_API_KEY`: API key for OpenAI services (required)
- `OPENAI_ORG_ID`: Organization ID for OpenAI (optional)
- `OPENAI_MODEL`: Model to use for AI operations (default: `gpt-4o-mini`)
- `OPENAI_ASSISTANT_ID`: Assistant ID for OpenAI (optional)
- `OPENAI_DOMAIN_KEY`: Domain key for OpenAI ChatKit (required)

### Better Auth Configuration
- `BETTER_AUTH_SECRET`: Secret key for authentication (minimum 32 characters, required)
- `BETTER_AUTH_URL`: URL for the authentication service (default: `http://localhost:3000`)

### Backend API Configuration
- `BACKEND_URL`: URL of the backend service (default: `http://localhost:8000`)
- `BACKEND_HOST`: Host address for the backend (default: `0.0.0.0`)
- `BACKEND_PORT`: Port for the backend service (default: `8000`)
- `BACKEND_WORKERS`: Number of worker processes (default: `4`)
- `BACKEND_RELOAD`: Enable/disable auto-reload in development (default: `true`)

### MCP Server Configuration
- `MCP_SERVER_URL`: URL of the MCP server (default: `http://localhost:3000`)
- `MCP_SERVER_HOST`: Host address for the MCP server (default: `0.0.0.0`)
- `MCP_SERVER_PORT`: Port for the MCP server (default: `3000`)

### Frontend Configuration
- `NEXT_PUBLIC_API_URL`: Public URL for the API (default: `http://localhost:8000`)
- `NEXT_PUBLIC_APP_URL`: Public URL for the application (default: `http://localhost:3000`)
- `NEXT_PUBLIC_ENABLE_VOICE`: Enable voice features (default: `true`)
- `NEXT_PUBLIC_ENABLE_ANALYTICS`: Enable analytics (default: `true`)
- `NEXT_PUBLIC_ENABLE_RECURRING`: Enable recurring tasks (default: `true`)

### Feature Flags
- `ENABLE_VOICE_INPUT`: Enable voice input functionality (default: `true`)
- `ENABLE_VOICE_OUTPUT`: Enable voice output functionality (default: `true`)
- `ENABLE_ANALYTICS`: Enable analytics tracking (default: `true`)
- `ENABLE_RECURRING_TASKS`: Enable recurring tasks (default: `true`)
- `ENABLE_DEBUG_LOGGING`: Enable debug logging (default: `true`)

### CORS Configuration
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `CORS_ALLOW_CREDENTIALS`: Allow credentials in CORS requests (default: `true`)

### Logging Configuration
- `LOG_LEVEL`: Logging level (default: `DEBUG`)
- `LOG_FORMAT`: Log format (`json` or other formats)

## Production Environment

Location: `config/prod/.env.example`

The production environment extends the local environment with additional security and performance settings:

### Production-Specific Variables
- `APP_ENV`: Should be set to `production`
- `APP_DEBUG`: Should be set to `false`
- `SECURE_COOKIES`: Enable secure cookies (default: `true`)
- `HTTPS_REDIRECT`: Force HTTPS redirects (default: `true`)
- `RATE_LIMIT_ENABLED`: Enable rate limiting (default: `true`)
- `MAX_REQUESTS_PER_MINUTE`: Maximum requests per minute (default: `100`)

## Docker Compose Environment

Location: `docker/.env.docker.example`

### Image Configuration
- `FRONTEND_IMAGE`: Docker image for frontend service
- `BACKEND_IMAGE`: Docker image for backend service
- `MCP_SERVER_IMAGE`: Docker image for MCP server

### Docker Compose Settings
- `COMPOSE_PROJECT_NAME`: Name of the Docker Compose project

### Service Ports
- `FRONTEND_PORT`: Port for frontend service (default: `3000`)
- `BACKEND_PORT`: Port for backend service (default: `8000`)
- `MCP_SERVER_PORT`: Port for MCP server (default: `3000`)

### Database Configuration for Docker
- `POSTGRES_DB`: Database name for PostgreSQL
- `POSTGRES_USER`: Database user for PostgreSQL
- `POSTGRES_PASSWORD`: Database password for PostgreSQL
- `POSTGRES_HOST`: Database host for Docker (default: `localhost`)
- `POSTGRES_PORT`: Database port for Docker (default: `5432`)

## Kubernetes Environment

Location: `k8s/.env.k8s.example`

### Kubernetes Configuration
- `K8S_NAMESPACE`: Kubernetes namespace for deployment (default: `todo-chatbot`)
- `K8S_CONTEXT`: Kubernetes context to use (default: `minikube`)

### Image Registry Configuration
- `IMAGE_REGISTRY`: Container registry (default: `docker.io`)
- `IMAGE_PULL_POLICY`: Pull policy for images (default: `IfNotPresent`)

### Image Versions
- `FRONTEND_IMAGE_VERSION`: Version tag for frontend image (default: `latest`)
- `BACKEND_IMAGE_VERSION`: Version tag for backend image (default: `latest`)
- `MCP_SERVER_IMAGE_VERSION`: Version tag for MCP server image (default: `latest`)

### Resource Limits and Requests
#### Backend
- `BACKEND_CPU_REQUEST`: CPU request for backend (default: `100m`)
- `BACKEND_CPU_LIMIT`: CPU limit for backend (default: `500m`)
- `BACKEND_MEMORY_REQUEST`: Memory request for backend (default: `128Mi`)
- `BACKEND_MEMORY_LIMIT`: Memory limit for backend (default: `512Mi`)

#### Frontend
- `FRONTEND_CPU_REQUEST`: CPU request for frontend (default: `100m`)
- `FRONTEND_CPU_LIMIT`: CPU limit for frontend (default: `300m`)
- `FRONTEND_MEMORY_REQUEST`: Memory request for frontend (default: `64Mi`)
- `FRONTEND_MEMORY_LIMIT`: Memory limit for frontend (default: `256Mi`)

#### MCP Server
- `MCP_SERVER_CPU_REQUEST`: CPU request for MCP server (default: `50m`)
- `MCP_SERVER_CPU_LIMIT`: CPU limit for MCP server (default: `200m`)
- `MCP_SERVER_MEMORY_REQUEST`: Memory request for MCP server (default: `64Mi`)
- `MCP_SERVER_MEMORY_LIMIT`: Memory limit for MCP server (default: `128Mi`)

### Replicas Configuration
- `BACKEND_REPLICAS`: Number of backend replicas (default: `2`)
- `FRONTEND_REPLICAS`: Number of frontend replicas (default: `2`)
- `MCP_SERVER_REPLICAS`: Number of MCP server replicas (default: `2`)

### Service Configuration
- `BACKEND_SERVICE_TYPE`: Kubernetes service type for backend (default: `ClusterIP`)
- `FRONTEND_SERVICE_TYPE`: Kubernetes service type for frontend (default: `ClusterIP`)
- `MCP_SERVER_SERVICE_TYPE`: Kubernetes service type for MCP server (default: `ClusterIP`)

### Ingress Configuration
- `INGRESS_HOST`: Host for ingress routing
- `INGRESS_TLS_ENABLED`: Enable TLS for ingress (default: `false`)

### Database Configuration for Kubernetes
- `POSTGRES_DB`: Database name for PostgreSQL
- `POSTGRES_USER`: Database user for PostgreSQL
- `POSTGRES_PASSWORD`: Database password for PostgreSQL
- `POSTGRES_HOST`: Database host for Kubernetes (default: `postgres-service`)
- `POSTGRES_PORT`: Database port for Kubernetes (default: `5432`)

## Security Best Practices

### Handling Sensitive Information
1. **Never commit `.env` files** to version control
2. Use `.env.example` files for documentation only
3. Store actual values in `.env` files which are git-ignored
4. Use Kubernetes Secrets for sensitive data in production

### API Keys and Secrets
1. Rotate API keys regularly
2. Use environment-specific keys when possible
3. Limit permissions of API keys to minimum required
4. Use strong, randomly generated secrets (at least 32 characters)

### Database Credentials
1. Use different credentials for different environments
2. Implement proper database user permissions
3. Use encrypted connections (SSL/TLS) for database access
4. Regularly rotate database passwords

## Validation and Troubleshooting

### Using Validation Script
Run the validation script to check environment configuration:
```bash
bash scripts/setup/validate-env-files.sh
```

### Common Issues
1. **Missing API Keys**: Ensure all required API keys are provided
2. **Incorrect Database URLs**: Verify database connection strings
3. **Authentication Secrets**: Check that auth secrets meet length requirements
4. **Port Conflicts**: Ensure ports are available and not in use

### Testing Environment Loading
Use the load script to test environment variable loading:
```bash
bash scripts/setup/load-env.sh [local|prod|docker|k8s]
```

## Additional Resources

- [Docker Environment Variables](../docker/README.md)
- [Kubernetes Configuration](../k8s/README.md)
- [Helm Chart Values](../helm/README.md)
- [Security Configuration](SECURITY.md)