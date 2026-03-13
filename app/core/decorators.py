# This is custom webhook validation decorator
from fastapi import Request, HTTPException
from functools import wraps

from app.core.security import verify_signature
from app.core.logger_middleware import logger


def validate_webhook(func):
    """
    Decorator to validate incoming webhook requests.

    Steps:
    1. Extract the Request object from function args or kwargs.
    2. Retrieve the signature from the headers.
    3. Normalize the request body line endings.
    4. Verify the signature using verify_signature.
    5. Log success or failure, and raise HTTP 403 on invalid signature.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Attempt to get the Request object from kwargs or args
        request: Request = kwargs.get("request") or (args[0] if args else None)
        if request is None:
            raise RuntimeError("Request object not found for webhook validation")

        # extract signature from request headers
        signature = request.headers.get("x-razorpay-signature")

        # Read raw request body and normalize line endings
        body = await request.body()
        body = body.replace(b"\r\n", b"\n")  # Normalize to Unix-style newlines

        # verify webhook signature
        if not verify_signature(signature, body):
            logger.warning("Invalid webhook signature detected")
            raise HTTPException(status_code=403, detail="Invalid signature")

        logger.info("Webhook signature verified successfully")

        # Invoke the original endpoint func
        return await func(*args, **kwargs)

    return wrapper