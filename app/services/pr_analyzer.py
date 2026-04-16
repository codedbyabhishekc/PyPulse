from app.services.git_loader import GitSchemaLoader
from app.contracts.diff_engine import DiffEngine


class PRContractAnalyzer:

    def __init__(self):
        self.loader = GitSchemaLoader()
        self.diff_engine = DiffEngine()

    def extract_first_schema(self, openapi: dict):

        schemas = openapi.get("components", {}).get("schemas", {})

        if not schemas:
            return {}

        return schemas[list(schemas.keys())[0]]

    # ✅ FIXED SIGNATURE
    def analyze(self, base_ref="origin/main", pr_ref="HEAD"):

        # =========================
        # BASE SNAPSHOT
        # =========================
        self.loader.checkout(base_ref)
        base_raw = self.loader.load_schema()

        # =========================
        # PR SNAPSHOT
        # =========================
        self.loader.checkout(pr_ref)
        pr_raw = self.loader.load_schema()

        base_schema = self.extract_first_schema(base_raw)
        pr_schema = self.extract_first_schema(pr_raw)

        print("\n🧠 BASE SCHEMA KEYS:", base_schema.keys())
        print("🧠 PR SCHEMA KEYS:", pr_schema.keys())

        return self.diff_engine.compare(base_schema, pr_schema)