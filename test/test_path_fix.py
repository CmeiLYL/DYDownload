#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试路径修复
"""

import requests
import json
from pathlib import Path

def test_path_fix():
    """测试路径修复"""
    print("=" * 60)
    print("测试路径修复")
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
            
            # 2. 测试视频文件API（带路径修复）
            if video_files:
                print(f"\n2. 测试视频文件API（带路径修复）...")
                test_video = video_files[0]
                video_path = test_video['path']  # 保持原始路径格式
                
                print(f"   测试视频: {test_video['name']}")
                print(f"   原始路径: {video_path}")
                print(f"   文件大小: {test_video['size']} bytes")
                
                # 测试视频API
                print(f"   请求URL: {base_url}/api/file/video?path={video_path}")
                video_response = requests.get(f"{base_url}/api/file/video?path={video_path}")
                
                print(f"   响应状态码: {video_response.status_code}")
                if video_response.status_code == 200:
                    print(f"   ✓ 视频API成功")
                    print(f"   返回大小: {len(video_response.content)} bytes")
                else:
                    print(f"   ✗ 视频API失败")
                    print(f"   错误信息: {video_response.text}")
            
            # 3. 测试图片文件API（带路径修复）
            if image_files:
                print(f"\n3. 测试图片文件API（带路径修复）...")
                test_image = image_files[0]
                image_path = test_image['path']  # 保持原始路径格式
                
                print(f"   测试图片: {test_image['name']}")
                print(f"   原始路径: {image_path}")
                print(f"   文件大小: {test_image['size']} bytes")
                
                # 测试预览API
                print(f"   请求URL: {base_url}/api/file/preview?path={image_path}")
                preview_response = requests.get(f"{base_url}/api/file/preview?path={image_path}")
                
                print(f"   响应状态码: {preview_response.status_code}")
                if preview_response.status_code == 200:
                    print(f"   ✓ 图片预览成功")
                    print(f"   返回大小: {len(preview_response.content)} bytes")
                else:
                    print(f"   ✗ 图片预览失败")
                    print(f"   错误信息: {preview_response.text}")
                
                # 测试缩略图API
                print(f"\n4. 测试缩略图API（带路径修复）...")
                print(f"   请求URL: {base_url}/api/file/thumbnail?path={image_path}")
                thumbnail_response = requests.get(f"{base_url}/api/file/thumbnail?path={image_path}")
                
                print(f"   响应状态码: {thumbnail_response.status_code}")
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
    
    print("\n路径修复说明:")
    print("1. 修复了Windows路径分隔符问题")
    print("2. 统一将反斜杠转换为正斜杠")
    print("3. 确保Path对象正确处理路径")
    print("4. 添加了原始路径和修复后路径的日志记录")
    
    print("\n修复内容:")
    print("1. 视频API: 添加路径分隔符修复")
    print("2. 预览API: 添加路径分隔符修复")
    print("3. 缩略图API: 添加路径分隔符修复")
    print("4. 日志记录: 显示原始路径和修复后路径")

if __name__ == '__main__':
    test_path_fix() 