#!/bin/bash

echo "=== 修复应用问题 ==="

# 进入项目目录
cd /www/wwwroot/report-generator

# 激活虚拟环境
source /www/server/pyporject_evn/report-generator_venv/bin/activate

# 停止现有进程
echo "停止现有进程..."
pkill -f uvicorn 2>/dev/null || true
pkill -f uwsgi 2>/dev/null || true
sleep 2

# 检查并安装依赖
echo "检查依赖..."
pip install python-docx docxtpl python-dotenv aiohttp aiofiles chromadb fastapi uvicorn python-multipart jinja2 requests

# 创建示例模板
echo "创建示例模板..."
python3 create_template.py

# 修复权限
echo "修复权限..."
mkdir -p logs uploads temp chroma_db static templates 2>/dev/null || true
chmod -R 755 . 2>/dev/null || true
chmod -R 777 logs uploads temp 2>/dev/null || true

# 确保环境变量文件存在
if [ ! -f ".env" ]; then
    echo "创建环境变量文件..."
    cat > .env << EOF
# 千问API配置
AI_API_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AI_MODEL_NAME=qwen-plus
AI_API_KEY=sk-442562cd6b6b4b2896ebdac8ce8d047e

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=False

# ChromaDB配置
CHROMA_PERSIST_DIR=./chroma_db
EOF
fi

# 测试API调用
echo "测试API调用..."
python3 test_api.py

if [ $? -eq 0 ]; then
    echo "✅ API测试通过"
else
    echo "❌ API测试失败"
    echo "继续启动应用，但AI功能可能有问题..."
fi

# 测试应用
echo "测试应用..."
python3 test_app.py

if [ $? -eq 0 ]; then
    echo "✅ 应用测试通过"
else
    echo "❌ 应用测试失败"
    exit 1
fi

# 测试文件上传
echo "测试文件上传..."
python3 test_upload.py

if [ $? -eq 0 ]; then
    echo "✅ 文件上传测试通过"
else
    echo "❌ 文件上传测试失败"
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
echo "等待应用启动..."
sleep 5

# 检查进程
echo "检查进程状态..."
ps aux | grep uvicorn | grep -v grep

# 检查端口
echo "检查端口状态..."
netstat -tlnp | grep 8000

# 测试访问
echo "测试本地访问..."
for i in {1..5}; do
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ 应用启动成功！"
        break
    else
        echo "等待应用启动... ($i/5)"
        sleep 2
    fi
done

# 显示日志
echo "显示启动日志..."
tail -20 logs/app.log

echo "修复完成！"
echo "应用地址: http://your-server-ip:8000"
echo "日志文件: logs/app.log"
echo "示例模板: templates/sample_template.docx"
echo "使用 'tail -f logs/app.log' 查看实时日志" 