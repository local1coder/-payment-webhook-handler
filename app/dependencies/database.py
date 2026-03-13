# FastAPI Database Dependency
# Provides an async SQLAlchemy session to routes
# Used for: db: AsyncSession = Depends(get_db)  that is dependency injection using Depends

from app.db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db() -> AsyncSession:
    """
    Async generator that yields a database session.

    Usage in FastAPI route:
        async def endpoint(db: AsyncSession = Depends(get_db)):

    This ensures:
        1 Proper connection pooling
        2 Automatic cleanup after request
    """
    # Here creating a new async session
    async with AsyncSessionLocal() as db:
        # Yield the session to the route
        yield db
        # Session is automatically closed after the req