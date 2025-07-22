import os
import aiofiles
from typing import Dict, List
from fastapi import UploadFile
import shutil

class FileUtils:
    """文件处理工具类"""
    
    @staticmethod
    async def save_uploaded_files(
        session_dir: str,
        template: UploadFile,
        markdown_files: List[UploadFile],
        doc_files: List[UploadFile],
        pdf_files: List[UploadFile],
        images: List[UploadFile]
    ) -> Dict[str, List[str]]:
        """保存上传的文件"""
        file_paths = {
            "template": "",
            "markdown_files": [],
            "docx_files": [],
            "pdf_files": [],
            "images": []
        }
        
        # 保存模板文件
        template_path = os.path.join(session_dir, f"template.{template.filename.split('.')[-1]}")
        async with aiofiles.open(template_path, 'wb') as f:
            content = await template.read()
            await f.write(content)
        file_paths["template"] = template_path
        
        # 保存Markdown文件
        for md_file in markdown_files:
            if md_file.filename:
                md_path = os.path.join(session_dir, md_file.filename)
                async with aiofiles.open(md_path, 'wb') as f:
                    content = await md_file.read()
                    await f.write(content)
                file_paths["markdown_files"].append(md_path)
        
        # 保存DOCX文件
        for doc_file in doc_files:
            if doc_file.filename:
                doc_path = os.path.join(session_dir, doc_file.filename)
                async with aiofiles.open(doc_path, 'wb') as f:
                    content = await doc_file.read()
                    await f.write(content)
                file_paths["docx_files"].append(doc_path)
        
        # 保存PDF文件
        for pdf_file in pdf_files:
            if pdf_file.filename:
                pdf_path = os.path.join(session_dir, pdf_file.filename)
                async with aiofiles.open(pdf_path, 'wb') as f:
                    content = await pdf_file.read()
                    await f.write(content)
                file_paths["pdf_files"].append(pdf_path)
        
        # 保存图片文件
        for img_file in images:
            if img_file.filename:
                img_path = os.path.join(session_dir, img_file.filename)
                async with aiofiles.open(img_path, 'wb') as f:
                    content = await img_file.read()
                    await f.write(content)
                file_paths["images"].append(img_path)
        
        return file_paths
    
    @staticmethod
    def validate_file_types(files: List[UploadFile], allowed_extensions: List[str]) -> bool:
        """验证文件类型"""
        for file in files:
            if file.filename:
                ext = os.path.splitext(file.filename)[1].lower()
                if ext not in allowed_extensions:
                    return False
        return True
    
    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """获取文件大小（MB）"""
        try:
            size_bytes = os.path.getsize(file_path)
            return size_bytes / (1024 * 1024)
        except:
            return 0
    
    @staticmethod
    def cleanup_directory(directory: str):
        """清理目录"""
        try:
            if os.path.exists(directory):
                shutil.rmtree(directory)
        except Exception as e:
            print(f"清理目录失败: {e}")
    
    @staticmethod
    def create_directory_if_not_exists(directory: str):
        """创建目录（如果不存在）"""
        os.makedirs(directory, exist_ok=True) 