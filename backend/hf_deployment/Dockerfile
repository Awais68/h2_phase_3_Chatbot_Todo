# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_hf.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:7860/health')"

# Create startup script
RUN echo '#!/bin/bash\nset -e\necho "Running database migrations..."\npython run_migrations.py || echo "Migrations completed or skipped"\necho "Starting application..."\nexec uvicorn app:app --host 0.0.0.0 --port 7860' > /app/start.sh && chmod +x /app/start.sh

# Run the application with migrations
CMD ["/app/start.sh"]
