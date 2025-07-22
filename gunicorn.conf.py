# Gunicorn配置文件
import multiprocessing

# 服务器配置
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100

# 超时配置
timeout = 120
keepalive = 2

# 日志配置
accesslog = "/www/wwwroot/report-generator/logs/gunicorn_access.log"
errorlog = "/www/wwwroot/report-generator/logs/gunicorn_error.log"
loglevel = "info"

# 进程配置
preload_app = True
daemon = False

# 用户配置
user = "www"
group = "www"

# 其他配置
reload = False
reload_engine = "auto" 