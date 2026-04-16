import importlib.util
import sys
import tempfile
import os
from pathlib import Path
from app.models import *


class SchemaBuilder:

    def build_from_ref(self, ref: str):

        # create temp dir
        tmp_dir = tempfile.mkdtemp()

        # extract code snapshot
        import subprocess
        subprocess.run(
            ["git", "checkout", ref],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # import models safely AFTER checkout

        # build schema
        schemas = {}

        for name in dir():
            obj = globals().get(name)
            try:
                from pydantic import BaseModel
                if isinstance(obj, type) and issubclass(obj, BaseModel):
                    schemas[name] = obj.model_json_schema()
            except:
                continue

        return {
            "components": {
                "schemas": schemas
            }
        }