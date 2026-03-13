# Generate HMAC-SHA256 Signatures for Mock Payloads
import hmac
import hashlib
import os

# Shared secret used for webhook signature verification
SECRET = "test_secret"

# Dir containing mock JSON payloads
MOCK_FOLDER = "mock_payloads"

# Loop over all JSON files in the folder
for filename in os.listdir(MOCK_FOLDER):
    if filename.endswith(".json"):
        filepath = os.path.join(MOCK_FOLDER, filename)

        # Read file as bytes
        with open(filepath, "rb") as f:
            body = f.read()

        # Normalize line endings to Unix-style
        body = body.replace(b"\r\n", b"\n")

        # Generate HMAC-SHA256 signature using the shared secret
        signature = hmac.new(SECRET.encode(), body, hashlib.sha256).hexdigest()

        # Print the filename and its corresponding signature
        print(f"{filename}: {signature}")