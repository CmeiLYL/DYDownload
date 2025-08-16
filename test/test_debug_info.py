#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试调试信息
"""

import requests
import json
from pathlib import Path

def test_debug_info():
    """测试调试信息"""
    print("=" * 60)
    print("测试调试信息")
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
            
            # 2. 测试视频文件API（带调试信息）
            if video_files:
                print(f"\n2. 测试视频文件API（带调试信息）...")
                test_video = video_files[0]
                video_path = test_video['path'].replace('\\', '/')
                
                print(f"   测试视频: {test_video['name']}")
                print(f"   文件路径: {video_path}")
                print(f"   文件大小: {test_video['size']} bytes")
                
                # 测试视频API
                print(f"   请求URL: {base_url}/api/file/video?path={video_path}")
                video_response = requests.get(f"{base_url}/api/file/video?path={video_path}")
                
                print(f"   响应状态码: {video_response.status_code}")
                print(f"   响应头:")
                for key, value in video_response.headers.items():
                    print(f"     {key}: {value}")
                
                if video_response.status_code == 200:
                    print(f"   ✓ 视频API成功")
                    print(f"   返回大小: {len(video_response.content)} bytes")
                else:
                    print(f"   ✗ 视频API失败")
                    print(f"   错误信息: {video_response.text}")
            
            # 3. 测试图片文件API（带调试信息）
            if image_files:
                print(f"\n3. 测试图片文件API（带调试信息）...")
                test_image = image_files[0]
                image_path = test_image['path'].replace('\\', '/')
                
                print(f"   测试图片: {test_image['name']}")
                print(f"   文件路径: {image_path}")
                print(f"   文件大小: {test_image['size']} bytes")
                
                # 测试预览API
                print(f"   请求URL: {base_url}/api/file/preview?path={image_path}")
                preview_response = requests.get(f"{base_url}/api/file/preview?path={image_path}")
                
                print(f"   响应状态码: {preview_response.status_code}")
                print(f"   响应头:")
                for key, value in preview_response.headers.items():
                    print(f"     {key}: {value}")
                
                if preview_response.status_code == 200:
                    print(f"   ✓ 图片预览成功")
                    print(f"   返回大小: {len(preview_response.content)} bytes")
                else:
                    print(f"   ✗ 图片预览失败")
                    print(f"   错误信息: {preview_response.text}")
                
                # 测试缩略图API
                print(f"\n4. 测试缩略图API（带调试信息）...")
                print(f"   请求URL: {base_url}/api/file/thumbnail?path={image_path}")
                thumbnail_response = requests.get(f"{base_url}/api/file/thumbnail?path={image_path}")
                
                print(f"   响应状态码: {thumbnail_response.status_code}")
                print(f"   响应头:")
                for key, value in thumbnail_response.headers.items():
                    print(f"     {key}: {value}")
                
                if thumbnail_response.status_code == 200:
                    print(f"   ✓ 缩略图API成功")
                    print(f"   返回大小: {len(thumbnail_response.content)} bytes")
                else:
                    print(f"   ✗ 缩略图API失败")
                    print(f"   错误信息: {thumbnail_response.text}")
            
        else:
            print(f"✗ 文件API异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n调试信息说明:")
    print("1. 视频API: 详细记录文件路径、大小、Range请求等信息")
    print("2. 预览API: 记录文件类型、MIME类型、处理过程等信息")
    print("3. 缩略图API: 记录缩略图状态、生成过程等信息")
    print("4. 错误处理: 详细的错误信息和异常堆栈")
    
    print("\n查看日志:")
    print("1. 查看控制台输出的实时日志")
    print("2. 查看 logs/douyin.log 文件")
    print("3. 在Web界面的'日志'标签页查看")

if __name__ == '__main__':
    test_debug_info() 