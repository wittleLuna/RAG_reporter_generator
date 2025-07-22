#!/bin/bash

echo "🔍 服务调试诊断"
echo "==============================="

# 1. 检查进程状态
echo "📋 检查uvicorn进程..."
ps aux | grep uvicorn | grep -v grep

# 2. 检查端口监听
echo ""
echo "🔌 检查端口监听状态..."
netstat -tlnp | grep :8000

# 3. 检查服务日志
echo ""
echo "📝 查看最近的服务日志..."
if [ -f "logs/app.log" ]; then
    echo "最后20行日志："
    tail -n 20 logs/app.log
else
    echo "❌ 日志文件不存在"
fi

# 4. 检查环境变量
echo ""
echo "🔧 检查环境变量..."
if [ -f ".env" ]; then
    echo "环境变量文件内容："
    cat .env
else
    echo "❌ .env文件不存在"
fi

# 5. 检查Python环境
echo ""
echo "🐍 检查Python环境..."
which python3
python3 --version
which pip3
pip3 --version

# 6. 检查虚拟环境
echo ""
echo "📦 检查虚拟环境..."
if [ -d "venv" ]; then
    echo "虚拟环境存在"
    source venv/bin/activate
    which python
    pip list | grep -E "(fastapi|uvicorn|openai|chromadb)"
else
    echo "❌ 虚拟环境不存在"
fi

# 7. 测试本地连接
echo ""
echo "🌐 测试本地连接..."
curl -v http://localhost:8000/health 2>&1 | head -20

# 8. 检查文件权限
echo ""
echo "📁 检查目录权限..."
ls -la | grep -E "(logs|uploads|temp|chroma_db)"

# 9. 检查依赖安装
echo ""
echo "📦 检查关键依赖..."
pip list | grep -E "(fastapi|uvicorn|openai|chromadb|aiofiles|python-dotenv)" || echo "❌ 依赖检查失败"

echo ""
echo "==============================="
echo "🔧 如果服务未启动，请运行："
echo "source venv/bin/activate"
echo "nohup uvicorn app:app --host 0.0.0.0 --port 8000 --reload > logs/app.log 2>&1 &"
echo ""
echo "📝 实时查看日志："
echo "tail -f logs/app.log" 