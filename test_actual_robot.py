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
import time
import uuid
import traceback

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
    session_id = str(uuid.uuid4())
    start_time = time.time()
    
    print(f"=== 使用实际企业微信机器人测试通知发送 ===")
    print(f"测试会话ID: {session_id}")
    print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"测试Webhook URL: {TEST_WEBHOOK_URL}")
    
    # 创建临时文件保存事件数据
    event_file_path = None
    result = None
    
    try:
        # 步骤1: 创建临时事件文件
        print(f"\n[步骤1/{session_id}] 创建临时事件文件")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_events["push"], f, ensure_ascii=False, indent=2)
            event_file_path = f.name
        print(f"[步骤1/{session_id}] 临时事件文件创建成功: {event_file_path}")
        
        # 步骤2: 设置环境变量
        print(f"\n[步骤2/{session_id}] 设置环境变量")
        env = os.environ.copy()
        env['INPUT_WECHAT_WEBHOOK_URL'] = TEST_WEBHOOK_URL
        env['GITHUB_EVENT_PATH'] = event_file_path
        env['GITHUB_EVENT_NAME'] = "push"
        env['INPUT_EVENT_TYPES'] = "push"
        env['GITHUB_REPOSITORY'] = "test/test-repo"
        env['GITHUB_ACTOR'] = "test-user"
        env['GITHUB_SHA'] = "test-sha-123456"
        print(f"[步骤2/{session_id}] 环境变量设置完成")
        
        # 步骤3: 运行main.py脚本
        print(f"\n[步骤3/{session_id}] 运行main.py脚本")
        print(f"[步骤3/{session_id}] 执行命令: {[sys.executable, 'main.py']}")
        
        script_start = time.time()
        result = subprocess.run(
            [sys.executable, 'main.py'],
            env=env,
            capture_output=True,
            text=True,
            timeout=30
        )
        script_end = time.time()
        
        # 步骤4: 输出结果
        print(f"\n[步骤4/{session_id}] 分析执行结果")
        print(f"[步骤4/{session_id}] 脚本执行时长: {script_end - script_start:.3f}秒")
        print(f"[步骤4/{session_id}] 退出码: {result.returncode}")
        print(f"[步骤4/{session_id}] 标准输出:\n{result.stdout}")
        print(f"[步骤4/{session_id}] 标准错误:\n{result.stderr}")
        
        return result.returncode == 0
    
    except subprocess.TimeoutExpired:
        print(f"[错误/{session_id}] 脚本执行超时")
        return False
    
    except Exception as e:
        print(f"[错误/{session_id}] 测试过程中发生异常: {e}")
        print(f"[错误/{session_id}] 异常堆栈: {traceback.format_exc()}")
        return False
    
    finally:
        # 清理临时文件
        if event_file_path and os.path.exists(event_file_path):
            os.unlink(event_file_path)
            print(f"\n[清理/{session_id}] 临时文件已删除: {event_file_path}")
        
        # 记录总执行时长
        end_time = time.time()
        total_duration = end_time - start_time
        print(f"\n[结束/{session_id}] 测试完成")
        print(f"[结束/{session_id}] 总执行时长: {total_duration:.3f}秒")
        print(f"[结束/{session_id}] 结束时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")

def test_direct_request():
    """
    直接测试企业微信Webhook API
    """
    session_id = str(uuid.uuid4())
    start_time = time.time()
    
    print(f"\n=== 直接测试企业微信Webhook API ===")
    print(f"测试会话ID: {session_id}")
    print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"测试Webhook URL: {TEST_WEBHOOK_URL}")
    
    # 直接发送一个简单的文本消息
    test_message = {
        "msgtype": "text",
        "text": {
            "content": f"这是一条直接测试消息 - 来自GitHub企业微信通知模块\n测试会话ID: {session_id}\n测试时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}"
        }
    }
    
    print(f"\n[请求/{session_id}] 消息内容: {json.dumps(test_message, ensure_ascii=False, indent=2)}")
    
    response = None
    response_json = None
    status_code = None
    response_text = None
    error_msg = None
    
    try:
        import requests
        
        # 发送请求
        request_start = time.time()
        print(f"\n[请求/{session_id}] 开始发送HTTP POST请求")
        response = requests.post(
            TEST_WEBHOOK_URL, 
            json=test_message, 
            timeout=10,
            verify=True
        )
        request_end = time.time()
        request_duration = request_end - request_start
        
        # 获取响应信息
        status_code = response.status_code
        response_text = response.text
        
        print(f"\n[响应/{session_id}] HTTP响应状态码: {status_code}")
        print(f"[响应/{session_id}] 请求耗时: {request_duration:.3f}秒")
        print(f"[响应/{session_id}] HTTP响应头: {dict(response.headers)}")
        print(f"[响应/{session_id}] HTTP响应内容: {response_text}")
        
        # 解析响应
        try:
            response_json = response.json()
            print(f"[响应/{session_id}] 解析JSON响应: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
            
            if response_json.get("errcode") == 0:
                print(f"\n✅ [结果/{session_id}] 直接测试成功！")
                return True
            else:
                error_msg = f"企业微信API错误: {response_json.get('errmsg')}"
                print(f"❌ [结果/{session_id}] 直接测试失败: {error_msg}")
                return False
        except json.JSONDecodeError:
            print(f"\n✅ [结果/{session_id}] 直接测试成功！（非JSON响应）")
            return True
    
    except requests.exceptions.ConnectionError as e:
        error_msg = f"网络连接错误: {str(e)}"
        print(f"❌ [结果/{session_id}] 直接测试异常: {error_msg}")
        print(f"[错误/{session_id}] 异常类型: {type(e).__name__}")
        print(f"[错误/{session_id}] 异常堆栈: {traceback.format_exc()}")
        return False
    
    except requests.exceptions.Timeout as e:
        error_msg = f"请求超时: {str(e)}"
        print(f"❌ [结果/{session_id}] 直接测试异常: {error_msg}")
        print(f"[错误/{session_id}] 异常类型: {type(e).__name__}")
        print(f"[错误/{session_id}] 异常堆栈: {traceback.format_exc()}")
        return False
    
    except requests.exceptions.RequestException as e:
        error_msg = f"HTTP请求异常: {str(e)}"
        print(f"❌ [结果/{session_id}] 直接测试异常: {error_msg}")
        print(f"[错误/{session_id}] 异常类型: {type(e).__name__}")
        print(f"[错误/{session_id}] 异常堆栈: {traceback.format_exc()}")
        
        if hasattr(e, 'response') and e.response is not None:
            print(f"[错误/{session_id}] 异常响应状态码: {e.response.status_code}")
            print(f"[错误/{session_id}] 异常响应内容: {e.response.text}")
        return False
    
    except Exception as e:
        error_msg = f"未知异常: {str(e)}"
        print(f"❌ [结果/{session_id}] 直接测试异常: {error_msg}")
        print(f"[错误/{session_id}] 异常类型: {type(e).__name__}")
        print(f"[错误/{session_id}] 异常堆栈: {traceback.format_exc()}")
        return False
    
    finally:
        # 记录总执行时长
        end_time = time.time()
        total_duration = end_time - start_time
        print(f"\n[结束/{session_id}] 直接测试完成")
        print(f"[结束/{session_id}] 总执行时长: {total_duration:.3f}秒")
        print(f"[结束/{session_id}] 结束时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
        
        # 输出最终结果
        if error_msg:
            print(f"[最终/{session_id}] 测试失败，原因: {error_msg}")
        elif status_code == 200:
            print(f"[最终/{session_id}] 测试成功，HTTP状态码: {status_code}")
        else:
            print(f"[最终/{session_id}] 测试结果不确定，HTTP状态码: {status_code}")

def main():
    """
    主测试函数
    """
    session_id = str(uuid.uuid4())
    start_time = time.time()
    
    print("企业微信机器人实际测试")
    print("=" * 50)
    print(f"主测试会话ID: {session_id}")
    print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"测试Webhook URL: {TEST_WEBHOOK_URL}")
    
    # 测试结果记录
    test_results = {
        "total_tests": 0,
        "passed_tests": 0,
        "failed_tests": 0,
        "test_details": []
    }
    
    try:
        # 测试1：使用main.py脚本测试
        print("\n1. 使用main.py脚本测试")
        test_results["total_tests"] += 1
        script_result = test_actual_robot()
        
        if script_result:
            test_results["passed_tests"] += 1
            test_results["test_details"].append({"name": "脚本测试", "result": "✅ 成功"})
        else:
            test_results["failed_tests"] += 1
            test_results["test_details"].append({"name": "脚本测试", "result": "❌ 失败"})
        
        # 测试2：直接测试Webhook API
        print("\n2. 直接测试Webhook API")
        test_results["total_tests"] += 1
        direct_result = test_direct_request()
        
        if direct_result:
            test_results["passed_tests"] += 1
            test_results["test_details"].append({"name": "直接API测试", "result": "✅ 成功"})
        else:
            test_results["failed_tests"] += 1
            test_results["test_details"].append({"name": "直接API测试", "result": "❌ 失败"})
        
        # 输出汇总结果
        print("\n" + "=" * 50)
        print("测试完成 - 汇总结果")
        print("=" * 50)
        print(f"主测试会话ID: {session_id}")
        print(f"总测试数: {test_results['total_tests']}")
        print(f"通过测试数: {test_results['passed_tests']}")
        print(f"失败测试数: {test_results['failed_tests']}")
        
        print("\n测试详情:")
        for test in test_results["test_details"]:
            print(f"  - {test['name']}: {test['result']}")
        
        # 计算总执行时长
        end_time = time.time()
        total_duration = end_time - start_time
        print(f"\n总执行时长: {total_duration:.3f}秒")
        print(f"结束时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
        
        # 最终结论
        print("\n最终结论:")
        if test_results["passed_tests"] == test_results["total_tests"]:
            print("✅ 所有测试通过！企业微信通知功能正常工作。")
            sys.exit(0)
        elif test_results["passed_tests"] > 0:
            print("⚠️  部分测试通过，请查看详细日志分析问题。")
            sys.exit(1)
        else:
            print("❌ 所有测试失败，请查看详细日志分析问题。")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 测试过程中发生严重异常: {e}")
        print(f"异常堆栈: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()