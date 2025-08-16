#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试分页和分类功能
"""

import os
import requests
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

def create_test_files():
    """创建测试文件"""
    print("=" * 50)
    print("创建测试文件")
    print("=" * 50)
    
    # 创建测试目录
    test_dir = Path("./Downloaded/test_pagination")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建不同来源的目录
    sources = ["用户A", "用户B", "合集C", "用户D", "合集E"]
    
    for source in sources:
        source_dir = test_dir / source
        source_dir.mkdir(exist_ok=True)
        
        # 为每个来源创建不同类型的文件
        file_types = [
            ("video", "mp4", 10),
            ("image", "jpg", 8),
            ("audio", "mp3", 5),
            ("data", "json", 3)
        ]
        
        for file_type, ext, count in file_types:
            for i in range(count):
                filename = f"{source}_{file_type}_{i+1}.{ext}"
                file_path = source_dir / filename
                
                if file_type == "image":
                    # 创建测试图片
                    img = Image.new('RGB', (300, 200), color=(
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255)
                    ))
                    draw = ImageDraw.Draw(img)
                    try:
                        font = ImageFont.load_default()
                    except:
                        font = None
                    draw.text((50, 80), f"{source}\n{filename}", fill='white', font=font)
                    img.save(file_path, 'JPEG')
                else:
                    # 创建其他类型的文件
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"测试文件: {filename}\n来源: {source}\n类型: {file_type}")
                
                print(f"✓ 创建文件: {file_path}")
    
    print(f"✓ 共创建了 {len(sources)} 个来源的测试文件")

def test_pagination_features():
    """测试分页功能"""
    print("\n" + "=" * 50)
    print("测试分页和分类功能")
    print("=" * 50)
    
    # 检查服务器是否运行
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code != 200:
            print("✗ 服务器未正常运行")
            return
    except:
        print("✗ 无法连接到服务器，请先启动Web UI")
        return
    
    print("✓ 服务器正在运行")
    
    # 测试获取文件列表
    print("\n1. 测试获取文件列表...")
    try:
        response = requests.get('http://localhost:5000/api/files')
        if response.status_code == 200:
            files = response.json()
            print(f"✓ 成功获取 {len(files)} 个文件")
            
            # 分析文件类型分布
            file_types = {}
            sources = set()
            
            for file in files:
                ext = Path(file['name']).suffix.lower()
                if ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm']:
                    file_types['video'] = file_types.get('video', 0) + 1
                elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                    file_types['image'] = file_types.get('image', 0) + 1
                elif ext in ['.mp3', '.wav', '.aac', '.flac', '.m4a']:
                    file_types['audio'] = file_types.get('audio', 0) + 1
                else:
                    file_types['other'] = file_types.get('other', 0) + 1
                
                # 提取来源
                path_parts = file['path'].split('/')
                if len(path_parts) >= 2:
                    sources.add(path_parts[0])
            
            print("文件类型分布:")
            for file_type, count in file_types.items():
                print(f"  - {file_type}: {count} 个")
            
            print(f"文件来源: {len(sources)} 个")
            for source in sorted(sources):
                print(f"  - {source}")
                
        else:
            print(f"✗ 获取文件列表失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 获取文件列表出错: {e}")
    
    # 测试缩略图API
    print("\n2. 测试缩略图API...")
    try:
        # 查找一个图片文件
        response = requests.get('http://localhost:5000/api/files')
        if response.status_code == 200:
            files = response.json()
            image_files = [f for f in files if f['name'].lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
            
            if image_files:
                test_image = image_files[0]
                image_path = test_image['path'].replace('\\', '/')
                
                thumbnail_url = f"http://localhost:5000/api/file/thumbnail?path={image_path}"
                thumbnail_response = requests.get(thumbnail_url)
                
                if thumbnail_response.status_code == 200:
                    content_type = thumbnail_response.headers.get('content-type', '')
                    if 'image' in content_type:
                        print(f"✓ 缩略图生成成功: {test_image['name']}")
                        print(f"  内容类型: {content_type}")
                        print(f"  文件大小: {len(thumbnail_response.content)} bytes")
                    else:
                        print(f"✗ 缩略图内容类型错误: {content_type}")
                else:
                    print(f"✗ 缩略图生成失败: {thumbnail_response.status_code}")
            else:
                print("✗ 没有找到图片文件进行测试")
        else:
            print("✗ 无法获取文件列表进行缩略图测试")
    except Exception as e:
        print(f"✗ 测试缩略图API出错: {e}")
    
    # 测试日志API
    print("\n3. 测试日志API...")
    try:
        response = requests.get('http://localhost:5000/api/logs')
        if response.status_code == 200:
            logs = response.json()
            print(f"✓ 成功获取 {len(logs)} 条日志")
            
            if logs:
                print("最新日志:")
                for i, log in enumerate(logs[-3:]):
                    print(f"  - {log.strip()}")
        else:
            print(f"✗ 获取日志失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 获取日志出错: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)
    print("\n现在可以在Web界面中测试以下功能:")
    print("1. 文件类型筛选 (视频、图片、音频、数据、其他)")
    print("2. 下载来源筛选 (按不同用户/合集分类)")
    print("3. 排序功能 (按日期、文件名、文件大小)")
    print("4. 搜索功能 (按文件名搜索)")
    print("5. 分页功能 (每页显示12个文件)")
    print("6. 缩略图显示 (图片文件)")
    print("7. 文件统计信息")
    print("8. 点击文件在文件夹中打开")

if __name__ == '__main__':
    # 创建测试文件
    create_test_files()
    
    # 测试分页功能
    test_pagination_features() 