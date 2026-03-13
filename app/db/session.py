# SQLAlchemy Async Database Session Configuration
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Async Engine Setup
# I uses conn pooling for efficient async database operations
async_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,        # Number of connections to keep in the pool
    max_overflow=30,     # Extra connections allowed beyond pool_size
    pool_timeout=30,     # Seconds to wait before giving up on getting a connection
    pool_recycle=1800,   # Recycle connections after 30 minutes
    echo=False,          # Set True for SQL query debugging
)


# Async Session Factory
# It provides a session class for async database operations
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent automatic expiration of objects after commit
)

# Base Model Class
# All SQLAlchemy models should inherit from this Base
Base = declarative_base()