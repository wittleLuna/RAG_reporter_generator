#!/bin/bash

echo "=== 修复OpenAI版本问题 ==="

# 进入项目目录
cd /www/wwwroot/report-generator

# 激活虚拟环境
source /www/server/pyporject_evn/report-generator_venv/bin/activate

# 卸载当前版本
echo "卸载当前OpenAI版本..."
pip uninstall openai -y

# 安装兼容版本
echo "安装兼容的OpenAI版本..."
pip install openai==0.28.1

# 检查版本
echo "检查OpenAI版本..."
pip show openai

# 测试API
echo "测试API..."
python3 test_example_code.py

if [ $? -eq 0 ]; then
    echo "✅ API测试通过"
else
    echo "❌ API测试失败，尝试其他版本..."
    pip uninstall openai -y
    pip install openai==1.3.0
    python3 test_example_code.py
fi

echo "修复完成！" 