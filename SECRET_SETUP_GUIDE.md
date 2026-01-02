# GitHub仓库密钥设置指南

## 目的
本指南旨在帮助您在GitHub仓库中设置`WECHAT_WEBHOOK_URL`密钥，并验证其是否可以正常访问。

## 步骤1：登录GitHub账号
1. 打开浏览器，访问 [GitHub](https://github.com)
2. 登录您的GitHub账号

## 步骤2：进入仓库设置
1. 访问仓库页面：[https://github.com/fsyinghua/wechatActions](https://github.com/fsyinghua/wechatActions)
2. 点击页面顶部的 **Settings** 标签

## 步骤3：创建密钥
1. 在左侧导航栏中，点击 **Secrets and variables** > **Actions**
2. 点击右上角的 **New repository secret** 按钮
3. 在弹出的表单中：
   - **Name**：输入 `WECHAT_WEBHOOK_URL`（推荐）或 `WCOM_WEBHOOK_URL`（兼容旧命名，必须完全一致，包括大小写）
   - **Secret**：输入您的企业微信机器人Webhook URL，例如：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key-here`
4. 点击 **Add secret** 按钮保存

## 步骤4：验证密钥设置
1. 返回仓库主页，点击 **Actions** 标签
2. 在左侧工作流列表中，找到 **Debug Secret Configuration** 工作流
3. 点击工作流名称，进入工作流页面
4. 点击右上角的 **Run workflow** 按钮
5. 在弹出的对话框中，保持默认设置，点击 **Run workflow** 按钮
6. 等待工作流运行完成，查看运行结果

## 步骤5：查看工作流日志
1. 在工作流页面中，点击最新的运行记录
2. 点击 **debug-secret** 作业，查看详细日志
3. 在日志中查找以下信息：
   - 检查 `检查WECHAT_WEBHOOK_URL Secret` 步骤的输出
   - 如果显示 `✅ WECHAT_WEBHOOK_URL Secret 已存在`，则表示密钥设置成功
   - 如果显示 `❌ WECHAT_WEBHOOK_URL Secret 不存在或为空`，则表示密钥设置失败，需要重新设置

## 常见问题排查

### 问题1：工作流运行失败
- **原因**：可能是密钥不存在或为空
- **解决方法**：重新检查密钥设置，确保密钥名称和值都正确

### 问题2：无法发送测试消息
- **原因**：可能是Webhook URL无效或企业微信机器人配置问题
- **解决方法**：检查Webhook URL是否正确，确保企业微信机器人已正确配置

### 问题3：PAT令牌权限不足
- **原因**：用于访问GitHub API的PAT令牌没有足够的权限
- **解决方法**：创建一个具有 `repo` 权限的新PAT令牌，或者直接通过GitHub网页界面进行操作

## 验证方法

### 方法1：通过GitHub Actions工作流验证
1. 按照步骤4和步骤5操作，运行工作流并查看日志
2. 如果工作流运行成功，且日志显示密钥存在，则验证通过

### 方法2：通过实际事件触发验证
1. 在仓库中进行一次代码推送或创建一个Pull Request
2. 检查企业微信是否收到通知
3. 如果收到通知，则验证通过

## 注意事项

1. **密钥名称必须完全一致**：必须使用 `WECHAT_WEBHOOK_URL` 作为密钥名称，包括大小写
2. **Webhook URL必须正确**：确保复制的Webhook URL没有多余的空格或换行符
3. **企业微信机器人必须正确配置**：确保企业微信机器人已添加到目标群组，并且具有发送消息的权限
4. **工作流权限必须正确**：确保GitHub Actions工作流具有访问密钥的权限

## 联系支持

如果您在设置过程中遇到任何问题，请随时联系项目维护者获取帮助。
