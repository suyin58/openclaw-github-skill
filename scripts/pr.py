#!/usr/bin/env python3
"""
GitHub Pull Request操作脚本
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


def create_pr(repo, title, body=None, source=None, target=None, draft=False):
    """创建GitHub Pull Request"""
    args = ["pr", "create", "--repo", repo, "--title", title]

    if body:
        args.extend(["--body", body])

    if source:
        args.extend(["--head", source])

    if target:
        args.extend(["--base", target])

    if draft:
        args.append("--draft")

    result = run_gh_command(args)
    print(f"Pull Request created successfully!")
    print(result)


def list_prs(repo, state="open"):
    """列出GitHub Pull Requests"""
    args = ["pr", "list", "--repo", repo, f"--state", state,
            "--json", "number,title,author,state,headRefName,baseRefName,url,createdAt,mergedAt",
            "--limit", "50"]

    result = run_gh_command(args)
    prs = json.loads(result)

    if not prs:
        print(f"No {state} pull requests found in {repo}")
        return

    print(f"\n{'#' * 60}")
    print(f"Pull Requests in {repo} (state: {state})")
    print(f"{'#' * 60}\n")

    for pr in prs:
        print(f"#{pr['number']}: {pr['title']}")
        print(f"  Author: {pr['author']['login']}")
        print(f"  State: {pr['state']}")
        print(f"  Branch: {pr['headRefName']} -> {pr['baseRefName']}")
        print(f"  URL: {pr['url']}")
        print(f"  Created: {pr['createdAt']}")
        print()


def get_pr(repo, number):
    """获取特定PR详情"""
    args = ["pr", "view", f"{repo}:{number}",
            "--json", "number,title,body,author,state,headRefName,baseRefName,comments,reviewDecision,url,createdAt,mergedAt"]

    result = run_gh_command(args)
    pr = json.loads(result)

    print(f"\n{'#' * 60}")
    print(f"Pull Request #{pr['number']}: {pr['title']}")
    print(f"{'#' * 60}\n")
    print(f"Author: {pr['author']['login']}")
    print(f"State: {pr['state']}")
    print(f"Branch: {pr['headRefName']} -> {pr['baseRefName']}")
    print(f"Review Decision: {pr.get('reviewDecision', 'N/A')}")
    print(f"Created: {pr['createdAt']}")
    print(f"URL: {pr['url']}")
    print(f"\nBody:\n{pr['body']}")
    print()


def merge_pr(repo, number, merge_method="merge"):
    """合并Pull Request"""
    args = ["pr", "merge", f"{repo}:{number}", f"--{merge_method}"]
    result = run_gh_command(args)
    print(f"Pull Request #{number} merged successfully!")
    print(result)


def main():
    # 检查依赖
    check_dependencies()

    parser = argparse.ArgumentParser(description="GitHub Pull Request操作")
    parser.add_argument("--create", action="store_true", help="创建PR")
    parser.add_argument("--list", action="store_true", help="列出PRs")
    parser.add_argument("--get", action="store_true", help="获取PR详情")
    parser.add_argument("--merge", action="store_true", help="合并PR")
    parser.add_argument("--repo", help="仓库标识 (owner/repo)")
    parser.add_argument("--number", type=int, help="PR编号")
    parser.add_argument("--title", help="PR标题")
    parser.add_argument("--body", help="PR描述")
    parser.add_argument("--source", help="源分支")
    parser.add_argument("--target", help="目标分支")
    parser.add_argument("--draft", action="store_true", help="创建草稿PR")
    parser.add_argument("--state", default="open", help="筛选状态 (open/closed/merged/all)")
    parser.add_argument("--merge-method", default="merge", choices=["merge", "squash", "rebase"], help="合并方式")

    args = parser.parse_args()

    if args.create:
        if not args.repo or not args.title:
            print("Error: --repo and --title are required for creating a PR", file=sys.stderr)
            sys.exit(1)
        create_pr(args.repo, args.title, args.body, args.source, args.target, args.draft)

    elif args.list:
        if not args.repo:
            print("Error: --repo is required for listing PRs", file=sys.stderr)
            sys.exit(1)
        list_prs(args.repo, args.state)

    elif args.get:
        if not args.repo or not args.number:
            print("Error: --repo and --number are required for getting a PR", file=sys.stderr)
            sys.exit(1)
        get_pr(args.repo, args.number)

    elif args.merge:
        if not args.repo or not args.number:
            print("Error: --repo and --number are required for merging a PR", file=sys.stderr)
            sys.exit(1)
        merge_pr(args.repo, args.number, args.merge_method)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
