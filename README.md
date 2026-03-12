# OpenClaw GitHub Skill

用于执行 GitHub 相关操作的 OpenClaw Skill，支持仓库管理、Issue 管理和 Pull Request 管理等功能。

## 系统要求

- **操作系统**: Windows 11 / Windows 10
- **Python**: 3.6 或更高版本
- **Git**: 已安装并配置
- **GitHub CLI (gh)**: 已安装并登录

## 安装前置依赖

### 1. 安装 Git

```bash
# 使用 winget 安装
winget install --id Git.Git

# 或访问官网下载
# https://git-scm.com/download/win
```

### 2. 安装 GitHub CLI

```bash
# 使用 winget 安装
winget install --id GitHub.cli

# 或访问官网下载
# https://cli.github.com/
```

### 3. 登录 GitHub

```bash
gh auth login
```

按照提示选择：
- GitHub.com
- HTTPS
- Yes (上传 SSH keys)
- Login with a web browser

然后在浏览器中授权登录。

## 功能特性

### 仓库操作 (repo.py)
- 创建公开/私有仓库
- 查看仓库信息

### Issue 操作 (issue.py)
- 创建 Issue（支持标题、正文、标签）
- 列出 Issues（按状态筛选）
- 查看 Issue 详情

### Pull Request 操作 (pr.py)
- 创建 PR（支持源分支、目标分支、草稿）
- 列出 PRs（按状态筛选）
- 查看 PR 详情
- 合并 PR（支持 merge/squash/rebase）

## 使用方式

### 创建仓库

```bash
python scripts/repo.py --create --name "my-repo" --description "我的第一个仓库"
```

```bash
# 创建私有仓库
python scripts/repo.py --create --name "private-repo" --private
```

### 创建 Issue

```bash
python scripts/issue.py --create --repo "owner/repo" --title "发现一个Bug" --body "详细描述bug内容" --labels "bug,high-priority"
```

### 列出 Issues

```bash
# 列出所有开放的 Issues
python scripts/issue.py --list --repo "owner/repo"

# 列出已关闭的 Issues
python scripts/issue.py --list --repo "owner/repo" --state closed
```

### 创建 Pull Request

```bash
python scripts/pr.py --create --repo "owner/repo" --title "添加新功能" --body "实现了用户登录功能" --source "feature/login" --target "main"
```

```bash
# 创建草稿 PR
python scripts/pr.py --create --repo "owner/repo" --title "WIP: 新功能开发中" --draft --source "feature/wip" --target "main"
```

### 列出 Pull Requests

```bash
# 列出所有开放的 PRs
python scripts/pr.py --list --repo "owner/repo"

# 列出已合并的 PRs
python scripts/pr.py --list --repo "owner/repo" --state merged
```

### 合并 Pull Request

```bash
# 使用 merge 方式合并
python scripts/pr.py --merge --repo "owner/repo" --number 123 --merge-method merge

# 使用 squash 方式合并
python scripts/pr.py --merge --repo "owner/repo" --number 123 --merge-method squash

# 使用 rebase 方式合并
python scripts/pr.py --merge --repo "owner/repo" --number 123 --merge-method rebase
```

## 参数说明

### 仓库操作 (repo.py)

| 参数 | 说明 |
|------|------|
| `--create` | 创建新仓库 |
| `--info` | 获取仓库信息 |
| `--name` | 仓库名称 |
| `--description` | 仓库描述 |
| `--private` | 创建私有仓库 |
| `--repo` | 仓库标识 (owner/repo) |

### Issue 操作 (issue.py)

| 参数 | 说明 |
|------|------|
| `--create` | 创建 Issue |
| `--list` | 列出 Issues |
| `--get` | 获取 Issue 详情 |
| `--repo` | 仓库标识 (owner/repo) |
| `--number` | Issue 编号 |
| `--title` | Issue 标题 |
| `--body` | Issue 内容 |
| `--labels` | Issue 标签（逗号分隔） |
| `--state` | 筛选状态 (open/closed/all) |

### Pull Request 操作 (pr.py)

| 参数 | 说明 |
|------|------|
| `--create` | 创建 PR |
| `--list` | 列出 PRs |
| `--get` | 获取 PR 详情 |
| `--merge` | 合并 PR |
| `--repo` | 仓库标识 (owner/repo) |
| `--number` | PR 编号 |
| `--title` | PR 标题 |
| `--body` | PR 描述 |
| `--source` | 源分支 |
| `--target` | 目标分支 |
| `--draft` | 创建草稿 PR |
| `--state` | 筛选状态 (open/closed/merged/all) |
| `--merge-method` | 合并方式 (merge/squash/rebase) |

## 前置检查

脚本在执行前会自动检查以下依赖：

- ✓ Git 是否安装
- ✓ GitHub CLI (gh) 是否安装
- ✓ 是否已登录 GitHub

如果缺少依赖，会显示详细的安装指引。

## 注意事项

1. 首次使用前请确保已运行 `gh auth login` 并完成授权
2. 创建仓库后，需要手动关联本地仓库到远程仓库
3. 合并 PR 需要有相应的权限
4. 所有操作都使用 GitHub API，不需要配置 SSH 密钥

## 常见问题

### Q: 提示 "GitHub CLI (gh) is not installed"
A: 运行 `winget install --id GitHub.cli` 安装 GitHub CLI

### Q: 提示 "Not logged in to GitHub"
A: 运行 `gh auth login` 进行登录授权

### Q: 提示 "Git is not installed"
A: 运行 `winget install --id Git.Git` 安装 Git

### Q: 合并 PR 时提示权限不足
A: 请确保你有该仓库的写权限和合并权限

## 许可证

MIT License
