# app/services/pr_report.py


class PRReportBuilder:
    """
    Builds human-readable PR contract intelligence report.
    """

    def build(self, result: dict) -> str:

        risk = result.get("risk", {})

        critical = risk.get("CRITICAL", [])
        high = risk.get("HIGH", [])
        medium = risk.get("MEDIUM", [])

        lines = []

        # Header
        lines.append("# 🧠 PyPulse Contract Intelligence Report\n")

        # Summary
        lines.append("## 📌 Summary")
        lines.append(f"- Base: `{result.get('base')}`")
        lines.append(f"- Head: `{result.get('head')}`")
        lines.append("")

        # 🔴 Critical
        lines.append("## 🔴 Breaking Changes")
        if critical:
            for item in critical:
                lines.append(f"- ❌ {item}")
        else:
            lines.append("- None")

        # 🟠 High
        lines.append("\n## 🟠 High Risk Changes")
        if high:
            for item in high:
                lines.append(f"- ⚠️ {item}")
        else:
            lines.append("- None")

        # 🟡 Medium
        lines.append("\n## 🟡 Medium Risk Changes")
        if medium:
            for item in medium:
                lines.append(f"- 🟡 {item}")
        else:
            lines.append("- None")

        # Summary counts
        lines.append("\n## 📊 Risk Summary")
        lines.append(f"- Critical: {len(critical)}")
        lines.append(f"- High: {len(high)}")
        lines.append(f"- Medium: {len(medium)}")

        # Decision
        decision = "FAIL ❌" if critical else "PASS ✅"
        lines.append(f"\n## 🚦 CI Decision: {decision}")

        return "\n".join(lines)