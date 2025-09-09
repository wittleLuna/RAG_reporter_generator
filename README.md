[English](#english) | [中文](#中文)

## 中文

# RAG实训报告生成系统

一个基于AI的智能实训报告生成系统，支持用户登录注册、模板管理和自动报告生成。

## 功能特性

### 🔐 用户系统
- **用户注册/登录**: 支持用户账户管理
- **个人信息管理**: 自动保存和填充用户基本信息
- **会话管理**: 安全的用户会话控制

### 📝 模板管理
- **模板创建**: 支持创建自定义封面和正文模板
- **模板使用**: 快速应用已保存的模板
- **模板删除**: 管理个人模板库

### 🤖 AI报告生成
- **多模式生成**: 支持融合模式和区分模式
- **智能补全**: 多轮自动补全功能
- **页面控制**: 精确控制生成报告的页数
- **高级提示词**: 支持自定义AI生成提示

### 📁 文件支持
- **多种格式**: 支持 .md, .doc, .docx, .pdf, 图片等格式
- **拖拽上传**: 便捷的文件上传体验
- **模板占位符**: 智能识别和替换模板变量

## 安装说明

### 1. 环境要求
- Python 3.8+
- 现代浏览器（Chrome, Firefox, Safari, Edge）

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 环境配置
创建 `.env` 文件并配置以下参数：
```env
# 数据库配置
DATABASE_URL=sqlite:///./rag_system.db

# 会话密钥
SECRET_KEY=your-secret-key-here

# AI服务配置
OPENAI_API_KEY=your-openai-api-key
DASHSCOPE_API_KEY=your-dashscope-api-key

# 其他配置
UPLOAD_DIR=uploads
TEMP_DIR=temp
```

### 4. 启动服务
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## 使用指南

### 1. 用户注册
1. 访问系统首页，点击"立即注册"
2. 填写用户名、邮箱、密码等基本信息
3. 完成注册后自动跳转到登录页面

### 2. 个人信息设置
1. 登录后点击右上角"个人信息"按钮
2. 填写姓名、学号、班级等信息
3. 保存后信息会自动填充到报告生成表单

### 3. 模板管理
1. 点击"模板管理"按钮打开模板管理界面
2. 创建新模板：
   - 选择模板类型（封面/正文）
   - 上传模板文件（.doc/.docx格式）
   - 设置模板名称
3. 使用现有模板：
   - 在模板列表中选择要使用的模板
   - 点击"使用模板"按钮

### 4. 生成报告
1. **填写基本信息**: 系统会自动填充用户信息
2. **上传模板文件**:
   - 封面模板：包含必要的占位符
   - 正文模板：包含 `{{report_body}}` 占位符
3. **上传资料文件**: 支持多种格式的文档和图片
4. **选择生成模式**:
   - 融合模式：将所有资料融合生成统一报告
   - 区分模式：按文件分别生成后整合
5. **设置页面控制**:
   - 选择目标页数或手动输入
   - 启用多轮补全功能
6. **生成报告**: 点击"生成报告"按钮开始处理

## 模板占位符说明

### 封面模板必需占位符
- `{{name}}` - 学生姓名
- `{{student_id}}` - 学号
- `{{project_name}}` - 课程名称

### 封面模板可选占位符
- `{{class_name}}` - 班级
- `{{instructor}}` - 导师

### 正文模板必需占位符
- `{{report_body}}` - 报告正文内容

### 正文模板可选占位符
- `{{name}}` - 学生姓名
- `{{student_id}}` - 学号
- `{{class_name}}` - 班级
- `{{instructor}}` - 导师
- `{{project_name}}` - 课程名称

## 系统架构

```
├── app.py                 # 主应用文件
├── templates/             # HTML模板
│   ├── index.html        # 主页面
│   ├── login.html        # 登录页面
│   └── register.html     # 注册页面
├── static/               # 静态文件
│   ├── css/             # 样式文件
│   └── js/              # JavaScript文件
├── uploads/             # 上传文件存储
├── user_templates/      # 用户模板存储
├── logs/               # 日志文件
└── requirements.txt    # 依赖包列表
```

## 技术栈

- **后端**: FastAPI + SQLAlchemy + SQLite
- **前端**: HTML5 + CSS3 + JavaScript
- **AI服务**: OpenAI API + 千问API
- **文档处理**: python-docx + PyPDF2
- **向量数据库**: ChromaDB
- **认证**: Passlib + Python-Jose

## 注意事项

1. **API密钥**: 请确保正确配置AI服务的API密钥
2. **文件大小**: 建议上传文件不超过50MB
3. **模板格式**: 模板文件必须为Word格式（.doc/.docx）
4. **占位符**: 请确保模板包含必要的占位符
5. **网络连接**: 生成报告需要稳定的网络连接

## 故障排除

### 常见问题

1. **登录失败**
   - 检查用户名和密码是否正确
   - 确认数据库文件存在且可写

2. **模板上传失败**
   - 检查文件格式是否为.doc或.docx
   - 确认文件大小不超过限制

3. **报告生成失败**
   - 检查API密钥配置
   - 确认网络连接正常
   - 查看日志文件获取详细错误信息

4. **页面显示异常**
   - 清除浏览器缓存
   - 检查浏览器兼容性

## 更新日志

### v1.0.0 (2025-06-20)
- 初始版本发布
- 支持用户注册登录
- 支持模板管理
- 支持AI报告生成
- 支持多种文件格式

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 联系方式

如有问题或建议，请联系开发团队。

## English

# RAG Training Report Generation System

An AI-powered intelligent training report generation system that supports user registration/login, template management, and automated report generation.

## Features

### 🔐 User System
- **User Registration/Login**: Manage user accounts securely
- **Profile Management**: Automatically save and fill in user information
- **Session Management**: Secure session control

### 📝 Template Management
- **Template Creation**: Create custom cover and body templates
- **Template Usage**: Quickly apply saved templates
- **Template Deletion**: Manage personal template library

### 🤖 AI Report Generation
- **Multi-Mode Generation**: Supports fusion mode and separate mode
- **Intelligent Completion**: Multi-round auto-completion
- **Page Control**: Precisely control the number of report pages
- **Advanced Prompts**: Customize AI generation prompts

### 📁 File Support
- **Multiple Formats**: Supports .md, .doc, .docx, .pdf, images, etc.
- **Drag-and-Drop Upload**: Convenient file upload
- **Template Placeholders**: Automatically detect and replace variables

## Installation

### 1. Requirements
- Python 3.8+
- Modern browsers (Chrome, Firefox, Safari, Edge)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
````

### 3. Environment Configuration

Create a `.env` file and configure the following:

```env
# Database
DATABASE_URL=sqlite:///./rag_system.db

# Secret Key
SECRET_KEY=your-secret-key-here

# AI Service
OPENAI_API_KEY=your-openai-api-key
DASHSCOPE_API_KEY=your-dashscope-api-key

# Others
UPLOAD_DIR=uploads
TEMP_DIR=temp
```

### 4. Start the Service

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## User Guide

### 1. User Registration

1. Visit the homepage and click "Register Now"
2. Fill in username, email, password, etc.
3. After registration, redirect to the login page

### 2. Profile Settings

1. After login, click "Profile" in the top-right
2. Fill in name, student ID, class, etc.
3. Saved info will auto-fill the report form

### 3. Template Management

1. Click "Template Management"
2. Create a new template:

   * Select type (Cover/Body)
   * Upload file (.doc/.docx)
   * Set template name
3. Use an existing template:

   * Select from the list
   * Click "Use Template"

### 4. Generate Report

1. **Fill in Basic Info**: Auto-filled from profile
2. **Upload Templates**:

   * Cover template: must include placeholders
   * Body template: must include `{{report_body}}`
3. **Upload Materials**: Supports multiple file formats
4. **Select Mode**:

   * Fusion mode: Merge all into one report
   * Separate mode: Generate separately, then combine
5. **Set Page Control**:

   * Choose target pages or enter manually
   * Enable multi-round completion if needed
6. **Generate Report**: Click "Generate" to start

## Template Placeholders

### Required in Cover Template

* `{{name}}` - Student Name
* `{{student_id}}` - Student ID
* `{{project_name}}` - Course Name

### Optional in Cover Template

* `{{class_name}}` - Class
* `{{instructor}}` - Instructor

### Required in Body Template

* `{{report_body}}` - Report Content

### Optional in Body Template

* `{{name}}` - Student Name
* `{{student_id}}` - Student ID
* `{{class_name}}` - Class
* `{{instructor}}` - Instructor
* `{{project_name}}` - Course Name

## System Architecture

```
├── app.py                 # Main Application
├── templates/             # HTML Templates
│   ├── index.html        # Homepage
│   ├── login.html        # Login Page
│   └── register.html     # Register Page
├── static/               # Static Files
│   ├── css/             # CSS
│   └── js/              # JavaScript
├── uploads/             # Uploaded Files
├── user_templates/      # User Templates
├── logs/               # Logs
└── requirements.txt    # Dependencies
```

## Tech Stack

* **Backend**: FastAPI + SQLAlchemy + SQLite
* **Frontend**: HTML5 + CSS3 + JavaScript
* **AI Services**: OpenAI API + Dashscope API
* **Document Processing**: python-docx + PyPDF2
* **Vector Database**: ChromaDB
* **Authentication**: Passlib + Python-Jose

## Notes

1. **API Keys**: Ensure proper AI service API keys
2. **File Size**: Recommended <50MB
3. **Template Format**: Must be .doc/.docx
4. **Placeholders**: Ensure required placeholders exist
5. **Network**: Requires stable connection

## Troubleshooting

### Common Issues

1. **Login Failed**

   * Check username/password
   * Ensure database is accessible

2. **Template Upload Failed**

   * Ensure format is .doc or .docx
   * Check file size limit

3. **Report Generation Failed**

   * Verify API keys
   * Check network connection
   * Review logs for details

4. **Page Display Issues**

   * Clear browser cache
   * Check browser compatibility

## Changelog

### v1.0.0 (2025-06-20)

* Initial release
* User registration & login
* Template management
* AI report generation
* Multi-format file support

## License

This project is licensed under the MIT License. See LICENSE for details.

## Contact

For issues or suggestions, please contact the development team.



