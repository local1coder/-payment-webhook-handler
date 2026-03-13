# Here app bootstraping 
import time
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.api.routes import router
from app.db.session import Base, async_engine
from app.core.logger_middleware import logger
from app.core.limiter import limiter

# Here initialize app
app = FastAPI(title="Payment Webhook System")

# Initialize rate limiter
app.state.limiter = limiter

# Exception Handlers
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    Return JSON response when rate limit is exceeded.
    """
    return JSONResponse(
        status_code=429,
        content={"error": "Status: 429 Too many requests. Please try again later."}
    )

# Include api routes
app.include_router(router)

# startup event
@app.on_event("startup")
async def on_startup():
    """
    Here ensuring database tables are created at startup (for dev environments).
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ensured at startup")

# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Logs incoming requests and outgoing responses with processing time.
    """
    start_time = time.time()

    # Read request body for logging
    body_bytes = await request.body()
    logger.info(f"Request: {request.method} {request.url} - Body length: {len(body_bytes)}")

    # Process the request
    response = await call_next(request)

    # compute processing time in milliseconds
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Response: status_code={response.status_code} - Processed in {process_time:.2f} ms")

    return response