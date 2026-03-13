# Webhook Security: HMAC Signature Verification
from app.core.config import settings
from .logger_middleware import logger
import hmac
import hashlib


def verify_signature(signature: str, body: bytes) -> bool:
    """
    Verify the HMAC SHA256 signature of a webhook request.

    Args:
        signature (str): The HMAC signature received in request headers.
        body (bytes): The raw request body.

    Returns:
        bool: True if signature matches, False otherwise.
    """

    # Here generate expected HMAC using the shared webhook secret
    # ensures that every comparison takes the same amount of time

    """
    For Instance:
              hmac.compare_digest(a, b)
              It checks all bytes of a and b, even if a mismatch is found early
              And the execution time does not reveal which bytes matched.
              Thus this prevents attackers from using timing measurements to guess your secret.
              Thus, secure
    """
    expected_signature = hmac.new(
        key=settings.WEBHOOK_SECRET.encode(),
        msg=body,
        digestmod=hashlib.sha256
    ).hexdigest()

    # Constant time comparison to prevent timing attacks
    if hmac.compare_digest(signature, expected_signature):
        logger.info(f"HMAC valid - signature={signature}")
        return True
    else:
        logger.warning(
            f"HMAC invalid - expected={expected_signature} | received={signature}"
        )
        return False