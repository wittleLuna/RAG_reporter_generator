#!/usr/bin/env python3
"""
RAG实训报告生成系统部署脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("✗ Python版本过低，需要3.8或更高版本")
        return False
    print(f"✓ Python版本: {sys.version}")
    return True

def install_dependencies():
    """安装依赖包"""
    print("📦 安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError:
        print("✗ 依赖包安装失败")
        return False

def create_production_config():
    """创建生产环境配置"""
    print("⚙️  创建生产环境配置...")
    
    # 创建生产环境.env文件
    env_content = """# 生产环境配置
DATABASE_URL=sqlite:///./rag_system.db

# 请修改为强密码
SECRET_KEY=your-production-secret-key-change-this-immediately

# AI服务配置
OPENAI_API_KEY=your-openai-api-key
DASHSCOPE_API_KEY=your-dashscope-api-key

# 文件路径配置
UPLOAD_DIR=uploads
TEMP_DIR=temp

# 生产环境设置
DEBUG=False
"""
    
    env_file = Path(".env")
    if not env_file.exists():
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✓ 已创建 .env 文件")
        print("⚠️  请修改 .env 文件中的配置参数")
    else:
        print("✓ .env 文件已存在")

def create_directories():
    """创建必要的目录"""
    print("📁 创建目录结构...")
    directories = [
        'uploads',
        'temp',
        'static',
        'templates',
        'chroma_db',
        'logs',
        'user_templates',
        'backups'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ 创建目录: {directory}")

def create_systemd_service():
    """创建systemd服务文件"""
    print("🔧 创建systemd服务...")
    
    service_content = """[Unit]
Description=RAG实训报告生成系统
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory={}
ExecStart={} -m uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
""".format(Path.cwd(), sys.executable)
    
    service_file = Path("/etc/systemd/system/rag-system.service")
    
    try:
        with open(service_file, "w") as f:
            f.write(service_content)
        print("✓ 已创建systemd服务文件")
        print("📝 请运行以下命令启用服务:")
        print("   sudo systemctl daemon-reload")
        print("   sudo systemctl enable rag-system")
        print("   sudo systemctl start rag-system")
    except PermissionError:
        print("⚠️  需要管理员权限创建服务文件")
        print("📝 请手动创建 /etc/systemd/system/rag-system.service")

def create_nginx_config():
    """创建Nginx配置文件"""
    print("🌐 创建Nginx配置...")
    
    nginx_config = """server {
    listen 80;
    server_name your-domain.com;  # 请修改为您的域名
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias {}/static/;
        expires 30d;
    }
    
    client_max_body_size 50M;
}
""".format(Path.cwd())
    
    nginx_file = Path("/etc/nginx/sites-available/rag-system")
    
    try:
        with open(nginx_file, "w") as f:
            f.write(nginx_config)
        print("✓ 已创建Nginx配置文件")
        print("📝 请运行以下命令启用Nginx配置:")
        print("   sudo ln -s /etc/nginx/sites-available/rag-system /etc/nginx/sites-enabled/")
        print("   sudo nginx -t")
        print("   sudo systemctl reload nginx")
    except PermissionError:
        print("⚠️  需要管理员权限创建Nginx配置")
        print("📝 请手动创建Nginx配置文件")

def create_backup_script():
    """创建备份脚本"""
    print("💾 创建备份脚本...")
    
    backup_script = """#!/bin/bash
# RAG系统备份脚本

BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="rag_backup_$DATE.tar.gz"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库和用户文件
tar -czf $BACKUP_DIR/$BACKUP_FILE \\
    rag_system.db \\
    uploads/ \\
    user_templates/ \\
    logs/ \\
    .env

echo "备份完成: $BACKUP_DIR/$BACKUP_FILE"

# 删除7天前的备份
find $BACKUP_DIR -name "rag_backup_*.tar.gz" -mtime +7 -delete
"""
    
    backup_file = Path("backup.sh")
    with open(backup_file, "w") as f:
        f.write(backup_script)
    
    # 设置执行权限
    os.chmod(backup_file, 0o755)
    print("✓ 已创建备份脚本: backup.sh")

def create_monitoring_script():
    """创建监控脚本"""
    print("📊 创建监控脚本...")
    
    monitor_script = """#!/bin/bash
# RAG系统监控脚本

LOG_FILE="logs/system_monitor.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# 检查服务状态
if systemctl is-active --quiet rag-system; then
    STATUS="运行中"
else
    STATUS="已停止"
    echo "[$DATE] 警告: RAG系统服务已停止" >> $LOG_FILE
fi

# 检查磁盘空间
DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "[$DATE] 警告: 磁盘使用率超过80%: ${DISK_USAGE}%" >> $LOG_FILE
fi

# 检查内存使用
MEMORY_USAGE=$(free | awk 'NR==2{printf "%.1f", $3*100/$2}')
if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    echo "[$DATE] 警告: 内存使用率超过80%: ${MEMORY_USAGE}%" >> $LOG_FILE
fi

echo "[$DATE] 系统状态: $STATUS, 磁盘: ${DISK_USAGE}%, 内存: ${MEMORY_USAGE}%" >> $LOG_FILE
"""
    
    monitor_file = Path("monitor.sh")
    with open(monitor_file, "w") as f:
        f.write(monitor_script)
    
    # 设置执行权限
    os.chmod(monitor_file, 0o755)
    print("✓ 已创建监控脚本: monitor.sh")

def main():
    """主部署函数"""
    print("🚀 RAG实训报告生成系统部署脚本")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 安装依赖
    if not install_dependencies():
        return
    
    # 创建目录
    create_directories()
    
    # 创建配置文件
    create_production_config()
    
    # 创建服务文件
    create_systemd_service()
    
    # 创建Nginx配置
    create_nginx_config()
    
    # 创建备份脚本
    create_backup_script()
    
    # 创建监控脚本
    create_monitoring_script()
    
    print("\n" + "=" * 50)
    print("🎉 部署完成！")
    print("\n📋 后续步骤:")
    print("1. 修改 .env 文件中的配置参数")
    print("2. 配置域名和SSL证书")
    print("3. 启动服务: sudo systemctl start rag-system")
    print("4. 设置定时备份: crontab -e")
    print("5. 设置监控: */5 * * * * ./monitor.sh")

if __name__ == "__main__":
    main() 