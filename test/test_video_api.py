#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试新的视频API
"""

import requests
import json
from pathlib import Path

def test_video_api():
    """测试新的视频API"""
    print("=" * 60)
    print("测试新的视频API")
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
            
            print(f"✓ 找到 {len(video_files)} 个视频文件")
            
            # 2. 测试新的视频API
            if video_files:
                print(f"\n2. 测试新的视频API...")
                test_video = video_files[0]
                video_path = test_video['path'].replace('\\', '/')
                
                print(f"   测试视频: {test_video['name']}")
                print(f"   文件路径: {video_path}")
                print(f"   文件大小: {test_video['size']} bytes")
                
                # 测试完整视频请求
                video_response = requests.get(f"{base_url}/api/file/video?path={video_path}")
                if video_response.status_code == 200:
                    print(f"   ✓ 视频API成功")
                    print(f"   状态码: {video_response.status_code}")
                    
                    # 检查响应头
                    headers = video_response.headers
                    print(f"   内容类型: {headers.get('content-type', 'N/A')}")
                    print(f"   接受范围: {headers.get('accept-ranges', 'N/A')}")
                    print(f"   缓存控制: {headers.get('cache-control', 'N/A')}")
                    print(f"   内容处置: {headers.get('content-disposition', 'N/A')}")
                    print(f"   内容长度: {headers.get('content-length', 'N/A')}")
                    print(f"   返回大小: {len(video_response.content)} bytes")
                    
                    # 验证返回的文件大小是否匹配
                    if len(video_response.content) == test_video['size']:
                        print(f"   ✓ 文件大小匹配")
                    else:
                        print(f"   ⚠ 文件大小不匹配: 期望 {test_video['size']}, 实际 {len(video_response.content)}")
                else:
                    print(f"   ✗ 视频API失败: {video_response.status_code}")
                    print(f"   错误信息: {video_response.text}")
                
                # 3. 测试Range请求
                print(f"\n3. 测试Range请求...")
                headers = {'Range': 'bytes=0-1023'}
                range_response = requests.get(f"{base_url}/api/file/video?path={video_path}", headers=headers)
                
                if range_response.status_code == 206:
                    print(f"   ✓ Range请求成功")
                    print(f"   状态码: {range_response.status_code}")
                    print(f"   内容范围: {range_response.headers.get('content-range', 'N/A')}")
                    print(f"   返回大小: {len(range_response.content)} bytes")
                else:
                    print(f"   ⚠ Range请求返回: {range_response.status_code}")
                
                # 4. 测试HEAD请求
                print(f"\n4. 测试HEAD请求...")
                head_response = requests.head(f"{base_url}/api/file/video?path={video_path}")
                if head_response.status_code == 200:
                    print(f"   ✓ HEAD请求成功")
                    print(f"   内容类型: {head_response.headers.get('content-type', 'N/A')}")
                    print(f"   内容长度: {head_response.headers.get('content-length', 'N/A')}")
                    print(f"   接受范围: {head_response.headers.get('accept-ranges', 'N/A')}")
                else:
                    print(f"   ⚠ HEAD请求返回: {head_response.status_code}")
            
        else:
            print(f"✗ 文件API异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n新功能:")
    print("1. 专门的视频API：/api/file/video")
    print("2. 更好的Range请求支持")
    print("3. 正确的响应头设置")
    print("4. 前端使用专门的视频API")
    print("5. 更好的错误处理和日志")
    
    print("\n使用方法:")
    print("1. 点击文件卡片预览")
    print("2. 视频：使用专门的视频API")
    print("3. 图片：继续使用预览API")
    print("4. 视频：应该能正常显示画面和声音")

if __name__ == '__main__':
    test_video_api() 