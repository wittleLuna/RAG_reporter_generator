#!/bin/bash

# Docker部署脚本
echo "🚀 开始Docker部署实训报告自动生成系统..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，正在安装Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER
    echo "✅ Docker安装完成，请重新登录或重启系统"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，正在安装..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# 创建项目目录
echo "📁 创建项目目录..."
sudo mkdir -p /opt/report-generator
cd /opt/report-generator

# 复制项目文件（如果当前目录是项目根目录）
if [ -f "app.py" ]; then
    echo "📋 复制项目文件..."
    cp -r . /opt/report-generator/
fi

# 创建必要的目录
echo "📂 创建必要的目录..."
mkdir -p uploads temp static templates chroma_db

# 设置权限
echo "🔐 设置文件权限..."
sudo chown -R $USER:$USER /opt/report-generator

# 构建并启动服务
echo "🔨 构建Docker镜像..."
docker-compose -f docker-compose.prod.yml build

echo "🚀 启动服务..."
docker-compose -f docker-compose.prod.yml up -d

# 检查服务状态
echo "📊 检查服务状态..."
sleep 10
docker-compose -f docker-compose.prod.yml ps

# 检查服务健康状态
echo "🏥 检查服务健康状态..."
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ 服务启动成功！"
    echo "🌐 访问地址: http://$(hostname -I | awk '{print $1}'):8000"
else
    echo "⚠️  服务可能还在启动中，请稍等..."
    echo "📋 查看日志: docker-compose -f docker-compose.prod.yml logs -f"
fi

echo ""
echo "📖 常用命令："
echo "  查看服务状态: docker-compose -f docker-compose.prod.yml ps"
echo "  查看日志: docker-compose -f docker-compose.prod.yml logs -f"
echo "  停止服务: docker-compose -f docker-compose.prod.yml down"
echo "  重启服务: docker-compose -f docker-compose.prod.yml restart"
echo "  更新服务: docker-compose -f docker-compose.prod.yml up -d --build" 