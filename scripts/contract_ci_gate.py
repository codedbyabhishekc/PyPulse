# scripts/contract_ci_gate.py

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

    # In GitHub Actions, we get these environment variables
    github_event_name = os.getenv("GITHUB_EVENT_NAME")
    github_base_ref = os.getenv("GITHUB_BASE_REF")  # Target branch (e.g., "main")
    github_head_ref = os.getenv("GITHUB_HEAD_REF")  # PR branch name

    print(f"🔍 GitHub Event: {github_event_name}")
    print(f"🔍 Base Ref: {github_base_ref}")
    print(f"🔍 Head Ref: {github_head_ref}")

    if github_event_name == "pull_request" and github_base_ref:
        # We're in a PR context - compare PR branch against target branch
        base_ref = f"origin/{github_base_ref}"
        pr_ref = "HEAD"
        print(f"🔍 PR Mode: Comparing {base_ref} → {pr_ref}")
    else:
        # Local testing or push to main - compare HEAD against HEAD~1
        try:
            # Check if we're on a branch that has diverged from main
            current_branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"]
            ).decode().strip()

            print(f"🔍 Current branch: {current_branch}")

            if current_branch == "main" or current_branch == "HEAD":
                # On main branch - compare against previous commit
                base_ref = "HEAD~1"
                pr_ref = "HEAD"
                print(f"🔍 Main branch mode: Comparing HEAD~1 → HEAD")
            else:
                # On a feature branch - compare against main
                base_ref = "origin/main"
                pr_ref = "HEAD"
                print(f"🔍 Feature branch mode: Comparing origin/main → HEAD")

        except Exception as e:
            print(f"⚠️ Error detecting branch: {e}")
            base_ref = "HEAD~1"
            pr_ref = "HEAD"
            print(f"🔍 Fallback: Comparing HEAD~1 → HEAD")

    # Verify refs are different
    try:
        base_sha = subprocess.check_output(
            ["git", "rev-parse", base_ref]
        ).decode().strip()
        pr_sha = subprocess.check_output(
            ["git", "rev-parse", pr_ref]
        ).decode().strip()

        print(f"🔍 Base SHA: {base_sha[:8]}")
        print(f"🔍 PR SHA:   {pr_sha[:8]}")

        if base_sha == pr_sha:
            print("\n⚠️ ERROR: Base and PR are the same commit!")
            print("   Falling back to HEAD~1 comparison...")
            base_ref = "HEAD~1"

    except Exception as e:
        print(f"⚠️ Could not verify commits: {e}")

    print(f"\n🔍 Final comparison: {base_ref} → {pr_ref}\n")

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