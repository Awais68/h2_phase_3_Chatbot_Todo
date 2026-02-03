# Docker Image Optimization Guide

## Current Image Sizes

Check current sizes:
```bash
docker images | grep todo-
```

## Optimization Techniques

### 1. Use Multi-Stage Builds ✓ (Already implemented)

Separate build dependencies from runtime:
```dockerfile
FROM python:3.11-slim AS builder
# Build dependencies
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
# Copy only what's needed
COPY --from=builder /root/.local /root/.local
```

### 2. Use Smaller Base Images

**Python:**
- ✓ Using `python:3.11-slim` (good)
- Alternative: `python:3.11-alpine` (smaller but may have compatibility issues)

**Node.js:**
- ✓ Using `node:20-alpine` (optimal)

### 3. Minimize Layers

Combine RUN commands:
```dockerfile
# Bad: 3 layers
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# Good: 1 layer
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*
```

### 4. Clean Package Manager Cache

**Python:**
```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

**APT:**
```dockerfile
RUN apt-get update && \
    apt-get install -y package && \
    rm -rf /var/lib/apt/lists/*
```

**NPM:**
```dockerfile
RUN npm ci --only=production && \
    npm cache clean --force
```

### 5. Use .dockerignore ✓ (Already implemented)

Exclude unnecessary files from build context.

### 6. Order Dockerfile Commands by Change Frequency ✓

1. Base image
2. System dependencies
3. Application dependencies (requirements.txt)
4. Application code

### 7. Remove Development Dependencies

Production images shouldn't include:
- Testing frameworks
- Development tools
- Documentation
- Example files

### 8. Optimize Layer Caching

Copy dependency files before source code:
```dockerfile
# Dependencies change less frequently
COPY requirements.txt .
RUN pip install -r requirements.txt

# Source code changes frequently
COPY . .
```

## Using Docker AI (if available)

```bash
# Analyze Dockerfile
docker ai "analyze docker/backend/Dockerfile and suggest improvements"

# Optimize for size
docker ai "how can I reduce the size of this image: todo-backend:latest"

# Security recommendations
docker ai "what security improvements can I make to this Dockerfile"
```

## Manual Analysis Tools

### Docker History

```bash
# View layer history and sizes
docker history todo-backend:latest

# See full commands
docker history --no-trunc todo-backend:latest
```

### Dive - Layer Analysis

```bash
# Install
brew install dive

# Analyze
dive todo-backend:latest

# In dive UI:
# - Tab: Switch between layers and files
# - Space: Collapse/expand directories
# - Ctrl+U: Show only unmodified files
# - Ctrl+A: Show aggregated changes
```

Look for:
- Large layers
- Wasted space (files added then removed)
- Duplicate files
- Inefficient layer usage

### Trivy - Security Scanning

```bash
# Install
brew install trivy

# Scan image
trivy image todo-backend:latest

# Scan with severity filter
trivy image --severity HIGH,CRITICAL todo-backend:latest

# Generate report
trivy image -f json -o report.json todo-backend:latest
```

## Optimization Checklist

Backend Dockerfile:
- [x] Multi-stage build
- [x] Slim base image
- [x] Combined RUN commands
- [x] No cache for pip
- [x] Removed apt lists
- [x] Non-root user
- [ ] Consider Alpine base (test compatibility)
- [ ] Audit installed packages (remove unnecessary)

MCP Server Dockerfile:
- [x] Slim base image
- [x] No cache for pip
- [x] Non-root user
- [ ] Multi-stage build (could improve)
- [ ] Audit dependencies

Frontend Dockerfile:
- [x] Multi-stage build (deps, builder, runner)
- [x] Alpine base
- [x] Standalone output
- [x] Clean npm cache
- [x] Non-root user
- [ ] Optimize node_modules (already using standalone)

## Advanced Optimizations

### 1. Distroless Images (Advanced)

For maximum security and minimal size:
```dockerfile
FROM gcr.io/distroless/python3-debian11
# No shell, no package manager
# Only runtime dependencies
```

### 2. Scratch Images (Advanced)

For compiled languages (Go, Rust):
```dockerfile
FROM scratch
COPY --from=builder /app/binary /binary
CMD ["/binary"]
```

### 3. Layer Squashing

Reduce layers after build:
```bash
docker build --squash -t todo-backend:optimized .
```

## Rebuilding Optimized Images

1. Update Dockerfiles with optimizations
2. Rebuild:
```bash
./scripts/docker/build-all-images.sh
```

3. Compare sizes:
```bash
docker images | grep todo-
```

4. Test functionality:
```bash
docker-compose up -d
# Test application
```

5. If all works, load to Minikube:
```bash
./scripts/docker/load-to-minikube.sh
```

## Target Sizes

- Backend: < 400MB
- MCP Server: < 350MB
- Frontend: < 200MB

## Measuring Success

```bash
# Before optimization
BEFORE=$(docker images --format "{{.Size}}" todo-backend:latest)

# After optimization
AFTER=$(docker images --format "{{.Size}}" todo-backend:optimized)

# Calculate reduction
echo "Size reduction: $BEFORE → $AFTER"
```