import subprocess
import json


class GitSchemaLoader:

    def __init__(self, schema_path="app/contracts/baseline_openapi.json"):
        self.schema_path = schema_path

    def load_from_ref(self, ref: str):
        cmd = ["git", "show", f"{ref}:{self.schema_path}"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Failed to load schema from {ref}")

        return json.loads(result.stdout)

    def load_main(self):
        return self.load_from_ref("origin/main")

    def load_pr(self):
        return self.load_from_ref("HEAD")