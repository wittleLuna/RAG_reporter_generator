#!/bin/bash

echo "=== 修复AI服务问题 ==="

# 进入项目目录
cd /www/wwwroot/report-generator

# 激活虚拟环境
source /www/server/pyporject_evn/report-generator_venv/bin/activate

# 停止现有进程
echo "停止现有进程..."
pkill -f uvicorn 2>/dev/null || true
sleep 2

# 检查并安装依赖
echo "检查依赖..."
pip install openai==1.3.0 python-dotenv python-docx docxtpl

# 确保环境变量文件正确
echo "检查环境变量配置..."
if [ ! -f ".env" ]; then
    echo "创建环境变量文件..."
    cat > .env << EOF
# 千问API配置
AI_API_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AI_MODEL_NAME=qwen-plus
AI_API_KEY=sk-442562cd6b6b4b2896ebdac8ce8d047e
AI_EMBEDDING_MODEL=text-embedding-v3

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=False

# ChromaDB配置
CHROMA_PERSIST_DIR=./chroma_db
EOF
else
    echo "更新环境变量文件..."
    # 确保API URL正确
    sed -i 's|AI_API_URL=.*|AI_API_URL=https://dashscope.aliyuncs.com/compatible-mode/v1|' .env
    sed -i 's|AI_MODEL_NAME=.*|AI_MODEL_NAME=qwen-plus|' .env
    # 添加embedding模型配置
    if ! grep -q "AI_EMBEDDING_MODEL" .env; then
        echo "AI_EMBEDDING_MODEL=text-embedding-v3" >> .env
    fi
fi

# 创建必要的目录
echo "创建必要目录..."
mkdir -p logs uploads temp chroma_db static templates 2>/dev/null || true
chmod -R 755 . 2>/dev/null || true
chmod -R 777 logs uploads temp 2>/dev/null || true

# 测试API
echo "测试API..."
python3 test_example_code.py

if [ $? -eq 0 ]; then
    echo "✅ API测试通过"
else
    echo "❌ API测试失败，但继续修复..."
fi

# 测试AI服务
echo "测试AI服务..."
python3 test_ai_service.py

if [ $? -eq 0 ]; then
    echo "✅ AI服务测试通过"
else
    echo "❌ AI服务测试失败"
fi

# 测试修复后的应用
echo "测试修复后的应用..."
python3 test_fixed_app.py

if [ $? -eq 0 ]; then
    echo "✅ 修复后的应用测试通过"
else
    echo "❌ 修复后的应用测试失败"
    exit 1
fi

# 启动应用
echo "启动应用..."
nohup python3 -c "
import uvicorn
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))

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
curl -s http://localhost:8000/health && echo "✅ 本地访问成功" || echo "❌ 本地访问失败"

echo "修复完成！"
echo "应用地址: http://your-server-ip:8000"
echo "日志文件: logs/app.log"
echo "查看日志: tail -f logs/app.log" 