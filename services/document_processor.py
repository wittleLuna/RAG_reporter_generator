import os
import re
from typing import Dict, List, Any
import markdown
from docx import Document
import PyPDF2
import io
from pathlib import Path

class DocumentProcessor:
    """文档处理服务"""
    
    def __init__(self):
        self.supported_extensions = {
            '.md': self._process_markdown,
            '.docx': self._process_docx,
            '.pdf': self._process_pdf,
            '.txt': self._process_text
        }
    
    async def process_documents(self, file_paths: Dict[str, List[str]]) -> Dict[str, Any]:
        """处理所有上传的文档"""
        content_data = {
            "markdown_content": [],
            "docx_content": [],
            "pdf_content": [],
            "all_text": "",
            "image_mappings": {}
        }
        
        # 处理Markdown文件
        for md_path in file_paths.get("markdown_files", []):
            content = await self._process_markdown(md_path)
            content_data["markdown_content"].append({
                "file": os.path.basename(md_path),
                "content": content
            })
            content_data["all_text"] += content + "\n\n"
        
        # 处理DOCX文件
        for docx_path in file_paths.get("docx_files", []):
            content = await self._process_docx(docx_path)
            content_data["docx_content"].append({
                "file": os.path.basename(docx_path),
                "content": content
            })
            content_data["all_text"] += content + "\n\n"
        
        # 处理PDF文件
        for pdf_path in file_paths.get("pdf_files", []):
            content = await self._process_pdf(pdf_path)
            content_data["pdf_content"].append({
                "file": os.path.basename(pdf_path),
                "content": content
            })
            content_data["all_text"] += content + "\n\n"
        
        # 分析图片映射关系
        content_data["image_mappings"] = self._analyze_image_mappings(
            file_paths.get("images", [])
        )
        
        return content_data
    
    async def _process_markdown(self, file_path: str) -> str:
        """处理Markdown文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 转换为HTML然后提取纯文本
            html = markdown.markdown(content)
            # 简单的HTML标签清理
            text = re.sub(r'<[^>]+>', '', html)
            return text.strip()
        except Exception as e:
            print(f"处理Markdown文件失败: {e}")
            return ""
    
    async def _process_docx(self, file_path: str) -> str:
        """处理DOCX文件"""
        try:
            doc = Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return '\n'.join(text)
        except Exception as e:
            print(f"处理DOCX文件失败: {e}")
            return ""
    
    async def _process_pdf(self, file_path: str) -> str:
        """处理PDF文件"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"处理PDF文件失败: {e}")
            return ""
    
    async def _process_text(self, file_path: str) -> str:
        """处理文本文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"处理文本文件失败: {e}")
            return ""
    
    def _analyze_image_mappings(self, image_paths: List[str]) -> Dict[str, List[str]]:
        """分析图片映射关系"""
        mappings = {}
        
        for img_path in image_paths:
            filename = os.path.basename(img_path)
            # 提取基础名称（去掉扩展名和数字）
            base_name = re.sub(r'\d+\.(png|jpg|jpeg|gif)$', '', filename)
            base_name = base_name.rstrip('_').rstrip('-')
            
            if base_name not in mappings:
                mappings[base_name] = []
            
            # 按数字排序
            mappings[base_name].append(img_path)
        
        # 对每个基础名称的图片列表按数字排序
        for base_name in mappings:
            mappings[base_name].sort(key=lambda x: self._extract_number(os.path.basename(x)))
        
        return mappings
    
    def _extract_number(self, filename: str) -> int:
        """从文件名中提取数字"""
        match = re.search(r'(\d+)', filename)
        return int(match.group(1)) if match else 0 