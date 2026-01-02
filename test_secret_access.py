#!/usr/bin/env python3
"""
测试脚本：验证WECHAT_WEBHOOK_URL密钥是否可以访问
"""
import os
import sys

print("=== 测试WECHAT_WEBHOOK_URL密钥访问 ===")

# 检查是否可以直接访问密钥（在GitHub Actions中）
webhook_url = os.getenv('INPUT_WECHAT_WEBHOOK_URL')
if webhook_url:
    print(f"✅ 成功获取到WECHAT_WEBHOOK_URL密钥")
    print(f"✅ 密钥长度: {len(webhook_url)} 字符")
    print(f"✅ 密钥前50字符: {webhook_url[:50]}...")
    sys.exit(0)
else:
    print(f"❌ 无法获取WECHAT_WEBHOOK_URL密钥")
    # 检查环境变量
    print("\n=== 检查环境变量 ===")
    for env_var in os.environ:
        if env_var.startswith('INPUT_'):
            print(f"- {env_var}: {os.environ[env_var]}")
    sys.exit(1)
