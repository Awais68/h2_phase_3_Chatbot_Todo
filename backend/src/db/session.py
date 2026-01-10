"""
Database session management for PostgreSQL connection.
"""
from typing import Generator
from sqlmodel import create_engine, Session
from src.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session.

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session
