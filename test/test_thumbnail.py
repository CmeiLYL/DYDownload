#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试缩略图功能
"""

import os
import requests
from pathlib import Path
from PIL import Image
import io

def create_test_image():
    """创建测试图片"""
    # 创建一个简单的测试图片
    img = Image.new('RGB', (300, 200), color='red')
    
    # 添加一些文字或图案
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)
    
    # 尝试使用默认字体
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    draw.text((50, 80), "Test Image", fill='white', font=font)
    
    # 保存测试图片
    test_dir = Path("./Downloaded/test")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_image_path = test_dir / "test_image.jpg"
    img.save(test_image_path, 'JPEG')
    
    print(f"✓ 创建测试图片: {test_image_path}")
    return str(test_image_path.relative_to(Path("./Downloaded/")))

def test_thumbnail_api():
    """测试缩略图API"""
    print("=" * 50)
    print("测试缩略图功能")
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
    
    # 创建测试图片
    print("\n1. 创建测试图片...")
    test_image_path = create_test_image()
    
    # 测试缩略图API
    print("\n2. 测试缩略图API...")
    try:
        url = f"http://localhost:5000/api/file/thumbnail?path={test_image_path}"
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✓ 缩略图生成成功")
            
            # 验证返回的是图片
            content_type = response.headers.get('content-type', '')
            if 'image' in content_type:
                print(f"✓ 返回内容类型正确: {content_type}")
                
                # 保存缩略图用于验证
                thumbnail_path = "./test_thumbnail.jpg"
                with open(thumbnail_path, 'wb') as f:
                    f.write(response.content)
                
                # 检查缩略图尺寸
                with Image.open(thumbnail_path) as img:
                    width, height = img.size
                    print(f"✓ 缩略图尺寸: {width}x{height}")
                    
                    if width <= 200 and height <= 150:
                        print("✓ 缩略图尺寸符合要求")
                    else:
                        print("✗ 缩略图尺寸超出限制")
                
                # 清理测试文件
                os.remove(thumbnail_path)
                
            else:
                print(f"✗ 返回内容类型错误: {content_type}")
        else:
            print(f"✗ 缩略图生成失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"✗ 测试缩略图API出错: {e}")
    
    # 测试文件列表API
    print("\n3. 测试文件列表API...")
    try:
        response = requests.get('http://localhost:5000/api/files')
        if response.status_code == 200:
            files = response.json()
            print(f"✓ 成功获取 {len(files)} 个文件")
            
            # 查找测试图片
            test_files = [f for f in files if 'test_image' in f['name']]
            if test_files:
                print("✓ 找到测试图片文件")
                for file in test_files:
                    print(f"  - {file['name']} ({file['size']} bytes)")
            else:
                print("✗ 未找到测试图片文件")
        else:
            print(f"✗ 获取文件列表失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 获取文件列表出错: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == '__main__':
    test_thumbnail_api() 