from app.services.pr_analyzer import PRContractAnalyzer
from app.services.pr_report import PRReportBuilder
from app.services.github_pr_commenter import GitHubPRCommenter

import os


def run():

    analyzer = PRContractAnalyzer()
    reporter = PRReportBuilder()

    # 1. Analyze PR vs main
    result = analyzer.analyze()

    # 2. Build report
    report = reporter.build(result)

    # 3. Print
    print(report)

    # 4. Post to GitHub PR
    try:
        commenter = GitHubPRCommenter()
        commenter.publish(report)
    except Exception as e:
        print(f"GitHub comment failed: {e}")

    # 5. CI decision
    if result.get("ci_status") == "FAILED":
        exit(1)

    exit(0)


if __name__ == "__main__":
    run()