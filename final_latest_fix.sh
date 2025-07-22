#!/bin/bash

echo "🚀 开始最终修复 - 使用最新版本OpenAI客户端"
echo "================================================"

# 切换到项目目录
cd /www/wwwroot/report-generator

# 激活虚拟环境
echo "📋 激活虚拟环境..."
source /www/server/pyporject_evn/report-generator_venv/bin/activate

# 停止现有进程
echo "🛑 停止现有进程..."
pkill -f uvicorn || true

# 安装最新版本OpenAI客户端
echo "📦 安装最新版本OpenAI客户端..."
pip install --upgrade openai

# 检查环境变量
echo "🔧 检查环境变量配置..."
if [ ! -f ".env" ]; then
    echo "创建.env文件..."
    cat > .env << EOF
AI_API_KEY=sk-442562cd6b6b4b2896ebdac8ce8d047e
AI_API_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AI_MODEL_NAME=qwen-plus
AI_EMBEDDING_MODEL=text-embedding-v3
EOF
else
    echo ".env文件已存在"
fi

# 创建必要目录
echo "📁 创建必要目录..."
mkdir -p logs uploads temp chroma_db static templates
chmod 755 logs uploads temp chroma_db static templates

# 安装依赖
echo "📦 安装依赖..."
pip install fastapi uvicorn python-multipart aiofiles python-dotenv chromadb

# 测试API连接
echo "🌐 测试API连接..."
python3 test_example_code.py
if [ $? -eq 0 ]; then
    echo "✅ API连接测试成功"
else
    echo "❌ API连接测试失败"
    exit 1
fi

# 测试最新版本AI服务
echo "🤖 测试最新版本AI服务..."
python3 test_latest_ai.py
if [ $? -eq 0 ]; then
    echo "✅ AI服务测试成功"
else
    echo "❌ AI服务测试失败"
    exit 1
fi

# 启动应用
echo "🚀 启动应用..."
nohup uvicorn app:app --host 0.0.0.0 --port 8000 --reload > logs/app.log 2>&1 &

# 等待应用启动
sleep 5

# 检查进程
echo "🔍 检查应用状态..."
if pgrep -f uvicorn > /dev/null; then
    echo "✅ 应用启动成功"
else
    echo "❌ 应用启动失败"
    echo "查看日志:"
    tail -n 20 logs/app.log
    exit 1
fi

# 检查端口
echo "🔌 检查端口状态..."
if netstat -tlnp | grep :8000 > /dev/null; then
    echo "✅ 端口8000监听正常"
else
    echo "❌ 端口8000未监听"
    exit 1
fi

# 测试本地访问
echo "🌐 测试本地访问..."
curl -s http://localhost:8000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ 本地访问测试成功"
else
    echo "❌ 本地访问测试失败"
fi

echo ""
echo "🎉 修复完成！"
echo "================================================"
echo "📋 修复内容:"
echo "  ✅ 安装最新版本OpenAI客户端"
echo "  ✅ 配置环境变量"
echo "  ✅ 创建必要目录"
echo "  ✅ 安装依赖"
echo "  ✅ 测试API连接"
echo "  ✅ 测试AI服务"
echo "  ✅ 启动应用"
echo ""
echo "🌐 应用访问地址: http://your-server-ip:8000"
echo "📊 健康检查: http://your-server-ip:8000/health"
echo "📝 查看日志: tail -f logs/app.log"
echo ""
echo "🔧 如果遇到问题，请检查:"
echo "  1. 环境变量配置 (.env文件)"
echo "  2. 依赖安装 (pip list)"
echo "  3. 应用日志 (logs/app.log)"
echo "  4. 端口占用 (netstat -tlnp | grep 8000)" 