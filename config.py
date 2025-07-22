"""
RAG实训报告生成系统配置文件
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 基础配置
BASE_DIR = Path(__file__).parent
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-this")

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rag_system.db")

# 文件上传配置
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
TEMP_DIR = Path(os.getenv("TEMP_DIR", "temp"))
USER_TEMPLATES_DIR = Path("user_templates")
LOGS_DIR = Path("logs")

# 确保目录存在
UPLOAD_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)
USER_TEMPLATES_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# 文件上传限制
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {
    'text': {'.txt', '.md', '.markdown'},
    'document': {'.doc', '.docx'},
    'pdf': {'.pdf'},
    'image': {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
}

# AI服务配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

# 报告生成配置
DEFAULT_MAX_TOKENS = 4000
MAX_MAX_TOKENS = 8192
DEFAULT_TARGET_PAGES = 5
MAX_TARGET_PAGES = 20

# 模板配置
TEMPLATE_PLACEHOLDERS = {
    'required_cover': ['{{name}}', '{{student_id}}', '{{project_name}}'],
    'optional_cover': ['{{class_name}}', '{{instructor}}'],
    'required_body': ['{{report_body}}'],
    'optional_body': ['{{name}}', '{{student_id}}', '{{class_name}}', '{{instructor}}', '{{project_name}}']
}

# 日志配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "app.log"

# 安全配置
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_DIGITS = True

# 会话配置
SESSION_COOKIE_NAME = "rag_session"
SESSION_COOKIE_MAX_AGE = 86400 * 7  # 7天

# 开发配置
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
RELOAD = DEBUG

class Config:
    """应用配置"""
    
    # 基础配置
    APP_NAME = "实训报告自动生成系统"
    VERSION = "1.0.0"
    DEBUG = DEBUG
    
    # 服务器配置
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # 文件上传配置
    MAX_FILE_SIZE = MAX_FILE_SIZE
    UPLOAD_FOLDER = UPLOAD_DIR
    TEMP_FOLDER = TEMP_DIR
    
    # 支持的文件类型
    SUPPORTED_EXTENSIONS = ALLOWED_EXTENSIONS
    
    # AI配置
    AI_API_URL = os.getenv("AI_API_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "qwen-plus")
    AI_API_KEY = os.getenv("AI_API_KEY", "sk-442562cd6b6b4b2896ebdac8ce8d047e")
    
    # 向量数据库配置
    CHROMA_PERSIST_DIR = "./chroma_db"
    EMBEDDING_MODEL = "shibing624/text2vec-base-chinese"
    
    # 文档处理配置
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # 图片配置
    IMAGE_WIDTH = 5  # 英寸
    IMAGE_ALIGNMENT = "center"
    
    # 清理配置
    CLEANUP_INTERVAL = 3600  # 1小时清理一次
    MAX_SESSION_AGE = 86400  # 24小时后清理会话文件 