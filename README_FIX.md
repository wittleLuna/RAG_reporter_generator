# AI服务修复说明

## 问题描述

根据日志分析，发现以下问题：
1. **千问API调用失败: 404** - API调用格式不正确
2. **Word模板处理失败** - 模板文件路径问题
3. **应用调用旧版本AI服务方法** - 方法名不匹配

## 修复内容

### 1. 修复AI服务调用
- 更新 `app.py` 中的AI服务调用，使用新版本的 `generate_report` 方法
- 修正API请求格式，使用正确的OpenAI兼容模式

### 2. 修正环境变量配置
- 确保 `AI_API_URL` 使用正确的兼容模式URL
- 添加 `AI_EMBEDDING_MODEL` 配置

### 3. 更新依赖
- 确保安装 `openai==1.3.0` 依赖
- 检查 `python-docx` 和 `docxtpl` 依赖

## 使用方法

### 方法1: 使用修复脚本（推荐）

```bash
# 给脚本执行权限
chmod +x fix_ai_service.sh

# 运行修复脚本
./fix_ai_service.sh
```

### 方法2: 手动修复

```bash
# 1. 进入项目目录
cd /www/wwwroot/report-generator

# 2. 激活虚拟环境
source /www/server/pyporject_evn/report-generator_venv/bin/activate

# 3. 安装依赖
pip install openai==1.3.0 python-dotenv python-docx docxtpl

# 4. 更新环境变量
# 确保 .env 文件中的 AI_API_URL 为：
# AI_API_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# 5. 测试修复
python3 test_fixed_app.py

# 6. 重启应用
pkill -f uvicorn
nohup python3 -c "
import uvicorn
from app import app
uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')
" > logs/app.log 2>&1 &
```

## 验证修复

### 1. 检查API连接
```bash
python3 test_example_code.py
```

### 2. 检查AI服务
```bash
python3 test_ai_service.py
```

### 3. 检查应用功能
```bash
python3 test_fixed_app.py
```

### 4. 检查应用状态
```bash
# 检查进程
ps aux | grep uvicorn

# 检查端口
netstat -tlnp | grep 8000

# 检查日志
tail -f logs/app.log
```

## 预期结果

修复后应该看到：
- ✅ API测试通过
- ✅ AI服务测试通过
- ✅ 修复后的应用测试通过
- ✅ 应用正常启动，无404错误

## 故障排除

如果仍有问题：

1. **检查环境变量**
   ```bash
   cat .env
   ```

2. **检查依赖**
   ```bash
   pip list | grep -E "(openai|docx|dotenv)"
   ```

3. **查看详细日志**
   ```bash
   tail -f logs/app.log
   ```

4. **手动测试API**
   ```bash
   python3 test_example_code.py
   ```

## 联系支持

如果问题仍然存在，请提供：
1. 完整的错误日志
2. 环境变量配置
3. 依赖包版本信息 