# 代码块样式使用指南

## 🎯 功能说明

系统现在支持使用自定义的"Code"样式来渲染被```包裹的代码块内容。如果模板中存在"Code"样式，系统会优先使用；如果不存在，则使用默认的代码块样式。

## 📋 样式优先级

### 代码块样式优先级
1. **Code** (自定义代码样式)
2. **List Paragraph** (列表段落样式)
3. **Normal** (普通段落样式)

### 其他样式优先级
- **标题1**: Heading 1 → 标题 1 → Normal
- **标题2**: Heading 2 → 标题 2 → Normal  
- **列表**: List Paragraph → 项目符号 → Normal
- **正文**: Normal → 正文

## 🔧 如何创建自定义Code样式

### 方法一：在Word模板中创建
1. 打开你的Word模板文件
2. 点击"样式"面板中的"新建样式"
3. 样式名称设置为：**Code**
4. 设置样式属性：
   - 字体：Consolas（等宽字体）
   - 字号：10pt
   - 颜色：深灰色
   - 背景：浅灰色
   - 边框：可选添加边框
5. 保存模板

### 方法二：使用现有样式
如果你想使用其他现有样式作为代码块样式，可以：
1. 在模板中重命名某个样式为"Code"
2. 或者修改代码中的样式优先级列表

## 📝 代码实现

```python
def get_style(doc, style_names):
    """获取存在的样式名，支持多个备选样式名"""
    for style_name in style_names:
        try:
            doc.styles[style_name]
            return style_name
        except KeyError:
            continue
    return None

# 代码块样式优先级
code_style = get_style(doc, ['Code', 'List Paragraph', 'Normal'])

# 渲染代码块
if code_style:
    p.style = code_style
    logger.info(f"使用自定义Code样式: {code_style}")
else:
    # 使用默认样式并设置字体
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(64, 64, 64)
    logger.info("使用默认代码块样式")
```

## ✅ 测试验证

运行测试脚本可以验证样式功能：

```bash
python test_rich_text_rendering.py
```

测试输出会显示：
- 可用的样式列表
- 代码块使用的具体样式
- 渲染结果验证

## 🎨 样式效果对比

### 使用自定义Code样式
- 代码块会应用模板中定义的"Code"样式
- 保持模板的一致性
- 支持复杂的样式设置（背景、边框等）

### 使用默认样式
- 代码块使用等宽字体（Consolas）
- 灰色文字（RGB: 64,64,64）
- 10pt字号
- 简洁的代码显示效果

## 🔄 兼容性说明

- **中英文样式名兼容**：系统会自动检测中英文样式名
- **样式不存在时的降级**：如果指定样式不存在，会自动使用备选样式
- **模板独立性**：每个模板可以有自己的样式定义

## 📞 使用建议

1. **推荐**：在模板中创建专门的"Code"样式，确保代码块显示效果一致
2. **备选**：如果没有自定义样式，系统会自动使用默认的代码块样式
3. **调试**：查看日志输出，确认实际使用的样式名称

## 🐛 常见问题

**Q: 为什么代码块没有使用我创建的Code样式？**
A: 检查样式名称是否完全匹配"Code"（区分大小写），或者查看日志确认实际使用的样式。

**Q: 如何修改样式优先级？**
A: 修改`get_style(doc, ['Code', 'List Paragraph', 'Normal'])`中的样式名列表顺序。

**Q: 支持哪些样式属性？**
A: 支持Word的所有段落样式属性，包括字体、字号、颜色、背景、边框等。 