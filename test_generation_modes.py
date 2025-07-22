import os
import asyncio
import requests
from pathlib import Path

def create_test_files():
    """创建测试文件"""
    test_files = [
        ("machine_learning.md", """# 机器学习基础

机器学习是人工智能的一个重要分支，它使计算机能够在没有明确编程的情况下学习和改进。

## 监督学习
监督学习使用标记的训练数据来学习输入和输出之间的映射关系。常见的算法包括：
- 线性回归
- 逻辑回归
- 决策树
- 支持向量机

## 无监督学习
无监督学习处理没有标签的数据，目标是发现数据中的隐藏模式。主要方法包括：
- 聚类分析
- 降维技术
- 关联规则学习

## 深度学习
深度学习是机器学习的一个子集，使用多层神经网络来模拟人脑的学习过程。它在图像识别、自然语言处理等领域取得了突破性进展。"""),
        
        ("data_analysis.txt", """数据分析是数据科学的核心组成部分，涉及收集、清理、转换和建模数据的过程。

## 数据预处理
数据预处理是数据分析的第一步，包括：
1. 数据清洗：处理缺失值、异常值和重复数据
2. 数据转换：标准化、归一化、编码分类变量
3. 特征工程：创建新特征、选择重要特征

## 探索性数据分析
探索性数据分析（EDA）帮助理解数据的基本特征：
- 描述性统计
- 数据可视化
- 相关性分析
- 分布分析

## 统计建模
统计建模使用数学方法描述数据之间的关系：
- 回归分析
- 时间序列分析
- 假设检验
- 置信区间估计"""),
        
        ("python_programming.md", """# Python编程实践

Python是一种高级编程语言，以其简洁的语法和丰富的库生态系统而闻名。

## 基础语法
Python的基础语法特点：
- 使用缩进表示代码块
- 动态类型系统
- 面向对象编程支持
- 函数式编程特性

## 数据处理库
Python在数据处理方面有强大的库支持：
- NumPy：数值计算基础库
- Pandas：数据分析和操作
- Matplotlib：数据可视化
- Scikit-learn：机器学习算法

## 实际应用
Python在实际项目中的应用：
1. 数据科学和机器学习
2. Web开发和API构建
3. 自动化和脚本编写
4. 科学计算和仿真""")
    ]
    
    # 确保uploads目录存在
    os.makedirs("uploads", exist_ok=True)
    
    # 创建测试文件
    for filename, content in test_files:
        file_path = Path("uploads") / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 创建测试文件: {filename}")

async def test_generation_modes():
    """测试融合模式和区分模式"""
    
    # 创建测试文件
    print("1. 创建测试文件...")
    create_test_files()
    
    # 测试融合模式
    print("\n2. 测试融合模式...")
    await test_mode("fusion", "融合模式")
    
    # 测试区分模式
    print("\n3. 测试区分模式...")
    await test_mode("separate", "区分模式")

async def test_mode(mode, mode_name):
    """测试指定的生成模式"""
    
    url = "http://localhost:8000/generate_report"
    
    data = {
        "query": "基于上传的资料，生成一份关于数据科学和机器学习的实训报告",
        "name": "张三",
        "student_id": "2021001",
        "class_name": "计算机科学与技术1班",
        "instructor": "李老师",
        "project_name": "数据科学实训项目",
        "generation_mode": mode
    }
    
    try:
        print(f"  正在测试{mode_name}...")
        response = requests.post(url, data=data)
        result = response.json()
        
        if result.get("filename"):
            print(f"  ✅ {mode_name}测试成功！")
            print(f"  📄 文件名: {result['filename']}")
            print(f"  📝 生成模式: {result.get('generation_mode', '未知')}")
            
            # 显示报告预览
            report_preview = result.get("report", "")[:200] + "..." if len(result.get("report", "")) > 200 else result.get("report", "")
            print(f"  📋 报告预览: {report_preview}")
            
        else:
            print(f"  ❌ {mode_name}测试失败: {result.get('detail', '未知错误')}")
            
    except requests.exceptions.ConnectionError:
        print(f"  ❌ 无法连接到服务器，请确保应用正在运行")
    except Exception as e:
        print(f"  ❌ {mode_name}测试失败: {e}")

def main():
    """主函数"""
    print("=== 生成模式功能测试 ===\n")
    
    # 测试功能
    asyncio.run(test_generation_modes())
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main() 