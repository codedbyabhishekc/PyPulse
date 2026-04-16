from app.contracts.diff_engine import DiffEngine
from app.contracts.schema_builder import SchemaBuilder


class PRContractAnalyzer:

    def __init__(self):
        self.builder = SchemaBuilder()
        self.diff_engine = DiffEngine()

    def extract_first(self, openapi):

        schemas = openapi.get("components", {}).get("schemas", {})
        if not schemas:
            return {}

        return schemas[list(schemas.keys())[0]]

    def analyze(self, base_ref="origin/main", pr_ref="HEAD"):

        # =========================
        # BUILD BASE
        # =========================
        base_raw = self.builder.build_from_ref(base_ref)

        # =========================
        # BUILD PR
        # =========================
        pr_raw = self.builder.build_from_ref(pr_ref)

        base_schema = self.extract_first(base_raw)
        pr_schema = self.extract_first(pr_raw)

        print("\n🧠 BASE:", base_schema.keys())
        print("🧠 PR:", pr_schema.keys())

        return self.diff_engine.compare(base_schema, pr_schema)