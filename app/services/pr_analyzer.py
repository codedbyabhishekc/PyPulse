# app/services/pr_analyzer.py

from app.services.git_loader import GitSchemaLoader
from app.contracts.diff_engine import DiffEngine


class PRContractAnalyzer:
    """
    Orchestrates PR contract intelligence:
    Git → Schema → Diff → Risk (inside diff engine)
    """

    def __init__(self):
        self.loader = GitSchemaLoader()
        self.diff_engine = DiffEngine()

    def analyze(self, base_ref="origin/main", pr_ref="HEAD"):
        """
        Run full PR analysis
        """

        # 1. Load schemas
        base_schema = self.loader.load_base(base_ref)
        pr_schema = self.loader.load_pr(pr_ref)

        # 2. Run diff engine (returns full report incl risk)
        result = self.diff_engine.compare(base_schema, pr_schema)

        return {
            "base": base_ref,
            "head": pr_ref,
            "diff": result.get("changes", []),
            "risk": {
                "CRITICAL": [
                    c for c in result.get("changes", [])
                    if c["severity"] == "CRITICAL"
                ],
                "HIGH": [
                    c for c in result.get("changes", [])
                    if c["severity"] == "HIGH"
                ],
                "MEDIUM": [
                    c for c in result.get("changes", [])
                    if c["severity"] == "MEDIUM"
                ],
                "LOW": [
                    c for c in result.get("changes", [])
                    if c["severity"] == "LOW"
                ],
            },
            "raw": result
        }