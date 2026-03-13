from fastapi import APIRouter, Request, Depends
from sqlalchemy import select

from app.services.webhook_service import WebhookService
from app.db.models import PaymentEvent
from app.schemas.payment_event import PaymentEventResponse
from app.dependencies.database import get_db
from app.core.decorators import validate_webhook
from app.core.limiter import limiter

# Initialize the FastAPI router
router = APIRouter(prefix="/api")


@router.post("/webhook/payments")
@limiter.limit("5/minute")  # Rate limit: max 5 requests per minute
@validate_webhook  # Custom decorator to verify webhook authenticity
async def receive_webhook(request: Request, db=Depends(get_db)):
    """
    Endpoint to receive payment webhooks.
    
    Steps:
    1. Read the JSON payload from the incoming request.
    2. Process and save the event using WebhookService with retry logic.
    3. Return a confirmation along with the generated event ID.
    """
    # Parse JSON payload from the webhook request
    payload = await request.json()
    
    # Process and save the webhook event
    event = await WebhookService.process_save_event(
        db, payload, max_retries=5, backoff_factor=0.3
    )
    
    # Return a simple acknowledgement
    return {"status": "received", "event_id": event.event_id}


@router.get("/payments/{payment_id}/events", response_model=list[PaymentEventResponse])
@limiter.limit("30/minute")  # Rate limit: max 30 requests per minute
async def get_events(payment_id: str, request: Request, db=Depends(get_db)):
    """
    Retrieve all events associated with a specific payment ID.
    
    Args:
        payment_id (str): The unique identifier of the payment.
    
    Returns:
        List of PaymentEventResponse objects.
    """
    # Query the database for events matching the payment_id
    result = await db.execute(
        select(PaymentEvent).where(PaymentEvent.payment_id == payment_id)
    )
    
    # Fetch all matched events as a list
    events = result.scalars().all()
    
    return events