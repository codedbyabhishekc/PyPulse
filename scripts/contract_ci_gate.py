from app.services.pr_analyzer import PRContractAnalyzer
from app.services.pr_report import PRReportBuilder
from app.services.github_pr_commenter import GitHubPRCommenter
from datetime import datetime
import os
import subprocess


def run():

    analyzer = PRContractAnalyzer()
    reporter = PRReportBuilder()

    # =====================
    # DETERMINE BASE AND PR REFS
    # =====================
    try:
        # Find the merge base (where the PR branched from main)
        merge_base = subprocess.check_output(
            ["git", "merge-base", "origin/main", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        base_ref = merge_base
        print(f"🔍 Using merge base: {merge_base}")
    except:
        # Fallback to origin/main
        base_ref = "origin/main"
        print(f"🔍 Using origin/main as base")

    pr_ref = "HEAD"

    print(f"🔍 Comparing: {base_ref} → {pr_ref}\n")

    # 🔥 FULL COMPILATION-BASED DIFF
    result = analyzer.analyze(
        base_ref=base_ref,
        pr_ref=pr_ref
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

    # 🔥 POST TO GITHUB PR
    try:
        commenter = GitHubPRCommenter()
        commenter.publish(report)
        print("✅ Comment posted to GitHub PR")
    except Exception as e:
        print(f"⚠️ Could not post to PR (running locally?): {e}")

    # Check for critical issues using the correct field
    critical_count = len(result.get("risk", {}).get("CRITICAL", []))

    if critical_count > 0:
        print("\n❌ CI FAILED")
        exit(1)

    print("\n✅ CI PASSED")
    exit(0)


if __name__ == "__main__":
    run()