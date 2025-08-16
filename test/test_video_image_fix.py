#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试视频和图片修复
"""

import requests
import json
from pathlib import Path

def test_video_image_fix():
    """测试视频和图片修复"""
    print("=" * 60)
    print("测试视频和图片修复")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # 1. 获取文件列表
    print("\n1. 获取文件列表...")
    try:
        response = requests.get(f"{base_url}/api/files", timeout=10)
        if response.status_code == 200:
            files = response.json()
            print(f"✓ 获取到 {len(files)} 个文件")
            
            # 分类文件
            video_files = [f for f in files if f['name'].lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm'))]
            image_files = [f for f in files if f['name'].lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
            
            print(f"✓ 找到 {len(video_files)} 个视频文件")
            print(f"✓ 找到 {len(image_files)} 个图片文件")
            
            # 2. 测试视频文件预览（检查响应头）
            if video_files:
                print(f"\n2. 测试视频文件预览...")
                test_video = video_files[0]
                video_path = test_video['path'].replace('\\', '/')
                
                print(f"   测试视频: {test_video['name']}")
                print(f"   文件路径: {video_path}")
                print(f"   文件大小: {test_video['size']} bytes")
                
                # 测试预览API
                preview_response = requests.get(f"{base_url}/api/file/preview?path={video_path}")
                if preview_response.status_code in [200, 206]:
                    print(f"   ✓ 视频预览成功")
                    print(f"   状态码: {preview_response.status_code}")
                    
                    # 检查响应头
                    headers = preview_response.headers
                    print(f"   内容类型: {headers.get('content-type', 'N/A')}")
                    print(f"   接受范围: {headers.get('accept-ranges', 'N/A')}")
                    print(f"   缓存控制: {headers.get('cache-control', 'N/A')}")
                    print(f"   内容处置: {headers.get('content-disposition', 'N/A')}")
                    print(f"   内容长度: {headers.get('content-length', 'N/A')}")
                    
                    # 检查文件大小
                    if len(preview_response.content) == test_video['size']:
                        print(f"   ✓ 文件大小匹配")
                    else:
                        print(f"   ⚠ 文件大小不匹配: 期望 {test_video['size']}, 实际 {len(preview_response.content)}")
                else:
                    print(f"   ✗ 视频预览失败: {preview_response.status_code}")
                    print(f"   错误信息: {preview_response.text}")
            
            # 3. 测试图片文件预览
            if image_files:
                print(f"\n3. 测试图片文件预览...")
                test_image = image_files[0]
                image_path = test_image['path'].replace('\\', '/')
                
                print(f"   测试图片: {test_image['name']}")
                print(f"   文件路径: {image_path}")
                print(f"   文件大小: {test_image['size']} bytes")
                
                # 测试预览API
                preview_response = requests.get(f"{base_url}/api/file/preview?path={image_path}")
                if preview_response.status_code == 200:
                    print(f"   ✓ 图片预览成功")
                    print(f"   状态码: {preview_response.status_code}")
                    print(f"   内容类型: {preview_response.headers.get('content-type', 'N/A')}")
                    print(f"   返回大小: {len(preview_response.content)} bytes")
                    
                    # 验证返回的文件大小是否匹配
                    if len(preview_response.content) == test_image['size']:
                        print(f"   ✓ 文件大小匹配")
                    else:
                        print(f"   ⚠ 文件大小不匹配: 期望 {test_image['size']}, 实际 {len(preview_response.content)}")
                else:
                    print(f"   ✗ 图片预览失败: {preview_response.status_code}")
                    print(f"   错误信息: {preview_response.text}")
            
            # 4. 测试Range请求
            if video_files:
                print(f"\n4. 测试Range请求...")
                test_video = video_files[0]
                video_path = test_video['path'].replace('\\', '/')
                
                # 测试Range请求
                headers = {'Range': 'bytes=0-1023'}
                range_response = requests.get(f"{base_url}/api/file/preview?path={video_path}", headers=headers)
                
                if range_response.status_code == 206:
                    print(f"   ✓ Range请求成功")
                    print(f"   状态码: {range_response.status_code}")
                    print(f"   内容范围: {range_response.headers.get('content-range', 'N/A')}")
                    print(f"   返回大小: {len(range_response.content)} bytes")
                else:
                    print(f"   ⚠ Range请求返回: {range_response.status_code}")
            
        else:
            print(f"✗ 文件API异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n修复内容:")
    print("1. 视频播放器：添加必要的响应头确保正确播放")
    print("2. 图片显示：改为4:3比例，尽量大")
    print("3. 视频容器：优化布局和尺寸")
    print("4. 图片缩放：支持4:3比例和原始大小切换")
    print("5. 响应头：添加Accept-Ranges、Cache-Control等")
    
    print("\n使用方法:")
    print("1. 点击文件卡片预览")
    print("2. 视频：现在应该正常显示画面和声音")
    print("3. 图片：4:3比例显示，点击可放大到原始大小")
    print("4. 视频：支持拖动进度条和流式播放")

if __name__ == '__main__':
    test_video_image_fix() 