#!/bin/bash

echo "=== 简化启动脚本 ==="

# 进入项目目录
cd /www/wwwroot/report-generator

# 激活虚拟环境
source /www/server/pyporject_evn/report-generator_venv/bin/activate

# 停止现有进程
echo "停止现有进程..."
pkill -f uvicorn 2>/dev/null || true
pkill -f uwsgi 2>/dev/null || true
sleep 2

# 创建必要目录（使用当前用户权限）
echo "创建必要目录..."
mkdir -p logs uploads temp chroma_db 2>/dev/null || true

# 直接启动应用（不使用nohup，便于查看错误）
echo "启动应用..."
python3 -c "
import uvicorn
from app import app
print('应用启动中...')
uvicorn.run(app, host='0.0.0.0', port=8000, reload=False)
" 