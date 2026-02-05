"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI, Response
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
from src.api import auth, tasks, sync, push, chat, analytics, recurring

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
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


@app.on_event("startup")
def on_startup():
    """Initialize database tables on startup."""
    SQLModel.metadata.create_all(engine)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/ready")
def ready_check():
    """Readiness check endpoint."""
    return {"status": "ready"}
