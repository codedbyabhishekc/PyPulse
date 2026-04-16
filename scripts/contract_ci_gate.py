from app.services.pr_analyzer import PRContractAnalyzer
from app.services.pr_report import PRReportBuilder
from datetime import datetime
import os


def run():

    analyzer = PRContractAnalyzer()
    reporter = PRReportBuilder()

    # 🔥 FULL COMPILATION-BASED DIFF
    result = analyzer.analyze(
        base_ref="origin/main",
        pr_ref="HEAD"
    )

    report = reporter.build(result)

    print("\n" + "=" * 80)
    print("🧠 PYPULSE CONTRACT INTELLIGENCE REPORT")
    print("=" * 80)
    print(report)
    print("=" * 80)

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/pypulse_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n📄 Report saved: {filename}")

    if result.get("summary", {}).get("critical", 0) > 0:
        print("\n❌ CI FAILED")
        exit(1)

    print("\n✅ CI PASSED")
    exit(0)


if __name__ == "__main__":
    run()