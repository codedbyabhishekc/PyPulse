import json
import inspect
import importlib
from pathlib import Path
from pydantic import BaseModel


class BaselineGenerator:
    """
    Generates contract baseline from Pydantic models in app/models
    """

    def __init__(self, models_module: str = "app.models"):
        self.models_module = models_module

    def load_models(self):
        module = importlib.import_module(self.models_module)

        models = {}

        for name in dir(module):
            obj = getattr(module, name)

            if inspect.isclass(obj) and issubclass(obj, BaseModel):
                if obj is not BaseModel:
                    models[name] = obj

        return models

    def model_to_schema(self, model):
        return model.model_json_schema()

    def generate(self):
        models = self.load_models()

        schemas = {}

        for name, model in models.items():
            schemas[name] = self.model_to_schema(model)

        return {
            "openapi": "3.0.0",
            "components": {
                "schemas": schemas
            }
        }

    def write(self, output_path="app/contracts/baseline_openapi.json"):
        data = self.generate()

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Baseline generated from app/models → {output_path}")