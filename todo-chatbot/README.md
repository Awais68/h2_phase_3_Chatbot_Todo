# Todo Chatbot Helm Chart

A Helm chart for deploying the Todo AI Chatbot application to Kubernetes.

## Chart Details

- **Name**: todo-chatbot
- **Version**: 0.1.0
- **App Version**: 2.0.0
- **Type**: Application

## Overview

This chart deploys the Todo AI Chatbot application, which consists of:
- **Frontend**: Next.js application with ChatKit widget
- **Backend**: FastAPI server with PostgreSQL database integration
- **Database**: PostgreSQL StatefulSet with persistent storage

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- PV provisioner support in the underlying infrastructure (for database persistence)
- Minikube or a Kubernetes cluster with sufficient resources

## Installing the Chart

To install the chart with the release name `todo-app`:

```bash
# Create namespace
kubectl create namespace todo-app

# Install the chart
helm install todo-app todo-chatbot/ \
  --namespace todo-app \
  --values todo-chatbot/values-dev.yaml
```

## Upgrading the Chart

```bash
helm upgrade todo-app todo-chatbot/ \
  --namespace todo-app \
  --values todo-chatbot/values-dev.yaml
```

## Uninstalling the Chart

```bash
helm uninstall todo-app -n todo-app
```

## Configuration

The following table lists the configurable parameters of the todo-chatbot chart and their default values.

### Global Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.environment` | Environment name (dev/prod) | `"dev"` |

### Frontend Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.image.repository` | Frontend image repository | `"todo-frontend"` |
| `frontend.image.tag` | Frontend image tag | `"v1"` |
| `frontend.image.pullPolicy` | Frontend image pull policy | `"IfNotPresent"` |
| `frontend.replicas` | Number of frontend replicas | `2` |
| `frontend.service.type` | Frontend service type | `"ClusterIP"` |
| `frontend.service.port` | Frontend service port | `3000` |
| `frontend.ingress.enabled` | Enable ingress for frontend | `true` |
| `frontend.ingress.host` | Host for ingress | `"todo.local"` |
| `frontend.resources.requests.cpu` | Frontend CPU requests | `"100m"` |
| `frontend.resources.requests.memory` | Frontend memory requests | `"128Mi"` |
| `frontend.resources.limits.cpu` | Frontend CPU limits | `"500m"` |
| `frontend.resources.limits.memory` | Frontend memory limits | `"512Mi"` |

### Backend Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.image.repository` | Backend image repository | `"todo-backend"` |
| `backend.image.tag` | Backend image tag | `"v1"` |
| `backend.image.pullPolicy` | Backend image pull policy | `"IfNotPresent"` |
| `backend.replicas` | Number of backend replicas | `2` |
| `backend.service.type` | Backend service type | `"ClusterIP"` |
| `backend.service.port` | Backend service port | `8000` |
| `backend.env.DATABASE_URL` | Database connection URL | `"postgresql://todouser:changeme123@postgres:5432/tododb"` |
| `backend.resources.requests.cpu` | Backend CPU requests | `"200m"` |
| `backend.resources.requests.memory` | Backend memory requests | `"256Mi"` |
| `backend.resources.limits.cpu` | Backend CPU limits | `"1000m"` |
| `backend.resources.limits.memory` | Backend memory limits | `"1Gi"` |

### Database Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `database.image.repository` | PostgreSQL image repository | `"postgres"` |
| `database.image.tag` | PostgreSQL image tag | `"15-alpine"` |
| `database.persistence.enabled` | Enable database persistence | `true` |
| `database.persistence.size` | Database storage size | `"5Gi"` |
| `database.persistence.storageClass` | Storage class for database | `"standard"` |
| `database.credentials.username` | Database username | `"todouser"` |
| `database.credentials.password` | Database password | `"changeme123"` |
| `database.credentials.database` | Database name | `"tododb"` |
| `database.resources.requests.cpu` | Database CPU requests | `"250m"` |
| `database.resources.requests.memory` | Database memory requests | `"256Mi"` |
| `database.resources.limits.cpu` | Database CPU limits | `"1000m"` |
| `database.resources.limits.memory` | Database memory limits | `"1Gi"` |

### HPA Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `hpa.enabled` | Enable Horizontal Pod Autoscaler | `true` |
| `hpa.minReplicas` | Minimum number of replicas | `2` |
| `hpa.maxReplicas` | Maximum number of replicas | `10` |
| `hpa.cpuThreshold` | CPU utilization threshold percentage | `70` |
| `hpa.memoryThreshold` | Memory utilization threshold percentage | `80` |

### Pod Disruption Budget Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `pdb.enabled` | Enable Pod Disruption Budget | `true` |
| `pdb.minAvailable` | Minimum available pods | `1` |

## Values Files

The chart includes sample values files for different environments:
- `values-dev.yaml`: Development environment configuration
- `values-prod.yaml`: Production environment configuration

## Customizing the Chart

You can customize the chart by creating your own values file:

```bash
# Create a custom values file
cp values-dev.yaml my-values.yaml
# Edit my-values.yaml with your custom settings
vim my-values.yaml

# Install with custom values
helm install todo-app todo-chatbot/ \
  --namespace todo-app \
  --values my-values.yaml
```

## Accessing the Application

After installation, you can access the application:

### With Ingress
If ingress is enabled, add the following to your `/etc/hosts` file:
```
<INGRESS_IP> todo.local
```

Then access the application at: `http://todo.local`

### Without Ingress
Use port forwarding to access the services:
```bash
kubectl port-forward -n todo-app service/todo-app-todo-chatbot-frontend 3000:3000
```

## Troubleshooting

### Common Issues

1. **Images not found**: Ensure your images are available in the cluster or registry
2. **Database connection issues**: Check the DATABASE_URL in backend configuration
3. **Service connectivity**: Verify that services can communicate within the cluster

### Useful Commands

```bash
# Check status of all resources
kubectl get all -n todo-app

# View logs
kubectl logs -f deployment/todo-app-todo-chatbot-backend -n todo-app
kubectl logs -f deployment/todo-app-todo-chatbot-frontend -n todo-app

# Check events
kubectl get events -n todo-app --sort-by='.lastTimestamp'

# Describe resources for more details
kubectl describe deployment/todo-app-todo-chatbot-backend -n todo-app
```

## Development

### Chart Testing

Test the chart template rendering:
```bash
helm template todo-app todo-chatbot/ --values todo-chatbot/values-dev.yaml
```

Validate the chart:
```bash
helm lint todo-chatbot/
```

### Local Development

For local development, use the `--dry-run` flag to test without actually deploying:
```bash
helm install todo-app todo-chatbot/ --dry-run --debug
```