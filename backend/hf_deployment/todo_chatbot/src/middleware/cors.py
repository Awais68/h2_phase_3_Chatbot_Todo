"""
CORS middleware configuration for frontend access.
"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.core.config import settings


def configure_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the application.

    Args:
        app: FastAPI application instance
    """
    # Allow all origins in development, restrict in production
    origins = settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=600,  # Cache preflight requests for 10 minutes
    )
