# GitHub企业微信通知Action - 设置指南

## 1. 准备工作

### 1.1 创建企业微信机器人

1. 打开企业微信群，点击右上角的群设置
2. 选择「智能群助手」
3. 点击「添加机器人」
4. 选择「新创建一个机器人」
5. 给机器人起一个名字，点击「添加」
6. 复制生成的Webhook URL，格式如下：
   ```
   https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```

### 1.2 在GitHub仓库中设置Secret

1. 登录GitHub，进入你的仓库页面
2. 点击顶部的「Settings」标签
3. 点击左侧菜单中的「Secrets and variables」→「Actions」
4. 点击「New repository secret」
5. 在「Name」字段中输入：`WECHAT_WEBHOOK_URL`
6. 在「Secret」字段中粘贴你的企业微信机器人Webhook URL
7. 点击「Add secret」

## 2. 配置工作流文件

### 2.1 创建或编辑工作流文件

在你的GitHub仓库中创建或编辑 `.github/workflows/wechat-notification.yml` 文件，添加以下内容：

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
      - name: 检出代码
        uses: actions/checkout@v3
        with:
          fetch-depth: 1
      
      - name: 发送通知到企业微信
        uses: fsyinghua/wechatActions@main
        with:
          wechat_webhook_url: ${{ secrets.WECHAT_WEBHOOK_URL }}
          event_types: push,pull_request,issues,release
```

### 2.2 关键配置说明

- `on:` - 定义触发通知的事件类型
- `wechat_webhook_url:` - 使用 `secrets.WECHAT_WEBHOOK_URL` 引用之前设置的Secret
- `event_types:` - 可选，指定需要通知的事件类型，默认包含所有支持的事件

## 3. 测试通知功能

### 3.1 推送代码测试

1. 确保工作流文件已提交到仓库
2. 推送一些更改到仓库的 `main` 或 `master` 分支
3. 登录GitHub，进入仓库的「Actions」页面
4. 查看最近的工作流运行状态
5. 检查企业微信是否收到通知

### 3.2 查看日志

如果工作流运行失败，可以查看详细日志：

1. 进入「Actions」页面
2. 点击失败的工作流运行
3. 点击「发送通知到企业微信」步骤
4. 查看详细日志，找出错误原因

## 4. 常见问题排查

### 4.1 工作流未触发

- 检查工作流文件的路径是否正确：`.github/workflows/`
- 检查触发事件的配置是否正确
- 确保推送的分支在 `branches` 列表中

### 4.2 通知未发送到企业微信

- 检查 `WECHAT_WEBHOOK_URL` Secret是否正确设置
- 确认Secret的名称与工作流文件中使用的名称一致
- 检查企业微信机器人是否被禁用
- 查看GitHub Actions日志，寻找错误信息

### 4.3 工作流运行失败

- 检查工作流文件的语法是否正确
- 查看详细日志，找出错误原因
- 确保所有必需的输入参数都已提供

## 5. 测试命令

### 5.1 本地测试

```bash
# 运行基本测试
python test_main.py

# 测试发送到企业微信
WECHAT_WEBHOOK_URL="你的Webhook URL" python test_actual_robot.py
```

### 5.2 推送测试

```bash
# 创建一个测试文件
touch test.txt

git add test.txt
git commit -m "Test notification"
git push origin main
```

## 6. 配置管理

### 6.1 多仓库复用

这个Action可以在多个仓库中复用，只需：

1. 在每个仓库中设置 `WECHAT_WEBHOOK_URL` Secret
2. 添加相同的工作流文件
3. 或者使用相同的组织Secret（如果是同一组织下的仓库）

### 6.2 组织Secret

如果你的仓库属于某个GitHub组织，可以设置组织级别的Secret：

1. 进入组织的「Settings」页面
2. 选择「Secrets and variables」→「Actions」
3. 点击「New organization secret」
4. 设置Secret名称和值，并选择可以访问这个Secret的仓库

## 7. 支持的事件类型

- `push` - 代码推送事件
- `pull_request` - Pull Request事件（创建、更新、关闭）
- `issues` - Issues事件（创建、编辑、关闭、重新打开）
- `release` - Release事件（发布、创建、编辑、删除）

## 8. 自定义配置

### 8.1 只通知特定事件类型

```yaml
with:
  event_types: push,release
```

### 8.2 只在特定分支触发

```yaml
on:
  push:
    branches: [ main, master, develop ]
```

## 9. 故障排除

### 9.1 查看GitHub Actions日志

1. 登录GitHub，进入仓库页面
2. 点击「Actions」标签
3. 点击最近的工作流运行
4. 点击「发送通知到企业微信」步骤
5. 查看详细日志

### 9.2 检查企业微信机器人状态

1. 打开企业微信群
2. 查看机器人是否在线
3. 尝试发送一条简单的消息测试

### 9.3 测试Webhook URL

使用curl命令测试Webhook URL是否可用：

```bash
curl -X POST "你的Webhook URL" \
  -H "Content-Type: application/json" \
  -d '{"msgtype":"text","text":{"content":"测试消息"}}'
```

## 10. 联系支持

如果遇到问题，可以：

1. 查看GitHub仓库的「Issues」页面
2. 提交新的Issue，描述你的问题
3. 附上相关的日志和配置信息

---

设置完成后，你应该能够收到GitHub仓库的所有通知，包括代码推送、Pull Request、Issues和Release事件。