# Todo Evolution Helm Chart

A comprehensive Helm chart for deploying the Todo Evolution application on Kubernetes, featuring PWA, Voice Interface, AI Optimization, and Cloud-Native Architecture.

## Features

- **Cloud-Native Architecture**: Microservices-based deployment with Kubernetes
- **Progressive Web App (PWA)**: Mobile-first frontend with offline capabilities
- **Voice Interface**: Multilingual voice commands (English & Urdu)
- **AI Optimization**: Intelligent task management with ML-powered suggestions
- **Event-Driven**: Kafka-based event streaming for scalability
- **Service Mesh**: Dapr integration for service-to-service communication
- **Auto-Scaling**: Horizontal Pod Autoscaler (HPA) with intelligent scaling policies
- **High Availability**: Multi-replica deployments with pod disruption budgets
- **Observability**: Integrated Prometheus, Grafana, and Jaeger

## Prerequisites

- Kubernetes 1.28+
- Helm 3.12+
- kubectl configured with cluster access
- cert-manager (for TLS certificates)
- nginx-ingress-controller
- Dapr 1.12+ (optional, but recommended)
- Storage provisioner for persistent volumes

## Installation

### Quick Start

```bash
# Add the Bitnami repository for dependencies
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Install the chart with default values
helm install todo-app ./helm-charts/todo-app \
  --namespace todo-app \
  --create-namespace
```

### Production Deployment

```bash
# Create namespace
kubectl create namespace todo-app

# Install with custom values
helm install todo-app ./helm-charts/todo-app \
  --namespace todo-app \
  --set global.domain=todo-app.example.com \
  --set postgresql.auth.password=YOUR_SECURE_PASSWORD \
  --set redis.auth.password=YOUR_SECURE_REDIS_PASSWORD \
  --set secrets.JWT_SECRET_KEY=YOUR_JWT_SECRET \
  --set secrets.OPENAI_API_KEY=YOUR_OPENAI_KEY \
  --set-file secrets.tlsCert=./tls.crt \
  --set-file secrets.tlsKey=./tls.key
```

### Using Custom Values File

```bash
# Create custom values file
cat > my-values.yaml <<EOF
global:
  domain: todo-app.mycompany.com

frontend:
  replicaCount: 5
  resources:
    requests:
      cpu: 200m
      memory: 512Mi

backend:
  replicaCount: 3
  resources:
    requests:
      cpu: 400m
      memory: 1Gi

postgresql:
  auth:
    password: secure-db-password

redis:
  auth:
    password: secure-redis-password
EOF

# Install with custom values
helm install todo-app ./helm-charts/todo-app \
  --namespace todo-app \
  --create-namespace \
  --values my-values.yaml
```

## Configuration

### Key Parameters

#### Global Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.environment` | Deployment environment | `production` |
| `global.domain` | Application domain | `todo-app.example.com` |
| `global.storageClass` | Storage class for PVCs | `standard` |

#### Frontend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.replicaCount` | Number of frontend replicas | `3` |
| `frontend.image.repository` | Frontend image repository | `todo-app/frontend` |
| `frontend.image.tag` | Frontend image tag | `2.0.0` |
| `frontend.resources.requests.cpu` | CPU request | `100m` |
| `frontend.resources.requests.memory` | Memory request | `256Mi` |
| `frontend.autoscaling.enabled` | Enable HPA | `true` |
| `frontend.autoscaling.minReplicas` | Minimum replicas | `3` |
| `frontend.autoscaling.maxReplicas` | Maximum replicas | `15` |

#### Backend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.replicaCount` | Number of backend replicas | `2` |
| `backend.image.repository` | Backend image repository | `todo-app/backend` |
| `backend.image.tag` | Backend image tag | `2.0.0` |
| `backend.resources.requests.cpu` | CPU request | `200m` |
| `backend.resources.requests.memory` | Memory request | `512Mi` |
| `backend.autoscaling.enabled` | Enable HPA | `true` |
| `backend.autoscaling.minReplicas` | Minimum replicas | `2` |
| `backend.autoscaling.maxReplicas` | Maximum replicas | `10` |

#### Database Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `postgresql.enabled` | Enable PostgreSQL | `true` |
| `postgresql.auth.database` | Database name | `todo_db` |
| `postgresql.auth.username` | Database username | `postgres` |
| `postgresql.auth.password` | Database password | `""` (required) |
| `postgresql.primary.persistence.size` | Database storage size | `50Gi` |

#### Redis Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `redis.enabled` | Enable Redis | `true` |
| `redis.auth.enabled` | Enable Redis authentication | `true` |
| `redis.auth.password` | Redis password | `""` (required) |
| `redis.master.persistence.size` | Redis storage size | `10Gi` |

#### Kafka Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `kafka.enabled` | Enable Kafka | `true` |
| `kafka.replicaCount` | Number of Kafka brokers | `3` |
| `kafka.persistence.size` | Kafka storage size | `50Gi` |
| `kafka.zookeeper.replicaCount` | Number of ZooKeeper nodes | `3` |

#### Ingress Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable Ingress | `true` |
| `ingress.className` | Ingress class | `nginx` |
| `ingress.tls[0].secretName` | TLS secret name | `todo-app-tls` |

## Upgrading

```bash
# Upgrade to new version
helm upgrade todo-app ./helm-charts/todo-app \
  --namespace todo-app \
  --values my-values.yaml

# Roll back to previous version
helm rollback todo-app -n todo-app
```

## Uninstallation

```bash
# Uninstall the chart
helm uninstall todo-app -n todo-app

# Delete PVCs (if needed)
kubectl delete pvc -n todo-app --all

# Delete namespace
kubectl delete namespace todo-app
```

## Monitoring

### Prometheus Metrics

The application exposes Prometheus metrics on port 9090:

```bash
kubectl port-forward -n todo-app svc/prometheus 9090:9090
```

### Grafana Dashboards

Access Grafana dashboards:

```bash
kubectl port-forward -n todo-app svc/grafana 3000:3000
```

### Jaeger Tracing

View distributed traces:

```bash
kubectl port-forward -n todo-app svc/jaeger 16686:16686
```

## Scaling

### Manual Scaling

```bash
# Scale frontend
kubectl scale deployment/todo-app-frontend -n todo-app --replicas=10

# Scale backend
kubectl scale deployment/todo-app-backend -n todo-app --replicas=5
```

### Auto-Scaling

The HPA automatically scales based on:
- CPU utilization (target: 70%)
- Memory utilization (target: 80%)
- Custom metrics (requests per second)

```bash
# Check HPA status
kubectl get hpa -n todo-app

# Describe HPA
kubectl describe hpa todo-app-frontend-hpa -n todo-app
```

## Troubleshooting

### Check Pod Status

```bash
kubectl get pods -n todo-app
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app -f
```

### Check Services

```bash
kubectl get svc -n todo-app
kubectl describe svc todo-app-backend -n todo-app
```

### Check Ingress

```bash
kubectl get ingress -n todo-app
kubectl describe ingress todo-app -n todo-app
```

### Database Connection Issues

```bash
# Test database connection
kubectl run psql-test --rm -it --image=postgres:16 -n todo-app -- \
  psql -h todo-app-postgresql -U postgres -d todo_db

# Check database logs
kubectl logs -n todo-app statefulset/todo-app-postgresql
```

### Redis Connection Issues

```bash
# Test Redis connection
kubectl run redis-test --rm -it --image=redis:7 -n todo-app -- \
  redis-cli -h todo-app-redis-master -a YOUR_REDIS_PASSWORD ping
```

## Security Considerations

1. **Secrets Management**: Use external secret management (e.g., HashiCorp Vault, AWS Secrets Manager)
2. **TLS Certificates**: Configure cert-manager for automatic certificate renewal
3. **Network Policies**: Enable network policies to restrict pod-to-pod communication
4. **RBAC**: Review and customize RBAC rules for least privilege access
5. **Pod Security**: Pods run as non-root user with security contexts
6. **Image Scanning**: Scan container images for vulnerabilities before deployment

## Multi-Cloud Support

This chart is tested and works on:

- **AWS EKS** (Elastic Kubernetes Service)
- **GCP GKE** (Google Kubernetes Engine)
- **Azure AKS** (Azure Kubernetes Service)
- **Self-hosted Kubernetes** (1.28+)

### Cloud-Specific Configuration

#### AWS EKS

```yaml
global:
  storageClass: gp3

ingress:
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
```

#### GCP GKE

```yaml
global:
  storageClass: pd-ssd

ingress:
  annotations:
    kubernetes.io/ingress.class: gce
```

#### Azure AKS

```yaml
global:
  storageClass: managed-premium

ingress:
  annotations:
    kubernetes.io/ingress.class: azure/application-gateway
```

## Performance Tuning

### Resource Optimization

1. **CPU Limits**: Adjust based on actual usage patterns
2. **Memory Limits**: Monitor OOMKill events and adjust accordingly
3. **Replica Count**: Scale based on traffic patterns
4. **Database Connection Pooling**: Configure appropriate pool sizes
5. **Cache Strategy**: Optimize Redis cache hit rates

### Load Testing

```bash
# Install k6 or use any load testing tool
k6 run --vus 100 --duration 5m load-test.js
```

## Support

- Documentation: https://todo-app.example.com/docs
- Issues: https://github.com/todo-app/todo-evolution/issues
- Email: admin@todo-app.example.com
- Slack: #todo-app-support

## License

MIT License - see LICENSE file for details

## Contributors

- Todo App Team
- Community Contributors

## Version History

### 2.0.0 (Current)
- Initial Helm chart release
- Full Kubernetes deployment support
- Multi-cloud compatibility
- Integrated monitoring and observability
- Event-driven architecture with Kafka
- Dapr service mesh integration
