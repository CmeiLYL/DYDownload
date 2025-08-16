#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Web界面修复验证脚本
"""

import requests
import json
from pathlib import Path

def test_web_fix():
    """测试Web界面修复"""
    print("=" * 60)
    print("Web界面修复验证")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # 1. 测试静态文件访问
    print("\n1. 测试静态文件访问...")
    static_files = [
        "/static/app.js",
        "/static/app_simple.js"
    ]
    
    for static_file in static_files:
        try:
            response = requests.get(f"{base_url}{static_file}", timeout=5)
            if response.status_code == 200:
                print(f"✓ {static_file} 可访问")
                # 检查文件内容是否包含新的函数名
                content = response.text
                if 'fileRefreshFiles' in content:
                    print(f"  ✓ 包含新的函数名: fileRefreshFiles")
                else:
                    print(f"  ⚠ 未找到新的函数名")
            else:
                print(f"✗ {static_file} 不可访问: {response.status_code}")
        except Exception as e:
            print(f"✗ {static_file} 访问失败: {e}")
    
    # 2. 测试文件API
    print("\n2. 测试文件API...")
    try:
        response = requests.get(f"{base_url}/api/files", timeout=10)
        if response.status_code == 200:
            files = response.json()
            print(f"✓ 文件API正常，获取到 {len(files)} 个文件")
            
            if files:
                # 分析文件路径结构
                path_analysis = {}
                for file in files[:5]:  # 只分析前5个文件
                    path = file.get('path', '')
                    parts = path.replace('\\', '/').split('/')
                    if len(parts) > 1:
                        first_dir = parts[0]
                        path_analysis[first_dir] = path_analysis.get(first_dir, 0) + 1
                
                print("文件路径分析:")
                for dir_name, count in path_analysis.items():
                    print(f"  - {dir_name}: {count} 个文件")
        else:
            print(f"✗ 文件API异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 文件API测试失败: {e}")
    
    # 3. 测试主页访问
    print("\n3. 测试主页访问...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✓ 主页可访问")
            content = response.text
            
            # 检查是否包含新的函数名
            if 'fileRefreshFiles' in content:
                print("  ✓ HTML包含新的函数名")
            else:
                print("  ⚠ HTML未包含新的函数名")
                
            # 检查是否包含文件管理相关的元素
            if 'filesContainer' in content:
                print("  ✓ 包含文件容器元素")
            else:
                print("  ⚠ 未找到文件容器元素")
        else:
            print(f"✗ 主页访问异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 主页访问失败: {e}")
    
    print("\n" + "=" * 60)
    print("验证完成")
    print("=" * 60)
    
    print("\n下一步:")
    print("1. 打开浏览器访问 http://localhost:5000")
    print("2. 切换到'文件'标签页")
    print("3. 检查是否正常显示文件列表")
    print("4. 测试筛选、排序、分页功能")
    print("5. 检查浏览器控制台是否有错误")

if __name__ == '__main__':
    test_web_fix() 