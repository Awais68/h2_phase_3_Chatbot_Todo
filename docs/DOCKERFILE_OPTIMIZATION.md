# Dockerfile Optimization Guide

## Best Practices

### Multi-stage Builds
Use multi-stage builds to reduce image size:
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
CMD ["node", "server.js"]
```

### Layer Caching
Order Dockerfile instructions to take advantage of layer caching:
```dockerfile
# Copy package files first (changes less frequently)
COPY package*.json ./
RUN npm ci

# Copy source code last (changes more frequently)
COPY . .
```

### Use Specific Tags
Always use specific version tags instead of `latest`:
```dockerfile
# Good
FROM node:18-alpine

# Avoid
FROM node:latest
```

### Minimal Base Images
Use minimal base images like Alpine:
```dockerfile
# Smaller attack surface and size
FROM node:18-alpine
```

### Security Hardening
Run containers as non-root user:
```dockerfile
FROM node:18-alpine
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs
```

### .dockerignore
Exclude unnecessary files with `.dockerignore`:
```
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.nyc_output
coverage
.nyc_output
```

### Optimize RUN Instructions
Combine RUN instructions to reduce layers:
```dockerfile
# Good - combines multiple commands
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*

# Avoid - creates multiple layers
RUN apt-get update
RUN apt-get install package1
RUN apt-get install package2
```

### Use Build Args
Use ARG for configurable builds:
```dockerfile
ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}
```

### Health Checks
Add health checks for better container management:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

## Backend-Specific Optimizations

### Python/Flask/FastAPI
```dockerfile
FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

FROM base AS dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS runtime
WORKDIR /app
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

## Frontend-Specific Optimizations

### Next.js
```dockerfile
FROM node:18-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
ENV PORT 3000
CMD ["node", "server.js"]
```

## MCP Server Optimizations

### Node.js Server
```dockerfile
FROM node:18-alpine AS base
RUN apk add --no-cache dumb-init

FROM base AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

FROM base AS runtime
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && adduser -S mcp -u 1001
COPY --from=dependencies --chown=mcp:nodejs /app/node_modules ./node_modules
COPY --chown=mcp:nodejs . .
USER mcp
EXPOSE 3001
ENTRYPOINT ["dumb-init", "--"]
CMD ["npm", "start"]
```

## Security Considerations

### Scan Images
Regularly scan images for vulnerabilities:
```bash
docker scan your-image:tag
```

### Signed Images
Use signed images from trusted sources.

### Minimal Permissions
Grant minimal necessary permissions to containers.