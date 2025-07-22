#!/usr/bin/env python3
"""
RAG实训报告生成系统测试脚本
"""

import requests
import json
import time
from pathlib import Path

# 测试配置
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123",
    "name": "测试用户",
    "student_id": "2024001",
    "class_name": "计算机科学1班"
}

def test_server_health():
    """测试服务器健康状态"""
    print("🔍 测试服务器健康状态...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✓ 服务器运行正常")
            return True
        else:
            print(f"✗ 服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到服务器，请确保服务器已启动")
        return False

def test_user_registration():
    """测试用户注册"""
    print("\n📝 测试用户注册...")
    try:
        response = requests.post(f"{BASE_URL}/register", data=TEST_USER)
        if response.status_code == 200:
            print("✓ 用户注册成功")
            return True
        else:
            print(f"✗ 用户注册失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 注册请求失败: {e}")
        return False

def test_user_login():
    """测试用户登录"""
    print("\n🔐 测试用户登录...")
    try:
        login_data = {
            "username": TEST_USER["username"],
            "password": TEST_USER["password"]
        }
        response = requests.post(f"{BASE_URL}/login", data=login_data)
        if response.status_code == 200:
            print("✓ 用户登录成功")
            return True
        else:
            print(f"✗ 用户登录失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 登录请求失败: {e}")
        return False

def test_template_management():
    """测试模板管理功能"""
    print("\n📋 测试模板管理...")
    try:
        # 获取模板列表
        response = requests.get(f"{BASE_URL}/templates")
        if response.status_code == 200:
            print("✓ 模板列表获取成功")
            return True
        else:
            print(f"✗ 模板列表获取失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 模板管理测试失败: {e}")
        return False

def test_report_generation():
    """测试报告生成功能"""
    print("\n🤖 测试报告生成...")
    try:
        # 创建测试数据
        test_data = {
            "name": TEST_USER["name"],
            "student_id": TEST_USER["student_id"],
            "class_name": TEST_USER["class_name"],
            "project_name": "测试课程",
            "instructor": "测试导师",
            "textbook": "测试教材",
            "lab": "测试实验室",
            "finish_date": "2025-01-01",
            "generation_mode": "fusion",
            "target_pages": "3",
            "multi_round_completion": "true"
        }
        
        # 创建测试文件
        test_file_path = Path("test_data.txt")
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("这是一个测试文档，用于验证报告生成功能。")
        
        # 发送报告生成请求
        with open(test_file_path, "rb") as f:
            files = {"data_files": f}
            response = requests.post(f"{BASE_URL}/generate_report", data=test_data, files=files)
        
        # 清理测试文件
        test_file_path.unlink()
        
        if response.status_code == 200:
            print("✓ 报告生成请求成功")
            return True
        else:
            print(f"✗ 报告生成失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 报告生成测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("🧪 开始系统功能测试")
    print("=" * 50)
    
    tests = [
        ("服务器健康状态", test_server_health),
        ("用户注册", test_user_registration),
        ("用户登录", test_user_login),
        ("模板管理", test_template_management),
        ("报告生成", test_report_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            time.sleep(1)  # 避免请求过于频繁
        except Exception as e:
            print(f"✗ {test_name}测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常")
    else:
        print("⚠️  部分测试失败，请检查系统配置")

if __name__ == "__main__":
    run_all_tests() 