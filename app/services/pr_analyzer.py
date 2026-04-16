from app.contracts.schema_builder import SchemaBuilder
from app.contracts.diff_engine import DiffEngine
import subprocess


class PRContractAnalyzer:

    def __init__(self):
        self.builder = SchemaBuilder()
        self.diff_engine = DiffEngine()

    def checkout(self, ref):
        # safer checkout
        subprocess.run(["git", "checkout", ref], check=True)

    def analyze(self, base_ref="main", pr_ref="HEAD"):

        # =====================
        # BASE SNAPSHOT
        # =====================
        self.checkout(base_ref)
        base_schema = self.builder.build()

        # =====================
        # PR SNAPSHOT
        # =====================
        self.checkout(pr_ref)
        pr_schema = self.builder.build()

        base_models = base_schema["components"]["schemas"]
        pr_models = pr_schema["components"]["schemas"]

        print("\n🧠 BASE MODELS:", list(base_models.keys()))
        print("🧠 PR MODELS:", list(pr_models.keys()))

        changes = []

        # =====================
        # FULL MODEL DIFF
        # =====================
        for model_name in base_models.keys() | pr_models.keys():

            if model_name not in base_models:
                changes.append({
                    "type": "MODEL_ADDED",
                    "model": model_name,
                    "severity": "LOW"
                })
                continue

            if model_name not in pr_models:
                changes.append({
                    "type": "MODEL_REMOVED",
                    "model": model_name,
                    "severity": "CRITICAL"
                })
                continue

            changes += self.diff_engine.compare(
                base_models[model_name],
                pr_models[model_name],
                model_name=model_name
            )

        # =====================
        # CATEGORIZE BY RISK
        # =====================
        risk = {
            "CRITICAL": [],
            "HIGH": [],
            "MEDIUM": [],
            "LOW": []
        }

        for change in changes:
            severity = change.get("severity", "LOW")
            model = change.get("model", "Unknown")
            change_type = change.get("type", "Unknown")
            field = change.get("field", "")

            # Format the message
            if field:
                message = f"`{model}.{field}` - {change_type}"
            else:
                message = f"`{model}` - {change_type}"

            risk[severity].append(message)

        return {
            "base": base_ref,
            "head": pr_ref,
            "changes": changes,
            "risk": risk
        }