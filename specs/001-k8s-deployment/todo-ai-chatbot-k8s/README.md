# Todo AI Chatbot - Kubernetes Deployment

Production-ready Kubernetes deployment for Todo AI Chatbot with voice commands, analytics, and recurring tasks.

## Quick Links
- [Quick Start Guide](QUICK_START.md)
- [Documentation](docs/README.md)
- [Deployment Guide](docs/deployment/README.md)

## Project Structure

```
todo-ai-chatbot-k8s/
├── docker/                          # Docker-related files
│   ├── backend/
│   │   ├── Dockerfile
│   │   ├── .dockerignore
│   │   └── README.md
│   ├── mcp-server/
│   │   ├── Dockerfile
│   │   ├── .dockerignore
│   │   └── README.md
│   ├── frontend/
│   │   ├── Dockerfile
│   │   ├── .dockerignore
│   │   └── README.md
│   ├── docker-compose.yml
│   └── README.md
│
├── k8s/                             # Kubernetes manifests
│   ├── base/                        # Base manifests
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   ├── secrets.yaml
│   │   └── README.md
│   ├── backend/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── hpa.yaml
│   │   └── README.md
│   ├── mcp-server/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── README.md
│   ├── frontend/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── hpa.yaml
│   │   └── README.md
│   ├── ingress/
│   │   ├── ingress.yaml
│   │   └── README.md
│   ├── network/
│   │   ├── network-policy.yaml
│   │   ├── pdb.yaml
│   │   └── README.md
│   └── README.md
│
├── helm/                            # Helm charts
│   └── todo-chatbot/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-local.yaml
│       ├── values-prod.yaml
│       ├── templates/
│       │   ├── _helpers.tpl
│       │   ├── namespace.yaml
│       │   ├── configmap.yaml
│       │   ├── secrets.yaml
│       │   ├── backend-deployment.yaml
│       │   ├── backend-service.yaml
│       │   ├── mcp-deployment.yaml
│       │   ├── mcp-service.yaml
│       │   ├── frontend-deployment.yaml
│       │   ├── frontend-service.yaml
│       │   ├── ingress.yaml
│       │   ├── hpa.yaml
│       │   ├── NOTES.txt
│       │   └── README.md
│       ├── charts/                  # Dependencies
│       └── README.md
│
├── scripts/                         # Automation scripts
│   ├── setup/                       # Setup scripts
│   │   ├── install-docker.sh
│   │   ├── install-minikube.sh
│   │   ├── install-kubectl.sh
│   │   ├── install-helm.sh
│   │   └── README.md
│   ├── docker/                      # Docker scripts
│   │   ├── build-all-images.sh
│   │   ├── build-backend.sh
│   │   ├── build-mcp.sh
│   │   ├── build-frontend.sh
│   │   ├── push-images.sh
│   │   └── README.md
│   ├── k8s/                         # Kubernetes scripts
│   │   ├── deploy-all.sh
│   │   ├── deploy-backend.sh
│   │   ├── deploy-mcp.sh
│   │   ├── deploy-frontend.sh
│   │   ├── rollback.sh
│   │   ├── cleanup.sh
│   │   └── README.md
│   ├── helm/                        # Helm scripts
│   │   ├── install-chart.sh
│   │   ├── upgrade-chart.sh
│   │   ├── package-chart.sh
│   │   └── README.md
│   ├── testing/                     # Testing scripts
│   │   ├── test-docker.sh
│   │   ├── test-k8s.sh
│   │   ├── test-app.sh
│   │   └── README.md
│   ├── monitoring/                  # Monitoring scripts
│   │   ├── view-logs.sh
│   │   ├── check-health.sh
│   │   ├── monitor-resources.sh
│   │   └── README.md
│   └── README.md
│
├── docs/                            # Documentation
│   ├── setup/
│   │   ├── DOCKER_INSTALLATION.md
│   │   ├── MINIKUBE_INSTALLATION.md
│   │   ├── KUBECTL_INSTALLATION.md
│   │   ├── HELM_INSTALLATION.md
│   │   └── README.md
│   ├── deployment/
│   │   ├── DOCKER_BUILD.md
│   │   ├── K8S_DEPLOYMENT.md
│   │   ├── HELM_DEPLOYMENT.md
│   │   └── README.md
│   ├── operations/
│   │   ├── SCALING.md
│   │   ├── MONITORING.md
│   │   ├── TROUBLESHOOTING.md
│   │   ├── ROLLBACK.md
│   │   └── README.md
│   ├── architecture/
│   │   ├── OVERVIEW.md
│   │   ├── NETWORKING.md
│   │   ├── STORAGE.md
│   │   ├── SECURITY.md
│   │   └── README.md
│   └── README.md
│
├── config/                          # Configuration files
│   ├── local/
│   │   ├── .env.example
│   │   └── README.md
│   ├── prod/
│   │   ├── .env.example
│   │   └── README.md
│   └── README.md
│
├── tests/                           # Test files
│   ├── docker/
│   │   └── README.md
│   ├── k8s/
│   │   └── README.md
│   └── README.md
│
├── .gitignore
└── README.md
```

## Prerequisites

- Docker Desktop with Kubernetes (or Minikube)
- kubectl
- Helm 3
- OpenAI API Key
- Neon PostgreSQL database credentials

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd todo-ai-chatbot-k8s
   ```

2. **Start Minikube**
   ```bash
   minikube start --cpus=4 --memory=8192
   minikube addons enable ingress
   ```

3. **Build Docker images**
   ```bash
   cd docker
   # Build images for your platform
   # (You'll need to implement the actual build process based on your source code)
   ```

4. **Load images to Minikube**
   ```bash
   minikube image load todo-backend:latest
   minikube image load todo-mcp-server:latest
   minikube image load todo-frontend:latest
   ```

5. **Deploy with Helm**
   ```bash
   cd helm
   ./install-chart.sh
   ```

6. **Verify deployment**
   ```bash
   ./scripts/monitoring/check-health.sh
   ```

## Documentation

See [docs/](docs/) for complete documentation.

## Architecture

The Todo AI Chatbot is deployed as a microservice architecture consisting of:

- **Frontend**: Next.js application with voice capabilities
- **Backend**: FastAPI server with OpenAI integration
- **MCP Server**: MCP server for tool integration
- All services are deployed as Kubernetes deployments with services, ingress, and proper networking configuration