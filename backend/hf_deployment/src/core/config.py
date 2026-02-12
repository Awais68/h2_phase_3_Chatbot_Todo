"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "Todo Evolution API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./todo_db.sqlite"

    # Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://mission-impossible-with-chatbot-git-main-hamzajiis-projects.vercel.app",
        "https://awais68-todo-chatbot.hf.space"
    ]

    # Better Auth (placeholder for future implementation)
    BETTER_AUTH_ENABLED: bool = False
    BETTER_AUTH_SECRET: Optional[str] = None
    BETTER_AUTH_URL: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env


settings = Settings()
