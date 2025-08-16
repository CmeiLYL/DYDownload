#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Web UI 演示脚本
展示如何使用Web UI的各种功能
"""

import requests
import json
import time
import sys
from pathlib import Path

def demo_config_management():
    """演示配置管理功能"""
    print("🔧 配置管理演示")
    print("-" * 30)
    
    # 1. 获取当前配置
    print("1. 获取当前配置...")
    response = requests.get('http://localhost:5000/api/config')
    if response.status_code == 200:
        config = response.json()
        print(f"   ✓ 当前配置包含 {len(config.get('link', []))} 个链接")
    else:
        print("   ✗ 获取配置失败")
        return False
    
    # 2. 添加测试链接
    print("2. 添加测试链接...")
    test_links = [
        "https://www.douyin.com/user/MS4wLjABAAAAo9d0IAmNP9MBWh4hDWFjMQ8sZduLS6PDnGagFhJ855E",
        "https://v.douyin.com/Q2g8wsibC44/"
    ]
    
    config['link'] = test_links
    config['music'] = True
    config['cover'] = False
    config['mode'] = ['post', 'mix']
    
    response = requests.post('http://localhost:5000/api/config', json=config)
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"   ✓ 成功添加 {len(test_links)} 个测试链接")
        else:
            print(f"   ✗ 保存配置失败: {result.get('message')}")
            return False
    else:
        print("   ✗ 保存配置请求失败")
        return False
    
    print()
    return True

def demo_download_control():
    """演示下载控制功能"""
    print("🎬 下载控制演示")
    print("-" * 30)
    
    # 1. 检查下载状态
    print("1. 检查下载状态...")
    response = requests.get('http://localhost:5000/api/download/status')
    if response.status_code == 200:
        status = response.json()
        print(f"   ✓ 当前状态: {status.get('current_task', '未知')}")
        print(f"   ✓ 进度: {status.get('progress', 0)}%")
    else:
        print("   ✗ 获取状态失败")
        return False
    
    # 2. 模拟启动下载（实际不会真正下载）
    print("2. 模拟启动下载...")
    test_config = {
        "link": ["https://www.douyin.com/user/test"],
        "path": "./demo_download/",
        "music": True,
        "cover": False,
        "avatar": False,
        "json": False,
        "folderstyle": False,
        "mode": ["post"],
        "number": {"post": 0, "like": 0, "allmix": 0, "mix": 0, "music": 0},
        "database": True,
        "increase": {"post": True, "like": False, "allmix": False, "mix": False, "music": False},
        "thread": 3,
        "cookies": {}
    }
    
    response = requests.post('http://localhost:5000/api/download/start', 
                           json={"config": test_config})
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print("   ✓ 下载任务已启动")
            
            # 等待几秒查看进度
            print("3. 监控下载进度...")
            for i in range(5):
                time.sleep(1)
                response = requests.get('http://localhost:5000/api/download/status')
                if response.status_code == 200:
                    status = response.json()
                    print(f"   - {status.get('current_task', '未知')} ({status.get('progress', 0)}%)")
            
            # 停止下载
            print("4. 停止下载...")
            response = requests.post('http://localhost:5000/api/download/stop')
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("   ✓ 下载已停止")
                else:
                    print(f"   ✗ 停止下载失败: {result.get('message')}")
        else:
            print(f"   ✗ 启动下载失败: {result.get('message')}")
    else:
        print("   ✗ 启动下载请求失败")
    
    print()
    return True

def demo_file_management():
    """演示文件管理功能"""
    print("📁 文件管理演示")
    print("-" * 30)
    
    # 1. 获取文件列表
    print("1. 获取已下载文件列表...")
    response = requests.get('http://localhost:5000/api/files')
    if response.status_code == 200:
        files = response.json()
        print(f"   ✓ 共找到 {len(files)} 个文件")
        
        if files:
            print("   文件列表:")
            for i, file in enumerate(files[:5]):  # 只显示前5个
                print(f"   - {file['name']} ({file['size']} bytes)")
            if len(files) > 5:
                print(f"   ... 还有 {len(files) - 5} 个文件")
        else:
            print("   - 暂无下载文件")
    else:
        print("   ✗ 获取文件列表失败")
        return False
    
    print()
    return True

def demo_log_viewing():
    """演示日志查看功能"""
    print("📋 日志查看演示")
    print("-" * 30)
    
    # 1. 获取系统日志
    print("1. 获取系统日志...")
    response = requests.get('http://localhost:5000/api/logs')
    if response.status_code == 200:
        logs = response.json()
        print(f"   ✓ 共找到 {len(logs)} 条日志")
        
        if logs:
            print("   最新日志:")
            for i, log in enumerate(logs[-3:]):  # 显示最后3条
                print(f"   - {log.strip()}")
        else:
            print("   - 暂无日志记录")
    else:
        print("   ✗ 获取日志失败")
        return False
    
    print()
    return True

def main():
    """主演示函数"""
    print("=" * 60)
    print("🎯 抖音下载器 Web UI 功能演示")
    print("=" * 60)
    print()
    
    # 检查服务器是否运行
    print("🔍 检查服务器状态...")
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print("✓ 服务器正在运行")
        else:
            print(f"✗ 服务器响应异常: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到服务器")
        print("请先启动Web UI:")
        print("  python run_web.py")
        print("  或者双击 start_web_ui.bat")
        return
    except Exception as e:
        print(f"✗ 检查服务器状态时出错: {e}")
        return
    
    print()
    
    # 运行演示
    demos = [
        ("配置管理", demo_config_management),
        ("下载控制", demo_download_control),
        ("文件管理", demo_file_management),
        ("日志查看", demo_log_viewing)
    ]
    
    successful_demos = 0
    total_demos = len(demos)
    
    for name, demo_func in demos:
        print(f"🎬 演示: {name}")
        if demo_func():
            successful_demos += 1
        print()
    
    # 输出演示结果
    print("=" * 60)
    print(f"📊 演示完成: {successful_demos}/{total_demos} 成功")
    
    if successful_demos == total_demos:
        print("🎉 所有功能演示成功！")
        print()
        print("💡 提示:")
        print("- 打开浏览器访问 http://localhost:5000 体验完整界面")
        print("- 在首页添加真实的抖音链接进行实际下载")
        print("- 在设置页面配置Cookie以提高下载成功率")
    else:
        print("⚠️  部分功能演示失败，请检查相关服务")
    
    print("=" * 60)

if __name__ == '__main__':
    main() 