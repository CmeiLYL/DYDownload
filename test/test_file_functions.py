#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试文件功能
"""

import os
import requests
import json
from pathlib import Path

def test_file_operations():
    """测试文件相关功能"""
    print("=" * 50)
    print("测试文件功能")
    print("=" * 50)
    
    # 检查服务器是否运行
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code != 200:
            print("✗ 服务器未正常运行")
            return
    except:
        print("✗ 无法连接到服务器，请先启动Web UI")
        return
    
    print("✓ 服务器正在运行")
    
    # 测试获取文件列表
    print("\n1. 测试获取文件列表...")
    try:
        response = requests.get('http://localhost:5000/api/files')
        if response.status_code == 200:
            files = response.json()
            print(f"✓ 成功获取 {len(files)} 个文件")
            
            if files:
                print("文件示例:")
                for i, file in enumerate(files[:3]):
                    print(f"  - {file['name']} ({file['size']} bytes)")
                if len(files) > 3:
                    print(f"  ... 还有 {len(files) - 3} 个文件")
        else:
            print(f"✗ 获取文件列表失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 获取文件列表出错: {e}")
    
    # 测试获取日志
    print("\n2. 测试获取日志...")
    try:
        response = requests.get('http://localhost:5000/api/logs')
        if response.status_code == 200:
            logs = response.json()
            print(f"✓ 成功获取 {len(logs)} 条日志")
            
            if logs:
                print("最新日志:")
                for i, log in enumerate(logs[-3:]):
                    print(f"  - {log.strip()}")
        else:
            print(f"✗ 获取日志失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 获取日志出错: {e}")
    
    # 测试配置获取
    print("\n3. 测试配置获取...")
    try:
        response = requests.get('http://localhost:5000/api/config')
        if response.status_code == 200:
            config = response.json()
            print(f"✓ 成功获取配置，包含 {len(config.get('link', []))} 个链接")
        else:
            print(f"✗ 获取配置失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 获取配置出错: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == '__main__':
    test_file_operations() 