import subprocess
import json
import os


class GitSchemaLoader:

    def __init__(self):
        self.original_ref = None

    # =========================
    # CHECKOUT GIT STATE
    # =========================
    def checkout(self, ref: str):
        """
        Switch git working directory to ref
        """
        subprocess.run(["git", "checkout", ref], check=True)

    # =========================
    # LOAD SCHEMA FROM CURRENT STATE
    # =========================
    def load_schema(self):
        """
        Build schema from current checked-out code
        """
        from app.contracts.schema_builder import SchemaBuilder

        builder = SchemaBuilder("app.models")
        return builder.build()