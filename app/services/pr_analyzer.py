from app.services.git_loader import GitSchemaLoader
from app.contracts.diff_engine import DiffEngine

class PRContractAnalyzer:

    def __init__(self):
        self.loader = GitSchemaLoader()
        self.diff_engine = DiffEngine()

    def analyze(self):

        # FIX: use correct loader methods
        base_schema = self.loader.load_main()
        pr_schema = self.loader.load_pr()

        result = self.diff_engine.compare(base_schema, pr_schema)

        return result