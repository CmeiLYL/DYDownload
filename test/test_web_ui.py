#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Web UI 测试脚本
"""

import requests
import json
import time
import sys
from pathlib import Path

def test_config_api():
    """测试配置API"""
    print("测试配置API...")
    
    try:
        # 测试获取配置
        response = requests.get('http://localhost:5000/api/config')
        if response.status_code == 200:
            config = response.json()
            print(f"✓ 获取配置成功，包含 {len(config.get('link', []))} 个链接")
        else:
            print(f"✗ 获取配置失败: {response.status_code}")
            return False
        
        # 测试更新配置
        test_config = {
            "link": ["https://www.douyin.com/user/test"],
            "path": "./test_download/",
            "music": True,
            "cover": False,
            "avatar": False,
            "json": False,
            "folderstyle": False,
            "mode": ["post"],
            "number": {"post": 0, "like": 0, "allmix": 0, "mix": 0, "music": 0},
            "database": True,
            "increase": {"post": True, "like": False, "allmix": False, "mix": False, "music": False},
            "thread": 5,
            "cookies": {}
        }
        
        response = requests.post('http://localhost:5000/api/config', 
                               json=test_config)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✓ 更新配置成功")
            else:
                print(f"✗ 更新配置失败: {result.get('message')}")
                return False
        else:
            print(f"✗ 更新配置请求失败: {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到服务器，请确保Web UI正在运行")
        return False
    except Exception as e:
        print(f"✗ 测试配置API时出错: {e}")
        return False

def test_download_api():
    """测试下载API"""
    print("测试下载API...")
    
    try:
        # 测试获取下载状态
        response = requests.get('http://localhost:5000/api/download/status')
        if response.status_code == 200:
            status = response.json()
            print(f"✓ 获取下载状态成功: {status.get('current_task', '未知')}")
        else:
            print(f"✗ 获取下载状态失败: {response.status_code}")
            return False
        
        # 测试停止下载（应该总是成功）
        response = requests.post('http://localhost:5000/api/download/stop')
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✓ 停止下载API正常")
            else:
                print(f"✗ 停止下载失败: {result.get('message')}")
                return False
        else:
            print(f"✗ 停止下载请求失败: {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到服务器")
        return False
    except Exception as e:
        print(f"✗ 测试下载API时出错: {e}")
        return False

def test_files_api():
    """测试文件API"""
    print("测试文件API...")
    
    try:
        response = requests.get('http://localhost:5000/api/files')
        if response.status_code == 200:
            files = response.json()
            print(f"✓ 获取文件列表成功，共 {len(files)} 个文件")
        else:
            print(f"✗ 获取文件列表失败: {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到服务器")
        return False
    except Exception as e:
        print(f"✗ 测试文件API时出错: {e}")
        return False

def test_logs_api():
    """测试日志API"""
    print("测试日志API...")
    
    try:
        response = requests.get('http://localhost:5000/api/logs')
        if response.status_code == 200:
            logs = response.json()
            print(f"✓ 获取日志成功，共 {len(logs)} 条日志")
        else:
            print(f"✗ 获取日志失败: {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到服务器")
        return False
    except Exception as e:
        print(f"✗ 测试日志API时出错: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("Web UI 功能测试")
    print("=" * 50)
    
    # 检查服务器是否运行
    print("检查服务器状态...")
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print("✓ 服务器正在运行")
        else:
            print(f"✗ 服务器响应异常: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到服务器，请先启动Web UI:")
        print("  python run_web.py")
        return
    except Exception as e:
        print(f"✗ 检查服务器状态时出错: {e}")
        return
    
    print()
    
    # 运行测试
    tests = [
        test_config_api,
        test_download_api,
        test_files_api,
        test_logs_api
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    # 输出测试结果
    print("=" * 50)
    print(f"测试完成: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！Web UI 运行正常")
    else:
        print("⚠️  部分测试失败，请检查相关功能")
    
    print("=" * 50)

if __name__ == '__main__':
    main() 