#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试文件过滤功能
"""

import requests
import json
from pathlib import Path

def test_file_filtering():
    """测试文件过滤功能"""
    print("=" * 60)
    print("测试文件过滤功能")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # 1. 获取文件列表
    print("\n1. 获取文件列表...")
    try:
        response = requests.get(f"{base_url}/api/files", timeout=10)
        if response.status_code == 200:
            files = response.json()
            print(f"✓ 获取到 {len(files)} 个文件")
            
            # 检查是否包含temp文件夹的文件
            temp_files = [f for f in files if 'temp' in f['path']]
            if temp_files:
                print(f"⚠ 发现 {len(temp_files)} 个temp文件夹中的文件:")
                for temp_file in temp_files[:5]:  # 只显示前5个
                    print(f"   - {temp_file['path']}")
                if len(temp_files) > 5:
                    print(f"   ... 还有 {len(temp_files) - 5} 个")
            else:
                print("✓ 已正确过滤temp文件夹中的文件")
            
            # 分类文件
            video_files = [f for f in files if f['name'].lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm'))]
            image_files = [f for f in files if f['name'].lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
            
            print(f"✓ 找到 {len(video_files)} 个视频文件")
            print(f"✓ 找到 {len(image_files)} 个图片文件")
            
            # 2. 测试视频文件预览（确保使用原文件）
            if video_files:
                print(f"\n2. 测试视频文件预览...")
                test_video = video_files[0]
                video_path = test_video['path'].replace('\\', '/')
                
                print(f"   测试视频: {test_video['name']}")
                print(f"   文件路径: {video_path}")
                print(f"   文件大小: {test_video['size']} bytes")
                
                # 检查路径是否包含temp
                if 'temp' in video_path:
                    print(f"   ⚠ 警告：视频文件路径包含temp")
                else:
                    print(f"   ✓ 视频文件路径正常")
                
                # 测试预览API
                preview_response = requests.get(f"{base_url}/api/file/preview?path={video_path}")
                if preview_response.status_code in [200, 206]:
                    content_type = preview_response.headers.get('content-type', '')
                    print(f"   ✓ 视频预览成功")
                    print(f"   状态码: {preview_response.status_code}")
                    print(f"   内容类型: {content_type}")
                    print(f"   返回大小: {len(preview_response.content)} bytes")
                    
                    # 验证返回的文件大小是否匹配
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
                
                # 检查路径是否包含temp
                if 'temp' in image_path:
                    print(f"   ⚠ 警告：图片文件路径包含temp")
                else:
                    print(f"   ✓ 图片文件路径正常")
                
                # 测试预览API
                preview_response = requests.get(f"{base_url}/api/file/preview?path={image_path}")
                if preview_response.status_code == 200:
                    content_type = preview_response.headers.get('content-type', '')
                    print(f"   ✓ 图片预览成功")
                    print(f"   状态码: {preview_response.status_code}")
                    print(f"   内容类型: {content_type}")
                    print(f"   返回大小: {len(preview_response.content)} bytes")
                    
                    # 验证返回的文件大小是否匹配
                    if len(preview_response.content) == test_image['size']:
                        print(f"   ✓ 文件大小匹配")
                    else:
                        print(f"   ⚠ 文件大小不匹配: 期望 {test_image['size']}, 实际 {len(preview_response.content)}")
                else:
                    print(f"   ✗ 图片预览失败: {preview_response.status_code}")
                    print(f"   错误信息: {preview_response.text}")
            
            # 4. 测试缩略图API（确保缩略图功能正常）
            print(f"\n4. 测试缩略图API...")
            if video_files:
                test_video = video_files[0]
                video_path = test_video['path'].replace('\\', '/')
                
                thumbnail_response = requests.get(f"{base_url}/api/file/thumbnail?path={video_path}")
                if thumbnail_response.status_code == 200:
                    content_type = thumbnail_response.headers.get('content-type', '')
                    print(f"   ✓ 缩略图获取成功")
                    print(f"   内容类型: {content_type}")
                    print(f"   缩略图大小: {len(thumbnail_response.content)} bytes")
                    
                    # 缩略图应该比原文件小
                    if len(thumbnail_response.content) < test_video['size']:
                        print(f"   ✓ 缩略图大小合理")
                    else:
                        print(f"   ⚠ 缩略图大小异常")
                else:
                    print(f"   ✗ 缩略图获取失败: {thumbnail_response.status_code}")
            
        else:
            print(f"✗ 文件API异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n修复内容:")
    print("1. 文件列表API排除temp文件夹内容")
    print("2. 预览功能使用原文件路径")
    print("3. 缩略图功能使用缩略图API")
    print("4. 前端检查防止预览temp文件")
    print("5. 确保视频和图片预览使用原文件")
    
    print("\n功能说明:")
    print("1. 文件列表：只显示用户下载的文件，不显示临时文件")
    print("2. 缩略图：使用缩略图API生成的小尺寸预览")
    print("3. 预览：使用原文件进行完整预览")
    print("4. 视频：支持流式播放，可拖动进度条")
    print("5. 图片：支持点击缩放查看")

if __name__ == '__main__':
    test_file_filtering() 