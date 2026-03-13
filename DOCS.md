This DOCS.md is for documented the webhook and query API

#Payment Webhook API Documentation

## Base URL
http://<HOST>:<PORT>

Defaults taken from .env:
1 HOST: 127.0.0.1
2 PORT: 8000




## 1. Webhook Receiver Endpoint
### POST /webhook/payments

Receives payment status updates from providers (Razorpay / PayPal).

Headers:

Header                   Description
Content-Type             Must be application/json
X-Razorpay-Signature     HMAC SHA256 signature (simulated)


Request Body (Json) :

{
  "event": "payment.authorized",
  "payload": {
    "payment": {
      "entity": {
        "id": "pay_014",
        "status": "authorized",
        "amount": 5000,
        "currency": "INR"
      }
    }
  },
  "created_at": 1751889865,
  "id": "evt_auth_014"
}



Behavior / Validations:
1 Validates signature against WEBHOOK_SECRET.
2 Rejects requests with:

  2.1 Missing/incorrect signature -> 403 Forbidden
  2.2 Invalid JSON -> 400 Bad Request
3 Deduplicates events by event_id.
4 Stores full payload in PostgreSQL with received_at timestamp.

Standard Responses:
Status                   Description
200 OK                   Event processed successfully
400 Bad Request          Invalid JSON or missing fields
403 Forbidden            Signature mismatch
405 Method Not Allowed   Wrong HTTP method




## 2. Payment event query endpoint
### GET /payments/{payment_id}/events
Fetches all events related to a specific payment ID.


Path Parameter:
Parameter      Type     Description
payment_id     string   ID of the payment (e.g., pay_014)

Response Example:
[
  {
    "event_type": "payment_authorized",
    "received_at": "2025-07-08T12:00:00Z"
  },
  {
    "event_type": "payment_captured",
    "received_at": "2025-07-08T12:01:23Z"
  }
]


Behavior / Edge Cases:
1 Events sorted chrono logical order by received_at.
2 Returns empty list if payment_id not found.
3 Returns 404 Not Found if payment_id format is invalid.

Responses:
Status              Description
200 OK              Successfully returned events
404 Not Found       Payment ID not found
400 Bad Request     Invalid payment ID format


## 3. Testing the Webhook
Using curl:

curl -X POST http://localhost:8000/webhook/payments \
-H "Content-Type: application/json" \
-H "X-Razorpay-Signature: TEST_SIGNATURE" \
-d @mock_payloads/payment_authorized.json




Fetching payment events:
curl http://localhost:8000/payments/pay_014/events