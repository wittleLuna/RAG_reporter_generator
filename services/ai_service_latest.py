import os
import json
import asyncio
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
import hashlib
from openai import OpenAI
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
        
        # 初始化OpenAI客户端（最新版本）
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
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
            # 使用最新版本OpenAI客户端获取embedding
            response = self.client.embeddings.create(
                input=[text],
                dimensions=1024,
                model=self.embedding_model,
                encoding_format="float"
            )
            
            embedding = response.data[0].embedding
            print(f"✅ 成功获取embedding，维度: {len(embedding)}")
            return embedding
            
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
            
            # 获取所有文档的embeddings
            embeddings = []
            for text in texts:
                embedding = await self.get_embeddings(text)
                embeddings.append(embedding)
            
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

    async def generate_report_with_prompt(self, query: str, custom_prompt: str, target_pages: int = None) -> str:
        """使用自定义Prompt生成报告"""
        try:
            # 根据目标页数调整max_tokens
            if target_pages and target_pages > 0:
                # 估算每个页面的token数（中文约1.5字符=1token）
                if target_pages <= 3:
                    max_tokens = 2000
                elif target_pages <= 6:
                    max_tokens = 4000
                elif target_pages <= 10:
                    max_tokens = 8000
                elif target_pages <= 15:
                    max_tokens = 8192  # 限制最大值
                else:
                    max_tokens = 8192
            else:
                max_tokens = 4000
            max_tokens = min(max_tokens, 8192)  # 再次保险
            print(f"📄 目标页数: {target_pages or '自动'}, 设置max_tokens: {max_tokens}")
            # 直接使用传入的自定义Prompt调用API
            report = await self._call_qwen_api(custom_prompt, max_tokens)
            return report
        except Exception as e:
            print(f"❌ 使用自定义Prompt生成报告失败: {e}")
            return f"生成报告时出现错误: {str(e)}"

    async def generate_report(self, query: str, context: List[str]) -> str:
        """生成报告（保持向后兼容）"""
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
        
        prompt = f"""你是一位实训报告自动生成助手，任务是将以下资料整合为一篇结构清晰、语言通顺、格式严格的 Markdown 报告。请严格按照以下格式要求生成内容：

【格式规则】（必须遵守）：
1. 只允许使用以下 Markdown 符号：`#`（一级标题）、`##`（二级标题）、`###`（三级标题）、```（代码块）、`-`（用于非编号列表）。
2. 禁止使用以下内容：
   - 禁止使用 `---` 分割段落（在每个段落的最后）；
   - 禁止使用 `#####`及以后的标题；
   - 禁止使用 HTML 标签（如 `<p>`、`<br>`）；
   - 禁止写"希望本报告对你有所帮助"等客套话。
   - 禁止在报告标题使用如"实训报告：xxx"的格式，直接写报告名
   - 禁止出现：' • **文本内容** ' 的格式, '•' 和 **xxx** 只能单独出现
3. 段落编号请使用 `1.`、`2.`、`3.` 的方式，**不要使用 `-` 和 '•' 作为编号列表**。
4. **图片插入格式为：`{{image:img_x}}`，如：`{{image:img_1}}`，必须出现在内容合适位置**。
5. 所有代码必须使用成对的 ``` 包裹，并保持原始缩进。
6. 除特殊说明外，请保持语气正式、中性、信息导向。
7. 在参考资料的基础上拓展内容，丰富报告的内容

【任务说明】：
请根据以下查询和资料内容，整合撰写实训报告：

查询问题：
{query}

相关资料（供参考）：
{context_text}

请根据内容撰写包含以下部分的报告：
1. 概述
2. 详细分析（可以多小节）
3. 结论与建议
4. 如有必要，可增加技术过程、图示描述等补充部分

最终请输出一段**结构良好、格式准确、内容严谨的 Markdown 报告**，无需说明"报告结束"等语句。"""

        return prompt

    async def _call_qwen_api(self, prompt: str, max_tokens: int) -> str:
        """调用千问API生成报告内容"""
        try:
            print(f"调用千问API生成报告...")
            
            # 使用最新版本OpenAI客户端调用聊天API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=max_tokens,
                top_p=0.9
            )
            
            content = response.choices[0].message.content
            print(f"✅ 成功生成报告内容，长度: {len(content)}")
            return content
            
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