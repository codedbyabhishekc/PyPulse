# scripts/contract_ci_gate.py

from app.services.pr_analyzer import PRContractAnalyzer
from app.services.pr_report import PRReportBuilder
from datetime import datetime
import os


def run():

    analyzer = PRContractAnalyzer()
    reporter = PRReportBuilder()

    # 1. Run analysis
    result = analyzer.analyze(
        base_ref="origin/main",
        pr_ref="HEAD"
    )

    # 2. Build report
    report = reporter.build(result)

    # 3. Console output
    print("\n" + "=" * 80)
    print("🧠 PYPULSE CONTRACT INTELLIGENCE REPORT")
    print("=" * 80)
    print(report)
    print("=" * 80)

    # 4. Save report locally
    os.makedirs("reports", exist_ok=True)

    filename = f"reports/pypulse_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n📄 Report saved: {filename}")

    # 5. CI decision
    if result.get("risk", {}).get("CRITICAL"):
        print("\n❌ CI FAILED: Breaking changes detected")
        exit(1)

    print("\n✅ CI PASSED: No breaking changes")
    exit(0)


if __name__ == "__main__":
    run()