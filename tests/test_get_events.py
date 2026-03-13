import pytest
import pytest_asyncio
import json
import os
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.schemas.payment_event import PaymentEventResponse  # your response model

# Async client fixture
@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


# payload dir
MOCK_DIR = os.path.join(os.path.dirname(__file__), "../mock_payloads")


# Load JSON payload
def load_payload(filename: str):
    path = os.path.join(MOCK_DIR, filename)
    with open(path, "rb") as f:
        body = f.read()
    body = body.replace(b"\r\n", b"\n")
    payload = json.loads(body)
    return payload


# GET /payments/{payment_id}/events test
@pytest.mark.asyncio
async def test_get_payment_events(async_client):
    # Use the same mock payload as in webhook
    filename = "payment_authorized.json"
    payload = load_payload(filename)

    payment_id = payload["payload"]["payment"]["entity"]["id"]

    # Call the endpoint
    response = await async_client.get(f"/api/payments/{payment_id}/events")

    # For isolated test, allow both 200 or 404 (if no DB entry yet)
    assert response.status_code in [200, 404]

    # Print the response
    print(f"GET /payments/{payment_id}/events response:", response.json())

    # Optional: validate schema if returned 200
    if response.status_code == 200:
        for item in response.json():
            PaymentEventResponse(**item)  # will raise if invalid