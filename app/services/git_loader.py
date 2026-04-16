# app/services/git_loader.py

import subprocess
import json

# ---- safe optional dependency ----
try:
    import yaml
except ImportError:
    yaml = None


class GitSchemaLoader:
    """
    Loads OpenAPI schema directly from Git refs.
    Supports JSON and YAML schemas.
    """

    def __init__(self, schema_path="app/contracts/baseline_openapi.json"):
        self.schema_path = schema_path

    def _read(self, ref: str):
        """
        Read file from git history:
        git show <ref>:<file>
        """

        cmd = ["git", "show", f"{ref}:{self.schema_path}"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(
                f"❌ Failed to load schema from git ref: {ref}\n"
                f"Path: {self.schema_path}\n"
                f"stderr: {result.stderr}"
            )

        content = result.stdout.strip()

        # ---- JSON ----
        if self.schema_path.endswith(".json"):
            return json.loads(content)

        # ---- YAML ----
        if self.schema_path.endswith((".yaml", ".yml")):
            if yaml is None:
                raise ImportError(
                    "PyYAML is required for YAML schemas. Install with: pip install pyyaml"
                )
            return yaml.safe_load(content)

        # fallback
        return content

    def load_base(self, base_ref="origin/main"):
        return self._read(base_ref)

    def load_pr(self, pr_ref="HEAD"):
        return self._read(pr_ref)