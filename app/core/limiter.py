# Rate Limiter Configuration
from slowapi import Limiter
from slowapi.util import get_remote_address

# Here initialize a global rate limiter instance
# and use the client IP address as the key to apply rate limits
limiter = Limiter(key_func=get_remote_address)