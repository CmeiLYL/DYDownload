#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
抖音下载器 Web UI - 快速启动脚本
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ 错误：需要 Python 3.7 或更高版本")
        print(f"当前版本：{sys.version}")
        return False
    print(f"✅ Python 版本：{sys.version.split()[0]}")
    return True

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        'flask', 'flask-cors', 'pyyaml', 'pillow', 'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} (缺失)")
    
    if missing_packages:
        print(f"\n⚠️  缺少依赖包：{', '.join(missing_packages)}")
        print("请运行以下命令安装：")
        print("pip install -r requirements.txt")
        print("或者运行：python test/install_dependencies.py")
        return False
    
    return True

def check_config():
    """检查配置文件"""
    config_file = Path("config.yml")
    if not config_file.exists():
        print("⚠️  配置文件不存在，正在创建...")
        example_config = Path("config.example.yml")
        if example_config.exists():
            import shutil
            shutil.copy(example_config, config_file)
            print("✅ 已创建配置文件 config.yml")
            print("请编辑 config.yml 文件，添加抖音链接")
        else:
            print("❌ 配置文件示例不存在")
            return False
    else:
        print("✅ 配置文件存在")
    
    return True

def check_directories():
    """检查必要目录"""
    directories = ['logs', 'Downloaded', 'templates', 'static']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ 目录 {directory}/")

def start_web_ui():
    """启动Web UI"""
    print("\n🚀 正在启动抖音下载器 Web UI...")
    
    try:
        # 启动Flask应用
        from app import app
        print("✅ Flask应用启动成功")
        print("🌐 访问地址：http://localhost:5000")
        print("📝 按 Ctrl+C 停止服务")
        
        # 自动打开浏览器
        time.sleep(2)
        try:
            webbrowser.open('http://localhost:5000')
            print("🌐 已自动打开浏览器")
        except:
            print("⚠️  无法自动打开浏览器，请手动访问：http://localhost:5000")
        
        # 启动Flask开发服务器
        app.run(debug=False, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ 导入错误：{e}")
        print("请确保已安装所有依赖包")
        return False
    except Exception as e:
        print(f"❌ 启动失败：{e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🎯 抖音下载器 Web UI - 快速启动")
    print("=" * 60)
    
    # 检查Python版本
    print("\n1. 检查Python版本...")
    if not check_python_version():
        return
    
    # 检查依赖包
    print("\n2. 检查依赖包...")
    if not check_dependencies():
        print("\n💡 提示：")
        print("1. 运行：pip install -r requirements.txt")
        print("2. 或者运行：python test/install_dependencies.py")
        print("3. 然后重新运行此脚本")
        return
    
    # 检查配置文件
    print("\n3. 检查配置文件...")
    if not check_config():
        return
    
    # 检查目录
    print("\n4. 检查目录结构...")
    check_directories()
    
    # 启动Web UI
    print("\n5. 启动Web UI...")
    start_web_ui()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已停止服务")
    except Exception as e:
        print(f"\n❌ 发生错误：{e}")
        print("\n💡 如果遇到问题，请：")
        print("1. 检查网络连接")
        print("2. 运行：python test/diagnose_web.py")
        print("3. 查看日志文件：logs/douyin.log") 