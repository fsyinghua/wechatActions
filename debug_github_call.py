#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本：模拟GitHub Actions环境，测试Docker Action的完整调用流程
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

def debug_github_call():
    """
    调试GitHub Actions调用流程
    """
    session_id = str(uuid.uuid4())
    start_time = time.time()
    
    print(f"=== 调试GitHub Actions调用流程 ===")
    print(f"调试会话ID: {session_id}")
    print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"当前目录: {os.getcwd()}")
    
    # 步骤1: 检查项目结构
    print(f"\n[步骤1/{session_id}] 检查项目结构")
    required_files = [
        "action.yml", "Dockerfile", "main.py", 
        "requirements.txt", "README.md"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ 找到文件: {file}")
        else:
            print(f"❌ 缺少文件: {file}")
            return False
    
    # 步骤2: 构建Docker镜像
    print(f"\n[步骤2/{session_id}] 构建Docker镜像")
    docker_image_name = f"wechat-actions-debug:{session_id[:8]}"
    
    build_cmd = [
        "docker", "build", 
        "-t", docker_image_name,
        "."
    ]
    
    print(f"执行命令: {' '.join(build_cmd)}")
    build_result = subprocess.run(
        build_cmd,
        capture_output=True,
        text=True,
        timeout=60
    )
    
    if build_result.returncode != 0:
        print(f"❌ Docker镜像构建失败")
        print(f"退出码: {build_result.returncode}")
        print(f"标准输出:\n{build_result.stdout}")
        print(f"标准错误:\n{build_result.stderr}")
        return False
    
    print(f"✅ Docker镜像构建成功: {docker_image_name}")
    
    # 步骤3: 准备模拟事件文件
    print(f"\n[步骤3/{session_id}] 准备模拟事件文件")
    
    event_data = get_mock_event_data()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(event_data, f, ensure_ascii=False, indent=2)
        event_file_path = f.name
    
    print(f"创建临时事件文件: {event_file_path}")
    print(f"事件数据: {json.dumps(event_data, ensure_ascii=False, indent=2)}")
    
    # 步骤4: 运行Docker容器，模拟GitHub Actions调用
    print(f"\n[步骤4/{session_id}] 运行Docker容器，模拟GitHub Actions调用")
    
    # 模拟GitHub Actions环境变量
    env_vars = [
        f"INPUT_WECHAT_WEBHOOK_URL={DEBUG_WEBHOOK_URL}",
        f"INPUT_EVENT_TYPES=push,pull_request,issues,release",
        f"GITHUB_EVENT_PATH=/github/workspace/event.json",
        f"GITHUB_EVENT_NAME=push",
        f"GITHUB_REPOSITORY=test/test-repo",
        f"GITHUB_ACTOR=test-user",
        f"GITHUB_SHA=test-sha-123456",
        f"GITHUB_WORKSPACE=/github/workspace",
    ]
    
    run_cmd = [
        "docker", "run",
        "--rm",
        "--name", f"wechat-actions-debug-{session_id[:8]}",
    ]
    
    # 添加环境变量
    for env_var in env_vars:
        run_cmd.extend(["-e", env_var])
    
    # 挂载事件文件
    run_cmd.extend([
        "-v", f"{event_file_path}:/github/workspace/event.json",
        docker_image_name
    ])
    
    print(f"执行命令: {' '.join(run_cmd)}")
    
    run_result = subprocess.run(
        run_cmd,
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
        print(f"\n✅ GitHub Actions调用模拟成功！")
        success = True
    else:
        print(f"\n❌ GitHub Actions调用模拟失败！")
        success = False
    
    # 步骤6: 清理Docker镜像
    print(f"\n[步骤6/{session_id}] 清理Docker镜像")
    cleanup_cmd = [
        "docker", "rmi", "-f", docker_image_name
    ]
    
    cleanup_result = subprocess.run(
        cleanup_cmd,
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if cleanup_result.returncode == 0:
        print(f"✅ Docker镜像清理成功")
    else:
        print(f"⚠️ Docker镜像清理失败")
        print(f"错误: {cleanup_result.stderr}")
    
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
    print("🎉 GitHub Actions调用调试工具")
    print("=" * 50)
    
    # 检查Docker是否可用
    docker_check = subprocess.run(
        ["docker", "--version"],
        capture_output=True,
        text=True
    )
    
    if docker_check.returncode != 0:
        print("❌ Docker未安装或不可用")
        print(f"错误: {docker_check.stderr}")
        return False
    
    print(f"✅ Docker版本: {docker_check.stdout.strip()}")
    
    # 运行调试
    success = debug_github_call()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 调试成功！GitHub Actions调用流程正常。")
        sys.exit(0)
    else:
        print("❌ 调试失败！请查看详细日志分析问题。")
        sys.exit(1)

if __name__ == "__main__":
    main()