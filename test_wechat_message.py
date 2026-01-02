#!/usr/bin/env python3
"""
简单测试脚本：测试发送企业微信消息
"""
import os
import sys
import requests
import json

def send_wechat_message(webhook_url, message):
    """
    发送企业微信消息
    """
    try:
        response = requests.post(webhook_url, json=message, timeout=10)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    print("=== 测试企业微信消息发送 ===")
    
    # 获取环境变量中的webhook URL
    webhook_url = os.getenv('INPUT_WECHAT_WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ 未找到webhook URL，尝试从环境变量获取...")
        # 尝试从其他环境变量获取
        webhook_url = os.getenv('WECHAT_WEBHOOK_URL') or os.getenv('WCOM_WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ 无法获取webhook URL，请设置环境变量INPUT_WECHAT_WEBHOOK_URL、WECHAT_WEBHOOK_URL或WCOM_WEBHOOK_URL")
        sys.exit(1)
    
    print(f"✅ 获取到webhook URL: {webhook_url[:50]}...")
    
    # 创建测试消息
    test_message = {
        'msgtype': 'text',
        'text': {
            'content': '这是来自GitHub Actions的简单测试消息 ✅'
        }
    }
    
    print("\n=== 发送测试消息 ===")
    success, result = send_wechat_message(webhook_url, test_message)
    
    if success:
        print("✅ 消息发送成功！")
        print(f"✅ 响应结果: {json.dumps(result)}")
        sys.exit(0)
    else:
        print(f"❌ 消息发送失败: {result}")
        sys.exit(1)
