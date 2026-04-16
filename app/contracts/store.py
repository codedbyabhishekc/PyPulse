"""
Contract Snapshot Store
-----------------------
Stores baseline schema snapshots.
"""

import json
from pathlib import Path

BASELINE_PATH = Path("app/contracts/baseline.json")


def save_baseline(schema: dict):
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(BASELINE_PATH, "w", encoding="utf-8") as f:
        json.dump(_serialize(schema), f, indent=2)


def load_baseline() -> dict | None:
    if not BASELINE_PATH.exists():
        return None

    with open(BASELINE_PATH, "r", encoding="utf-8") as f:
        return _deserialize(json.load(f))


# -------------------------
# JSON SAFE CONVERSION
# -------------------------

def _serialize(schema: dict):
    return {
        **schema,
        "required": list(schema.get("required", []))
    }


def _deserialize(schema: dict):
    return {
        **schema,
        "required": set(schema.get("required", []))
    }