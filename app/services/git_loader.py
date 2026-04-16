import subprocess


class GitSchemaLoader:

    def get_file(self, ref: str, path: str):

        cmd = ["git", "show", f"{ref}:{path}"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Failed to load {ref}:{path}")

        return result.stdout