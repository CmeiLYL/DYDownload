#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试下载功能 - DouYinCommand集成版本
"""

import requests
import json
import time
from pathlib import Path

def test_download():
    """测试下载功能"""
    print("=" * 60)
    print("测试下载功能 - DouYinCommand集成版本")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # 1. 获取当前配置
    print("\n1. 获取当前配置...")
    try:
        response = requests.get(f"{base_url}/api/config", timeout=10)
        if response.status_code == 200:
            config = response.json()
            print(f"✓ 成功获取配置")
            print(f"   下载路径: {config.get('path', './Downloaded/')}")
            print(f"   链接数量: {len(config.get('link', []))}")
            print(f"   下载模式: {config.get('mode', ['post'])}")
            print(f"   线程数: {config.get('thread', 5)}")
            print(f"   音乐下载: {config.get('music', True)}")
            print(f"   封面下载: {config.get('cover', True)}")
            print(f"   头像下载: {config.get('avatar', True)}")
            print(f"   JSON保存: {config.get('json', True)}")
            print(f"   文件夹样式: {config.get('folderstyle', True)}")
        else:
            print(f"✗ 获取配置失败: {response.status_code}")
            return
    except Exception as e:
        print(f"✗ 获取配置失败: {e}")
        return
    
    # 2. 测试链接解析
    print(f"\n2. 测试链接解析...")
    test_links = [
        "https://www.douyin.com/user/MS4wLjABAAAAhBZqyDFJkFetl3-mwoa8TZqQFMSf--LtuIVt6ovsTsQ7rOBwbgyXNwsUr5Ezy-R0",  # 用户主页
        "https://v.douyin.com/kcvMpuN/",  # 单个视频
        "https://www.douyin.com/collection/7123456789012345678"  # 合集
    ]
    
    for i, test_link in enumerate(test_links):
        print(f"   测试链接 {i+1}: {test_link}")
        try:
            response = requests.post(f"{base_url}/api/link/parse", 
                                   json={"link": test_link}, 
                                   timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"   ✓ 链接解析成功")
                    print(f"      用户名称: {result.get('nickname', 'N/A')}")
                    print(f"      链接类型: {result.get('link_type', 'N/A')}")
                else:
                    print(f"   ✗ 链接解析失败: {result.get('message', '未知错误')}")
            else:
                print(f"   ✗ 链接解析请求失败: {response.status_code}")
        except Exception as e:
            print(f"   ✗ 链接解析失败: {e}")
    
    # 3. 测试下载状态
    print(f"\n3. 测试下载状态...")
    try:
        response = requests.get(f"{base_url}/api/download/status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print(f"✓ 下载状态: {status.get('current_task', 'N/A')}")
            print(f"   运行状态: {status.get('running', False)}")
            print(f"   进度: {status.get('progress', 0)}%")
        else:
            print(f"✗ 获取下载状态失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 获取下载状态失败: {e}")
    
    # 4. 测试添加链接到配置
    print(f"\n4. 测试添加链接到配置...")
    try:
        # 添加测试链接到配置
        config['link'] = [test_links[0]]  # 使用用户主页链接
        
        response = requests.post(f"{base_url}/api/config", 
                               json=config, 
                               timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✓ 配置更新成功")
                print(f"   已添加链接: {test_links[0]}")
            else:
                print(f"✗ 配置更新失败: {result.get('message', '未知错误')}")
        else:
            print(f"✗ 配置更新请求失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 配置更新失败: {e}")
    
    # 5. 测试启动下载
    print(f"\n5. 测试启动下载...")
    try:
        response = requests.post(f"{base_url}/api/download/start", 
                               json={"config": config}, 
                               timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✓ 下载任务启动成功")
                print(f"   消息: {result.get('message', 'N/A')}")
                
                # 监控下载进度
                print(f"\n6. 监控下载进度...")
                for i in range(120):  # 监控120秒（2分钟）
                    time.sleep(2)
                    try:
                        status_response = requests.get(f"{base_url}/api/download/status", timeout=5)
                        if status_response.status_code == 200:
                            status = status_response.json()
                            print(f"   进度: {status.get('progress', 0)}% - {status.get('current_task', 'N/A')}")
                            
                            if not status.get('running', False):
                                print(f"   下载任务已结束")
                                break
                    except:
                        pass
            else:
                print(f"✗ 下载任务启动失败: {result.get('message', '未知错误')}")
        else:
            print(f"✗ 下载任务启动请求失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 下载任务启动失败: {e}")
    
    # 7. 测试文件列表
    print(f"\n7. 测试文件列表...")
    try:
        response = requests.get(f"{base_url}/api/files", timeout=10)
        if response.status_code == 200:
            files = response.json()
            print(f"✓ 获取文件列表成功")
            print(f"   文件数量: {len(files)}")
            
            # 分类文件
            video_files = [f for f in files if f['name'].lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm'))]
            image_files = [f for f in files if f['name'].lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
            
            print(f"   视频文件: {len(video_files)} 个")
            print(f"   图片文件: {len(image_files)} 个")
            
            if files:
                print(f"   最新文件: {files[0]['name']}")
        else:
            print(f"✗ 获取文件列表失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 获取文件列表失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n下载功能说明:")
    print("1. 直接使用DouYinCommand.py的main函数")
    print("2. 支持所有链接类型：用户主页、单个视频、合集、音乐、直播")
    print("3. 完整的配置支持：音乐、封面、头像、JSON、文件夹样式")
    print("4. 支持增量下载和数量限制")
    print("5. 多线程下载，可配置线程数")
    print("6. 实时进度监控和状态更新")
    print("7. 无需额外依赖，使用原有下载逻辑")
    
    print("\n支持的链接类型:")
    print("1. 用户主页: https://www.douyin.com/user/...")
    print("2. 单个视频: https://v.douyin.com/...")
    print("3. 合集: https://www.douyin.com/collection/...")
    print("4. 音乐: https://www.douyin.com/music/...")
    print("5. 直播: https://live.douyin.com/...")
    
    print("\n使用方法:")
    print("1. 在Web界面添加抖音链接")
    print("2. 配置下载选项")
    print("3. 点击'开始下载'按钮")
    print("4. 监控下载进度")
    print("5. 在'文件'页面查看下载结果")
    
    print("\n优势:")
    print("1. 使用经过验证的下载逻辑")
    print("2. 无需处理复杂的依赖问题")
    print("3. 保持与原项目的一致性")
    print("4. 更稳定可靠的下载体验")

if __name__ == '__main__':
    test_download() 