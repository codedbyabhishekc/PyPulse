from app.services.git_loader import GitSchemaLoader
from app.contracts.diff_engine import DiffEngine


class PRContractAnalyzer:
    """
    Contract intelligence pipeline:
    Models → Baseline → PR Schema → Diff
    """

    def __init__(self):
        self.loader = GitSchemaLoader()
        self.diff_engine = DiffEngine()

    def extract_schema(self, openapi: dict):
        """
        Extract first available Pydantic model schema
        """
        schemas = openapi.get("components", {}).get("schemas", {})

        if not schemas:
            return {}

        # deterministic pick (sorted for consistency)
        first_key = sorted(schemas.keys())[0]
        return schemas[first_key]

    def analyze(self):

        base_raw = self.loader.load_main()
        pr_raw = self.loader.load_pr()

        base_schema = self.extract_schema(base_raw)
        pr_schema = self.extract_schema(pr_raw)

        print("\n🧠 BASE SCHEMA:", base_schema.keys())
        print("🧠 PR SCHEMA:", pr_schema.keys())

        return self.diff_engine.compare(base_schema, pr_schema)