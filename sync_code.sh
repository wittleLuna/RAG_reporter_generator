#!/bin/bash

echo "🔄 同步代码到服务器..."
echo "==============================="

# 1. 停止现有服务
echo "🛑 停止现有服务..."
pkill -f uvicorn || true

# 2. 备份当前代码
echo "📦 备份当前代码..."
if [ -d "backup_$(date +%Y%m%d_%H%M%S)" ]; then
    rm -rf backup_$(date +%Y%m%d_%H%M%S)
fi
cp -r . backup_$(date +%Y%m%d_%H%M%S)

# 3. 检查关键文件
echo "🔍 检查关键文件..."
files_to_check=(
    "app.py"
    "services/ai_service_latest.py"
    "services/__init__.py"
    "test_latest_ai.py"
    "deploy_latest.sh"
    ".env"
)

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 不存在"
    fi
done

# 4. 检查services目录
echo ""
echo "📁 检查services目录..."
if [ -d "services" ]; then
    echo "services目录存在，包含文件："
    ls -la services/
else
    echo "❌ services目录不存在"
    mkdir -p services
fi

# 5. 重新创建__init__.py
echo ""
echo "🔧 确保__init__.py存在..."
if [ ! -f "services/__init__.py" ]; then
    echo "# services package" > services/__init__.py
    echo "✅ 创建services/__init__.py"
else
    echo "✅ services/__init__.py已存在"
fi

# 6. 检查Python路径
echo ""
echo "🐍 检查Python路径..."
python3 -c "import sys; print('Python路径:'); [print(p) for p in sys.path]"

# 7. 测试导入
echo ""
echo "🧪 测试模块导入..."
python3 -c "
import sys
import os
sys.path.append(os.getcwd())
try:
    from services.ai_service_latest import AIService
    print('✅ ai_service_latest 导入成功')
except ImportError as e:
    print(f'❌ 导入失败: {e}')
    print('当前目录:', os.getcwd())
    print('services目录内容:', os.listdir('services') if os.path.exists('services') else '不存在')
"

# 8. 如果导入失败，重新创建文件
echo ""
echo "📝 如果导入失败，重新创建ai_service_latest.py..."
if ! python3 -c "from services.ai_service_latest import AIService" 2>/dev/null; then
    echo "重新创建ai_service_latest.py..."
    cat > services/ai_service_latest.py << 'EOF'
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
            
            # 使用最新版本OpenAI客户端调用聊天API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=4000,
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
EOF
    echo "✅ ai_service_latest.py 重新创建完成"
fi

# 9. 再次测试导入
echo ""
echo "🧪 再次测试模块导入..."
python3 -c "
import sys
import os
sys.path.append(os.getcwd())
try:
    from services.ai_service_latest import AIService
    print('✅ ai_service_latest 导入成功')
except ImportError as e:
    print(f'❌ 导入失败: {e}')
"

# 10. 启动服务
echo ""
echo "🚀 启动服务..."
nohup uvicorn app:app --host 0.0.0.0 --port 8000 --reload > logs/app.log 2>&1 &

# 等待启动
sleep 5

# 检查服务状态
if pgrep -f uvicorn > /dev/null; then
    echo "✅ 服务启动成功"
    echo "🌐 访问地址: http://47.109.24.229:8000"
else
    echo "❌ 服务启动失败，查看日志:"
    tail -n 10 logs/app.log
fi

echo ""
echo "📝 查看实时日志:"
echo "tail -f logs/app.log" 