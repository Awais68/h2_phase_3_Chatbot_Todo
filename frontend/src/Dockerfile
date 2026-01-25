# syntax=docker/dockerfile:1

ARG NODE_VERSION=22.13.1
FROM node:${NODE_VERSION}-slim AS base
WORKDIR /app

# Install system dependencies for Prisma (for native bindings)
RUN apt-get update && \
    apt-get install -y --no-install-recommends openssl && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies only, leveraging cache
COPY --link package.json ./
COPY --link package-lock.json ./

RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Copy the rest of the application source code
COPY --link . .

# Build the Next.js app and generate Prisma client
RUN npm run build

# Remove dev dependencies to reduce image size
RUN npm prune --production

# --- Production image ---
FROM node:${NODE_VERSION}-slim AS final
WORKDIR /app

# System dependencies for Prisma
RUN apt-get update && \
    apt-get install -y --no-install-recommends openssl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy built app and production node_modules from builder
COPY --from=base /app/.next ./.next
COPY --from=base /app/public ./public
COPY --from=base /app/node_modules ./node_modules
COPY --from=base /app/package.json ./
COPY --from=base /app/prisma ./prisma
COPY --from=base /app/next.config.js ./
COPY --from=base /app/tsconfig.json ./

# If you have any other files needed at runtime, copy them here

ENV NODE_ENV=production
ENV NODE_OPTIONS="--max-old-space-size=4096"

USER appuser

EXPOSE 3000
CMD ["npm", "start"]
