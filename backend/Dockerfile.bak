# Phase II Deployment - Dockerfile for FastAPI Backend
# This Dockerfile builds a production-ready container for the FastAPI application.
# Optimized for Render deployment.

# ============================================
# Stage: Production Runtime
# ============================================
FROM python:3.12-slim-bookworm

WORKDIR /app

# Create non-root user for security
RUN groupadd --gid=1000 appgroup && \
    useradd --uid=1000 --gid=appgroup --shell=/bin/bash --create-home appuser

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && \
    uv venv /app/.venv && \
    uv pip install --system --no-cache --compile -r pyproject.toml

# Copy application code
COPY --chown=appuser:appgroup main.py ./

# Switch to non-root user
USER appuser

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Expose port (Render will override PORT env var)
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Start the application - use PORT from environment (Render sets this)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
