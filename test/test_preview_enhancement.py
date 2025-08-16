#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试预览功能增强
"""

import requests
import json
from pathlib import Path

def test_preview_enhancement():
    """测试预览功能增强"""
    print("=" * 60)
    print("测试预览功能增强")
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
            
            # 2. 测试视频文件预览（检查Range请求支持）
            if video_files:
                print(f"\n2. 测试视频文件预览...")
                test_video = video_files[0]
                video_path = test_video['path'].replace('\\', '/')
                
                print(f"   测试视频: {test_video['name']}")
                print(f"   文件路径: {video_path}")
                print(f"   文件大小: {test_video['size']} bytes")
                
                # 测试Range请求
                headers = {'Range': 'bytes=0-1023'}  # 请求前1KB
                preview_response = requests.get(f"{base_url}/api/file/preview?path={video_path}", headers=headers)
                
                if preview_response.status_code == 206:
                    content_range = preview_response.headers.get('content-range', '')
                    content_length = preview_response.headers.get('content-length', '')
                    print(f"   ✓ 视频Range请求成功")
                    print(f"   状态码: {preview_response.status_code}")
                    print(f"   Content-Range: {content_range}")
                    print(f"   Content-Length: {content_length}")
                    print(f"   返回大小: {len(preview_response.content)} bytes")
                elif preview_response.status_code == 200:
                    print(f"   ✓ 视频预览成功（完整文件）")
                    print(f"   状态码: {preview_response.status_code}")
                    print(f"   返回大小: {len(preview_response.content)} bytes")
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
                
                # 测试完整图片预览
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
            
            # 4. 测试视频文件的完整请求
            if video_files:
                print(f"\n4. 测试视频文件完整请求...")
                test_video = video_files[0]
                video_path = test_video['path'].replace('\\', '/')
                
                # 不发送Range头，请求完整文件
                preview_response = requests.get(f"{base_url}/api/file/preview?path={video_path}")
                if preview_response.status_code == 200:
                    content_type = preview_response.headers.get('content-type', '')
                    print(f"   ✓ 视频完整请求成功")
                    print(f"   状态码: {preview_response.status_code}")
                    print(f"   内容类型: {content_type}")
                    print(f"   返回大小: {len(preview_response.content)} bytes")
                    
                    # 验证返回的文件大小是否匹配
                    if len(preview_response.content) == test_video['size']:
                        print(f"   ✓ 文件大小匹配")
                    else:
                        print(f"   ⚠ 文件大小不匹配: 期望 {test_video['size']}, 实际 {len(preview_response.content)}")
                else:
                    print(f"   ✗ 视频完整请求失败: {preview_response.status_code}")
                    print(f"   错误信息: {preview_response.text}")
            
        else:
            print(f"✗ 文件API异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n增强功能:")
    print("1. 视频文件支持Range请求（206状态码）")
    print("2. 图片文件支持点击缩放")
    print("3. 预览模态框尺寸优化")
    print("4. 视频播放器优化")
    print("5. 图片容器样式改进")
    
    print("\n使用方法:")
    print("1. 点击文件卡片预览")
    print("2. 视频：支持流式播放，可拖动进度条")
    print("3. 图片：点击图片可放大/缩小")
    print("4. 右键点击在文件夹中打开")

if __name__ == '__main__':
    test_preview_enhancement() 