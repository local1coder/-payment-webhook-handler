# Logger configuration with rotating file handler
import logging
from logging.handlers import RotatingFileHandler
import os
from app.core.config import LOG_FILE

# LOG_FILE is a string path
LOG_FILE_PATH = str(LOG_FILE)
print("LOG_FILE_PATH:", LOG_FILE_PATH)

# here checking log directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)


# Create the main logger
logger = logging.getLogger("webhook_logger")
logger.setLevel(logging.INFO)  # here set minimum log level
logger.propagate = False       # For prevent duplicate logs in FastAPI

# here clearing any existing handlers to avoid duplicate logs
if logger.hasHandlers():
    logger.handlers.clear()

# here console handler for real-time logging
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Standard log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
stream_handler.setFormatter(formatter)

# here attach console handler to logger
logger.addHandler(stream_handler)

# File handler with rotation
file_handler = RotatingFileHandler(
    LOG_FILE_PATH,        # Path to log file
    maxBytes=5 * 1024 * 1024,  # 5 MB per file
    backupCount=3,        # Keeping up to 3 backup files
    encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# here attaching file handler to logger
logger.addHandler(file_handler)

logger.info("Logger initialized successfully")