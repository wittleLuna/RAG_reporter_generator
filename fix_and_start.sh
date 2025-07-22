#!/bin/bash

echo "=== 修复并启动应用 ==="

# 进入项目目录
cd /www/wwwroot/report-generator

# 激活虚拟环境
source /www/server/pyporject_evn/report-generator_venv/bin/activate

# 停止现有进程
echo "停止现有进程..."
pkill -f uvicorn 2>/dev/null || true
pkill -f uwsgi 2>/dev/null || true
sleep 2

# 修复权限问题
echo "修复权限..."
# 使用当前用户权限创建目录
mkdir -p logs uploads temp chroma_db static templates 2>/dev/null || true

# 设置基本权限（不使用www用户，避免权限问题）
chmod -R 755 . 2>/dev/null || true
chmod -R 777 logs uploads temp 2>/dev/null || true

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "创建环境变量文件..."
    cat > .env << EOF
# 千问API配置
AI_API_URL=https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
AI_MODEL_NAME=qwen-turbo
AI_API_KEY=sk-442562cd6b6b4b2896ebdac8ce8d047e

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=False

# ChromaDB配置
CHROMA_PERSIST_DIR=./chroma_db
EOF
fi

# 测试应用
echo "测试应用..."
python3 test_app.py

if [ $? -eq 0 ]; then
    echo "✅ 应用测试通过，开始启动..."
    
    # 启动应用（后台运行）
    nohup python3 -c "
import uvicorn
from app import app
print('应用启动中...')
uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')
" > logs/app.log 2>&1 &
    
    # 等待启动
    sleep 5
    
    # 检查进程
    echo "检查进程状态..."
    ps aux | grep uvicorn | grep -v grep
    
    # 检查端口
    echo "检查端口状态..."
    netstat -tlnp | grep 8000
    
    # 测试访问
    echo "测试本地访问..."
    curl -s http://localhost:8000/health || echo "本地访问失败"
    
    echo "启动完成！"
    echo "应用地址: http://your-server-ip:8000"
    echo "日志文件: logs/app.log"
else
    echo "❌ 应用测试失败，请检查错误信息"
    exit 1
fi 