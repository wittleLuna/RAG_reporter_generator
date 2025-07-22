# 富文本字段使用指南

## 🎯 功能概述

系统现在支持为各个字段（name, student_id, class_name, instructor, project_name）应用富文本渲染，就像 `report_body` 一样。每个字段都可以：

- 使用自定义段落样式
- 支持粗体文本（`**粗体**`）
- 保持模板的一致性

## ✅ 支持的字段

### 基本信息字段
- **name**: 姓名字段
- **student_id**: 学号字段  
- **class_name**: 班级字段
- **instructor**: 指导教师字段
- **project_name**: 项目名称字段

### 报告正文字段
- **report_body**: 报告正文（原有功能）

## 🔧 如何创建自定义字段样式

### 方法一：在Word模板中手动创建

1. 打开Word模板文件
2. 点击"样式"面板中的"新建样式"
3. 为每个字段创建对应的样式：

#### 姓名样式 (name)
- 样式名称：**name**
- 样式类型：段落
- 字体：微软雅黑
- 字号：12pt
- 颜色：蓝色 (RGB: 0, 0, 255)

#### 学号样式 (student_id)
- 样式名称：**student_id**
- 样式类型：段落
- 字体：微软雅黑
- 字号：12pt
- 颜色：紫色 (RGB: 128, 0, 128)

#### 班级样式 (class_name)
- 样式名称：**class_name**
- 样式类型：段落
- 字体：微软雅黑
- 字号：12pt
- 颜色：绿色 (RGB: 0, 128, 0)

#### 指导教师样式 (instructor)
- 样式名称：**instructor**
- 样式类型：段落
- 字体：微软雅黑
- 字号：12pt
- 颜色：红色 (RGB: 255, 0, 0)

#### 项目名称样式 (project_name)
- 样式名称：**project_name**
- 样式类型：段落
- 字体：微软雅黑
- 字号：12pt
- 颜色：橙色 (RGB: 255, 165, 0)

### 方法二：使用测试脚本自动创建

运行测试脚本会自动创建所有样式：

```bash
python test_rich_text_fields.py
```

## 📝 模板占位符格式

在Word模板中，使用以下格式的占位符：

```
姓名：{{name}}
学号：{{student_id}}
班级：{{class_name}}
指导教师：{{instructor}}
项目名称：{{project_name}}
报告正文：{{report_body}}
```

## 🎨 富文本内容格式

### 粗体文本
使用 `**文本**` 格式来标记粗体：

```
姓名：张三（**优秀学生**）
学号：**20230001**（学号）
班级：软件工程**1班**
指导教师：**李老师**（副教授）
项目名称：RAG实训**项目**
```

### 普通文本
直接输入文本，无需特殊标记：

```
姓名：张三
学号：20230001
班级：软件工程1班
指导教师：李老师
项目名称：RAG实训项目
```

## 🔄 渲染流程

### 1. docxtpl渲染
首先使用docxtpl渲染模板字段，将占位符替换为实际内容：

```python
context_dict = {
    "name": "张三（**优秀学生**）",
    "student_id": "**20230001**（学号）",
    "class_name": "软件工程**1班**",
    "instructor": "**李老师**（副教授）",
    "project_name": "RAG实训**项目**",
    "report_body": "{{report_body}}"  # 保留占位符
}
tpl.render(context_dict)
```

### 2. 富文本处理
然后使用python-docx处理每个字段的富文本内容：

```python
for field_name, field_content in field_mappings.items():
    if field_content and field_content.strip():
        success = add_rich_text_to_field(doc, field_name, field_content)
```

### 3. 样式应用
为每个字段应用对应的段落样式：

```python
field_style = get_style(doc, [field_name, 'Normal'])
if field_style:
    new_paragraph.style = field_style
```

## 📊 样式优先级

每个字段的样式优先级：

1. **字段名样式**：优先使用与字段名相同的样式
2. **Normal样式**：如果没有字段名样式，使用Normal样式
3. **默认样式**：如果都没有，使用Word默认样式

## ✅ 测试验证

### 运行测试脚本
```bash
python test_rich_text_fields.py
```

### 测试输出示例
```
🧪 开始测试各个字段的富文本渲染功能...
✅ 成功创建样式: name
✅ 成功创建样式: student_id
✅ 成功创建样式: class_name
✅ 成功创建样式: instructor
✅ 成功创建样式: project_name

📝 处理字段: name
   内容: 张三（**优秀学生**）
✅ 为name字段应用样式: name
✅ 为name字段应用粗体: 优秀学生
✅ 成功处理name字段

🔍 验证字段渲染结果...
  - name样式段落数: 1
    - 姓名：张三（优秀学生）
  - 粗体文本数量: 5
    - 优秀学生
    - 20230001
    - 1班
    - 李老师
    - 项目
```

## 🎯 使用示例

### 示例1：基本使用
```python
# 在generate_report函数中
field_mappings = {
    "name": "张三",
    "student_id": "20230001",
    "class_name": "软件工程1班",
    "instructor": "李老师",
    "project_name": "RAG实训项目"
}
```

### 示例2：富文本使用
```python
# 包含粗体文本
field_mappings = {
    "name": "张三（**优秀学生**）",
    "student_id": "**20230001**（学号）",
    "class_name": "软件工程**1班**",
    "instructor": "**李老师**（副教授）",
    "project_name": "RAG实训**项目**"
}
```

## 🔧 自定义样式

### 修改样式属性
在Word模板中可以自定义每个字段的样式：

- **字体**：Arial, 微软雅黑, 宋体等
- **字号**：10pt, 12pt, 14pt等
- **颜色**：任意RGB颜色
- **加粗**：是/否
- **斜体**：是/否
- **下划线**：是/否

### 样式继承
字段样式会继承模板中定义的属性，确保文档风格一致。

## 🐛 常见问题

**Q: 为什么字段没有应用自定义样式？**
A: 检查模板中是否有与字段名完全相同的样式名称。

**Q: 粗体文本没有显示？**
A: 确保使用正确的格式 `**粗体文本**`，注意星号数量。

**Q: 如何添加更多字段？**
A: 在 `field_mappings` 字典中添加新字段，并在模板中创建对应的样式。

**Q: 支持哪些富文本格式？**
A: 目前支持粗体（`**文本**`），后续可以扩展支持斜体、下划线等。

## 📞 技术支持

如果遇到问题，可以：

1. 运行测试脚本检查功能
2. 查看日志输出确认样式应用
3. 检查Word模板中的样式设置
4. 确认占位符格式正确

现在您的系统可以完美支持各个字段的富文本渲染了！ 