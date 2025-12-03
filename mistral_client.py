import os
import requests
from dotenv import load_dotenv

class MistralClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.base_url = "https://api.mistral.ai/v1/chat/completions"
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment variables.")

    def send_message(self, messages, model="mistral-tiny"):  # model can be changed as needed
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": messages
        }
        response = requests.post(self.base_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
