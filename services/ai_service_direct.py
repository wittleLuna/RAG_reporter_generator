import os
import json
import asyncio
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
import hashlib
import aiohttp
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class AIService:
    def __init__(self):
        """初始化AI服务"""
        self.api_key = os.getenv("AI_API_KEY", "sk-442562cd6b6b4b2896ebdac8ce8d047e")
        self.base_url = os.getenv("AI_API_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        self.model_name = os.getenv("AI_MODEL_NAME", "qwen-plus")
        self.embedding_model = os.getenv("AI_EMBEDDING_MODEL", "text-embedding-v3")
        
        # 初始化ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=Settings(anonymized_telemetry=False)
        )
        
        # 获取或创建集合
        self.collection = self.chroma_client.get_or_create_collection(
            name="report_documents",
            metadata={"description": "实训报告文档向量存储"}
        )
        
        print(f"AI服务初始化完成 - 模型: {self.model_name}, Embedding模型: {self.embedding_model}")

    async def get_embeddings(self, text: str) -> List[float]:
        """获取文本的向量表示"""
        try:
            # 直接使用aiohttp调用embedding API
            payload = {
                "model": self.embedding_model,
                "input": [text],
                "dimensions": 1024,
                "encoding_format": "float"
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    json=payload,
                    headers=headers,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if "data" in result and len(result["data"]) > 0:
                            embedding = result["data"][0]["embedding"]
                            print(f"✅ 成功获取embedding，维度: {len(embedding)}")
                            return embedding
                    
                    # 如果API调用失败，使用备用方案
                    print(f"❌ Embedding API调用失败: {response.status}")
                    return self._fallback_embedding(text)
            
        except Exception as e:
            print(f"❌ Embedding API调用失败: {e}")
            # 使用简单的哈希作为备用方案
            return self._fallback_embedding(text)

    def _fallback_embedding(self, text: str) -> List[float]:
        """备用embedding方法"""
        # 使用简单的哈希生成1024维向量
        hash_obj = hashlib.sha256(text.encode())
        hash_hex = hash_obj.hexdigest()
        
        # 将哈希转换为1024维向量
        embedding = []
        for i in range(1024):
            start = (i * 2) % len(hash_hex)
            end = start + 2
            if end > len(hash_hex):
                end = len(hash_hex)
            hex_part = hash_hex[start:end]
            if len(hex_part) < 2:
                hex_part = hex_part + "0" * (2 - len(hex_part))
            value = int(hex_part, 16) / 255.0  # 归一化到0-1
            embedding.append(value)
        
        print(f"使用备用embedding方法，维度: {len(embedding)}")
        return embedding

    async def add_documents_to_vectorstore(self, documents: List[Dict[str, Any]]):
        """将文档添加到向量数据库"""
        try:
            texts = [doc["content"] for doc in documents]
            metadatas = [{"source": doc["source"], "type": doc["type"]} for doc in documents]
            ids = [f"doc_{i}_{hash(doc['source'])}" for i, doc in enumerate(documents)]
            
            # 获取embeddings
            embeddings = await self.get_embeddings(texts[0])
            
            # 添加到ChromaDB
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"成功添加 {len(documents)} 个文档到向量数据库")
            
        except Exception as e:
            print(f"添加文档到向量数据库失败: {e}")

    async def search_similar_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """搜索相似文档"""
        try:
            # 获取查询的embedding
            query_embeddings = await self.get_embeddings(query)
            
            # 在ChromaDB中搜索
            results = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=top_k
            )
            
            # 格式化结果
            similar_docs = []
            if results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    similar_docs.append({
                        "content": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] and results["metadatas"][0] else {},
                        "distance": results["distances"][0][i] if results["distances"] and results["distances"][0] else 0
                    })
            
            return similar_docs
            
        except Exception as e:
            print(f"搜索相似文档失败: {e}")
            return []

    async def generate_report(self, query: str, context: List[str]) -> str:
        """生成报告"""
        try:
            # 构建提示词
            prompt = self._build_prompt(query, context)
            
            # 调用API生成报告
            report = await self._call_qwen_api(prompt)
            
            return report
            
        except Exception as e:
            print(f"❌ 生成报告失败: {e}")
            return f"生成报告时出现错误: {str(e)}"

    def _build_prompt(self, query: str, context: List[str]) -> str:
        """构建提示词"""
        context_text = "\n\n".join(context)
        
        prompt = f"""基于以下信息生成一份详细的报告：

查询问题：{query}

相关信息：
{context_text}

请生成一份结构化的报告，包含以下部分：
1. 概述
2. 详细分析
3. 结论和建议

请确保报告内容准确、详细且易于理解。"""

        return prompt

    async def _call_qwen_api(self, prompt: str) -> str:
        """调用千问API生成报告内容"""
        try:
            print(f"调用千问API生成报告...")
            
            # 直接使用aiohttp调用聊天API
            payload = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 4000,
                "top_p": 0.9
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    json=payload,
                    headers=headers,
                    timeout=60
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if "choices" in result and len(result["choices"]) > 0:
                            content = result["choices"][0]["message"]["content"]
                            print(f"✅ 成功生成报告内容，长度: {len(content)}")
                            return content
                    
                    # 如果API调用失败，返回错误信息
                    error_text = await response.text()
                    print(f"❌ 千问API调用失败: {response.status}, {error_text}")
                    return f"抱歉，生成报告时出现错误: API调用失败 ({response.status})"
            
        except Exception as e:
            print(f"❌ 千问API调用失败: {e}")
            return f"抱歉，生成报告时出现错误: {str(e)}"

    async def clear_vectorstore(self):
        """清空向量数据库"""
        try:
            self.chroma_client.delete_collection("report_documents")
            self.collection = self.chroma_client.create_collection(
                name="report_documents",
                metadata={"description": "实训报告文档向量存储"}
            )
            print("向量数据库已清空")
        except Exception as e:
            print(f"清空向量数据库失败: {e}") 