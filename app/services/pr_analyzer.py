from app.services.git_loader import GitSchemaLoader
from app.contracts.diff_engine import DiffEngine
import json


class PRContractAnalyzer:

    def __init__(self):
        self.loader = GitSchemaLoader()
        self.diff_engine = DiffEngine()

    def extract_first(self, openapi):

        schemas = openapi.get("components", {}).get("schemas", {})
        if not schemas:
            return {}

        return schemas[list(schemas.keys())[0]]

    def analyze(self, base_ref="origin/main", pr_ref="HEAD"):

        # =========================
        # BASE
        # =========================
        base_raw = self.loader.get_file(
            base_ref,
            "app/contracts/baseline_openapi.json"
        )

        # =========================
        # PR
        # =========================
        pr_raw = self.loader.get_file(
            pr_ref,
            "app/contracts/baseline_openapi.json"
        )

        base_schema = json.loads(base_raw)
        pr_schema = json.loads(pr_raw)

        base_final = self.extract_first(base_schema)
        pr_final = self.extract_first(pr_schema)

        print("\n🧠 BASE KEYS:", base_final.keys())
        print("🧠 PR KEYS:", pr_final.keys())

        return self.diff_engine.compare(base_final, pr_final)