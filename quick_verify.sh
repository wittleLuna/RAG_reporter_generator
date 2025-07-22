#!/bin/bash

echo "=== 快速验证修复 ==="

# 进入项目目录
cd /www/wwwroot/report-generator

# 激活虚拟环境
source /www/server/pyporject_evn/report-generator_venv/bin/activate

# 检查OpenAI版本
echo "检查OpenAI版本..."
pip show openai

# 检查环境变量
echo "检查环境变量..."
cat .env

# 快速测试
echo "快速测试..."
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('API URL:', os.getenv('AI_API_URL'))
print('Model:', os.getenv('AI_MODEL_NAME'))
print('API Key:', os.getenv('AI_API_KEY')[:10] + '...' if os.getenv('AI_API_KEY') else '未设置')
"

# 测试AI服务导入
echo "测试AI服务导入..."
python3 -c "
from services.ai_service_qwen import AIService
print('✅ AI服务导入成功')
ai = AIService()
print('✅ AI服务初始化成功')
"

# 测试方法存在
echo "测试方法存在..."
python3 -c "
from services.ai_service_qwen import AIService
ai = AIService()
methods = [method for method in dir(ai) if not method.startswith('_')]
print('可用方法:', methods)
if 'generate_report' in methods:
    print('✅ generate_report方法存在')
else:
    print('❌ generate_report方法不存在')
"

echo "验证完成！" 