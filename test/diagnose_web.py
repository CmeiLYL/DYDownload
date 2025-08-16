#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Web界面诊断脚本
"""

import requests
import json
from pathlib import Path

def diagnose_web_ui():
    """诊断Web界面问题"""
    print("=" * 60)
    print("Web界面诊断工具")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # 1. 检查服务器是否运行
    print("\n1. 检查服务器状态...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✓ 服务器正在运行")
        else:
            print(f"✗ 服务器响应异常: {response.status_code}")
            return
    except Exception as e:
        print(f"✗ 无法连接到服务器: {e}")
        print("请确保服务器正在运行: python run_web.py")
        return
    
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
                for file in files[:10]:  # 只分析前10个文件
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
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"✗ 文件API测试失败: {e}")
    
    # 3. 测试缩略图API
    print("\n3. 测试缩略图API...")
    try:
        # 先获取一个图片文件
        response = requests.get(f"{base_url}/api/files")
        if response.status_code == 200:
            files = response.json()
            image_files = [f for f in files if f['name'].lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
            
            if image_files:
                test_file = image_files[0]
                image_path = test_file['path'].replace('\\', '/')
                
                thumbnail_url = f"{base_url}/api/file/thumbnail?path={image_path}"
                thumbnail_response = requests.get(thumbnail_url, timeout=10)
                
                if thumbnail_response.status_code == 200:
                    content_type = thumbnail_response.headers.get('content-type', '')
                    if 'image' in content_type:
                        print(f"✓ 缩略图API正常")
                        print(f"  测试文件: {test_file['name']}")
                        print(f"  内容类型: {content_type}")
                        print(f"  文件大小: {len(thumbnail_response.content)} bytes")
                    else:
                        print(f"✗ 缩略图内容类型错误: {content_type}")
                else:
                    print(f"✗ 缩略图API异常: {thumbnail_response.status_code}")
            else:
                print("⚠ 没有找到图片文件进行测试")
        else:
            print("✗ 无法获取文件列表进行缩略图测试")
    except Exception as e:
        print(f"✗ 缩略图API测试失败: {e}")
    
    # 4. 测试日志API
    print("\n4. 测试日志API...")
    try:
        response = requests.get(f"{base_url}/api/logs", timeout=5)
        if response.status_code == 200:
            logs = response.json()
            print(f"✓ 日志API正常，获取到 {len(logs)} 条日志")
            
            if logs:
                print("最新日志:")
                for log in logs[-3:]:
                    print(f"  - {log.strip()}")
        else:
            print(f"✗ 日志API异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 日志API测试失败: {e}")
    
    # 5. 测试配置API
    print("\n5. 测试配置API...")
    try:
        response = requests.get(f"{base_url}/api/config", timeout=5)
        if response.status_code == 200:
            config = response.json()
            print("✓ 配置API正常")
            print(f"  下载路径: {config.get('path', '未设置')}")
            print(f"  链接数量: {len(config.get('link', []))}")
        else:
            print(f"✗ 配置API异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 配置API测试失败: {e}")
    
    # 6. 检查静态文件
    print("\n6. 检查静态文件...")
    static_files = [
        "/static/app.js",
        "/static/app_simple.js",
        "/test_fix.js"
    ]
    
    for static_file in static_files:
        try:
            response = requests.get(f"{base_url}{static_file}", timeout=5)
            if response.status_code == 200:
                print(f"✓ {static_file} 可访问")
            else:
                print(f"✗ {static_file} 不可访问: {response.status_code}")
        except Exception as e:
            print(f"✗ {static_file} 访问失败: {e}")
    
    # 7. 检查下载目录
    print("\n7. 检查下载目录...")
    download_path = Path("./Downloaded")
    if download_path.exists():
        print(f"✓ 下载目录存在: {download_path.absolute()}")
        
        # 统计文件数量
        file_count = 0
        for _ in download_path.rglob('*'):
            if _.is_file():
                file_count += 1
        
        print(f"  文件总数: {file_count}")
        
        # 检查子目录
        subdirs = [d for d in download_path.iterdir() if d.is_dir()]
        print(f"  子目录数量: {len(subdirs)}")
        
        if subdirs:
            print("  子目录列表:")
            for subdir in subdirs[:5]:  # 只显示前5个
                subdir_files = len(list(subdir.rglob('*')))
                print(f"    - {subdir.name}: {subdir_files} 个文件")
            
            if len(subdirs) > 5:
                print(f"    ... 还有 {len(subdirs) - 5} 个目录")
    else:
        print(f"✗ 下载目录不存在: {download_path.absolute()}")
    
    print("\n" + "=" * 60)
    print("诊断完成")
    print("=" * 60)
    
    print("\n建议:")
    print("1. 如果API测试都通过，问题可能在前端JavaScript")
    print("2. 打开浏览器开发者工具查看控制台错误")
    print("3. 检查网络面板中的API请求")
    print("4. 确保所有静态文件都能正常加载")

if __name__ == '__main__':
    diagnose_web_ui() 