"""
config.py
---------
Centralized configuration. All secrets/config come from environment
variables (loaded from a local .env file via python-dotenv), so no
credentials ever need to be hardcoded or committed to source control.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # --- OpenRouter (OpenAI-compatible API, routes to Gemma 3 27B models) ---
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    
    OPENROUTER_MODEL= "google/gemma-3-27b-it"  # gemma model via OpenRouter
    OPENROUTER_MAX_TOKENS = int(os.getenv("OPENROUTER_MAX_TOKENS", "600"))

    # Optional but recommended by OpenRouter for their leaderboards/rankings
    OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "")
    OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "Job Application Agent")

    # --- SMTP (outgoing email) ---
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    @classmethod
    def validate(cls):
        """Raise a clear error early if required config is missing."""
        missing = []
        if not cls.OPENROUTER_API_KEY:
            missing.append("OPENROUTER_API_KEY")
        if not cls.SMTP_USERNAME:
            missing.append("SMTP_USERNAME")
        if not cls.SMTP_PASSWORD:
            missing.append("SMTP_PASSWORD")

        if missing:
            raise EnvironmentError(
                "Missing required environment variable(s): "
                f"{', '.join(missing)}. "
            )