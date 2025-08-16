#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ffmpeg 安装指南
"""

import subprocess
import sys
import platform
import os

def check_ffmpeg():
    """检查ffmpeg是否已安装"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ ffmpeg 已安装")
            print(f"版本信息: {result.stdout.split('ffmpeg version')[1].split('\n')[0]}")
            return True
        else:
            print("✗ ffmpeg 安装有问题")
            return False
    except FileNotFoundError:
        print("✗ ffmpeg 未安装")
        return False
    except Exception as e:
        print(f"✗ 检查ffmpeg时出错: {e}")
        return False

def install_ffmpeg_windows():
    """Windows安装指南"""
    print("\n=== Windows 安装指南 ===")
    print("1. 访问 https://ffmpeg.org/download.html")
    print("2. 点击 'Windows Builds'")
    print("3. 下载 'ffmpeg-master-latest-win64-gpl.zip'")
    print("4. 解压到 C:\\ffmpeg")
    print("5. 将 C:\\ffmpeg\\bin 添加到系统环境变量 PATH")
    print("\n或者使用 Chocolatey:")
    print("choco install ffmpeg")
    print("\n或者使用 Scoop:")
    print("scoop install ffmpeg")

def install_ffmpeg_macos():
    """macOS安装指南"""
    print("\n=== macOS 安装指南 ===")
    print("使用 Homebrew:")
    print("brew install ffmpeg")
    print("\n或者使用 MacPorts:")
    print("sudo port install ffmpeg")

def install_ffmpeg_linux():
    """Linux安装指南"""
    print("\n=== Linux 安装指南 ===")
    print("Ubuntu/Debian:")
    print("sudo apt update")
    print("sudo apt install ffmpeg")
    print("\nCentOS/RHEL/Fedora:")
    print("sudo yum install ffmpeg")
    print("或")
    print("sudo dnf install ffmpeg")
    print("\nArch Linux:")
    print("sudo pacman -S ffmpeg")

def main():
    """主函数"""
    print("=" * 60)
    print("ffmpeg 安装检查")
    print("=" * 60)
    
    # 检查当前系统
    system = platform.system()
    print(f"当前系统: {system}")
    
    # 检查ffmpeg
    if check_ffmpeg():
        print("\n✓ ffmpeg 已正确安装，视频缩略图功能可用！")
        return
    
    print("\n⚠ ffmpeg 未安装，视频缩略图功能将不可用")
    
    # 根据系统提供安装指南
    if system == "Windows":
        install_ffmpeg_windows()
    elif system == "Darwin":  # macOS
        install_ffmpeg_macos()
    elif system == "Linux":
        install_ffmpeg_linux()
    else:
        print(f"\n未知系统: {system}")
        print("请访问 https://ffmpeg.org/download.html 手动安装")
    
    print("\n" + "=" * 60)
    print("安装完成后，请重新启动Web服务器")
    print("=" * 60)

if __name__ == '__main__':
    main() 