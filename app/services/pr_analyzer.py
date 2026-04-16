from app.services.git_loader import GitSchemaLoader
from app.contracts.diff_engine import DiffEngine


class PRContractAnalyzer:
    """
    Orchestrates PR contract intelligence:
    Git → OpenAPI → Schema Extract → Diff → Risk
    """

    def __init__(self):
        self.loader = GitSchemaLoader()
        self.diff_engine = DiffEngine()

    # -----------------------------
    # Extract correct model schema
    # -----------------------------
    def extract_schema(self, openapi: dict):
        """
        OpenAPI → actual model schema
        """
        return (
            openapi
            .get("components", {})
            .get("schemas", {})
            .get("PickupCreate", {})
        )

    # -----------------------------
    # Main pipeline
    # -----------------------------
    def analyze(self):

        # 1. Load full OpenAPI from git
        base_raw = self.loader.load_main()
        pr_raw = self.loader.load_pr()

        print("BASE TYPE:", type(base_raw))
        print("BASE KEYS:", base_raw.keys())
        print("CURR TYPE:", type(pr_raw))
        print("CURR KEYS:", pr_raw.keys())

        # 2. Extract actual schema (IMPORTANT FIX)
        base_schema = self.extract_schema(base_raw)
        pr_schema = self.extract_schema(pr_raw)

        # 3. Run diff engine
        result = self.diff_engine.compare(base_schema, pr_schema)

        return result