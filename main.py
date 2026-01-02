import os
import sys
import json
import requests

def get_input(name, required=False, default=None):
    """
    获取GitHub Action输入参数
    从环境变量中读取，环境变量格式为 INPUT_参数名大写
    """
    value = os.getenv(f'INPUT_{name.upper()}', default)
    if required and not value:
        print(f'::error::Missing required input: {name}')
        sys.exit(1)
    return value

def send_wechat_message(webhook_url, message):
    """
    发送企业微信通知
    :param webhook_url: 企业微信机器人Webhook URL
    :param message: 通知消息内容
    :return: 是否发送成功
    """
    try:
        response = requests.post(webhook_url, json=message, timeout=10)
        response.raise_for_status()
        print(f'::info::企业微信通知发送成功')
        return True
    except requests.exceptions.RequestException as e:
        print(f'::error::企业微信通知发送失败: {e}')
        if hasattr(e, 'response') and e.response is not None:
            print(f'::error::响应状态: {e.response.status_code}')
            print(f'::error::响应内容: {e.response.text}')
        return False

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
    # 获取输入参数
    webhook_url = get_input('wechat_webhook_url', required=True)
    event_types = get_input('event_types', default='push,pull_request,issues,release').split(',')
    
    # 获取GitHub事件信息
    event_path = os.getenv('GITHUB_EVENT_PATH')
    if not event_path:
        print('::error::GITHUB_EVENT_PATH not found')
        sys.exit(1)
    
    try:
        with open(event_path, 'r') as f:
            event_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f'::error::解析GitHub事件数据失败: {e}')
        sys.exit(1)
    
    event_name = os.getenv('GITHUB_EVENT_NAME')
    if not event_name:
        print('::error::GITHUB_EVENT_NAME not found')
        sys.exit(1)
    
    print(f'::info::当前事件类型: {event_name}')
    print(f'::info::配置的通知事件类型: {event_types}')
    
    # 检查是否需要处理该事件类型
    if event_name not in event_types:
        print(f'::info::事件类型 {event_name} 不在配置的通知列表中，跳过通知')
        return
    
    # 根据事件类型生成通知内容
    message = None
    if event_name == 'push':
        message = generate_push_message(event_data)
    elif event_name == 'pull_request':
        message = generate_pull_request_message(event_data)
    elif event_name == 'issues':
        message = generate_issues_message(event_data)
    elif event_name == 'release':
        message = generate_release_message(event_data)
    else:
        print(f'::warning::未处理的事件类型: {event_name}')
        return
    
    if message:
        send_wechat_message(webhook_url, message)

if __name__ == '__main__':
    main()