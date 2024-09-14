import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_github_token():
    """Load GitHub API token from environment variables."""
    return os.getenv("GITHUB_API_TOKEN")

class GitHubScraper:
    def __init__(self, github_token=None):
        """Initialize with the provided GitHub API token."""
        if github_token is None:
            self.api_token = load_github_token()
        else:
            self.api_token = github_token

    def get_repo_details(self, repo_url):
        repo_api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/")
        headers = {"Authorization": f"token {self.api_token}"}
        response = requests.get(repo_api_url, headers=headers)
    
        # Debugging step to print the API response and status code
        print(f"API Response: {response.json()}")
        print(f"Status Code: {response.status_code}")
    
        if response.status_code == 200:
            return response.json()
        else:
            return None

