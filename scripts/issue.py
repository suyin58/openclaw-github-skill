#!/usr/bin/env python3
"""
GitHub Issue操作脚本
"""

import subprocess
import json
import argparse
import sys
import shutil


def check_dependencies():
    """检查必要的依赖是否已安装"""
    # 检查 git
    if not shutil.which("git"):
        print("❌ Error: Git is not installed.", file=sys.stderr)
        print("   Please install Git first:", file=sys.stderr)
        print("   Windows: https://git-scm.com/download/win", file=sys.stderr)
        print("   Or use: winget install --id Git.Git", file=sys.stderr)
        sys.exit(1)
    print("✓ Git is installed")

    # 检查 gh CLI
    if not shutil.which("gh"):
        print("❌ Error: GitHub CLI (gh) is not installed.", file=sys.stderr)
        print("   Please install GitHub CLI first:", file=sys.stderr)
        print("   Windows: winget install --id GitHub.cli", file=sys.stderr)
        print("   Or visit: https://cli.github.com/", file=sys.stderr)
        sys.exit(1)
    print("✓ GitHub CLI is installed")

    # 检查是否已登录 GitHub
    result = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("❌ Error: Not logged in to GitHub.", file=sys.stderr)
        print("   Please run: gh auth login", file=sys.stderr)
        sys.exit(1)
    print("✓ Logged in to GitHub")


def run_gh_command(args):
    """执行gh命令并返回结果"""
    cmd = ["gh"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    return result.stdout


def create_issue(repo, title, body=None, labels=None):
    """创建GitHub Issue"""
    args = ["issue", "create", "--repo", repo, "--title", title]

    if body:
        args.extend(["--body", body])

    if labels:
        args.extend(["--label", labels])

    result = run_gh_command(args)
    print(f"Issue created successfully!")
    print(result)


def list_issues(repo, state="open"):
    """列出GitHub Issues"""
    args = ["issue", "list", "--repo", repo, f"--state", state,
            "--json", "number,title,author,state,labels,url,createdAt,closedAt",
            "--limit", "50"]

    result = run_gh_command(args)
    issues = json.loads(result)

    if not issues:
        print(f"No {state} issues found in {repo}")
        return

    print(f"\n{'#' * 60}")
    print(f"Issues in {repo} (state: {state})")
    print(f"{'#' * 60}\n")

    for issue in issues:
        labels = ", ".join([label["name"] for label in issue.get("labels", [])])
        print(f"#{issue['number']}: {issue['title']}")
        print(f"  Author: {issue['author']['login']}")
        print(f"  State: {issue['state']}")
        if labels:
            print(f"  Labels: {labels}")
        print(f"  URL: {issue['url']}")
        print(f"  Created: {issue['createdAt']}")
        print()


def get_issue(repo, number):
    """获取特定Issue详情"""
    args = ["issue", "view", f"{repo}:{number}",
            "--json", "number,title,body,author,state,labels,comments,url,createdAt,closedAt"]

    result = run_gh_command(args)
    issue = json.loads(result)

    print(f"\n{'#' * 60}")
    print(f"Issue #{issue['number']}: {issue['title']}")
    print(f"{'#' * 60}\n")
    print(f"Author: {issue['author']['login']}")
    print(f"State: {issue['state']}")
    print(f"Created: {issue['createdAt']}")
    print(f"URL: {issue['url']}")
    print(f"\nBody:\n{issue['body']}")
    print()


def main():
    # 检查依赖
    check_dependencies()

    parser = argparse.ArgumentParser(description="GitHub Issue操作")
    parser.add_argument("--create", action="store_true", help="创建Issue")
    parser.add_argument("--list", action="store_true", help="列出Issues")
    parser.add_argument("--get", action="store_true", help="获取Issue详情")
    parser.add_argument("--repo", help="仓库标识 (owner/repo)")
    parser.add_argument("--number", type=int, help="Issue编号")
    parser.add_argument("--title", help="Issue标题")
    parser.add_argument("--body", help="Issue内容")
    parser.add_argument("--labels", help="Issue标签 (逗号分隔)")
    parser.add_argument("--state", default="open", help="筛选状态 (open/closed/all)")

    args = parser.parse_args()

    if args.create:
        if not args.repo or not args.title:
            print("Error: --repo and --title are required for creating an issue", file=sys.stderr)
            sys.exit(1)
        create_issue(args.repo, args.title, args.body, args.labels)

    elif args.list:
        if not args.repo:
            print("Error: --repo is required for listing issues", file=sys.stderr)
            sys.exit(1)
        list_issues(args.repo, args.state)

    elif args.get:
        if not args.repo or not args.number:
            print("Error: --repo and --number are required for getting an issue", file=sys.stderr)
            sys.exit(1)
        get_issue(args.repo, args.number)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
