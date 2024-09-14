import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_api_key():
    """Load Google Gemini API key from environment variables."""
    return os.getenv("GOOGLE_GEMINI_API_KEY")

class GeminiAPIHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        # Hardcode the API URL here
        self.api_url = "https://api.google.com/gemini/endpoint"  # Replace with the actual API URL

    def generate_text(self, prompt):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"prompt": prompt, "max_tokens": 100}

        # Make the POST request to the Gemini API
        response = requests.post(self.api_url, headers=headers, json=data)

        # Debugging step to print the response
        print(f"Raw Gemini API Response: {response.text}")

        if response.status_code == 200:
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                return "Error: Invalid response format"
        else:
            return f"Error: Received status code {response.status_code}"
