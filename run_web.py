#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
抖音下载器 Web UI 启动脚本
"""

import os
import sys
import webbrowser
import threading
import time
from pathlib import Path

def check_dependencies():
    """检查依赖包"""
    required_packages = ['flask', 'flask-cors', 'pyyaml']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"缺少依赖包: {', '.join(missing_packages)}")
        print("请运行以下命令安装:")
        print(f"pip install {' '.join(missing_packages)}")
    
    return True

def create_directories():
    """创建必要的目录"""
    directories = ['templates', 'static', 'logs', 'Downloaded']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def main():
    """主函数"""
    print("=" * 50)
    print("抖音下载器 Web UI")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        input("按回车键退出...")
        return
    
    # 创建目录
    create_directories()
    
    # 导入并启动Flask应用
    try:
        from app import app
        
        # 在后台线程中打开浏览器
        def open_browser():
            time.sleep(2)  # 等待服务器启动
            webbrowser.open('http://localhost:5000')
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        print("正在启动Web界面...")
        print("浏览器将自动打开 http://localhost:5000")
        print("按 Ctrl+C 停止服务器")
        print("-" * 50)
        
        # 启动Flask应用
        app.run(debug=False, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        input("按回车键退出...")

if __name__ == '__main__':
    main() 