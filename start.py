#!/usr/bin/env python3
"""
RAG实训报告生成系统启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def create_directories():
    """创建必要的目录"""
    directories = [
        'uploads',
        'temp', 
        'static',
        'templates',
        'chroma_db',
        'logs',
        'user_templates'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ 创建目录: {directory}")

def check_dependencies():
    """检查依赖包"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import passlib
        print("✓ 依赖包检查通过")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_env_file():
    """检查环境配置文件"""
    if not os.path.exists('.env'):
        print("⚠ 未找到 .env 文件，创建默认配置...")
        with open('.env', 'w', encoding='utf-8') as f:
            f.write("""# 数据库配置
DATABASE_URL=sqlite:///./rag_system.db

# 会话密钥 (请修改为随机字符串)
SECRET_KEY=your-secret-key-here-change-this

# AI服务配置 (请填入您的API密钥)
OPENAI_API_KEY=your-openai-api-key
DASHSCOPE_API_KEY=your-dashscope-api-key

# 其他配置
UPLOAD_DIR=uploads
TEMP_DIR=temp
""")
        print("✓ 已创建 .env 文件，请配置您的API密钥")
        return False
    else:
        print("✓ 找到 .env 文件")
        return True

def start_server():
    """启动服务器"""
    print("\n🚀 启动RAG实训报告生成系统...")
    print("📝 访问地址: http://localhost:8000")
    print("📚 API文档: http://localhost:8000/docs")
    print("⏹️  按 Ctrl+C 停止服务\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 服务已停止")

def main():
    """主函数"""
    print("=" * 50)
    print("🎯 RAG实训报告生成系统")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 创建目录
    create_directories()
    
    # 检查配置文件
    check_env_file()
    
    # 启动服务
    start_server()

if __name__ == "__main__":
    main() 