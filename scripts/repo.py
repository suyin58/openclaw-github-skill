#!/usr/bin/env python3
"""
GitHub仓库操作脚本
"""

import subprocess
import json
import argparse
import sys
import shutil


def check_dependencies():
    """检查必要的依赖是否已安装"""
    import os

    # 检查 GitHub Token 环境变量
    gh_token = os.environ.get("GH_TOKEN")

    if gh_token:
        print("✓ GH_TOKEN environment variable is set")
    else:
        print("⚠️  Warning: GH_TOKEN environment variable is not set", file=sys.stderr)
        print("   Please set GH_TOKEN environment variable:", file=sys.stderr)
        print("   PowerShell: $env:GH_TOKEN = 'your_token'", file=sys.stderr)
        print("   Bash: export GH_TOKEN='your_token'", file=sys.stderr)
        print("   Get your token: https://github.com/settings/tokens", file=sys.stderr)
        print("   Required scopes: repo, workflow", file=sys.stderr)
        sys.exit(1)

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


def run_gh_command(args):
    """执行gh命令并返回结果"""
    import os

    cmd = ["gh"] + args
    env = os.environ.copy()

    # 确保使用 GH_TOKEN 环境变量
    if "GH_TOKEN" in env:
        env["GH_TOKEN"] = env["GH_TOKEN"]

    result = subprocess.run(cmd, capture_output=True, text=True, env=env)

    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    return result.stdout


def create_repo(name, description=None, private=False):
    """创建GitHub仓库"""
    args = ["repo", "create", name]

    if description:
        args.extend(["--description", description])

    if private:
        args.append("--private")
    else:
        args.append("--public")

    result = run_gh_command(args)
    print(f"Repository '{name}' created successfully!")
    print(result)


def get_repo_info(repo_path):
    """获取仓库信息"""
    result = run_gh_command(["repo", "view", repo_path, "--json", "name,description,visibility,url,owner"])
    data = json.loads(result)
    return data


def main():
    # 检查依赖
    check_dependencies()

    parser = argparse.ArgumentParser(description="GitHub仓库操作")
    parser.add_argument("--create", action="store_true", help="创建新仓库")
    parser.add_argument("--info", action="store_true", help="获取仓库信息")
    parser.add_argument("--name", help="仓库名称")
    parser.add_argument("--description", help="仓库描述")
    parser.add_argument("--private", action="store_true", help="创建私有仓库")
    parser.add_argument("--repo", help="仓库标识 (owner/repo)")

    args = parser.parse_args()

    if args.create:
        if not args.name:
            print("Error: --name is required for creating a repository", file=sys.stderr)
            sys.exit(1)
        create_repo(args.name, args.description, args.private)

    elif args.info:
        if not args.repo:
            print("Error: --repo is required for getting repository info", file=sys.stderr)
            sys.exit(1)
        info = get_repo_info(args.repo)
        print(json.dumps(info, indent=2, ensure_ascii=False))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
