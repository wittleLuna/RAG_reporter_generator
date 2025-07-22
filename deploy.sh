#!/bin/bash

# 实训报告自动生成系统部署脚本
# 适用于CentOS/RHEL系统

echo "开始部署实训报告自动生成系统..."

# 更新系统
echo "更新系统包..."
sudo yum update -y

# 安装Python3和pip
echo "安装Python3和pip..."
sudo yum install -y python3 python3-pip

# 安装开发工具
echo "安装开发工具..."
sudo yum groupinstall -y "Development Tools"
sudo yum install -y python3-devel

# 安装系统依赖
echo "安装系统依赖..."
sudo yum install -y gcc gcc-c++ make cmake
sudo yum install -y libffi-devel openssl-devel

# 创建项目目录
echo "创建项目目录..."
mkdir -p /opt/report-generator
cd /opt/report-generator

# 复制项目文件（假设当前目录是项目根目录）
echo "复制项目文件..."
cp -r . /opt/report-generator/

# 创建虚拟环境
echo "创建Python虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 升级pip
pip install --upgrade pip

# 安装Python依赖
echo "安装Python依赖..."
pip install -r requirements.txt

# 创建必要的目录
echo "创建必要的目录..."
mkdir -p uploads temp static templates chroma_db

# 设置权限
echo "设置文件权限..."
chmod +x /opt/report-generator/app.py
chown -R $USER:$USER /opt/report-generator

# 创建环境变量文件
echo "创建环境变量文件..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "请编辑 .env 文件配置您的环境变量"
fi

# 创建systemd服务文件
echo "创建systemd服务..."
sudo tee /etc/systemd/system/report-generator.service > /dev/null <<EOF
[Unit]
Description=Report Generator Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/report-generator
Environment=PATH=/opt/report-generator/venv/bin
ExecStart=/opt/report-generator/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 重新加载systemd配置
sudo systemctl daemon-reload

# 启用服务
sudo systemctl enable report-generator

# 启动服务
echo "启动服务..."
sudo systemctl start report-generator

# 检查服务状态
echo "检查服务状态..."
sudo systemctl status report-generator

echo "部署完成！"
echo "服务已启动在 http://$(hostname -I | awk '{print $1}'):8000"
echo ""
echo "常用命令："
echo "  查看服务状态: sudo systemctl status report-generator"
echo "  启动服务: sudo systemctl start report-generator"
echo "  停止服务: sudo systemctl stop report-generator"
echo "  重启服务: sudo systemctl restart report-generator"
echo "  查看日志: sudo journalctl -u report-generator -f" 