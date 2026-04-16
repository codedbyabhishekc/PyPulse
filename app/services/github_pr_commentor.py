import os
import requests


class GitHubPRCommenter:
    """
    Posts or updates PyPulse contract intelligence report
    directly into GitHub PR as an idempotent comment.
    """

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise Exception("❌ GITHUB_TOKEN not found")

        self.repo = os.getenv("GITHUB_REPOSITORY")  # owner/repo
        self.pr_number = os.getenv("PR_NUMBER") or os.getenv("GITHUB_PR_NUMBER")

        if not self.repo:
            raise Exception("❌ GITHUB_REPOSITORY not set")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def publish(self, report: str):
        """
        Create or update PR comment.
        """

        if not self.pr_number:
            print("⚠️ No PR context detected. Skipping GitHub comment.")
            return

        existing_id = self._find_existing_comment()

        if existing_id:
            self._update_comment(existing_id, report)
        else:
            self._create_comment(report)

    # ----------------------------
    # Find existing PyPulse comment
    # ----------------------------
    def _find_existing_comment(self):
        url = f"https://api.github.com/repos/{self.repo}/issues/{self.pr_number}/comments"

        res = requests.get(url, headers=self.headers)
        res.raise_for_status()

        comments = res.json()

        for c in comments:
            if "🧠 PyPulse Contract Intelligence Report" in c.get("body", ""):
                return c["id"]

        return None

    # ----------------------------
    # Create comment
    # ----------------------------
    def _create_comment(self, body: str):
        url = f"https://api.github.com/repos/{self.repo}/issues/{self.pr_number}/comments"

        res = requests.post(url, json={"body": body}, headers=self.headers)
        res.raise_for_status()

        print("✅ PR comment created")

    # ----------------------------
    # Update comment
    # ----------------------------
    def _update_comment(self, comment_id: int, body: str):
        url = f"https://api.github.com/repos/{self.repo}/issues/comments/{comment_id}"

        res = requests.patch(url, json={"body": body}, headers=self.headers)
        res.raise_for_status()

        print("♻️ PR comment updated")