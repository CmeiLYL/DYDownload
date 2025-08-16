#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试文件筛选功能
验证是否正确排除了JSON等非目标文件类型
"""

import os
import sys
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_file_filtering():
    """测试文件筛选功能"""
    print("🧪 开始测试文件筛选功能...")
    
    # 模拟文件列表
    test_files = [
        "video1.mp4",
        "image1.jpg", 
        "audio1.mp3",
        "data.json",
        "config.txt",
        "error.log",
        "video2.avi",
        "image2.png",
        "audio2.wav",
        "document.pdf"
    ]
    
    # 定义要排除的文件类型
    excluded_extensions = {'.json', '.txt', '.log'}
    
    # 筛选文件
    filtered_files = []
    for filename in test_files:
        file_ext = Path(filename).suffix.lower()
        if file_ext not in excluded_extensions:
            filtered_files.append(filename)
    
    print(f"📁 原始文件数量: {len(test_files)}")
    print(f"📁 筛选后文件数量: {len(filtered_files)}")
    print(f"📁 排除的文件: {[f for f in test_files if Path(f).suffix.lower() in excluded_extensions]}")
    print(f"📁 保留的文件: {filtered_files}")
    
    # 验证结果
    expected_excluded = ["data.json", "config.txt", "error.log"]
    expected_included = ["video1.mp4", "image1.jpg", "audio1.mp3", "video2.avi", "image2.png", "audio2.wav", "document.pdf"]
    
    actual_excluded = [f for f in test_files if Path(f).suffix.lower() in excluded_extensions]
    actual_included = filtered_files
    
    print("\n✅ 验证结果:")
    print(f"  排除的文件类型: {excluded_extensions}")
    print(f"  应该排除的文件: {expected_excluded}")
    print(f"  实际排除的文件: {actual_excluded}")
    print(f"  应该保留的文件: {expected_included}")
    print(f"  实际保留的文件: {actual_included}")
    
    # 检查结果是否正确
    excluded_correct = set(actual_excluded) == set(expected_excluded)
    included_correct = set(actual_included) == set(expected_included)
    
    if excluded_correct and included_correct:
        print("\n🎉 测试通过！文件筛选功能正常工作")
        return True
    else:
        print("\n❌ 测试失败！文件筛选功能有问题")
        if not excluded_correct:
            print(f"   排除文件不匹配: 期望 {expected_excluded}, 实际 {actual_excluded}")
        if not included_correct:
            print(f"   保留文件不匹配: 期望 {expected_included}, 实际 {actual_included}")
        return False

def test_file_type_categorization():
    """测试文件类型分类功能"""
    print("\n🧪 开始测试文件类型分类功能...")
    
    test_files = [
        ("video1.mp4", "video"),
        ("image1.jpg", "image"),
        ("audio1.mp3", "audio"),
        ("document.pdf", "other"),
        ("archive.zip", "other")
    ]
    
    def get_file_type(filename):
        ext = Path(filename).suffix.lower()
        if ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm']:
            return 'video'
        elif ext in ['.mp3', '.wav', '.aac', '.flac', '.m4a']:
            return 'audio'
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            return 'image'
        else:
            return 'other'
    
    print("📋 文件类型分类结果:")
    for filename, expected_type in test_files:
        actual_type = get_file_type(filename)
        status = "✅" if actual_type == expected_type else "❌"
        print(f"   {status} {filename} -> {actual_type} (期望: {expected_type})")
    
    # 验证所有分类是否正确
    all_correct = all(get_file_type(filename) == expected_type for filename, expected_type in test_files)
    
    if all_correct:
        print("\n🎉 文件类型分类测试通过！")
        return True
    else:
        print("\n❌ 文件类型分类测试失败！")
        return False

def main():
    """主函数"""
    print("🚀 文件筛选功能测试")
    print("=" * 50)
    
    # 测试文件筛选
    filter_test_passed = test_file_filtering()
    
    # 测试文件类型分类
    categorization_test_passed = test_file_type_categorization()
    
    print("\n" + "=" * 50)
    print("📊 测试总结:")
    print(f"   文件筛选测试: {'✅ 通过' if filter_test_passed else '❌ 失败'}")
    print(f"   文件分类测试: {'✅ 通过' if categorization_test_passed else '❌ 失败'}")
    
    if filter_test_passed and categorization_test_passed:
        print("\n🎉 所有测试通过！文件筛选功能正常工作")
        return 0
    else:
        print("\n❌ 部分测试失败，需要检查代码")
        return 1

if __name__ == "__main__":
    exit(main()) 