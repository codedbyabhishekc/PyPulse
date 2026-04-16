def run_diff(baseline: dict, current: dict):
    changes = diff_schema(baseline, current)
    return build_report(changes)


def diff_schema(base, curr):

    base = base or {}
    curr = curr or {}

    base_props = base.get("properties", {})
    curr_props = curr.get("properties", {})

    base_keys = set(base_props.keys())
    curr_keys = set(curr_props.keys())

    removed = base_keys - curr_keys
    added = curr_keys - base_keys

    changes = []

    for k in base_keys & curr_keys:
        b = base_props[k]
        c = curr_props[k]

        if b.get("type") != c.get("type"):
            changes.append({
                "type": "TYPE_CHANGED",
                "field": k,
                "from": b.get("type"),
                "to": c.get("type"),
                "severity": "HIGH"
            })

        b_req = k in base.get("required", [])
        c_req = k in curr.get("required", [])

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

    for k in removed:
        changes.append({
            "type": "FIELD_REMOVED",
            "field": k,
            "severity": "CRITICAL"
        })

    for k in added:
        changes.append({
            "type": "FIELD_ADDED",
            "field": k,
            "severity": "LOW"
        })

    return changes


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
    def compare(self, baseline: dict, current: dict, model_name: str = None):
        """
        Compare two schemas and return a list of changes.

        Args:
            baseline: Base schema dict
            current: Current schema dict
            model_name: Optional model name to include in change dicts

        Returns:
            List of change dicts
        """
        changes = diff_schema(baseline, current)

        # Add model_name to each change if provided
        if model_name:
            for change in changes:
                change["model"] = model_name

        return changes