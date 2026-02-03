# syntax=docker/dockerfile:1

# =========================
# Base image
# =========================
FROM python:3.13-slim AS base

# Install curl for healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# =========================
# Builder stage
# =========================
FROM base AS builder

WORKDIR /app

# Install uv (fast Python package manager) from official container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files first for better cache utilization
COPY --link pyproject.toml ./
COPY --link uv.lock ./

# Create virtual environment and install dependencies
ENV UV_CACHE_DIR=/root/.cache/uv
RUN --mount=type=cache,target=$UV_CACHE_DIR \
    uv venv /app/.venv && \
    . /app/.venv/bin/activate && \
    pip install --upgrade pip && \
    uv pip install --no-cache --compile -r pyproject.toml

# =========================
# Final image
# =========================
FROM base AS final

WORKDIR /app

# Create non-root user and group
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code (including MCP server from backend/src/mcp)
COPY --link . .

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8001

# Switch to non-root user
USER appuser

# Set working directory for the user
WORKDIR /app

# Expose port
EXPOSE 8001

# Healthcheck endpoint (assuming MCP server has a health endpoint)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8001}/health || exit 1

# Start the MCP server (adjust the command based on how the MCP server should be started)
CMD ["sh", "-c", "python -m src.mcp.server --host 0.0.0.0 --port ${PORT:-8001}"]