#!/bin/bash

set -e

echo "==============================="
echo "🚀 RAG实训报告生成系统一键部署"
echo "==============================="

# 1. 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到python3，请先安装Python 3.8+"
    exit 1
fi

# 2. 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 未检测到pip3，请先安装pip"
    exit 1
fi

# 3. 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi
source venv/bin/activate

# 4. 升级pip
pip install --upgrade pip

# 5. 安装依赖
if [ -f requirements.txt ]; then
    echo "📦 安装requirements.txt依赖..."
    pip install -r requirements.txt
else
    echo "⚠️ 未找到requirements.txt，安装核心依赖..."
    pip install fastapi uvicorn python-multipart aiofiles python-dotenv chromadb openai
fi

# 6. 检查.env文件
if [ ! -f ".env" ]; then
    echo "🔧 创建.env文件..."
    cat > .env << EOF
AI_API_KEY=sk-442562cd6b6b4b2896ebdac8ce8d047e
AI_API_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AI_MODEL_NAME=qwen-plus
AI_EMBEDDING_MODEL=text-embedding-v3
EOF
else
    echo "✅ .env文件已存在"
fi

# 7. 创建必要目录
for d in logs uploads temp chroma_db static templates; do
    mkdir -p $d
    chmod 755 $d
done

# 8. 检查端口占用
if lsof -i:8000 | grep LISTEN; then
    echo "🛑 端口8000已被占用，尝试关闭旧进程..."
    fuser -k 8000/tcp || true
fi

# 9. 启动服务
nohup venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000 --reload > logs/app.log 2>&1 &
sleep 5

# 10. 检查服务状态
if pgrep -f "uvicorn app:app" > /dev/null; then
    echo "✅ 服务已启动，监听端口8000"
else
    echo "❌ 服务启动失败，请检查logs/app.log"
    tail -n 30 logs/app.log
    exit 1
fi

# 11. 健康检查
if curl -s http://localhost:8000/health | grep 'healthy' > /dev/null; then
    echo "🎉 部署成功！访问: http://<你的服务器IP>:8000"
else
    echo "⚠️ 健康检查未通过，请检查logs/app.log"
    tail -n 30 logs/app.log
fi

echo "==============================="
echo "📋 日志查看: tail -f logs/app.log"
echo "===============================" 