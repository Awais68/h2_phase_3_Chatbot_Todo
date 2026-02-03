# Minikube Docker Images

## Why Load Images to Minikube?

Minikube runs its own Docker daemon. Images built on your host machine are not automatically available to Minikube. You must either:
1. Build images directly in Minikube's Docker
2. Load images from host to Minikube

## Method 1: Build in Minikube Docker (Recommended)

### Advantages
- Faster for multiple builds
- No image transfer needed
- Direct access to images

### Process
```bash
# Set Docker environment to Minikube
eval $(minikube docker-env)

# Build all images
./scripts/docker/build-all-images.sh

# Reset to host Docker
eval $(minikube docker-env -u)
```

### Using Script
```bash
./scripts/docker/build-in-minikube.sh
```

**Important**: Images built this way will NOT appear in your host's `docker images` output.

## Method 2: Load from Host Docker

### Advantages
- Keep images in host Docker
- Can test locally before loading
- Version control easier

### Process
```bash
# First, build on host
./scripts/docker/build-all-images.sh

# Then load to Minikube
minikube image load todo-backend:latest
minikube image load todo-mcp-server:latest
minikube image load todo-frontend:latest
```

### Using Script
```bash
./scripts/docker/load-to-minikube.sh
```

## Verification

### Check images in Minikube
```bash
# Using script
./scripts/docker/verify-minikube-images.sh

# Manual check
minikube ssh docker images | grep todo-
```

## Image Pull Policy

In Kubernetes manifests, use `imagePullPolicy: Never` or `imagePullPolicy: IfNotPresent` for local images:

```yaml
spec:
  containers:
  - name: backend
    image: todo-backend:latest
    imagePullPolicy: Never  # Don't try to pull from registry
```

## Troubleshooting

### Images not found by Kubernetes
```bash
# Verify images in Minikube
minikube ssh docker images

# Reload images
./scripts/docker/load-to-minikube.sh

# Or rebuild in Minikube
./scripts/docker/build-in-minikube.sh
```

### Which Docker am I using?
```bash
# Check current Docker environment
docker context ls
echo $DOCKER_HOST

# If in Minikube Docker, you'll see Minikube context
```

### Reset Docker environment
```bash
# If stuck in Minikube Docker context
eval $(minikube docker-env -u)

# Or restart terminal
```

## Best Practices

1. **For Development**: Build in Minikube Docker
   - Faster iteration
   - No transfer overhead

2. **For Testing Registry Workflow**: Load from host
   - Tests pull policy
   - Simulates production

3. **Always verify** images are in Minikube before deploying

4. **Use specific tags** in production (not :latest)

## Rebuilding After Code Changes

```bash
# Rebuild in Minikube
eval $(minikube docker-env)
./scripts/docker/build-all-images.sh
eval $(minikube docker-env -u)

# Restart pods to use new images
kubectl rollout restart deployment/backend -n todo-chatbot
kubectl rollout restart deployment/mcp-server -n todo-chatbot
kubectl rollout restart deployment/frontend -n todo-chatbot
```