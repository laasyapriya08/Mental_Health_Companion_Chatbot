import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Application configuration
APP_NAME = "MindMate"
APP_TAGLINE = "Your Supportive Mental Wellness Companion"

# Gemini model
GEMINI_MODEL = "gemini-3.6-flash"


def validate_api_key():
    """Check whether the Gemini API key is available."""
    return bool(GOOGLE_API_KEY)