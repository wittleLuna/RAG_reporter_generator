#!/usr/bin/env python3
"""
创建示例Word模板文件
"""

from services.report_generator import ReportGenerator
import os

def create_sample_template():
    """创建示例模板"""
    generator = ReportGenerator()
    
    # 确保目录存在
    os.makedirs("templates", exist_ok=True)
    
    # 创建示例模板
    template_path = "templates/sample_template.docx"
    generator.create_sample_template(template_path)
    
    print(f"示例模板已创建: {template_path}")
    print("模板包含以下占位符:")
    print("- {{name}}: 学生姓名")
    print("- {{student_id}}: 学号")
    print("- {{class_name}}: 班级")
    print("- {{instructor}}: 指导老师")
    print("- {{project_name}}: 项目名称")
    print("- {{report_body}}: 报告正文内容")

if __name__ == "__main__":
    create_sample_template() 