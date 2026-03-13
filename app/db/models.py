# SQLAlchemy models for payment webhook events
from sqlalchemy import Column, Integer, String, JSON, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from .session import Base


class PaymentEvent(Base):
    """
    It represents a payment related event received from the webhook.

    Fields:
        -> id: Internal primary key.
        -> event_id: Unique identifier from the payment provider.
        -> payment_id: Associated payment ID.
        -> event_type: Type of event (for instane, "payment.captured").
        -> payload: Full webhook payload (JSON).
        -> received_at: Timestamp when the event was received.
    """

    __tablename__ = "payment_events"

    # ----------------------------------------
    # Columns
    # ----------------------------------------
    id = Column(Integer, primary_key=True)
    event_id = Column(String, unique=True, index=True)  # Unique webhook event id
    payment_id = Column(String, nullable=False)         # Associated payment
    event_type = Column(String, nullable=False)         # Event type from provider
    payload = Column(JSON, nullable=False)              # Full payload for record-keeping
    received_at = Column(DateTime(timezone=True), server_default=func.now())  # Auto timestamp

    # Table-level constraints
    # Ensures database-level idempotency: no duplicate event_ids
    __table_args__ = (
        UniqueConstraint("event_id", name="uq_event_id"),
    )