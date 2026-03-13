# Pydantic Schemas for payment events
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PaymentEventBase(BaseModel):
    """
    Base schema with common fields for payment events
    """
    event_id: str       # Unique event identifier
    payment_id: str     # Associated payment ID
    event_type: str     # Type of the event (for instance "payment.captured")


class PaymentEventCreate(PaymentEventBase):
    """
    Schema used when creating a new payment event.
    Includes the full payload received from the webhook.
    """
    payload: dict       # JSON payload of the event


class PaymentEventResponse(PaymentEventBase):
    """
    Schema used when returning payment events via api
    Includes timestamp when the event was received
    """
    received_at: datetime

    class Config:
        # For Enable orm mode to allow reading data from SQLAlchemy models 
        from_attributes = True