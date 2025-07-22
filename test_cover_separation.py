#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试封面页分离功能
"""

import os
import shutil
from pathlib import Path

def test_cover_separation():
    """测试封面页分离功能"""
    print("🧪 开始测试封面页分离功能...")
    
    # 检查模板文件是否存在
    templates_dir = Path("templates")
    cover_template = templates_dir / "cover_template.docx"
    body_template = templates_dir / "body_template.docx"
    
    if not cover_template.exists():
        print("❌ 封面模板文件不存在，请先运行 create_sample_templates.py")
        return False
    
    if not body_template.exists():
        print("❌ 正文模板文件不存在，请先运行 create_sample_templates.py")
        return False
    
    print("✅ 模板文件检查通过")
    
    # 创建测试目录
    test_uploads = Path("test_uploads")
    test_uploads.mkdir(exist_ok=True)
    
    # 复制模板文件到测试目录
    shutil.copy(cover_template, test_uploads / "cover_template.docx")
    shutil.copy(body_template, test_uploads / "body_template.docx")
    
    # 创建测试资料文件
    test_md = test_uploads / "test_data.md"
    with open(test_md, 'w', encoding='utf-8') as f:
        f.write("""
# 测试项目

这是一个测试项目，用于验证封面页分离功能。

## 项目概述

本项目主要测试以下功能：
1. 封面模板识别
2. 正文模板识别
3. 文档合并功能

## 技术实现

使用Python和docxcompose库实现文档合并。
        """)
    
    print("✅ 测试文件准备完成")
    print(f"📁 测试目录: {test_uploads.absolute()}")
    print("📄 测试文件:")
    print("  - cover_template.docx (封面模板)")
    print("  - body_template.docx (正文模板)")
    print("  - test_data.md (测试资料)")
    
    print("\n💡 测试步骤:")
    print("1. 启动应用: python app.py")
    print("2. 访问: http://localhost:8000")
    print("3. 上传测试文件")
    print("4. 填写基本信息")
    print("5. 生成报告")
    print("6. 检查生成的报告是否包含封面和正文")
    
    return True

if __name__ == "__main__":
    test_cover_separation() 