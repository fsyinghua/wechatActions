import os
import sys
import json
import requests
import time
import uuid
import traceback

def get_input(name, required=False, default=None):
    """
    获取GitHub Action输入参数
    从环境变量中读取，环境变量格式为 INPUT_参数名大写
    """
    start_time = time.time()
    session_id = str(uuid.uuid4())
    env_var_name = f'INPUT_{name.upper()}'
    
    print(f'::debug::[{session_id}] 开始执行 get_input 函数')
    print(f'::debug::[{session_id}] 参数: name={name}, required={required}, default={default}')
    print(f'::debug::[{session_id}] 环境变量名: {env_var_name}')
    
    value = os.getenv(env_var_name, default)
    print(f'::debug::[{session_id}] 环境变量值: {value}')
    
    if required and not value:
        error_msg = f'Missing required input: {name}'
        print(f'::error::[{session_id}] {error_msg}')
        print(f'::debug::[{session_id}] 执行时间: {time.time() - start_time:.3f}s')
        sys.exit(1)
    
    print(f'::debug::[{session_id}] 返回值: {value}')
    print(f'::debug::[{session_id}] 执行时间: {time.time() - start_time:.3f}s')
    print(f'::debug::[{session_id}] 结束执行 get_input 函数')
    return value

def send_wechat_message(webhook_url, message):
    """
    发送企业微信通知
    :param webhook_url: 企业微信机器人Webhook URL
    :param message: 通知消息内容
    :return: 是否发送成功
    """
    start_time = time.time()
    session_id = str(uuid.uuid4())
    parent_session = os.getenv('CURRENT_SESSION_ID', 'main')
    
    print(f'::debug::[{session_id}] 开始执行 send_wechat_message 函数')
    print(f'::debug::[{session_id}] 上一级调用会话ID: {parent_session}')
    print(f'::debug::[{session_id}] 参数: webhook_url={webhook_url[:50]}...(已截断), message_type={message.get("msgtype")}')
    print(f'::debug::[{session_id}] 消息内容摘要: {json.dumps(message, ensure_ascii=False)[:100]}...(已截断)')
    
    success = False
    error_msg = None
    status_code = None
    response_content = None
    
    try:
        # 发送请求
        print(f'::debug::[{session_id}] 开始发送HTTP请求')
        response = requests.post(webhook_url, json=message, timeout=10, verify=True)
        
        # 记录响应信息
        status_code = response.status_code
        response_content = response.text
        
        print(f'::debug::[{session_id}] HTTP响应状态码: {status_code}')
        print(f'::debug::[{session_id}] HTTP响应头: {dict(response.headers)}')
        print(f'::debug::[{session_id}] HTTP响应内容: {response_content}')
        
        # 检查响应状态
        response.raise_for_status()
        
        # 解析响应内容
        try:
            response_json = response.json()
            print(f'::debug::[{session_id}] JSON响应: {json.dumps(response_json, ensure_ascii=False)}')
            if response_json.get('errcode') == 0:
                success = True
                print(f'::info::[{session_id}] 企业微信通知发送成功')
            else:
                success = False
                error_msg = f'企业微信API错误: {response_json.get("errmsg")}'
                print(f'::error::[{session_id}] {error_msg}')
        except json.JSONDecodeError:
            success = True
            print(f'::info::[{session_id}] 企业微信通知发送成功（非JSON响应）')
            
    except requests.exceptions.RequestException as e:
        success = False
        error_msg = f'请求异常: {str(e)}'
        print(f'::error::[{session_id}] {error_msg}')
        print(f'::debug::[{session_id}] 异常类型: {type(e).__name__}')
        print(f'::debug::[{session_id}] 异常堆栈: {traceback.format_exc()}')
        
        if hasattr(e, 'response') and e.response is not None:
            status_code = e.response.status_code
            response_content = e.response.text
            print(f'::debug::[{session_id}] 异常响应状态码: {status_code}')
            print(f'::debug::[{session_id}] 异常响应内容: {response_content}')
    except Exception as e:
        success = False
        error_msg = f'未知异常: {str(e)}'
        print(f'::error::[{session_id}] {error_msg}')
        print(f'::debug::[{session_id}] 异常类型: {type(e).__name__}')
        print(f'::debug::[{session_id}] 异常堆栈: {traceback.format_exc()}')
    
    # 记录执行时间
    duration = time.time() - start_time
    print(f'::debug::[{session_id}] 执行时长: {duration:.3f}s')
    
    # 输出执行结果摘要
    result_msg = f'发送结果: {"成功" if success else "失败"}'
    if not success:
        result_msg += f', 错误原因: {error_msg}'
    if status_code:
        result_msg += f', HTTP状态码: {status_code}'
    print(f'::info::[{session_id}] {result_msg}')
    
    print(f'::debug::[{session_id}] 结束执行 send_wechat_message 函数')
    return success

def generate_push_message(event_data):
    """
    生成Push事件通知内容
    :param event_data: GitHub事件数据
    :return: 企业微信通知消息
    """
    repo = event_data['repository']
    pusher = event_data['pusher']
    commits = event_data['commits']
    compare_url = event_data['compare']
    
    # 获取分支名称
    branch = event_data['ref'].split('/')[-1]
    
    return {
        'msgtype': 'markdown',
        'markdown': {
            'content': f"""## 📢 GitHub 代码推送通知

**仓库**: [{repo['full_name']}]({repo['html_url']})
**操作**: 代码推送
**分支**: {branch}
**作者**: {pusher['name']}
**提交数**: {len(commits)} 个
**查看对比**: [点击查看]({compare_url})

**最新提交**:
- **提交信息**: {commits[0]['message'].splitlines()[0]}
- **提交者**: {commits[0]['committer']['name']}
- **提交哈希**: {commits[0]['id'][:7]}
            """
        }
    }

def generate_pull_request_message(event_data):
    """
    生成Pull Request事件通知内容
    :param event_data: GitHub事件数据
    :return: 企业微信通知消息
    """
    repo = event_data['repository']
    pr = event_data['pull_request']
    action = event_data['action']
    sender = event_data['sender']
    
    # 生成操作文本
    action_text_map = {
        'opened': '创建了',
        'synchronize': '更新了',
        'closed': '关闭了' if not pr['merged'] else '合并了',
        'reopened': '重新打开了'
    }
    action_text = action_text_map.get(action, f'{action}了')
    
    return {
        'msgtype': 'markdown',
        'markdown': {
            'content': f"""## 📢 GitHub Pull Request 通知

**仓库**: [{repo['full_name']}]({repo['html_url']})
**操作**: {sender['login']} {action_text} Pull Request
**标题**: [{pr['title']}]({pr['html_url']})
**编号**: #{pr['number']}
**状态**: {pr['state']}
**源分支**: {pr['head']['ref']} → 目标分支: {pr['base']['ref']}
**作者**: {pr['user']['login']}
            """
        }
    }

def generate_issues_message(event_data):
    """
    生成Issues事件通知内容
    :param event_data: GitHub事件数据
    :return: 企业微信通知消息
    """
    repo = event_data['repository']
    issue = event_data['issue']
    action = event_data['action']
    sender = event_data['sender']
    
    # 生成操作文本
    action_text_map = {
        'opened': '创建了',
        'edited': '编辑了',
        'closed': '关闭了',
        'reopened': '重新打开了',
        'labeled': '添加了标签',
        'unlabeled': '移除了标签'
    }
    action_text = action_text_map.get(action, f'{action}了')
    
    return {
        'msgtype': 'markdown',
        'markdown': {
            'content': f"""## 📢 GitHub Issues 通知

**仓库**: [{repo['full_name']}]({repo['html_url']})
**操作**: {sender['login']} {action_text} Issue
**标题**: [{issue['title']}]({issue['html_url']})
**编号**: #{issue['number']}
**状态**: {issue['state']}
**作者**: {issue['user']['login']}
            """
        }
    }

def generate_release_message(event_data):
    """
    生成Release事件通知内容
    :param event_data: GitHub事件数据
    :return: 企业微信通知消息
    """
    repo = event_data['repository']
    release = event_data['release']
    action = event_data['action']
    sender = event_data['sender']
    
    # 生成操作文本
    action_text_map = {
        'published': '发布了',
        'created': '创建了',
        'edited': '编辑了',
        'deleted': '删除了',
        'prereleased': '发布了预发布版本',
        'released': '正式发布了'
    }
    action_text = action_text_map.get(action, f'{action}了')
    
    return {
        'msgtype': 'markdown',
        'markdown': {
            'content': f"""## 📢 GitHub Release 通知

**仓库**: [{repo['full_name']}]({repo['html_url']})
**操作**: {sender['login']} {action_text} Release
**名称**: [{release['name'] or release['tag_name']}]({release['html_url']})
**版本**: {release['tag_name']}
**类型**: {'预发布' if release['prerelease'] else '正式发布'}
            """
        }
    }

def main():
    """
    主函数
    """
    start_time = time.time()
    session_id = str(uuid.uuid4())
    
    # 设置当前会话ID环境变量，供子函数使用
    os.environ['CURRENT_SESSION_ID'] = session_id
    
    print(f'::debug::[{session_id}] 开始执行 main 函数')
    print(f'::debug::[{session_id}] 进程ID: {os.getpid()}')
    print(f'::debug::[{session_id}] 开始时间: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))}')
    
    # 获取环境信息
    github_event_name = os.getenv('GITHUB_EVENT_NAME')
    github_repository = os.getenv('GITHUB_REPOSITORY')
    github_actor = os.getenv('GITHUB_ACTOR')
    github_sha = os.getenv('GITHUB_SHA')
    
    print(f'::debug::[{session_id}] GitHub环境信息:')
    print(f'::debug::[{session_id}]   事件名称: {github_event_name}')
    print(f'::debug::[{session_id}]   仓库名称: {github_repository}')
    print(f'::debug::[{session_id}]   操作人: {github_actor}')
    print(f'::debug::[{session_id}]   提交SHA: {github_sha}')
    
    try:
        # 1. 获取输入参数
        print(f'::debug::[{session_id}] 步骤1: 获取输入参数')
        webhook_url = get_input('wechat_webhook_url', required=True)
        event_types = get_input('event_types', default='push,pull_request,issues,release').split(',')
        print(f'::debug::[{session_id}] 输入参数获取完成: webhook_url={webhook_url[:50]}..., event_types={event_types}')
        
        # 2. 获取GitHub事件信息
        print(f'::debug::[{session_id}] 步骤2: 获取GitHub事件信息')
        event_path = os.getenv('GITHUB_EVENT_PATH')
        if not event_path:
            print(f'::error::[{session_id}] GITHUB_EVENT_PATH 环境变量未找到')
            sys.exit(1)
        
        print(f'::debug::[{session_id}] 事件文件路径: {event_path}')
        
        try:
            with open(event_path, 'r') as f:
                event_data = json.load(f)
            print(f'::debug::[{session_id}] 事件数据加载成功，数据大小: {len(json.dumps(event_data))} 字节')
        except json.JSONDecodeError as e:
            print(f'::error::[{session_id}] 解析GitHub事件数据失败: {e}')
            print(f'::debug::[{session_id}] 异常堆栈: {traceback.format_exc()}')
            sys.exit(1)
        
        if not github_event_name:
            print(f'::error::[{session_id}] GITHUB_EVENT_NAME 环境变量未找到')
            sys.exit(1)
        
        print(f'::info::[{session_id}] 当前事件类型: {github_event_name}')
        print(f'::info::[{session_id}] 配置的通知事件类型: {event_types}')
        
        # 3. 检查是否需要处理该事件类型
        print(f'::debug::[{session_id}] 步骤3: 检查事件类型是否需要处理')
        if github_event_name not in event_types:
            print(f'::info::[{session_id}] 事件类型 {github_event_name} 不在配置的通知列表中，跳过通知')
            return
        
        # 4. 根据事件类型生成通知内容
        print(f'::debug::[{session_id}] 步骤4: 生成通知内容')
        message = None
        
        if github_event_name == 'push':
            print(f'::debug::[{session_id}] 处理 push 事件')
            message = generate_push_message(event_data)
        elif github_event_name == 'pull_request':
            print(f'::debug::[{session_id}] 处理 pull_request 事件')
            message = generate_pull_request_message(event_data)
        elif github_event_name == 'issues':
            print(f'::debug::[{session_id}] 处理 issues 事件')
            message = generate_issues_message(event_data)
        elif github_event_name == 'release':
            print(f'::debug::[{session_id}] 处理 release 事件')
            message = generate_release_message(event_data)
        else:
            print(f'::warning::[{session_id}] 未处理的事件类型: {github_event_name}')
            return
        
        if message:
            # 5. 发送通知
            print(f'::debug::[{session_id}] 步骤5: 发送企业微信通知')
            print(f'::debug::[{session_id}] 调用 send_wechat_message 函数')
            send_result = send_wechat_message(webhook_url, message)
            print(f'::debug::[{session_id}] send_wechat_message 返回结果: {send_result}')
        else:
            print(f'::warning::[{session_id}] 未生成通知消息')
            
    except KeyboardInterrupt:
        print(f'::warning::[{session_id}] 程序被用户中断')
        sys.exit(1)
    except Exception as e:
        print(f'::error::[{session_id}] 主函数执行异常')
        print(f'::error::[{session_id}] 异常类型: {type(e).__name__}')
        print(f'::error::[{session_id}] 异常信息: {str(e)}')
        print(f'::debug::[{session_id}] 异常堆栈: {traceback.format_exc()}')
        sys.exit(1)
    finally:
        # 计算执行时长
        end_time = time.time()
        duration = end_time - start_time
        
        print(f'::debug::[{session_id}] 结束执行 main 函数')
        print(f'::debug::[{session_id}] 结束时间: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))}')
        print(f'::debug::[{session_id}] 总执行时长: {duration:.3f}s')
        print(f'::debug::[{session_id}] 会话ID: {session_id}')
        print(f'::info::[{session_id}] 程序执行完成')

if __name__ == '__main__':
    main()