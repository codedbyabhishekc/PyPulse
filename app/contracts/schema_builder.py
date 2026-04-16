import inspect
import importlib
from pydantic import BaseModel


class SchemaBuilder:

    def build(self, module_path="app.models"):

        module = importlib.import_module(module_path)

        schemas = {}

        for name in dir(module):
            obj = getattr(module, name)

            if inspect.isclass(obj) and issubclass(obj, BaseModel):
                if obj is not BaseModel:
                    schemas[name] = obj.model_json_schema()

        return {
            "components": {
                "schemas": schemas
            }
        }