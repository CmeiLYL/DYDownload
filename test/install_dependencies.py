#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
安装缺失的依赖
"""

import subprocess
import sys
import os

def install_package(package):
    """安装单个包"""
    try:
        print(f"正在安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ {package} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {package} 安装失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("抖音下载器 Web UI - 依赖安装")
    print("=" * 60)
    
    # 需要安装的包
    packages = [
        "tqdm==4.66.1",
        "requests==2.31.0",
        "pyyaml==6.0.1",
        "rich==13.7.0",
        "flask==3.0.0",
        "flask-cors==4.0.0",
        "werkzeug==3.0.1",
        "pillow==10.0.1",
        "python-dateutil>=2.8.2",
        "requests-toolbelt>=1.0.0"
    ]
    
    print("\n开始安装依赖包...")
    
    success_count = 0
    total_count = len(packages)
    
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n安装完成: {success_count}/{total_count} 个包安装成功")
    
    if success_count == total_count:
        print("✓ 所有依赖安装成功！")
        print("\n现在可以启动 Web UI:")
        print("python app.py")
    else:
        print("⚠ 部分依赖安装失败，请检查网络连接或手动安装")
        print("\n手动安装命令:")
        for package in packages:
            print(f"pip install {package}")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main() 