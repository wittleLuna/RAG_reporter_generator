#!/bin/bash

echo "=== 调试启动脚本 ==="

# 进入项目目录
cd /www/wwwroot/report-generator

echo "当前目录: $(pwd)"
echo "目录内容:"
ls -la

# 检查虚拟环境
echo "检查虚拟环境..."
if [ -f "/www/server/pyporject_evn/report-generator_venv/bin/activate" ]; then
    echo "✅ 虚拟环境存在"
    source /www/server/pyporject_evn/report-generator_venv/bin/activate
    echo "Python版本: $(python3 --version)"
    echo "Python路径: $(which python3)"
else
    echo "❌ 虚拟环境不存在"
    exit 1
fi

# 检查关键文件
echo "检查关键文件..."
files_to_check=("app.py" "services/ai_service_qwen.py" "templates/index.html" ".env")
for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 不存在"
    fi
done

# 检查依赖
echo "检查依赖..."
python3 -c "
import sys
print('Python路径:', sys.path)
try:
    import fastapi
    print('✅ FastAPI:', fastapi.__version__)
except ImportError as e:
    print('❌ FastAPI导入失败:', e)

try:
    import uvicorn
    print('✅ Uvicorn:', uvicorn.__version__)
except ImportError as e:
    print('❌ Uvicorn导入失败:', e)

try:
    import aiohttp
    print('✅ aiohttp导入成功')
except ImportError as e:
    print('❌ aiohttp导入失败:', e)

try:
    import chromadb
    print('✅ chromadb导入成功')
except ImportError as e:
    print('❌ chromadb导入失败:', e)

try:
    import aiofiles
    print('✅ aiofiles导入成功')
except ImportError as e:
    print('❌ aiofiles导入失败:', e)
"

# 测试应用导入
echo "测试应用导入..."
python3 -c "
try:
    import app
    print('✅ 应用导入成功')
    print('应用对象:', app.app)
    print('应用类型:', type(app.app))
except Exception as e:
    print('❌ 应用导入失败:', e)
    import traceback
    traceback.print_exc()
"

# 检查端口占用
echo "检查端口占用..."
netstat -tlnp | grep 8000 || echo "端口8000未被占用"

# 检查进程
echo "检查相关进程..."
ps aux | grep -E "(uvicorn|uwsgi|python)" | grep -v grep || echo "没有相关进程运行"

# 尝试启动应用（前台运行，显示错误）
echo "尝试启动应用（前台模式）..."
echo "按 Ctrl+C 停止测试"
python3 -c "
import uvicorn
from app import app
print('开始启动应用...')
uvicorn.run(app, host='0.0.0.0', port=8000, log_level='debug')
" 