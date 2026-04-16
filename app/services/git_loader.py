import subprocess
import json
import tempfile
import shutil
import os


class GitSchemaLoader:

    def __init__(self, schema_path="app"):
        self.schema_path = schema_path

    # =========================
    # READ FILE FROM GIT SNAPSHOT
    # =========================
    def load_from_git(self, ref: str):

        cmd = ["git", "show", f"{ref}:app"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Failed to read git ref: {ref}")

        return result.stdout

    # (we no longer use checkout at all)