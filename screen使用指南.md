# Screen 使用指南

## 1. 安装 Screen

```bash
# CentOS/RHEL
yum install screen -y

# Ubuntu/Debian
apt-get install screen -y
```

## 2. Screen 基本用法

### 2.1 创建新会话
```bash
# 创建一个新的 screen 会话并命名（推荐）
screen -S 会话名称

# 例如：创建一个名为 rag-uvicorn 的会话
screen -S rag-uvicorn
```

### 2.2 会话管理
```bash
# 查看所有会话
screen -ls

# 重新连接到指定会话
screen -r 会话名称

# 强制重新连接（会话可能卡住时使用）
screen -D -r 会话名称

# 删除死掉的会话
screen -wipe
```

### 2.3 会话操作
在 screen 会话中：
- `Ctrl+A` 然后按 `D`：分离当前会话（程序继续在后台运行）
- `Ctrl+A` 然后按 `K`：杀死当前会话
- `Ctrl+A` 然后按 `?`：显示所有快捷键帮助

## 3. 实际应用示例

### 3.1 启动 Uvicorn 服务
```bash
# 1. 创建新会话
screen -S rag-uvicorn

# 2. 在会话中启动服务
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# 生产部署
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4 --limit-concurrency 1000 --limit-max-requests 10000 --timeout-keep-alive 65 --loop uvloop --http httptools

# 后台服务
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8090

# 3. 按 Ctrl+A 然后按 D 分离会话
# 现在服务会在后台继续运行
```

### 3.2 管理运行中的服务
```bash
# 查看所有运行的 screen 会话
screen -ls

# 重新连接到 uvicorn 服务会话
screen -r rag-uvicorn

# 停止服务：重新连接后按 Ctrl+C
```

## 4. 常见问题处理

### 4.1 会话无法连接
如果出现 "There is no screen to be resumed" 错误：
```bash
# 检查是否有会话在运行
screen -ls

# 如果显示 "No Sockets found"，说明没有运行中的会话
# 需要重新创建会话
```

### 4.2 会话卡死
如果会话无响应：
```bash
# 强制重新连接
screen -D -r 会话名称

# 如果还是无法连接，可以杀死会话
pkill screen
# 然后重新创建会话
```

## 5. 最佳实践

### 5.1 会话命名规范
- 使用有意义的名称
- 建议格式：服务名-功能
- 例如：rag-uvicorn, rag-worker, rag-api

### 5.2 日志处理
```bash
# 在 screen 中启动服务时重定向日志
uvicorn app:app --host 0.0.0.0 --port 8000 --reload > uvicorn.log 2>&1
```

### 5.3 定期维护
```bash
# 查看所有会话状态
screen -ls

# 清理死掉的会话
screen -wipe

# 检查日志
tail -f uvicorn.log
```

## 6. 快捷键备忘录

| 快捷键 | 功能 |
|--------|------|
| Ctrl+A, D | 分离会话 |
| Ctrl+A, K | 杀死会话 |
| Ctrl+A, ? | 显示帮助 |
| Ctrl+A, C | 创建新窗口 |
| Ctrl+A, N | 切换到下一个窗口 |
| Ctrl+A, P | 切换到上一个窗口 |
| Ctrl+A, " | 显示所有窗口列表 |
| Ctrl+A, A | 切换到之前的窗口 |

## 7. 安全建议

1. 定期检查运行中的会话
2. 及时清理不需要的会话
3. 使用有意义的会话名称
4. 保持日志文件的整洁
5. 定期备份重要的会话配置

## 8. 故障排除

如果遇到问题，按以下步骤排查：

1. 检查 screen 是否正确安装
```bash
screen --version
```

2. 检查会话状态
```bash
screen -ls
```

3. 检查系统资源
```bash
top
df -h
free -m
```

4. 检查日志
```bash
# 系统日志
tail -f /var/log/messages

# 应用日志
tail -f uvicorn.log
```

5. 如果都无法解决，可以：
   - 杀死所有 screen 进程：`pkill screen`
   - 重新创建会话：`screen -S 会话名称` 