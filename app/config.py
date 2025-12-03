import os
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-medium")  # adjust if needed
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL", "https://api.mistral.ai/v1/chat/completions")