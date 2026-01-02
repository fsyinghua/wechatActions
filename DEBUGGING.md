# GitHub企业微信通知Action - 调试指南

## 问题分析与修复

### 1. 主要问题
GitHub Actions报错：`using: python3 is not supported, use 'docker', 'node12', 'node16', 'node20' or 'node24' instead`

### 2. 修复方案
将GitHub Action的运行环境从`python3`改为`docker`，使用Docker容器提供稳定的Python环境。

### 3. 修复内容

#### 3.1 创建了Dockerfile
- 使用官方Python 3.10-slim镜像
- 自动安装依赖包
- 设置正确的入口点

#### 3.2 修改了action.yml
- 将`using: python3`改为`using: docker`
- 使用`image: Dockerfile`指定Docker构建上下文

## 调试步骤

### 1. 本地测试

```bash
# 运行基本测试
python test_main.py

# 测试发送到企业微信
WECHAT_WEBHOOK_URL="你的Webhook URL" python test_actual_robot.py
```

### 2. 推送修改到GitHub

```bash
# 确保所有修改已提交
git commit -m "Fix action.yml to use docker runner"

# 推送修改
git push origin main
```

### 3. 检查GitHub Actions日志

1. 登录GitHub，进入仓库页面
2. 点击顶部的"Actions"标签
3. 查看最近的工作流运行
4. 点击失败的工作流，查看详细日志

### 4. 常见问题排查

#### 4.1 工作流未触发
- 检查`.github/workflows/`目录下的YAML文件
- 确保`on:`关键字正确，而不是`actions:`
- 检查触发事件的配置是否正确

#### 4.2 通知未发送到企业微信
- 检查`WECHAT_WEBHOOK_URL` Secret是否正确设置
- 确认Secret的名称与工作流文件中使用的名称一致
- 检查企业微信机器人是否被禁用

#### 4.3 Docker构建失败
- 检查Dockerfile语法是否正确
- 确保requirements.txt文件存在且格式正确
- 查看GitHub Actions日志中的Docker构建错误

### 5. 手动测试

可以使用以下命令手动测试Docker构建：

```bash
# 构建Docker镜像
docker build -t wechat-actions .

# 运行Docker容器
docker run --rm -e INPUT_WECHAT_WEBHOOK_URL