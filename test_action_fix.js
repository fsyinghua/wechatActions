// 本地测试脚本，验证我们的 Action 修复是否正确
// 模拟 GitHub Actions 环境，测试 Node.js 入口文件

const { execSync } = require('child_process');
const fs = require('fs');

// 设置测试环境变量
process.env.INPUT_WECHAT_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c473353f-846b-4c2c-bea4-ae2644e4d955";
process.env.INPUT_EVENT_TYPES = "push,pull_request,issues,release";

// 模拟 GitHub 事件数据
const mockEventData = {
  "event_name": "push",
  "repository": {
    "full_name": "fsyinghua/test-repo",
    "html_url": "https://github.com/fsyinghua/test-repo"
  },
  "pusher": {
    "name": "test-user"
  },
  "commits": [
    {
      "message": "Test commit",
      "committer": {
        "name": "test-committer"
      },
      "id": "test1234567890"
    }
  ],
  "compare": "https://github.com/fsyinghua/test-repo/compare/test",
  "ref": "refs/heads/main"
};

// 创建临时事件文件
const tempEventPath = './temp_event.json';
fs.writeFileSync(tempEventPath, JSON.stringify(mockEventData, null, 2));
process.env.GITHUB_EVENT_PATH = tempEventPath;
process.env.GITHUB_EVENT_NAME = "push";

console.log('🔧 开始测试 Action 修复...');

// 1. 检查当前目录结构
console.log('📁 当前目录:', process.cwd());
console.log('📄 文件列表:', fs.readdirSync(process.cwd()));

// 2. 检查 action.yml 文件
if (fs.existsSync('./action.yml')) {
  const actionYml = fs.readFileSync('./action.yml', 'utf8');
  console.log('✅ action.yml 内容:');
  console.log(actionYml);
} else {
  console.error('❌ 未找到 action.yml 文件');
  process.exit(1);
}

// 3. 检查 index.js 文件
if (fs.existsSync('./index.js')) {
  const indexJs = fs.readFileSync('./index.js', 'utf8');
  console.log('✅ index.js 内容:');
  console.log(indexJs);
} else {
  console.error('❌ 未找到 index.js 文件');
  process.exit(1);
}

// 4. 检查 main.py 文件
if (fs.existsSync('./main.py')) {
  console.log('✅ main.py 文件存在');
} else {
  console.error('❌ 未找到 main.py 文件');
  process.exit(1);
}

// 5. 测试 Python 环境
console.log('🐍 测试 Python 环境...');
try {
  const pythonVersion = execSync('python --version', { encoding: 'utf8' }).trim();
  console.log('✅ Python 版本:', pythonVersion);
  
  const pipVersion = execSync('pip --version', { encoding: 'utf8' }).trim();
  console.log('✅ Pip 版本:', pipVersion);
} catch (error) {
  console.error('⚠️  Python 环境测试失败:', error.message);
  console.error('⚠️  这可能是因为本地没有安装 Python，或者 Python 不在 PATH 中');
  console.error('⚠️  但在 GitHub Actions 环境中，我们会自动安装 Python');
}

// 6. 测试直接运行 main.py
console.log('🚀 测试直接运行 main.py...');
try {
  execSync('python main.py', { stdio: 'inherit' });
  console.log('✅ main.py 直接运行成功！');
} catch (error) {
  console.error('⚠️  main.py 直接运行失败:', error.message);
  console.error('⚠️  这可能是因为缺少必要的环境变量，或者本地没有安装依赖');
}

// 清理临时文件
fs.unlinkSync(tempEventPath);

console.log('🎉 Action 修复测试完成！');
console.log('📋 修复总结:');
console.log('1. 将 action.yml 中的 using: python3 改为 using: node20');
console.log('2. 创建了 index.js 作为入口文件，负责设置 Python 环境并执行 main.py');
console.log('3. index.js 会自动安装 Python 3.10 和依赖包');
console.log('4. 在 GitHub Actions 环境中，这个修复应该能解决 "using: python3 is not supported" 错误');

// 提示网络连接问题
console.log('\n⚠️  注意: 由于网络连接不稳定，我们无法将修改推送到 GitHub 进行实际测试');
console.log('⚠️  请在网络连接恢复后，手动执行 git push origin main 命令来推送修改');
console.log('⚠️  或者，您可以在 GitHub Actions 页面手动触发工作流来测试修复');
