README.md File For Assignment application  setup 

# A Webhook Payment system using FastAPI

## Index
1 Overall Project Structure
2 Features
3 [Requirements]  
4 [Setup](#setup)  
5 [Running the App]
6 [Running Tests] 



## Overall Project Structure


payment-webhook-handler
                        > app             # app bootraping
                              > main.py 
                              > core      # setting ahving ratelimiter, miidleware fro logging , custome decorator
                              > schemas   # pydantic schema

                        > tests           # test pytest cases
                        > mock_payloads   # contains mock payloads
                        > requirements.txt # dependeccies 
                        > .env             # stores secrets and configuration
                        > generate_all_hmac_signatures.py # Generate HMAC-SHA256 Signatures for Mock Payloads
                        > alembic          # database migration tool for Python projects that use SQLAlchemy
                        > DOCS.md
                        > README.md

## Features

  FastAPI webhook endpoint for payments (microservice).  
  Async tests using pytest  
  HMAC signature verification for webhooks.  
  Event retrieval endpoint with schema validation. 
  Rate Limiting
  ACID compliant transactions and Row-level locking to prevent race conditions
  Table level constraint
  custom webhook validation decorator
  Logger configuration with rotating file handler
  Webhook Security: HMAC Signature Verification
  Idempotency checks
  Retry logic with exponential backoff




## Requirements

  Python 3.10+  
  pip for dependency management  


Dependencies include:
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic-settings
python-dotenv
pytest
httpx
pytest
pytest-asyncio
pydantic
alembic
slowapi
asyncpg



## Setup

1.Clone the repository

Duumy Ref git clone https://github.com/your-username/fastapi-razorpay-webhook.git

clone https://github.com/local1coder/-payment-webhook-handler.git
cd -payment-webhook-handler


2. Create a virtual environment

python -m venv venv
source venv/bin/activate  # Linux 
D:\payment-webhook-handler\Scripts\activate     # Windows


3. Install dependencies

Using pip:
pip install -r requirements.txt


4. Set environment variables

Create a .env file in the project root:

DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost:5432/webhook_payments"
WEBHOOK_SECRET=test_secret
DEBUG=True
HOST=127.0.0.1
PORT=8000

## Running the App

Start the FastAPI server:
uvicorn app.main:app --reload

The server runs at public (local server) http://127.0.0.1:8000.

* Webhook endpoint: POST /api/webhook/payments
* Retrieve payment events: GET /api/payments/{payment_id}/events


## Running Tests

Tests are written with pytest and pytest-asyncio.
pytest -v

1 test_webhook.py ensures the webhook endpoint validates HMAC and processes payload.
2 test_get_events.py checks that payment events are correctly stored and retrieved.