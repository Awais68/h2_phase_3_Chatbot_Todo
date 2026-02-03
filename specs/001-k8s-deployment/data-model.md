# Data Model: Kubernetes Resources for Todo AI Chatbot

## Overview
This document defines the Kubernetes resources and configuration structures for the Todo AI Chatbot deployment. It outlines the entities, relationships, and schemas used in the Kubernetes manifests and Helm charts.

## Kubernetes Resource Entities

### 1. Namespace
**Purpose**: Isolate the Todo AI Chatbot application in its own namespace
**Schema**:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-chatbot  # Fixed name for the application namespace
```

### 2. ConfigMap
**Purpose**: Store non-sensitive configuration data for the application
**Schema**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-config           # Configuration name
  namespace: todo-chatbot     # Associated namespace
data:                        # Key-value pairs of configuration
  FRONTEND_URL: string       # Frontend application URL
  BACKEND_URL: string        # Backend API URL
  LOG_LEVEL: string          # Logging verbosity level
  ENVIRONMENT: string        # Environment name (dev, staging, prod)
```

### 3. Secret
**Purpose**: Store sensitive information securely
**Schema**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets          # Secret name
  namespace: todo-chatbot     # Associated namespace
type: Opaque                 # Standard secret type
data:                        # Base64 encoded sensitive data
  DATABASE_URL: string       # Encoded database connection string
  OPENAI_API_KEY: string     # Encoded OpenAI API key
  OPENAI_DOMAIN_KEY: string  # Encoded OpenAI domain key
  BETTER_AUTH_SECRET: string # Encoded authentication secret
```

### 4. Deployment
**Purpose**: Define how application containers should be deployed and managed
**Schema**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: string               # Deployment name (frontend, backend, mcp)
  namespace: todo-chatbot    # Associated namespace
  labels:                    # Labels for identification
    app: string              # Application name
spec:
  replicas: integer          # Number of pod replicas (default: 2)
  selector:                  # Label selector for pods
    matchLabels:
      app: string            # Must match pod template labels
  template:                  # Pod template specification
    metadata:
      labels:                # Pod labels
        app: string          # Application identifier
    spec:
      containers:            # List of containers in the pod
      - name: string         # Container name
        image: string        # Container image with tag
        imagePullPolicy: string  # Image pull policy (Always, IfNotPresent, Never)
        ports:               # List of container ports
        - containerPort: integer  # Port number
          name: string       # Port name
        env:                 # Environment variables
        - name: string       # Variable name
          valueFrom:         # Source for variable value
            secretKeyRef:    # From secret
              name: string   # Secret name
              key: string    # Secret key
            configMapRef:    # From configmap
              name: string   # ConfigMap name
              key: string    # ConfigMap key
        resources:           # Resource constraints
          requests:          # Minimum resources
            cpu: string      # CPU request (e.g., "100m")
            memory: string   # Memory request (e.g., "128Mi")
          limits:            # Maximum resources
            cpu: string      # CPU limit
            memory: string   # Memory limit
        livenessProbe:       # Liveness probe configuration
          httpGet:           # HTTP GET probe
            path: string     # Health check path
            port: integer    # Health check port
          initialDelaySeconds: integer  # Initial delay before probe
          periodSeconds: integer       # Interval between probes
        readinessProbe:      # Readiness probe configuration
          httpGet:           # HTTP GET probe
            path: string     # Health check path
            port: integer    # Health check port
          initialDelaySeconds: integer  # Initial delay before probe
          periodSeconds: integer       # Interval between probes
```

### 5. Service
**Purpose**: Expose applications to network traffic
**Schema**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: string               # Service name
  namespace: todo-chatbot    # Associated namespace
  labels:                    # Labels for identification
    app: string              # Application name
spec:
  selector:                  # Selector for pods to expose
    app: string              # Matches pod labels
  ports:                     # List of service ports
  - protocol: string         # Protocol (TCP, UDP, SCTP)
    port: integer            # Service port
    targetPort: integer      # Target port on pod
    name: string             # Port name
  type: string               # Service type (ClusterIP, NodePort, LoadBalancer)
```

### 6. Ingress
**Purpose**: Manage external access to services
**Schema**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-ingress         # Ingress name
  namespace: todo-chatbot    # Associated namespace
  annotations:               # Ingress controller specific annotations
    nginx.ingress.kubernetes.io/rewrite-target: string  # Path rewrite rule
spec:
  rules:                     # List of ingress rules
  - host: string             # Host name (optional)
    http:
      paths:                 # List of path rules
      - path: string         # Path pattern
        pathType: string     # Path type (Exact, Prefix, ImplementationSpecific)
        backend:             # Backend service
          service:
            name: string     # Service name
            port:
              number: integer  # Service port
```

## Helm Values Schema

### Global Configuration
```yaml
global:
  imageRegistry: string      # Global image registry
  imagePullSecrets: []       # Global image pull secrets
  storageClass: string       # Global storage class
```

### Application-Specific Values
```yaml
# Namespace configuration
namespace:
  name: string              # Namespace name (default: todo-chatbot)

# Frontend configuration
frontend:
  replicaCount: integer     # Number of frontend replicas (default: 2)
  image:
    repository: string      # Frontend image repository
    tag: string            # Frontend image tag
    pullPolicy: string     # Image pull policy
  service:
    type: string           # Service type (default: ClusterIP)
    port: integer          # Service port (default: 3000)
  resources:               # Resource constraints
    limits:
      cpu: string          # CPU limit
      memory: string       # Memory limit
    requests:
      cpu: string          # CPU request
      memory: string       # Memory request
  nodeSelector: {}         # Node selector for frontend pods
  tolerations: []          # Tolerations for frontend pods
  affinity: {}             # Affinity rules for frontend pods

# Backend configuration
backend:
  replicaCount: integer     # Number of backend replicas (default: 2)
  image:
    repository: string      # Backend image repository
    tag: string            # Backend image tag
    pullPolicy: string     # Image pull policy
  service:
    type: string           # Service type (default: ClusterIP)
    port: integer          # Service port (default: 8000)
  resources:               # Resource constraints (similar to frontend)
    limits:
      cpu: string
      memory: string
    requests:
      cpu: string
      memory: string
  nodeSelector: {}
  tolerations: []
  affinity: {}

# MCP server configuration
mcp:
  replicaCount: integer     # Number of MCP server replicas (default: 2)
  image:
    repository: string      # MCP server image repository
    tag: string            # MCP server image tag
    pullPolicy: string     # Image pull policy
  service:
    type: string           # Service type (default: ClusterIP)
    port: integer          # Service port (default: 3001)
  resources:               # Resource constraints (similar to others)
    limits:
      cpu: string
      memory: string
    requests:
      cpu: string
      memory: string
  nodeSelector: {}
  tolerations: []
  affinity: {}

# Ingress configuration
ingress:
  enabled: boolean         # Enable ingress (default: true)
  className: string        # Ingress class name
  annotations: {}          # Ingress annotations
  hosts:                   # List of host configurations
    - host: string         # Host name
      paths:               # List of paths
        - path: string     # Path
          pathType: string # Path type
  tls: []                  # TLS configuration

# Secrets configuration
secrets:
  databaseUrl: string      # Database URL
  openaiApiKey: string     # OpenAI API key
  openaiDomainKey: string  # OpenAI domain key
  betterAuthSecret: string # Better Auth secret

# ConfigMap configuration
config:
  frontendUrl: string      # Frontend URL
  backendUrl: string       # Backend URL
  environment: string      # Environment name
  logLevel: string         # Log level
```

## Relationship Diagram

```
Namespace (todo-chatbot)
    |
    |-- ConfigMap (todo-config)
    |-- Secret (todo-secrets)
    |
    |-- Deployment (frontend)
    |   |-- Service (frontend-service)
    |   |-- Pods (frontend-pod-*)
    |
    |-- Deployment (backend)
    |   |-- Service (backend-service)
    |   |-- Pods (backend-pod-*)
    |
    |-- Deployment (mcp)
        |-- Service (mcp-service)
        |-- Pods (mcp-pod-*)

    |-- Ingress (todo-ingress)
        |-- Routes to Services
```

## Validation Rules

### 1. Deployment Validation
- Replicas must be >= 1 for availability
- Resource requests must be <= limits
- Image pull policy must be one of: Always, IfNotPresent, Never
- Container ports must be valid (1-65535)

### 2. Service Validation
- Service type must be one of: ClusterIP, NodePort, LoadBalancer
- Port numbers must be valid (1-65535)
- Target port must match container port

### 3. Ingress Validation
- Path type must be one of: Exact, Prefix, ImplementationSpecific
- Host names must be valid DNS names
- Backend services must exist in the same namespace

### 4. Secret/ConfigMap Validation
- Keys must be valid DNS subdomain names
- Values must not exceed Kubernetes limits (1MB for secrets)
- Required keys must be present based on application needs

## State Transitions

### Pod Lifecycle States
```
Pending → Running → Succeeded/Terminated
           ↓
         Failed
```

### Deployment States
```
Active → Updating → Active
  ↓         ↓         ↓
Failed ←  Paused  ←  Active
```

## API Version Compatibility

### Kubernetes Versions Supported
- Deployment: apps/v1 (Kubernetes 1.16+)
- Service: v1 (all versions)
- ConfigMap/Secret: v1 (all versions)
- Ingress: networking.k8s.io/v1 (Kubernetes 1.19+)