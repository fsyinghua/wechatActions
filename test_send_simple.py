#!/usr/bin/env python3
"""
发送简单测试消息到企业微信机器人
"""

import requests
import sys

# 企业微信机器人Webhook URL
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c473353f-846b-4c2c-bea4-ae2644e4d955"

def send_simple_message(message):
    """
    发送简单文本消息到企业微信
    :param message: 要发送的文本消息
    :return: 是否发送成功
    """
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        if result.get("errcode") == 0:
            print(f"✅ 测试消息发送成功: {message}")
            return True
        else:
            print(f"❌ 测试消息发送失败: {result.get('errmsg')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 发送请求失败: {e}")
        return False

if __name__ == "__main__":
    # 发送测试消息
    send_simple_message("测试")