"""
Hugging Face Space application entry point.
This file creates the FastAPI app for deployment on Hugging Face Spaces.
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel
from src.core.config import settings
from src.db.session import engine
from src.middleware.cors import configure_cors
from src.middleware.error_handler import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)
from src.api import auth, tasks, sync, push, chat, analytics, recurring, history
from src.services.scheduler_service import initialize_scheduler, shutdown_scheduler

# Import all models to register them with SQLModel metadata
# This ensures tables are created when SQLModel.metadata.create_all() is called
from src.models.task import Task  # noqa: F401
from src.models.task_history import TaskHistory  # noqa: F401
from src.models.notification_preference import NotificationPreference  # noqa: F401


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan event handler for startup and shutdown."""
    # Startup: Create all database tables
    SQLModel.metadata.create_all(engine)
    # Initialize scheduler with database connection
    initialize_scheduler(str(settings.DATABASE_URL))
    yield
    # Shutdown: Cleanup scheduler
    shutdown_scheduler()


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    debug=settings.DEBUG
)

# Configure CORS FIRST before any routes
configure_cors(app)

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Register API routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(sync.router)
app.include_router(push.router)
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])
app.include_router(recurring.router, prefix="/api", tags=["recurring"])
app.include_router(history.router, prefix="/api", tags=["history"])


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "deployment": "huggingface-space"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/ready")
def ready_check():
    """Readiness check endpoint."""
    return {"status": "ready"}


# For Hugging Face Space to run with Gradio if needed
def run_hf_space():
    import gradio as gr

    with gr.Blocks() as demo:
        gr.Markdown(f"# {settings.APP_NAME}")
        gr.Markdown(f"Version: {settings.APP_VERSION}")
        gr.Markdown("FastAPI backend running on Hugging Face Spaces")

        with gr.Row():
            with gr.Column():
                gr.Textbox(label="API Status", value="Healthy", interactive=False)
                gr.Textbox(label="API Endpoint", value="/docs", interactive=False)

        gr.Button("Open API Documentation").click(
            None,
            None,
            None,
            js="() => {window.open('/docs', '_blank');}"
        )

    return demo


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )