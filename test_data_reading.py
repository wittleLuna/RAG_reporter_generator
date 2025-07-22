#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据读取功能修复
"""

import os
import tempfile
from pathlib import Path

# 模拟app.py中的函数
TEXT_FILE_EXTENSIONS = {'.txt', '.md', '.markdown', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv', '.log', '.ini', '.conf', '.yaml', '.yml'}

def is_text_file(file_path):
    """判断是否为文本文件"""
    return file_path.suffix.lower() in TEXT_FILE_EXTENSIONS

def read_text_file_content(file_path):
    """安全读取文本文件内容"""
    try:
        # 尝试多种编码
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    # 检查内容是否包含大量不可打印字符（可能是二进制文件）
                    if len(content) > 0 and len([c for c in content if ord(c) < 32 and c not in '\n\r\t']) / len(content) < 0.1:
                        return content
            except UnicodeDecodeError:
                continue
        return None
    except Exception as e:
        print(f"无法读取文件 {file_path}: {e}")
        return None

def test_data_reading():
    """测试数据读取功能"""
    print("🧪 开始测试数据读取功能...")
    
    # 创建临时测试目录
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir) / "uploads"
        test_dir.mkdir()
        
        # 创建测试文件
        test_files = {
            "test.txt": "这是一个测试文本文件\n包含中文内容",
            "test.md": "# 测试Markdown\n- 项目1\n- 项目2",
            "test.py": "print('Hello World')\n# 这是Python代码",
            "test.json": '{"name": "test", "value": 123}',
            "test.jpg": b"\xff\xd8\xff\xe0",  # 模拟JPEG文件头
            "test.png": b"\x89PNG\r\n\x1a\n",  # 模拟PNG文件头
            "test.docx": b"PK\x03\x04",  # 模拟DOCX文件头
        }
        
        # 写入测试文件
        for filename, content in test_files.items():
            file_path = test_dir / filename
            if isinstance(content, str):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            else:
                with open(file_path, 'wb') as f:
                    f.write(content)
        
        print(f"📁 创建测试目录: {test_dir}")
        print(f"📄 创建测试文件: {list(test_files.keys())}")
        
        # 测试文件过滤和读取
        documents = []
        template_path = None
        
        for file_path in test_dir.glob("*"):
            if file_path.is_file():
                print(f"\n🔍 处理文件: {file_path.name}")
                
                # 检查是否为模板文件
                if file_path.suffix.lower() in ['.docx', '.doc']:
                    if not template_path or file_path.suffix.lower() == '.docx':
                        template_path = str(file_path)
                    print(f"  ✅ 识别为模板文件: {file_path.name}")
                    continue
                
                # 检查是否为文本文件
                if is_text_file(file_path):
                    print(f"  📝 识别为文本文件: {file_path.name}")
                    content = read_text_file_content(file_path)
                    if content:
                        documents.append({
                            "content": content,
                            "source": str(file_path),
                            "type": file_path.suffix
                        })
                        print(f"  ✅ 成功读取: {file_path.name} (长度: {len(content)}字符)")
                    else:
                        print(f"  ❌ 读取失败: {file_path.name}")
                else:
                    print(f"  🖼️  跳过非文本文件: {file_path.name}")
        
        # 输出结果
        print(f"\n📊 测试结果:")
        print(f"  - 模板文件: {template_path or '无'}")
        print(f"  - 成功读取的文本文档: {len(documents)}个")
        
        for doc in documents:
            print(f"    - {Path(doc['source']).name}: {len(doc['content'])}字符")
        
        # 验证结果
        expected_text_files = ['test.txt', 'test.md', 'test.py', 'test.json']
        actual_text_files = [Path(doc['source']).name for doc in documents]
        
        if set(actual_text_files) == set(expected_text_files):
            print("✅ 测试通过！所有文本文件都被正确识别和读取")
        else:
            print("❌ 测试失败！文件识别结果不符合预期")
            print(f"  期望: {expected_text_files}")
            print(f"  实际: {actual_text_files}")
        
        if template_path and Path(template_path).name == 'test.docx':
            print("✅ 模板文件识别正确")
        else:
            print("❌ 模板文件识别失败")

if __name__ == "__main__":
    test_data_reading() 