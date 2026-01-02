#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本：在本地Python环境中模拟GitHub Actions环境，测试main.py的功能
"""

import os
import sys
import json
import uuid
import subprocess
import tempfile
import time

# 调试配置
DEBUG_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c473353f-846b-4c2c-bea4-ae2644e4d955"

# 模拟GitHub事件数据
def get_mock_event_data(event_type="push"):
    """
    获取模拟的GitHub事件数据
    """
    if event_type == "push":
        return {
            "repository": {
                "full_name": "test/test-repo",
                "html_url": "https://github.com/test/test-repo"
            },
            "pusher": {
                "name": "test-user"
            },
            "commits": [
                {
                    "message": "测试提交信息 - 来自GitHub Actions调试",
                    "committer": {
                        "name": "test-committer"
                    },
                    "id": "1234567890abcdef"
                }
            ],
            "compare": "https://github.com/test/test-repo/compare/old..new",
            "ref": "refs/heads/main"
        }
    return {}

def debug_github_call_local():
    """
    在本地Python环境中模拟GitHub Actions调用流程
    """
    session_id = str(uuid.uuid4())
    start_time = time.time()
    
    print(f"=== 在本地Python环境中调试GitHub Actions调用流程 ===")
    print(f"调试会话ID: {session_id}")
    print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"当前目录: {os.getcwd()}")
    
    # 步骤1: 检查项目结构
    print(f"\n[步骤1/{session_id}] 检查项目结构")
    required_files = [
        "action.yml", "main.py", 
        "requirements.txt", "README.md"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ 找到文件: {file}")
        else:
            print(f"❌ 缺少文件: {file}")
            return False
    
    # 步骤2: 检查Python环境和依赖
    print(f"\n[步骤2/{session_id}] 检查Python环境和依赖")
    
    # 检查Python版本
    python_version = subprocess.run(
        [sys.executable, "--version"],
        capture_output=True,
        text=True
    )
    print(f"✅ Python版本: {python_version.stdout.strip()}")
    
    # 安装依赖
    print(f"安装依赖: pip install -r requirements.txt")
    install_result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        capture_output=True,
        text=True
    )
    
    if install_result.returncode != 0:
        print(f"❌ 依赖安装失败")
        print(f"标准错误:\n{install_result.stderr}")
        return False
    
    print(f"✅ 依赖安装成功")
    
    # 步骤3: 准备模拟事件文件
    print(f"\n[步骤3/{session_id}] 准备模拟事件文件")
    
    event_data = get_mock_event_data()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(event_data, f, ensure_ascii=False, indent=2)
        event_file_path = f.name
    
    print(f"创建临时事件文件: {event_file_path}")
    print(f"事件数据: {json.dumps(event_data, ensure_ascii=False, indent=2)}")
    
    # 步骤4: 模拟GitHub Actions环境，运行main.py
    print(f"\n[步骤4/{session_id}] 模拟GitHub Actions环境，运行main.py")
    
    # 设置环境变量
    env = os.environ.copy()
    env['INPUT_WECHAT_WEBHOOK_URL'] = DEBUG_WEBHOOK_URL
    env['INPUT_EVENT_TYPES'] = "push,pull_request,issues,release"
    env['GITHUB_EVENT_PATH'] = event_file_path
    env['GITHUB_EVENT_NAME'] = "push"
    env['GITHUB_REPOSITORY'] = "test/test-repo"
    env['GITHUB_ACTOR'] = "test-user"
    env['GITHUB_SHA'] = "test-sha-123456"
    env['GITHUB_WORKSPACE'] = os.getcwd()
    
    # 运行main.py
    run_cmd = [sys.executable, "main.py"]
    print(f"执行命令: {' '.join(run_cmd)}")
    
    run_result = subprocess.run(
        run_cmd,
        env=env,
        capture_output=True,
        text=True,
        timeout=30
    )
    
    # 清理临时文件
    os.unlink(event_file_path)
    
    # 步骤5: 分析结果
    print(f"\n[步骤5/{session_id}] 分析执行结果")
    print(f"退出码: {run_result.returncode}")
    print(f"标准输出:\n{run_result.stdout}")
    print(f"标准错误:\n{run_result.stderr}")
    
    if run_result.returncode == 0:
        print(f"\n✅ GitHub Actions本地模拟调用成功！")
        success = True
    else:
        print(f"\n❌ GitHub Actions本地模拟调用失败！")
        success = False
    
    # 结束调试
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n=== 调试完成 ===")
    print(f"调试会话ID: {session_id}")
    print(f"总执行时长: {duration:.3f}秒")
    print(f"结束时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    
    return success

def main():
    """
    主函数
    """
    print("🎉 GitHub Actions本地调用调试工具")
    print("=" * 50)
    
    # 运行调试
    success = debug_github_call_local()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 本地调试成功！GitHub Actions调用流程正常。")
        sys.exit(0)
    else:
        print("❌ 本地调试失败！请查看详细日志分析问题。")
        sys.exit(1)

if __name__ == "__main__":
    main()