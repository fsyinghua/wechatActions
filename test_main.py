#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：模拟GitHub事件数据，测试企业微信通知发送功能
"""

import os
import sys
import json
import tempfile
import subprocess

# 测试用的企业微信Webhook URL（替换为实际的测试URL）
TEST_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-test-key"

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
                "message": "测试提交信息",
                "committer": {
                    "name": "test-committer"
                },
                "id": "1234567890abcdef"
            }
        ],
        "compare": "https://github.com/test/test-repo/compare/old..new",
        "ref": "refs/heads/main"
    },
    "pull_request": {
        "repository": {
            "full_name": "test/test-repo",
            "html_url": "https://github.com/test/test-repo"
        },
        "pull_request": {
            "title": "测试PR标题",
            "html_url": "https://github.com/test/test-repo/pull/1",
            "number": 1,
            "state": "open",
            "head": {
                "ref": "feature-branch"
            },
            "base": {
                "ref": "main"
            },
            "user": {
                "login": "test-author"
            },
            "merged": False
        },
        "action": "opened",
        "sender": {
            "login": "test-sender"
        }
    }
}

def test_event(event_type, event_data):
    """
    测试指定类型的GitHub事件
    """
    print(f"\n=== 测试 {event_type} 事件 ===")
    
    # 创建临时文件保存事件数据
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(event_data, f)
        event_file_path = f.name
    
    try:
        # 设置环境变量
        env = os.environ.copy()
        env['INPUT_WECHAT_WEBHOOK_URL'] = TEST_WEBHOOK_URL
        env['GITHUB_EVENT_PATH'] = event_file_path
        env['GITHUB_EVENT_NAME'] = event_type
        env['INPUT_EVENT_TYPES'] = event_type
        
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

def test_message_generation():
    """
    测试消息生成功能
    """
    print("\n=== 测试消息生成功能 ===")
    
    # 导入main.py中的函数
    import main
    
    # 测试push事件消息生成
    push_event = test_events["push"]
    push_message = main.generate_push_message(push_event)
    print("Push事件消息:")
    print(json.dumps(push_message, indent=2, ensure_ascii=False))
    
    # 测试pull_request事件消息生成
    pr_event = test_events["pull_request"]
    pr_message = main.generate_pull_request_message(pr_event)
    print("\nPull Request事件消息:")
    print(json.dumps(pr_message, indent=2, ensure_ascii=False))
    
    return True

def main():
    """
    主测试函数
    """
    print("GitHub企业微信通知模块测试")
    print("=" * 50)
    
    # 测试消息生成功能
    test_message_generation()
    
    # 测试实际发送通知（可选，需要配置正确的Webhook URL）
    print("\n=== 测试实际发送通知 ===")
    print("注意：需要配置正确的企业微信Webhook URL才能测试实际发送功能")
    print(f"当前测试URL: {TEST_WEBHOOK_URL}")
    
    # 询问是否继续测试实际发送
    if input("是否继续测试实际发送通知？(y/n): ").lower() == 'y':
        # 测试push事件
        test_event("push", test_events["push"])
        
        # 测试pull_request事件
        test_event("pull_request", test_events["pull_request"])
    
    print("\n" + "=" * 50)
    print("测试完成")

if __name__ == "__main__":
    main()