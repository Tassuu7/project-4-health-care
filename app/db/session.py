"""
AegisCare Enterprise Patient Management System - Database Connection & Session Factory
Configures SQLAlchemy engine, session maker, connection pool, and request dependency.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.config import get_settings
from app.db.base import Base

settings = get_settings()

# Engine creation with SQLite/PostgreSQL optimizations
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO_SQL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)


def init_db():
    """Create all database tables defined by SQLAlchemy declarative models."""
    # Import all models to register with Base.metadata before create_all
    import app.models # noqa
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for yielding database session with automatic cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
