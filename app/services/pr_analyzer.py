from app.services.git_loader import GitSchemaLoader
from app.contracts.diff_engine import DiffEngine


class PRContractAnalyzer:
    """
    Orchestrates PR contract intelligence:
    Git → Schema → Diff → Risk
    """

    def __init__(self):
        self.loader = GitSchemaLoader()
        self.diff_engine = DiffEngine()

    def analyze(self, base_ref="origin/main", pr_ref="HEAD"):

        base_schema = self.loader.load_base(base_ref)
        pr_schema = self.loader.load_pr(pr_ref)

        result = self.diff_engine.compare(base_schema, pr_schema)

        return result