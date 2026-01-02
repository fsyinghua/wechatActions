#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：使用实际的企业微信机器人Webhook URL测试通知发送功能
"""

import os
import sys
import json
import tempfile
import subprocess

# 使用您提供的企业微信Webhook URL
TEST_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c473353f-846b-4c2c-bea4-ae2644e4d955"

# 模拟GitHub事件数据
test_events = {
    "push": {
        "repository": {
            "full_name": "test/test-repo",
            "html_url": "https://github.com/test/test-repo"
        },
        "pusher": {
            "name": "test-user"
        },
        "commits": [
            {
                "message": "测试提交信息 - 来自实际企业微信机器人测试",
                "committer": {
                    "name": "test-committer"
                },
                "id": "1234567890abcdef"
            }
        ],
        "compare": "https://github.com/test/test-repo/compare/old..new",
        "ref": "refs/heads/main"
    }
}

def test_actual_robot():
    """
    使用实际企业微信机器人测试通知发送
    """
    print("=== 使用实际企业微信机器人测试通知发送 ===")
    
    # 创建临时文件保存事件数据
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_events["push"], f)
        event_file_path = f.name
    
    try:
        # 设置环境变量
        env = os.environ.copy()
        env['INPUT_WECHAT_WEBHOOK_URL'] = TEST_WEBHOOK_URL
        env['GITHUB_EVENT_PATH'] = event_file_path
        env['GITHUB_EVENT_NAME'] = "push"
        env['INPUT_EVENT_TYPES'] = "push"
        
        # 运行main.py脚本
        result = subprocess.run(
            [sys.executable, 'main.py'],
            env=env,
            capture_output=True,
            text=True
        )
        
        # 输出结果
        print(f"退出码: {result.returncode}")
        print(f"标准输出:\n{result.stdout}")
        print(f"标准错误:\n{result.stderr}")
        
        return result.returncode == 0
    finally:
        # 删除临时文件
        os.unlink(event_file_path)

def test_direct_request():
    """
    直接测试企业微信Webhook API
    """
    print("\n=== 直接测试企业微信Webhook API ===")
    
    # 直接发送一个简单的文本消息
    test_message = {
        "msgtype": "text",
        "text": {
            "content": "这是一条直接测试消息 - 来自GitHub企业微信通知模块"
        }
    }
    
    try:
        import requests
        response = requests.post(TEST_WEBHOOK_URL, json=test_message, timeout=10)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 解析响应
        response_json = response.json()
        if response_json.get("errcode") == 0:
            print("✅ 直接测试成功！")
            return True
        else:
            print(f"❌ 直接测试失败: {response_json.get('errmsg')}")
            return False
    except Exception as e:
        print(f"❌ 直接测试异常: {e}")
        return False

def main():
    """
    主测试函数
    """
    print("企业微信机器人实际测试")
    print("=" * 50)
    
    # 测试1：使用main.py脚本测试
    print("\n1. 使用main.py脚本测试")
    script_result = test_actual_robot()
    
    # 测试2：直接测试Webhook API
    print("\n2. 直接测试Webhook API")
    direct_result = test_direct_request()
    
    print("\n" + "=" * 50)
    print("测试完成")
    print(f"脚本测试结果: {'✅ 成功' if script_result else '❌ 失败'}")
    print(f"直接测试结果: {'✅ 成功' if direct_result else '❌ 失败'}")

if __name__ == "__main__":
    main()