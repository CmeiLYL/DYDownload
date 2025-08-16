#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试后台缩略图生成功能
"""

import requests
import json
import time
from pathlib import Path

def test_background_thumbnails():
    """测试后台缩略图生成功能"""
    print("=" * 60)
    print("测试后台缩略图生成功能")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # 1. 检查ffmpeg
    print("\n1. 检查ffmpeg...")
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ ffmpeg 可用")
        else:
            print("✗ ffmpeg 不可用")
            return
    except FileNotFoundError:
        print("✗ ffmpeg 未安装")
        return
    
    # 2. 获取文件列表
    print("\n2. 获取文件列表...")
    try:
        response = requests.get(f"{base_url}/api/files", timeout=10)
        if response.status_code == 200:
            files = response.json()
            print(f"✓ 获取到 {len(files)} 个文件")
            
            # 查找视频文件
            video_files = [f for f in files if f['name'].lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm'))]
            print(f"✓ 找到 {len(video_files)} 个视频文件")
            
            if not video_files:
                print("⚠ 没有找到视频文件进行测试")
                return
            
            # 测试第一个视频文件
            test_video = video_files[0]
            video_path = test_video['path'].replace('\\', '/')
            
            print(f"\n3. 测试视频: {test_video['name']}")
            print(f"   路径: {video_path}")
            
            # 3. 检查初始状态
            print("\n4. 检查初始状态...")
            status_response = requests.get(f"{base_url}/api/file/thumbnail/status?path={video_path}")
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"   初始状态: {status_data['status']}")
            else:
                print(f"   ✗ 状态检查失败: {status_response.status_code}")
                return
            
            # 4. 请求缩略图生成
            print("\n5. 请求缩略图生成...")
            thumbnail_response = requests.get(f"{base_url}/api/file/thumbnail?path={video_path}")
            
            if thumbnail_response.status_code == 202:
                print("   ✓ 缩略图生成请求已接受，正在后台生成")
                
                # 5. 轮询状态
                print("\n6. 轮询生成状态...")
                max_polls = 30
                for i in range(max_polls):
                    time.sleep(1)
                    
                    status_response = requests.get(f"{base_url}/api/file/thumbnail/status?path={video_path}")
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        print(f"   第 {i+1} 次检查: {status_data['status']}")
                        
                        if status_data['status'] == 'ready':
                            print("   ✓ 缩略图生成完成！")
                            break
                    else:
                        print(f"   ✗ 状态检查失败: {status_response.status_code}")
                        break
                else:
                    print("   ⚠ 生成超时")
                
                # 6. 验证缩略图
                print("\n7. 验证缩略图...")
                final_response = requests.get(f"{base_url}/api/file/thumbnail?path={video_path}")
                if final_response.status_code == 200:
                    content_type = final_response.headers.get('content-type', '')
                    if 'image' in content_type:
                        print(f"   ✓ 缩略图验证成功")
                        print(f"   内容类型: {content_type}")
                        print(f"   文件大小: {len(final_response.content)} bytes")
                        
                        # 保存缩略图用于检查
                        with open('test_background_thumbnail.jpg', 'wb') as f:
                            f.write(final_response.content)
                        print(f"   缩略图已保存为: test_background_thumbnail.jpg")
                    else:
                        print(f"   ✗ 缩略图内容类型错误: {content_type}")
                else:
                    print(f"   ✗ 缩略图验证失败: {final_response.status_code}")
                    
            elif thumbnail_response.status_code == 200:
                print("   ✓ 缩略图已存在，直接返回")
            else:
                print(f"   ✗ 缩略图请求失败: {thumbnail_response.status_code}")
                print(f"   错误信息: {thumbnail_response.text}")
                
        else:
            print(f"✗ 文件API异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
    
    # 7. 检查缓存目录
    print("\n8. 检查缓存目录...")
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
    print("3. 观察视频文件的缩略图生成过程")
    print("4. 检查状态显示和轮询功能")

if __name__ == '__main__':
    test_background_thumbnails() 