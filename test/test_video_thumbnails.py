#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试视频缩略图功能
"""

import requests
import json
from pathlib import Path
import subprocess
import sys

def check_ffmpeg():
    """检查ffmpeg是否可用"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ ffmpeg 可用")
            return True
        else:
            print("✗ ffmpeg 不可用")

    except FileNotFoundError:
        print("✗ 未找到 ffmpeg，请安装 ffmpeg")


def test_video_thumbnails():
    """测试视频缩略图功能"""
    print("=" * 60)
    print("测试视频缩略图功能")
    print("=" * 60)
    
    # 检查ffmpeg
    print("\n1. 检查ffmpeg...")
    if not check_ffmpeg():
        print("请先安装ffmpeg:")
        print("Windows: 下载 https://ffmpeg.org/download.html")
        print("macOS: brew install ffmpeg")
        print("Ubuntu: sudo apt install ffmpeg")
        return
    
    base_url = "http://localhost:5000"
    
    # 测试文件API
    print("\n2. 获取文件列表...")
    try:
        response = requests.get(f"{base_url}/api/files", timeout=10)
        if response.status_code == 200:
            files = response.json()
            print(f"✓ 获取到 {len(files)} 个文件")
            
            # 查找视频文件
            video_files = [f for f in files if f['name'].lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm'))]
            print(f"✓ 找到 {len(video_files)} 个视频文件")
            
            if video_files:
                # 测试第一个视频文件的缩略图
                test_video = video_files[0]
                print(f"\n3. 测试视频缩略图: {test_video['name']}")
                
                video_path = test_video['path'].replace('\\', '/')
                thumbnail_url = f"{base_url}/api/file/thumbnail?path={video_path}"
                
                print(f"  视频路径: {video_path}")
                print(f"  缩略图URL: {thumbnail_url}")
                
                # 请求缩略图
                thumbnail_response = requests.get(thumbnail_url, timeout=30)
                
                if thumbnail_response.status_code == 200:
                    content_type = thumbnail_response.headers.get('content-type', '')
                    if 'image' in content_type:
                        print(f"✓ 视频缩略图生成成功")
                        print(f"  内容类型: {content_type}")
                        print(f"  文件大小: {len(thumbnail_response.content)} bytes")
                        
                        # 保存缩略图用于检查
                        with open('test_video_thumbnail.jpg', 'wb') as f:
                            f.write(thumbnail_response.content)
                        print(f"  缩略图已保存为: test_video_thumbnail.jpg")
                    else:
                        print(f"✗ 缩略图内容类型错误: {content_type}")
                else:
                    print(f"✗ 缩略图生成失败: {thumbnail_response.status_code}")
                    print(f"  错误信息: {thumbnail_response.text}")
            else:
                print("⚠ 没有找到视频文件进行测试")
                
        else:
            print(f"✗ 文件API异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
    
    # 检查缓存目录
    print("\n4. 检查缓存目录...")
    cache_dir = Path("./Downloaded/temp/thumbnails")
    if cache_dir.exists():
        thumbnail_files = list(cache_dir.glob('*.jpg'))
        print(f"✓ 缓存目录存在: {cache_dir}")
        print(f"  缓存文件数量: {len(thumbnail_files)}")
        
        if thumbnail_files:
            print("  缓存文件列表:")
            for thumb_file in thumbnail_files[:5]:  # 只显示前5个
                print(f"    - {thumb_file.name}")
            
            if len(thumbnail_files) > 5:
                print(f"    ... 还有 {len(thumbnail_files) - 5} 个文件")
    else:
        print(f"⚠ 缓存目录不存在: {cache_dir}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n下一步:")
    print("1. 打开浏览器访问 http://localhost:5000")
    print("2. 切换到'文件'标签页")
    print("3. 检查视频文件是否显示缩略图")
    print("4. 测试懒加载功能")
    print("5. 检查缓存目录中的缩略图文件")

if __name__ == '__main__':
    test_video_thumbnails() 