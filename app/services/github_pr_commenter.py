import os
import requests


class GitHubPRCommenter:

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo = os.getenv("GITHUB_REPOSITORY")
        self.pr_number = os.getenv("PR_NUMBER")

        if not all([self.token, self.repo, self.pr_number]):
            raise Exception("Missing GitHub environment variables")

    def publish(self, message: str):

        url = f"https://api.github.com/repos/{self.repo}/issues/{self.pr_number}/comments"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

        payload = {
            "body": message
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to post PR comment: {response.text}")

        print("✅ PR comment posted successfully")