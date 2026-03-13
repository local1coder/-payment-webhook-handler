# A utility or helper function parse payment event payload

def parse_payment_event(payload: dict):
    """
    Extract essential fields from a payment webhook payload.

    Args:
        payload (dict): The raw webhook JSON payload.

    Returns:
        tuple: (event_id, event_type, payment_id)

    Raises:
        ValueError: If any required field is missing.
        Exception: If any unexpected error occurs.
    """
    try:
        # Extract the event id from top-level payload
        event_id = payload.get("id")
        # Extract the event type (for instance, "payment.captured")
        event_type = payload.get("event")
        # Nested extraction of payment id
        payment_id = payload.get("payload", {}) \
                            .get("payment", {}) \
                            .get("entity", {}) \
                            .get("id")

        # Here ensuring all required fields are present
        if not all([event_id, event_type, payment_id]):
            raise ValueError("Missing required fields in payload")

        return event_id, event_type, payment_id

    except Exception as e:
        # Log parsing errors with payload for debugging instaed of printing for cleaner struct
        from app.core.logger_middleware import logger
        logger.error(f"Failed to parse payment event: {e} | payload={payload}")
        raise