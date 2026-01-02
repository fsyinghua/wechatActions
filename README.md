# GitHub 企业微信通知 Action

一个可复用的 GitHub Action，当 GitHub 仓库发生事件时，自动发送通知到企业微信群。

## 功能特性

- ✅ 支持多种 GitHub 事件类型：push、pull_request、issues、release
- ✅ 可自定义需要通知的事件类型
- ✅ 企业微信 Markdown 消息格式
- ✅ 易于在多个仓库中复用
- ✅ 使用 GitHub Secrets 保护敏感信息

## 支持的事件类型

- `push` - 代码推送事件
- `pull_request` - Pull Request 事件（创建、更新、关闭）
- `issues` - Issues 事件（创建、编辑、关闭、重新打开）
- `release` - Release 事件（发布、创建、编辑、删除）

## 使用方法

### 1. 准备工作

1. 在企业微信中创建一个群机器人，获取 Webhook URL
2. 在 GitHub 仓库的 **Settings > Secrets and variables > Actions** 中添加一个新的 secret：
   - 名称：`WECHAT_WEBHOOK_URL`
   - 值：你的企业微信机器人 Webhook URL

### 2. 在工作流中使用

在你的 GitHub 仓库中创建或编辑 `.github/workflows/wechat-notification.yml` 文件，添加以下内容：

```yaml
name: 企业微信通知

on:
  push:
    branches: [ main, master ]
  pull_request:
    types: [ opened, synchronize, closed ]
  issues:
    types: [ opened, edited, closed, reopened ]
  release:
    types: [ published, created, edited, deleted ]

jobs:
  notify-wechat:
    runs-on: ubuntu-latest
    name: 发送企业微信通知
    steps:
      - name: 发送通知到企业微信
        uses: fsyinghua/wechatActions@v1
        with:
          wechat_webhook_url: ${{ secrets.WECHAT_WEBHOOK_URL }}
          event_types: push,pull_request,issues,release
```

### 3. 自定义配置

| 参数名 | 描述 | 是否必填 | 默认值 |
|--------|------|----------|--------|
| `wechat_webhook_url` | 企业微信机器人 Webhook URL | 是 | - |
| `event_types` | 需要通知的事件类型，逗号分隔 | 否 | `push,pull_request,issues,release` |

## 示例消息格式

### Push 事件
```markdown
## 📢 GitHub 代码推送通知

**仓库**: [username/repo](https://github.com/username/repo)
**操作**: 代码推送
**分支**: main
**作者**: pusher_name
**提交数**: 2 个
**查看对比**: [点击查看](https://github.com/username/repo/compare/...)

**最新提交**:
- **提交信息**: 修复bug
- **提交者**: committer_name
- **提交哈希**: a1b2c3d
```

### Pull Request 事件
```markdown
## 📢 GitHub Pull Request 通知

**仓库**: [username/repo](https://github.com/username/repo)
**操作**: user 创建了 Pull Request
**标题**: [修复bug](https://github.com/username/repo/pull/1)
**编号**: #1
**状态**: open
**源分支**: feature → 目标分支: main
**作者**: user
```

## 本地开发和测试

### 环境要求

- Python 3.8+
- 安装依赖：`pip install -r requirements.txt`

### 测试脚本

- `test_main.py` - 模拟 GitHub 事件，测试消息生成逻辑
- `test_actual_robot.py` - 使用真实的 Webhook URL 测试发送功能

### 运行测试

```bash
# 运行模拟测试
python test_main.py

# 运行真实机器人测试（需要设置环境变量）
WECHAT_WEBHOOK_URL="你的Webhook URL" python test_actual_robot.py
```

## 开发计划

- [ ] 支持更多 GitHub 事件类型
- [ ] 支持自定义消息模板
- [ ] 支持多个通知群
- [ ] 添加消息确认机制

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
