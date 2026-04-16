import importlib
import pkgutil
import inspect
from pydantic import BaseModel
import app.models as models_pkg


class SchemaBuilder:

    def build(self, package=models_pkg):

        schemas = {}

        # 👇 iterate ALL files in app/models/
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):

            module = importlib.import_module(f"{package.__name__}.{module_name}")

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