from app.services.git_loader import GitSchemaLoader
from app.contracts.diff_engine import DiffEngine


class PRContractAnalyzer:
    """
    Orchestrates PR contract intelligence:
    Git → OpenAPI → Schema Extraction → Diff Engine
    """

    def __init__(self):
        self.loader = GitSchemaLoader()
        self.diff_engine = DiffEngine()

    # -----------------------------
    # Extract actual model schema
    # -----------------------------
    def extract_schema(self, openapi: dict):
        """
        Extract target model from OpenAPI spec
        (currently hardcoded to PickupCreate for v1)
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

        # 1. Load full OpenAPI from Git refs
        base_raw = self.loader.load_main()
        pr_raw = self.loader.load_pr()

        # 2. Extract ONLY model schema (CRITICAL FIX)
        base_schema = self.extract_schema(base_raw)
        pr_schema = self.extract_schema(pr_raw)

        # 3. Debug (safe to remove later)
        print("\n🧠 BASE SCHEMA KEYS:", base_schema.keys())
        print("🧠 PR SCHEMA KEYS:", pr_schema.keys())

        # 4. Run diff engine
        result = self.diff_engine.compare(base_schema, pr_schema)

        return result