"""
Deterministic Schema Extractor
------------------------------
NO FastAPI. NO OpenAPI. PURE Pydantic source of truth.
"""

from pydantic import BaseModel


def extract_pydantic_schema(model: type[BaseModel]) -> dict:
    """
    Convert Pydantic model → normalized schema.
    """

    raw = model.model_json_schema()

    return normalize_schema(raw)


def normalize_schema(schema: dict) -> dict:
    """
    Reduce noise + keep only diff-relevant structure.
    """

    return {
        "title": schema.get("title"),
        "type": schema.get("type"),
        "properties": schema.get("properties", {}),
        "required": set(schema.get("required", [])),
    }