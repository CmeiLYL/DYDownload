#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试图片和视频预览修复
"""

import requests
import json
from pathlib import Path

def test_preview_fix():
    """测试图片和视频预览修复"""
    print("=" * 60)
    print("测试图片和视频预览修复")
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
            
            # 2. 测试视频文件预览
            if video_files:
                print(f"\n2. 测试视频文件预览...")
                test_video = video_files[0]
                video_path = test_video['path'].replace('\\', '/')
                
                print(f"   测试视频: {test_video['name']}")
                print(f"   文件路径: {video_path}")
                print(f"   文件大小: {test_video['size']} bytes")
                
                # 测试视频API
                video_response = requests.get(f"{base_url}/api/file/video?path={video_path}")
                if video_response.status_code == 200:
                    print(f"   ✓ 视频API成功")
                    print(f"   状态码: {video_response.status_code}")
                    print(f"   内容类型: {video_response.headers.get('content-type', 'N/A')}")
                    print(f"   返回大小: {len(video_response.content)} bytes")
                    
                    # 检查响应头
                    headers = video_response.headers
                    print(f"   接受范围: {headers.get('accept-ranges', 'N/A')}")
                    print(f"   内容长度: {headers.get('content-length', 'N/A')}")
                    print(f"   缓存控制: {headers.get('cache-control', 'N/A')}")
                else:
                    print(f"   ✗ 视频API失败: {video_response.status_code}")
                    print(f"   错误信息: {video_response.text}")
            
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
                else:
                    print(f"   ✗ 图片预览失败: {preview_response.status_code}")
                    print(f"   错误信息: {preview_response.text}")
            
            # 4. 测试缩略图API
            if image_files:
                print(f"\n4. 测试缩略图API...")
                test_image = image_files[0]
                image_path = test_image['path'].replace('\\', '/')
                
                thumbnail_response = requests.get(f"{base_url}/api/file/thumbnail?path={image_path}")
                if thumbnail_response.status_code == 200:
                    print(f"   ✓ 缩略图API成功")
                    print(f"   状态码: {thumbnail_response.status_code}")
                    print(f"   内容类型: {thumbnail_response.headers.get('content-type', 'N/A')}")
                    print(f"   返回大小: {len(thumbnail_response.content)} bytes")
                else:
                    print(f"   ✗ 缩略图API失败: {thumbnail_response.status_code}")
            
        else:
            print(f"✗ 文件API异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n修复内容:")
    print("1. 视频容器：简化布局，使用100%宽高，黑色背景")
    print("2. 图片容器：移除复杂的wrapper，直接使用img标签")
    print("3. 图片缩放：简化缩放逻辑，直接操作img样式")
    print("4. CSS样式：更新容器样式，移除不必要的复杂布局")
    print("5. 错误处理：改进图片加载失败的错误显示")
    
    print("\n预期效果:")
    print("1. 视频：全屏显示，黑色背景，支持播放控制")
    print("2. 图片：居中显示，支持点击缩放")
    print("3. 布局：简洁清晰，响应式设计")
    print("4. 交互：流畅的缩放动画和悬停效果")

if __name__ == '__main__':
    test_preview_fix() 