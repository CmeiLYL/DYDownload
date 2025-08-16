#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试ffmpeg编码问题修复
"""

import subprocess
import sys
import os
from pathlib import Path

def test_ffmpeg_encoding():
    """测试ffmpeg编码问题"""
    print("=" * 60)
    print("测试ffmpeg编码问题修复")
    print("=" * 60)
    
    # 1. 检查ffmpeg是否安装
    print("\n1. 检查ffmpeg安装...")
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'], 
            capture_output=True, 
            text=True, 
            timeout=5,
            encoding='utf-8',
            errors='ignore'
        )
        if result.returncode == 0:
            print("✓ ffmpeg 已安装")
            print(f"版本信息: {result.stdout.split('ffmpeg version')[1].split('\n')[0] if 'ffmpeg version' in result.stdout else '未知版本'}")
        else:
            print("✗ ffmpeg 安装有问题")
            return
    except FileNotFoundError:
        print("✗ ffmpeg 未安装")
        return
    except Exception as e:
        print(f"✗ 检查ffmpeg时出错: {e}")
        return
    
    # 2. 查找测试视频文件
    print("\n2. 查找测试视频文件...")
    download_path = Path("./Downloaded/")
    if not download_path.exists():
        print("✗ 下载目录不存在")
        return
    
    video_files = []
    for ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm']:
        video_files.extend(download_path.rglob(f'*{ext}'))
    
    if not video_files:
        print("⚠ 没有找到视频文件")
        return
    
    test_video = video_files[0]
    print(f"✓ 找到测试视频: {test_video.name}")
    print(f"   路径: {test_video}")
    
    # 3. 测试ffmpeg命令
    print("\n3. 测试ffmpeg命令...")
    
    # 创建临时输出文件
    temp_output = Path("test_thumbnail_temp.jpg")
    
    try:
        cmd = [
            'ffmpeg', '-i', str(test_video),
            '-ss', '00:00:01',
            '-vframes', '1',
            '-vf', 'scale=200:150:force_original_aspect_ratio=decrease,pad=200:150:(ow-iw)/2:(oh-ih)/2',
            '-y',
            str(temp_output)
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        
        # 测试不同的编码方式
        encoding_methods = [
            ("UTF-8 with ignore", {'encoding': 'utf-8', 'errors': 'ignore'}),
            ("UTF-8 with replace", {'encoding': 'utf-8', 'errors': 'replace'}),
            ("System default", {}),
            ("No encoding (bytes)", {'text': False})
        ]
        
        for method_name, params in encoding_methods:
            print(f"\n   测试方法: {method_name}")
            try:
                if 'text' in params and not params['text']:
                    # 二进制模式
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        timeout=30,
                        **params
                    )
                    stdout = result.stdout.decode('utf-8', errors='ignore') if result.stdout else ""
                    stderr = result.stderr.decode('utf-8', errors='ignore') if result.stderr else ""
                else:
                    # 文本模式
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=30,
                        **params
                    )
                    stdout = result.stdout or ""
                    stderr = result.stderr or ""
                
                if result.returncode == 0:
                    print(f"   ✓ 成功 (返回码: {result.returncode})")
                    if temp_output.exists():
                        print(f"   ✓ 输出文件已生成: {temp_output.stat().st_size} bytes")
                    else:
                        print(f"   ⚠ 输出文件未生成")
                else:
                    print(f"   ✗ 失败 (返回码: {result.returncode})")
                    if stderr:
                        print(f"   错误信息: {stderr[:200]}...")
                
            except subprocess.TimeoutExpired:
                print(f"   ⚠ 超时")
            except Exception as e:
                print(f"   ✗ 异常: {e}")
    
    finally:
        # 清理临时文件
        if temp_output.exists():
            try:
                temp_output.unlink()
                print(f"\n   清理临时文件: {temp_output}")
            except:
                pass
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n建议:")
    print("1. 如果所有方法都失败，请检查ffmpeg安装")
    print("2. 如果某些方法成功，说明编码问题已解决")
    print("3. 推荐使用 'UTF-8 with ignore' 方法")

if __name__ == '__main__':
    test_ffmpeg_encoding() 