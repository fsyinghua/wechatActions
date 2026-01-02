# GitHub连接调试指南

## 1. 手动触发调试工作流

### 步骤1：访问仓库Actions页面
1. 登录GitHub，进入仓库页面：[https://github.com/fsyinghua/wechatActions](https://github.com/fsyinghua/wechatActions)
2. 点击顶部的 **Actions** 标签

### 步骤2：找到调试工作流
1. 在左侧工作流列表中，找到 **Debug Secret Configuration** 工作流
2. 点击工作流名称，进入工作流页面

### 步骤3：手动触发工作流
1. 点击右上角的 **Run workflow** 按钮
2. 在弹出的对话框中，保持默认设置（选择main分支）
3. 点击 **Run workflow** 按钮

### 步骤4：查看工作流运行状态
1. 工作流将开始运行，显示为 "in progress"
2. 等待几秒钟，刷新页面，查看运行结果
3. 如果显示 "success"，则表示工作流运行成功
4. 如果显示 "failure"，则表示工作流运行失败，需要查看日志

## 2. 查看工作流日志

### 步骤1：进入工作流运行详情
1. 在工作流页面中，点击最新的运行记录
2. 进入运行详情页面

### 步骤2：查看作业日志
1. 点击 **debug-secret** 作业，进入作业详情页面
2. 查看完整的作业日志
3. 日志中包含详细的调试信息，包括：
   - 密钥检查结果
   - 环境变量访问测试
   - Python脚本测试结果
   - 企业微信消息发送结果

### 步骤3：分析日志信息
1. **检查Webhook Secret** 步骤：查看密钥是否存在
2. **测试环境变量访问** 步骤：查看环境变量是否正确设置
3. **使用Python脚本测试密钥访问** 步骤：查看Python脚本是否能成功获取密钥
4. **发送测试消息** 步骤：查看是否能成功发送企业微信消息

## 3. 常见问题排查

### 问题1：密钥不存在或为空
- **日志表现**：
  ```
  1. 检查WECHAT_WEBHOOK_URL Secret...
     ⚠️ WECHAT_WEBHOOK_URL Secret 不存在或为空
  2. 检查WCOM_WEBHOOK_URL Secret...
     ⚠️ WCOM_WEBHOOK_URL Secret 不存在或为空
  ❌ 未找到有效的Webhook Secret
  ```
- **解决方法**：
  1. 进入仓库 **Settings** > **Secrets and variables** > **Actions**
  2. 创建名为 `WECHAT_WEBHOOK_URL` 或 `WCOM_WEBHOOK_URL` 的密钥
  3. 确保密钥值为有效的企业微信机器人Webhook URL

### 问题2：无法获取环境变量
- **日志表现**：
  ```
  === 测试WECHAT_WEBHOOK_URL密钥访问 ===
  ❌ 无法获取WECHAT_WEBHOOK_URL密钥
  
  === 检查环境变量 ===
  ```
- **解决方法**：
  1. 检查工作流文件中是否正确设置了环境变量
  2. 确保密钥名称与工作流中使用的名称一致
  3. 重新运行工作流

### 问题3：企业微信消息发送失败
- **日志表现**：
  ```
  === 发送测试消息 ===
  使用Webhook URL: https://qyapi.weixin.qq.com/cgi-bin/...
  HTTP状态码: 400
  响应内容: {"errcode":40001,"errmsg":"invalid token"}
  ❌ 测试消息发送失败: 400 Client Error: Bad Request for url: ...
  ```
- **解决方法**：
  1. 检查Webhook URL是否正确
  2. 确保企业微信机器人已添加到目标群组
  3. 确保机器人有发送消息的权限
  4. 检查机器人的key是否正确

### 问题4：工作流运行超时
- **日志表现**：
  ```
  This job is taking too long to run and has been cancelled.
  ```
- **解决方法**：
  1. 检查网络连接
  2. 确保企业微信服务器可以访问
  3. 调整工作流中的超时设置

## 4. 手动测试企业微信通知

### 方法1：使用本地Python脚本测试
1. 打开命令行终端
2. 进入项目目录
3. 运行以下命令：
   ```bash
   # 将YOUR_WEBHOOK_URL替换为您的企业微信机器人Webhook URL
   INPUT_WECHAT_WEBHOOK_URL=YOUR_WEBHOOK_URL python3 test_secret_access.py
   ```
4. 查看输出结果，确认是否能成功获取密钥

### 方法2：使用GitHub API测试
1. 打开浏览器，访问GitHub API端点：
   ```
   https://api.github.com/repos/fsyinghua/wechatActions/actions/workflows
   ```
2. 检查是否能看到 `Debug Secret Configuration` 工作流
3. 如果能看到，则表示GitHub API访问正常

## 5. 验证GitHub与企业微信的连接

### 步骤1：确保密钥已正确设置
1. 登录GitHub，进入仓库 **Settings** > **Secrets and variables** > **Actions**
2. 确认 `WECHAT_WEBHOOK_URL` 或 `WCOM_WEBHOOK_URL` 密钥已存在且值正确

### 步骤2：运行调试工作流
1. 按照前面的步骤手动触发 `Debug Secret Configuration` 工作流
2. 等待工作流运行完成
3. 查看工作流日志，确认所有步骤都成功执行

### 步骤3：检查企业微信消息
1. 打开企业微信，进入目标群组
2. 查看是否收到了来自GitHub Actions的测试消息
3. 如果收到消息，则表示GitHub与企业微信的连接正常

## 6. 高级调试技巧

### 技巧1：添加更多调试信息
1. 修改 `main.py` 文件，添加更多的日志输出
2. 在关键位置添加 `print` 语句，输出调试信息
3. 重新提交代码，运行工作流，查看详细日志

### 技巧2：使用GitHub CLI调试
1. 安装GitHub CLI：[https://cli.github.com/](https://cli.github.com/)
2. 登录GitHub CLI：
   ```bash
   gh auth login
   ```
3. 查看工作流运行状态：
   ```bash
   gh run list -w "Debug Secret Configuration" -L 5
   ```
4. 查看工作流日志：
   ```bash
   # 将RUN_ID替换为实际的运行ID
   gh run view RUN_ID --log
   ```

### 技巧3：使用本地Docker测试
1. 安装Docker：[https://www.docker.com/](https://www.docker.com/)
2. 构建Docker镜像：
   ```bash
   docker build -t wechat-actions .
   ```
3. 运行Docker容器，测试通知功能：
   ```bash
   # 将YOUR_WEBHOOK_URL替换为您的企业微信机器人Webhook URL
   docker run --rm -e INPUT_WECHAT_WEBHOOK_URL=YOUR_WEBHOOK_URL wechat-actions
   ```

## 7. 联系支持

如果您在调试过程中遇到任何问题，可以通过以下方式获取支持：
1. 查看项目的 **README.md** 文件，获取更多信息
2. 检查项目的 **Issues** 页面，查看是否有类似问题的解决方案
3. 提交新的Issue，描述您遇到的问题和详细的日志信息

## 8. 调试完成后

调试完成后，您可以：
1. 将调试工作流用于其他仓库的测试
2. 集成到实际的项目工作流中
3. 定期运行调试工作流，确保连接正常

---

**调试成功标志**：
1. 工作流运行状态为 "success"
2. 日志中显示 "✅ 最终选择的Secret: XXX"
3. 企业微信收到测试消息
4. 所有步骤都成功执行，没有错误信息

祝您调试顺利！