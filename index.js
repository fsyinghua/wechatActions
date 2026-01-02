// GitHub Action 入口文件
// 使用 Node.js 运行器来设置 Python 环境并执行 Python 脚本

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 设置 Python 版本
const PYTHON_VERSION = '3.10';

async function run() {
  try {
    console.log('🔧 开始设置 GitHub 企业微信通知 Action...');
    
    // 1. 检查当前目录结构
    console.log('📁 当前目录:', process.cwd());
    console.log('📄 文件列表:', fs.readdirSync(process.cwd()));
    
    // 2. 安装 Python
    console.log(`🐍 安装 Python ${PYTHON_VERSION}...`);
    execSync('apt-get update -y', { stdio: 'inherit' });
    execSync(`apt-get install -y python${PYTHON_VERSION} python3-pip`, { stdio: 'inherit' });
    
    // 3. 验证 Python 版本
    const pythonVersion = execSync(`python${PYTHON_VERSION} --version`, { encoding: 'utf8' }).trim();
    console.log('✅ Python 版本:', pythonVersion);
    
    // 4. 安装依赖
    console.log('📦 安装依赖包...');
    if (fs.existsSync('requirements.txt')) {
      execSync(`python${PYTHON_VERSION} -m pip install -r requirements.txt`, { stdio: 'inherit' });
    } else {
      console.log('⚠️  未找到 requirements.txt 文件，跳过依赖安装');
    }
    
    // 5. 执行 Python 主脚本
    console.log('🚀 执行 Python 主脚本...');
    execSync(`python${PYTHON_VERSION} main.py`, { stdio: 'inherit' });
    
    console.log('🎉 GitHub 企业微信通知 Action 执行完成！');
  } catch (error) {
    console.error('❌ Action 执行失败:', error.message);
    process.exit(1);
  }
}

run();