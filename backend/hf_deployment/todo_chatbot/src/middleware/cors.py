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
    # Allow all origins - credentials are set to False when using wildcard
    # This enables cross-origin requests from any frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,  # Must be False when using wildcard origins
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=86400,  # Cache preflight requests for 24 hours
    )
