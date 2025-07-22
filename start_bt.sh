#!/bin/bash

echo "=== 宝塔面板启动脚本 ==="

# 进入项目目录
cd /www/wwwroot/report-generator

# 激活虚拟环境
source /www/server/pyporject_evn/report-generator_venv/bin/activate

# 停止现有进程
echo "停止现有进程..."
pkill -f uvicorn
pkill -f uwsgi
sleep 2

# 检查端口
if netstat -tlnp | grep 8000 > /dev/null; then
    echo "端口8000被占用，强制释放..."
    fuser -k 8000/tcp 2>/dev/null
fi

# 创建必要的目录
echo "创建必要目录..."
mkdir -p logs static templates uploads temp chroma_db

# 设置权限
echo "设置权限..."
chown -R www:www /www/wwwroot/report-generator
chmod -R 755 /www/wwwroot/report-generator
chmod -R 777 logs uploads temp

# 检查依赖
echo "检查依赖..."
python3 -c "import fastapi, uvicorn, aiohttp, chromadb, aiofiles" 2>/dev/null || {
    echo "依赖检查失败，请先运行 ./install.sh"
    exit 1
}

# 启动应用
echo "启动应用..."
nohup uvicorn app:app --host 0.0.0.0 --port 8000 --workers 2 > logs/app.log 2>&1 &

# 等待启动
sleep 3

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