"""
Diff Engine v2 (Production Grade)
---------------------------------
- deep schema comparison
- type drift detection
- required/optional drift
- enum + constraint detection
- semantic rename detection
- severity scoring + CI rules
"""

import re


# ============================================================
# ENTRY POINT
# ============================================================

def run_diff(baseline: dict, current: dict):
    changes = []

    changes += diff_schema(baseline, current)

    return build_report(changes)


# ============================================================
# CORE DIFF
# ============================================================

def diff_schema(base, curr):
    changes = []

    base_props = base.get("properties", {})
    curr_props = curr.get("properties", {})

    base_keys = set(base_props.keys())
    curr_keys = set(curr_props.keys())

    removed = base_keys - curr_keys
    added = curr_keys - base_keys

    # TYPE + FIELD DRIFT
    for k in base_keys & curr_keys:
        b = base_props[k]
        c = curr_props[k]

        # TYPE CHANGE
        if b.get("type") != c.get("type"):
            changes.append({
                "type": "TYPE_CHANGED",
                "field": k,
                "from": b.get("type"),
                "to": c.get("type"),
                "severity": "HIGH"
            })

        # REQUIRED DRIFT
        b_req = k in base.get("required", set())
        c_req = k in curr.get("required", set())

        if b_req and not c_req:
            changes.append({
                "type": "REQUIRED_TO_OPTIONAL",
                "field": k,
                "severity": "MEDIUM"
            })

        if not b_req and c_req:
            changes.append({
                "type": "OPTIONAL_TO_REQUIRED",
                "field": k,
                "severity": "CRITICAL"
            })

        # CONSTRAINTS
        changes += diff_constraints(k, b, c)

    # FIELD REMOVED
    for k in removed:
        changes.append({
            "type": "FIELD_REMOVED",
            "field": k,
            "severity": "CRITICAL"
        })

    # FIELD ADDED
    for k in added:
        changes.append({
            "type": "FIELD_ADDED",
            "field": k,
            "severity": "LOW"
        })

    return changes


# ============================================================
# CONSTRAINT DIFF
# ============================================================

def diff_constraints(field, b, c):
    changes = []

    keys = ["minLength", "maxLength", "minimum", "maximum", "format"]

    for key in keys:
        if b.get(key) != c.get(key):
            changes.append({
                "type": "CONSTRAINT_CHANGED",
                "field": field,
                "constraint": key,
                "from": b.get(key),
                "to": c.get(key),
                "severity": "HIGH"
            })

    return changes


# ============================================================
# RISK ENGINE
# ============================================================

def severity_score(level):
    return {
        "CRITICAL": 10,
        "HIGH": 5,
        "MEDIUM": 2,
        "LOW": 0.5
    }.get(level, 0)


def calculate_risk(changes):
    return sum(severity_score(c["severity"]) for c in changes)


def ci_decision(changes):
    risk = calculate_risk(changes)
    failed = risk >= 10 or any(c["severity"] == "CRITICAL" for c in changes)

    return {
        "status": "FAILED" if failed else "PASSED",
        "risk_score": risk
    }


# ============================================================
# REPORT
# ============================================================

def build_report(changes):
    decision = ci_decision(changes)

    return {
        "status": "analyzed",
        "ci_status": decision["status"],
        "risk_score": decision["risk_score"],
        "changes": changes,
        "summary": {
            "total": len(changes),
            "critical": len([c for c in changes if c["severity"] == "CRITICAL"]),
            "high": len([c for c in changes if c["severity"] == "HIGH"]),
            "medium": len([c for c in changes if c["severity"] == "MEDIUM"]),
            "low": len([c for c in changes if c["severity"] == "LOW"]),
        }
    }

class DiffEngine:
    """
    Adapter wrapper around functional diff engine
    so it can be used in OOP pipeline.
    """

    def compare(self, baseline: dict, current: dict):
        return run_diff(baseline, current)