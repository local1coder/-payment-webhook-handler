import pytest
import pytest_asyncio
import json
import os
import hmac
import hashlib

from httpx import AsyncClient, ASGITransport

from app.main import app
from app.core.config import settings


# Async test client
@pytest_asyncio.fixture
async def async_client():
    """Async client for FastAPI testing"""
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        yield client


# payload dir
MOCK_DIR = os.path.join(
    os.path.dirname(__file__),
    "../mock_payloads"
)


# Loading JSON payload
def load_payload(filename: str):
    path = os.path.join(MOCK_DIR, filename)

    with open(path, "rb") as f:
        body = f.read()

    body = body.replace(b"\r\n", b"\n")
    payload = json.loads(body)

    return body, payload


# Generate HMAC
def generate_hmac(body: bytes) -> str:
    return hmac.new(
        settings.WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()


# Test webhook POST Req
@pytest.mark.asyncio
async def test_webhook_receive(async_client):

    filename = "payment_authorized.json"

    body, payload = load_payload(filename)

    signature = generate_hmac(body)

    headers = {
        "x-razorpay-signature": signature
    }

    response = await async_client.post("/api/webhook/payments", content=body, headers=headers)

    assert response.status_code == 200

    data = response.json()

    print("Webhook response:", data)

