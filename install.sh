#!/bin/bash

echo "安装项目依赖..."

# 进入项目目录
cd /www/wwwroot/report-generator

# 激活虚拟环境
source /www/server/pyporject_evn/report-generator_venv/bin/activate

# 升级pip
pip install --upgrade pip

# 安装基础依赖
pip install fastapi uvicorn python-multipart jinja2

# 安装文档处理依赖
pip install python-docx docxtpl

# 安装AI和向量化依赖
pip install chromadb aiohttp

# 安装其他工具依赖
pip install aiofiles

echo "依赖安装完成！" 