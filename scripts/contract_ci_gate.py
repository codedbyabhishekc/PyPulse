from app.services.pr_analyzer import PRContractAnalyzer
from app.services.pr_report import PRReportBuilder
from app.services.github_pr_commenter import GitHubPRCommenter
from datetime import datetime
import os
import subprocess


def run():

    # =====================
    # CHECK FOR UNCOMMITTED CHANGES
    # =====================
    try:
        status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        if status:
            print("⚠️ ERROR: You have uncommitted changes!")
            print("\nModified files:")
            for line in status.split('\n'):
                print(f"  {line}")
            print("\nPlease commit or stash your changes before running this script:")
            print("  git add .")
            print("  git commit -m 'your message'")
            print("\nOr stash them:")
            print("  git stash")
            exit(1)
    except Exception as e:
        print(f"⚠️ Warning: Could not check git status: {e}\n")

    analyzer = PRContractAnalyzer()
    reporter = PRReportBuilder()

    # =====================
    # DETERMINE BASE AND PR REFS
    # =====================

    github_event_name = os.getenv("GITHUB_EVENT_NAME")
    github_base_ref = os.getenv("GITHUB_BASE_REF")

    print(f"🔍 GitHub Event: {github_event_name or 'Local Testing'}")

    if github_event_name == "pull_request" and github_base_ref:
        base_ref = f"origin/{github_base_ref}"
        pr_ref = "HEAD"
        print(f"🔍 PR Mode: Comparing {base_ref} → {pr_ref}\n")
    else:
        print("🔍 Local Mode")

        try:
            current_branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            head_sha = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            try:
                main_sha = subprocess.check_output(
                    ["git", "rev-parse", "origin/main"],
                    stderr=subprocess.DEVNULL
                ).decode().strip()
            except:
                main_sha = None

            print(f"🔍 Current branch: {current_branch}")
            print(f"🔍 Current commit: {head_sha[:8]}")

            if main_sha and head_sha == main_sha:
                # On main branch
                print(f"🔍 On main branch - comparing HEAD~1 → HEAD\n")
                base_ref = "HEAD~1"
                pr_ref = "HEAD"
            elif current_branch != "main" and current_branch != "HEAD":
                # On feature branch
                print(f"🔍 On feature branch - comparing origin/main → HEAD\n")
                base_ref = "origin/main"
                pr_ref = "HEAD"
            else:
                # Fallback
                print(f"🔍 Fallback - comparing HEAD~1 → HEAD\n")
                base_ref = "HEAD~1"
                pr_ref = "HEAD"

        except Exception as e:
            print(f"⚠️ Error: {e}")
            print(f"🔍 Using fallback: HEAD~1 → HEAD\n")
            base_ref = "HEAD~1"
            pr_ref = "HEAD"

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