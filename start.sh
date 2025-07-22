#!/bin/bash

echo "启动实训报告生成系统..."

# 进入项目目录
cd /www/wwwroot/report-generator

# 激活虚拟环境
source /www/server/pyporject_evn/report-generator_venv/bin/activate

# 停止现有进程
pkill -f uvicorn
pkill -f uwsgi
sleep 2

# 检查端口
if netstat -tlnp | grep 8000 > /dev/null; then
    echo "端口8000被占用，强制释放..."
    fuser -k 8000/tcp 2>/dev/null
fi

# 创建必要的目录
mkdir -p logs static templates uploads temp chroma_db

# 启动应用
echo "使用Uvicorn启动应用..."
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 2 