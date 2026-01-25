# syntax=docker/dockerfile:1

ARG NODE_VERSION=22.13.1
FROM node:${NODE_VERSION}-slim AS base
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -s /bin/bash appuser

# Copy dependency manifests first for better caching
COPY --link package.json package.json
COPY --link package-lock.json package-lock.json

# Copy prisma schema before npm install (needed for postinstall hook)
COPY --link prisma ./prisma

# Install dependencies with cache
RUN --mount=type=cache,target=/root/.npm \
    npm install --legacy-peer-deps

# Copy the rest of the application code (excluding files in .dockerignore)
COPY --link . .

# Copy environment files needed for build
COPY --link .env.production .env.production

# Set environment variables for build
ENV NEXT_PUBLIC_API_URL="http://localhost:8000"
ENV NEXT_PUBLIC_APP_URL="http://localhost:3000"
ENV NEXT_PUBLIC_APP_NAME="Todo Evolution"
ENV NEXT_PUBLIC_ENABLE_VOICE_COMMANDS=true
ENV NEXT_PUBLIC_ENABLE_MULTI_LANGUAGE=true
ENV NEXT_PUBLIC_VOICE_LANG="en-US"
ENV NEXT_PUBLIC_VOICE_AUTO_SPEAK=true
ENV NEXT_PUBLIC_ANALYTICS_DEFAULT_DAYS=30
ENV NEXT_PUBLIC_ENABLE_VOICE=true
ENV NEXT_PUBLIC_ENABLE_ANALYTICS=true
ENV NEXT_PUBLIC_ENABLE_RECURRING=true

# Copy environment variables to the default location for build
RUN cp .env.production .env

# Build the Next.js app (includes Prisma generate)
RUN --mount=type=cache,target=/root/.npm \
    npm run build

# Remove dev dependencies for production
RUN npm prune --production

# Final production image
FROM node:${NODE_VERSION}-slim AS final
WORKDIR /app

# Create non-root user in final image
RUN useradd -m -s /bin/bash appuser

# Copy built app and production dependencies from builder
COPY --from=base /app/.next ./.next
COPY --from=base /app/public ./public
# COPY --from=base /app/node_modules ./node_modules
COPY --from=base /app/package.json ./package.json
COPY --from=base /app/prisma ./prisma
COPY --from=base /app/src ./src
COPY --from=base /app/next.config.mjs ./next.config.mjs
COPY --from=base /app/tsconfig.json ./tsconfig.json

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV NODE_OPTIONS="--max-old-space-size=4096"

# Expose Next.js port
EXPOSE 3000

# Use non-root user
USER appuser

# Start the Next.js app using the standalone server
CMD ["node", ".next/standalone/server.js"]
