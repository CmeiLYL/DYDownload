#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试文件预览功能
"""

import requests
import json
from pathlib import Path

def test_file_preview():
    """测试文件预览功能"""
    print("=" * 60)
    print("测试文件预览功能")
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
                print(f"   路径: {video_path}")
                
                preview_response = requests.get(f"{base_url}/api/file/preview?path={video_path}")
                if preview_response.status_code == 200:
                    content_type = preview_response.headers.get('content-type', '')
                    print(f"   ✓ 视频预览成功")
                    print(f"   内容类型: {content_type}")
                    print(f"   文件大小: {len(preview_response.content)} bytes")
                    
                    # 保存测试文件
                    with open('test_video_preview.mp4', 'wb') as f:
                        f.write(preview_response.content)
                    print(f"   测试文件已保存为: test_video_preview.mp4")
                else:
                    print(f"   ✗ 视频预览失败: {preview_response.status_code}")
                    print(f"   错误信息: {preview_response.text}")
            
            # 3. 测试图片文件预览
            if image_files:
                print(f"\n3. 测试图片文件预览...")
                test_image = image_files[0]
                image_path = test_image['path'].replace('\\', '/')
                
                print(f"   测试图片: {test_image['name']}")
                print(f"   路径: {image_path}")
                
                preview_response = requests.get(f"{base_url}/api/file/preview?path={image_path}")
                if preview_response.status_code == 200:
                    content_type = preview_response.headers.get('content-type', '')
                    print(f"   ✓ 图片预览成功")
                    print(f"   内容类型: {content_type}")
                    print(f"   文件大小: {len(preview_response.content)} bytes")
                    
                    # 保存测试文件
                    ext = Path(test_image['name']).suffix
                    test_filename = f"test_image_preview{ext}"
                    with open(test_filename, 'wb') as f:
                        f.write(preview_response.content)
                    print(f"   测试文件已保存为: {test_filename}")
                else:
                    print(f"   ✗ 图片预览失败: {preview_response.status_code}")
                    print(f"   错误信息: {preview_response.text}")
            
            # 4. 测试不支持的文件类型
            print(f"\n4. 测试不支持的文件类型...")
            unsupported_files = [f for f in files if not f['name'].lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
            
            if unsupported_files:
                test_unsupported = unsupported_files[0]
                unsupported_path = test_unsupported['path'].replace('\\', '/')
                
                print(f"   测试文件: {test_unsupported['name']}")
                print(f"   路径: {unsupported_path}")
                
                preview_response = requests.get(f"{base_url}/api/file/preview?path={unsupported_path}")
                if preview_response.status_code == 400:
                    print(f"   ✓ 正确拒绝不支持的文件类型")
                    print(f"   错误信息: {preview_response.json()}")
                else:
                    print(f"   ⚠ 意外响应: {preview_response.status_code}")
            else:
                print("   ⚠ 没有不支持的文件类型进行测试")
            
            # 5. 测试不存在的文件
            print(f"\n5. 测试不存在的文件...")
            fake_path = "nonexistent/file.mp4"
            preview_response = requests.get(f"{base_url}/api/file/preview?path={fake_path}")
            if preview_response.status_code == 404:
                print(f"   ✓ 正确处理不存在的文件")
                print(f"   错误信息: {preview_response.json()}")
            else:
                print(f"   ⚠ 意外响应: {preview_response.status_code}")
            
        else:
            print(f"✗ 文件API异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n下一步:")
    print("1. 打开浏览器访问 http://localhost:5000")
    print("2. 切换到'文件'标签页")
    print("3. 点击文件卡片上的预览按钮")
    print("4. 在模态框中查看视频或图片")
    print("5. 测试下载功能")

if __name__ == '__main__':
    test_file_preview() 