---
name: openclaw-github-skill
description: |
  执行GitHub相关的操作，包括创建仓库、创建Issue、管理Pull Request等。
  使用GitHub CLI (gh) 与GitHub API交互。
  触发场景：(1) 用户需要在GitHub上创建仓库 (2) 用户需要创建Issue (3) 用户需要创建或管理PR (4) "创建GitHub仓库"、"提交issue"、"创建PR"等请求
---

# GitHub 操作

使用GitHub CLI (gh) 执行各种GitHub操作。

## 使用方式

### 创建仓库

```bash
python {baseDir}/scripts/repo.py --create --name "repo-name" --description "Repo description"
```

### 创建 Issue

```bash
python {baseDir}/scripts/issue.py --create --repo "owner/repo" --title "Issue title" --body "Issue description"
```

### 列出 Issues

```bash
python {baseDir}/scripts/issue.py --list --repo "owner/repo"
```

### 创建 Pull Request

```bash
python {baseDir}/scripts/pr.py --create --repo "owner/repo" --title "PR title" --body "PR description" --source "source-branch" --target "main"
```

### 列出 Pull Requests

```bash
python {baseDir}/scripts/pr.py --list --repo "owner/repo"
```

## 参数说明

### 仓库操作 (repo.py)

| 参数 | 说明 |
|------|------|
| `--create` | 创建新仓库 |
| `--name` | 仓库名称 |
| `--description` | 仓库描述 |
| `--private` | 创建私有仓库 |
| `--repo` | 仓库标识 (owner/repo) |

### Issue 操作 (issue.py)

| 参数 | 说明 |
|------|------|
| `--create` | 创建Issue |
| `--list` | 列出Issues |
| `--repo` | 仓库标识 (owner/repo) |
| `--title` | Issue标题 |
| `--body` | Issue内容 |
| `--labels` | Issue标签 (逗号分隔) |
| `--state` | 筛选状态 (open/closed/all) |

### Pull Request 操作 (pr.py)

| 参数 | 说明 |
|------|------|
| `--create` | 创建PR |
| `--list` | 列出PRs |
| `--repo` | 仓库标识 (owner/repo) |
| `--title` | PR标题 |
| `--body` | PR描述 |
| `--source` | 源分支 |
| `--target` | 目标分支 |
| `--draft` | 创建草稿PR |
| `--state` | 筛选状态 (open/closed/merged/all) |

## 环境要求

需要安装并配置 GitHub CLI (gh):

```bash
# 安装 gh CLI
# Windows: winget install --id GitHub.cli

# 登录
gh auth login
```

## 示例

```bash
# 创建公开仓库
python {baseDir}/scripts/repo.py --create --name "my-awesome-project" --description "An awesome project"

# 创建私有仓库
python {baseDir}/scripts/repo.py --create --name "private-repo" --private

# 创建 Issue
python {baseDir}/scripts/issue.py --create --repo "owner/repo" --title "Bug found" --body "描述bug的详细信息" --labels "bug,priority-high"

# 创建 PR
python {baseDir}/scripts/pr.py --create --repo "owner/repo" --title "Add new feature" --body "实现新功能的描述" --source "feature/new-feature" --target "main"

# 列出所有 PR
python {baseDir}/scripts/pr.py --list --repo "owner/repo"
```
