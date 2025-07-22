#!/bin/bash

echo "=== RAG报告生成器快速测试 ==="

# 检查依赖
echo "1. 检查依赖..."
pip install openai==1.3.0 python-dotenv

# 测试API
echo "2. 测试API..."
python3 test_example_code.py

# 检查结果
if [ $? -eq 0 ]; then
    echo "✅ API测试通过"
else
    echo "❌ API测试失败"
    exit 1
fi

echo "3. 测试完成！" 