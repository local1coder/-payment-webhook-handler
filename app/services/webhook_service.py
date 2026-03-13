# Webhook Service for Payment Event Processing
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy import select

from app.db.models import PaymentEvent
from app.utils.parser import parse_payment_event
from app.core.logger_middleware import logger


class WebhookService:
    """
    Async service to process and save payment webhook events safely.
    Features:
        1 Idempotency checks
        2 ACID compliant transactions
        3 Retry logic with exponential backoff
        4 Row-level locking to prevent race conditions
    """

    @staticmethod
    async def process_save_event(
        db: AsyncSession,
        payload: dict,
        max_retries: int = 3,
        backoff_factor: float = 0.5
    ):
        """
        Process a webhook payload and save the event to the database safely.

        Args:
            db (AsyncSession): Async SQLAlchemy session.
            payload (dict): Incoming webhook JSON payload.
            max_retries (int): Max number of retry attempts for transient database errors.
            backoff_factor (float): Multiplier for exponential backoff between retries.

        Returns:
            PaymentEvent: The saved or existing PaymentEvent instance.
        """

        # Here parsing required data from the payload
        event_id, event_type, payment_id = parse_payment_event(payload)
        attempt = 0

        while attempt <= max_retries:
            try:
                # Start an async transaction
                async with db.begin():
                    # Check for existing event with row-level lock
                    stmt = select(PaymentEvent).where(PaymentEvent.event_id == event_id).with_for_update()
                    result = await db.execute(stmt)
                    existing_event = result.scalar_one_or_none()

                    if existing_event:
                        logger.info(f"Event {event_id} already exists, skipping.")
                        return existing_event

                    # Create and add new event
                    event = PaymentEvent(
                        event_id=event_id,
                        payment_id=payment_id,
                        event_type=event_type,
                        payload=payload
                    )
                    db.add(event)

                    # Flush to DB to generate IDs and refresh instance
                    await db.flush()
                    await db.refresh(event)

                    logger.info(f"Saved event {event_id} for payment {payment_id}")
                    return event

            except (OperationalError, IntegrityError) as e:
                # Rollback the transaction for retryable errors
                await db.rollback()
                attempt += 1

                if attempt > max_retries:
                    logger.error(f"Max retries reached for event {event_id}: {e}")
                    raise
                else:
                    # Exponential backoff before retrying
                    sleep_time = backoff_factor * (2 ** (attempt - 1))
                    logger.warning(
                        f"Retry {attempt} for event {event_id} in {sleep_time:.2f}s due to: {e}"
                    )
                    await asyncio.sleep(sleep_time)

            except Exception as e:
                # Catch-all for unexpected errors
                await db.rollback()
                logger.error(f"Unexpected error saving event {event_id}: {e}")
                raise