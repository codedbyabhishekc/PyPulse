import subprocess
import json
import tempfile
import os


class GitSchemaLoader:

    def __init__(self):
        pass

    # =========================
    # GET FILE CONTENT FROM GIT
    # =========================
    def get_file(self, ref: str, path: str):

        cmd = ["git", "show", f"{ref}:{path}"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Failed to load {ref}:{path}")

        return result.stdout