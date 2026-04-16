from app.contracts.schema_builder import SchemaBuilder
from app.contracts.diff_engine import DiffEngine
import subprocess
import json


class PRContractAnalyzer:

    def __init__(self):
        self.builder = SchemaBuilder()
        self.diff_engine = DiffEngine()

    def checkout(self, ref):
        # safer checkout
        result = subprocess.run(
            ["git", "checkout", ref],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"⚠️ Git checkout failed: {result.stderr}")
            raise Exception(f"Failed to checkout {ref}")

    def analyze(self, base_ref="main", pr_ref="HEAD"):

        # =====================
        # BASE SNAPSHOT
        # =====================
        print(f"\n🔍 Checking out BASE: {base_ref}")
        self.checkout(base_ref)
        base_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        print(f"   Commit: {base_commit[:8]}")

        base_schema = self.builder.build()

        # =====================
        # PR SNAPSHOT
        # =====================
        print(f"\n🔍 Checking out PR: {pr_ref}")
        self.checkout(pr_ref)
        pr_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        print(f"   Commit: {pr_commit[:8]}")

        pr_schema = self.builder.build()

        # Check if commits are the same
        if base_commit == pr_commit:
            print("\n⚠️ WARNING: Base and PR commits are identical!")
            print("   This means there are no changes between the branches.")

        base_models = base_schema["components"]["schemas"]
        pr_models = pr_schema["components"]["schemas"]

        print("\n🧠 BASE MODELS:", list(base_models.keys()))
        print("🧠 PR MODELS:", list(pr_models.keys()))

        # DEBUG: Print detailed schema for comparison
        for model_name in base_models.keys() | pr_models.keys():
            if model_name in base_models and model_name in pr_models:
                base_json = json.dumps(base_models[model_name], sort_keys=True)
                pr_json = json.dumps(pr_models[model_name], sort_keys=True)

                if base_json != pr_json:
                    print(f"\n🔍 SCHEMA DIFF for {model_name}:")
                    print(f"   BASE properties: {list(base_models[model_name].get('properties', {}).keys())}")
                    print(f"   PR properties:   {list(pr_models[model_name].get('properties', {}).keys())}")
                    print(f"   BASE required: {base_models[model_name].get('required', [])}")
                    print(f"   PR required:   {pr_models[model_name].get('required', [])}")

        changes = []

        # =====================
        # FULL MODEL DIFF
        # =====================
        for model_name in base_models.keys() | pr_models.keys():

            if model_name not in base_models:
                print(f"\n✅ MODEL ADDED: {model_name}")
                changes.append({
                    "type": "MODEL_ADDED",
                    "model": model_name,
                    "severity": "LOW"
                })
                continue

            if model_name not in pr_models:
                print(f"\n❌ MODEL REMOVED: {model_name}")
                changes.append({
                    "type": "MODEL_REMOVED",
                    "model": model_name,
                    "severity": "CRITICAL"
                })
                continue

            print(f"\n🔍 Analyzing {model_name}...")
            model_changes = self.diff_engine.compare(
                base_models[model_name],
                pr_models[model_name],
                model_name=model_name
            )

            if model_changes:
                print(f"   Found {len(model_changes)} change(s):")
                for change in model_changes:
                    print(f"     • {change.get('type')} - {change.get('field', 'N/A')} [{change.get('severity')}]")
            else:
                print(f"   No changes detected")

            changes += model_changes

        print(f"\n📊 TOTAL CHANGES DETECTED: {len(changes)}")

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