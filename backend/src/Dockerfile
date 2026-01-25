# syntax=docker/dockerfile:1

# ----------- Base image (for both build and final) -----------
FROM python:3.13-slim AS base

# ----------- Builder stage: install dependencies and venv -----------
FROM base AS builder
WORKDIR /app

# Install uv (fast Python package manager) from official container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files first for better cache utilization
COPY --link pyproject.toml ./
# If you have a lock file, copy it too (but not .env or secrets)
COPY --link ../uv.lock ./uv.lock

# Create virtual environment and install dependencies
ENV UV_CACHE_DIR=/root/.cache/uv
RUN --mount=type=cache,target=$UV_CACHE_DIR \
    uv venv .venv && \
    uv pip install --system --no-cache --compile -r pyproject.toml

# ----------- Final stage: minimal runtime image -----------
FROM base AS final
WORKDIR /app

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code (src/ directory and entrypoint)
COPY --link . ./

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Healthcheck (optional, FastAPI default health endpoint is /health)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Start the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
