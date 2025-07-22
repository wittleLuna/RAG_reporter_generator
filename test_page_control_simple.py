#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试页面控制功能
"""

from app import build_prompt

def test_page_control_prompt():
    """测试页面控制提示词生成"""
    print("🧪 测试页面控制提示词生成...")
    
    # 测试不同页数的提示词
    test_cases = [
        (2, "短报告"),
        (5, "中等报告"),
        (10, "长报告"),
        (20, "超长报告"),
        (None, "默认报告")
    ]
    
    query = "测试查询"
    context_text = "这是测试上下文内容"
    
    for target_pages, description in test_cases:
        print(f"\n📄 测试 {description} (目标页数: {target_pages or '自动'})")
        
        # 确保target_pages参数正确传递
        if target_pages is not None:
            prompt = build_prompt(query, context_text, target_pages=target_pages)
        else:
            prompt = build_prompt(query, context_text)
        
        # 检查是否包含页面控制内容
        if target_pages:
            if f"目标页数：{target_pages} 页" in prompt or f"对应 {target_pages} 页" in prompt:
                print(f"  ✅ 包含页面控制要求")
                # 检查是否包含详细要求
                if target_pages > 10:
                    if "极其详细" in prompt or "全面的技术分析" in prompt:
                        print(f"  ✅ 包含超长报告要求")
                    else:
                        print(f"  ⚠️  可能缺少超长报告要求")
            else:
                print(f"  ❌ 未包含页面控制要求")
                # 调试：打印prompt的一部分
                print(f"  🔍 Prompt片段: {prompt[800:900]}...")
        else:
            if "页面控制要求" not in prompt:
                print(f"  ✅ 自动模式，无页面控制")
            else:
                print(f"  ❌ 自动模式不应包含页面控制")
        
        print(f"  📝 提示词长度: {len(prompt)} 字符")

def main():
    """主测试函数"""
    print("🚀 开始测试页面控制功能")
    print("=" * 50)
    
    try:
        # 测试提示词生成
        test_page_control_prompt()
        
        print("\n" + "=" * 50)
        print("✅ 页面控制功能测试完成")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 