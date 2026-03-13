from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
import os

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Default log file path (can be overridden by Settings)
LOG_FILE = BASE_DIR / "logs" / "webhook.log"


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables or .env file.
    Uses Pydantic's BaseSettings for type validation and default values.
    """
    # Application settings
    APP_NAME: str = "Payment Webhook System"
    DEBUG: bool = True  # Enable debug mode for development

    
    # Database settings
    DATABASE_URL: str = Field(
        default="postgresql://postgres:root@localhost:5432/webhook_payments",
        env="DATABASE_URL"
    )

    # Webhook settings
    WEBHOOK_SECRET: str = Field(
        default="test_secret",
        env="WEBHOOK_SECRET"
    )

    # Logging settings
    LOG_FILE: str = str(BASE_DIR / "logs/webhook.log")

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        """
        Pydantic configuration for loading environment variables from a .env file.
        """
        env_file = BASE_DIR / ".env"
        env_file_encoding = 'utf-8'


# Instantiate the settings object to be imported throughout the app
settings = Settings()





class TestSettings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"
    WEBHOOK_SECRET: str = "test_secret"

test_settings = TestSettings()