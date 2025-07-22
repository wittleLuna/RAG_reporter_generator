# 使用示例

本文档提供了实训报告自动生成系统的详细使用示例。

## 📋 准备工作

### 1. 准备Word模板

创建一个包含以下占位符的Word模板文件：

```
实训报告

学生信息：
姓名：{{name}}
学号：{{student_id}}
班级：{{class_name}}
指导老师：{{instructor}}
项目名称：{{project_name}}

报告正文：
{{report_body}}
```

### 2. 准备资料文件

#### Markdown文件示例 (project_guide.md)
```markdown
# OpenWebUI项目实训指南

## 项目概述
OpenWebUI是一个开源的Web界面，用于部署和管理大语言模型。

## 环境要求
- Docker 20.10+
- Docker Compose 2.0+
- 至少4GB内存

## 部署步骤

### 1. 克隆仓库
```bash
git clone https://github.com/open-webui/open-webui.git
cd open-webui
```

### 2. 配置环境
创建.env文件并配置必要的环境变量。

### 3. 启动服务
```bash
docker-compose up -d
```

## 功能特性
- 支持多种大语言模型
- 提供Web界面管理
- 支持对话历史记录
```

#### Word文件示例 (experiment_steps.docx)
包含详细的实验步骤和配置说明。

#### PDF文件示例 (reference_manual.pdf)
包含相关的技术手册和参考资料。

### 3. 准备图片文件

按照以下命名规则准备图片：

- `openwebui1.png` - OpenWebUI界面截图
- `openwebui2.png` - 配置过程截图
- `openwebui3.png` - 运行结果截图
- `rag1.png` - RAG系统架构图
- `rag2.png` - 向量数据库截图

## 🚀 使用步骤

### 1. 启动系统

```bash
# 本地开发
python start.py

# 或使用Docker
docker-compose up -d
```

### 2. 访问系统

打开浏览器访问：`http://localhost:8000`

### 3. 填写基本信息

- 姓名：张三
- 学号：2024001
- 班级：计算机科学与技术2班
- 指导老师：李老师
- 项目名称：OpenWebUI部署与RAG系统实现

### 4. 上传文件

#### 上传Word模板
- 点击"Word模板文件"区域
- 选择准备好的模板文件

#### 上传资料文件
- 点击"Markdown资料文件"区域
- 选择 `project_guide.md`
- 点击"Word资料文件"区域
- 选择 `experiment_steps.docx`
- 点击"PDF资料文件"区域
- 选择 `reference_manual.pdf`

#### 上传图片文件
- 点击"图片文件"区域
- 选择所有准备好的图片文件

### 5. 生成报告

点击"生成实训报告"按钮，系统将：

1. 处理所有上传的文档
2. 使用AI分析内容并生成报告
3. 自动插入图片到相应位置
4. 填充个人信息到模板
5. 生成最终的Word文档

### 6. 下载报告

生成完成后，点击"下载报告"按钮获取生成的实训报告。

## 📄 生成的报告示例

生成的报告将包含：

```
实训报告

学生信息：
姓名：张三
学号：2024001
班级：计算机科学与技术2班
指导老师：李老师
项目名称：OpenWebUI部署与RAG系统实现

报告正文：

## OpenWebUI部署与配置

OpenWebUI是一个开源的Web界面，专门用于部署和管理大语言模型。本项目通过Docker容器化技术，实现了OpenWebUI的快速部署和配置。

### 环境准备

在开始部署之前，需要确保系统满足以下要求：
- Docker 20.10或更高版本
- Docker Compose 2.0或更高版本
- 至少4GB可用内存
- 稳定的网络连接

[图片: openwebui1.png]

### 部署过程

1. 首先克隆OpenWebUI的官方仓库到本地环境
2. 进入项目目录并创建必要的配置文件
3. 使用Docker Compose启动所有服务

[图片: openwebui2.png]

### 配置说明

OpenWebUI提供了丰富的配置选项，包括模型选择、参数调整、界面定制等功能。通过Web界面可以方便地进行各种设置。

[图片: openwebui3.png]

## RAG系统实现

基于检索增强生成（RAG）技术，我们实现了一个智能问答系统。

### 系统架构

RAG系统主要由以下几个组件构成：
- 文档处理模块
- 向量数据库
- 检索模块
- 生成模块

[图片: rag1.png]

### 向量数据库配置

使用ChromaDB作为向量数据库，存储文档的向量表示，支持高效的相似性检索。

[图片: rag2.png]

## 总结

通过本次实训，我们成功完成了OpenWebUI的部署和RAG系统的实现。掌握了容器化部署、大语言模型应用、向量数据库使用等关键技术。
```

## 🔧 高级配置

### 自定义AI模型

在 `.env` 文件中配置不同的AI模型：

```env
# 使用通义千问
AI_API_URL=https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
AI_MODEL_NAME=qwen-turbo
AI_API_KEY=your_api_key

# 使用百度文心一言
AI_API_URL=https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions
AI_MODEL_NAME=ernie-bot-4
AI_API_KEY=your_api_key
```

### 自定义模板

可以创建多个不同的Word模板，适应不同的报告格式要求。

### 图片命名规则

系统支持灵活的图片命名规则：

- `模块名+数字.扩展名` - 基本格式
- `模块名_描述_数字.扩展名` - 带描述的格式
- `数字_模块名.扩展名` - 数字前缀格式

## 🐛 故障排除

### 常见问题

1. **文件上传失败**
   - 检查文件大小是否超过限制（默认50MB）
   - 确认文件格式是否支持
   - 检查磁盘空间是否充足

2. **AI生成失败**
   - 检查AI服务是否正常运行
   - 确认API配置是否正确
   - 查看网络连接是否正常

3. **图片插入失败**
   - 检查图片命名是否符合规则
   - 确认图片格式是否支持
   - 验证图片文件是否损坏

### 日志查看

```bash
# 查看应用日志
tail -f logs/app.log

# 查看Docker日志
docker-compose logs -f report-generator
```

## 📞 技术支持

如遇到问题，请：

1. 查看本文档的故障排除部分
2. 检查系统日志
3. 联系技术支持团队 