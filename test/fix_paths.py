#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
路径修复脚本 - 检查和修复项目中的路径问题
"""

import os
import sys
from pathlib import Path

def check_and_fix_paths():
    """检查并修复项目中的路径问题"""
    print("=" * 60)
    print("🔧 路径修复脚本")
    print("=" * 60)
    
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    print(f"项目根目录: {project_root}")
    
    # 检查必要的目录是否存在
    required_dirs = [
        'docs',
        'ui',
        'script', 
        'settings',
        'utils',
        'test',
        'logs',
        'img',
        'apiproxy'
    ]
    
    print("\n📁 检查目录结构...")
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ (不存在)")
    
    # 检查必要的文件是否存在
    required_files = [
        'app.py',
        'requirements.txt',
        'settings/config.yml',
        'settings/config.example.yml',
        'ui/templates/index.html',
        'ui/static/app.js'
    ]
    
    print("\n📄 检查必要文件...")
    for file_name in required_files:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} (不存在)")
    
    # 检查Python路径
    print("\n🐍 检查Python路径...")
    current_dir = str(project_root)
    if current_dir in sys.path:
        print(f"✅ 项目根目录已在Python路径中")
    else:
        print(f"❌ 项目根目录不在Python路径中")
        print("建议在运行脚本时添加项目根目录到Python路径")
    
    # 检查配置文件路径
    print("\n⚙️ 检查配置文件路径...")
    config_path = project_root / 'settings' / 'config.yml'
    if config_path.exists():
        print(f"✅ 配置文件存在: {config_path}")
    else:
        print(f"❌ 配置文件不存在: {config_path}")
        example_config = project_root / 'settings' / 'config.example.yml'
        if example_config.exists():
            print("💡 建议复制 config.example.yml 为 config.yml")
    
    # 检查数据库文件
    print("\n🗄️ 检查数据库文件...")
    db_path = project_root / 'settings' / 'data.db'
    if db_path.exists():
        print(f"✅ 数据库文件存在: {db_path}")
    else:
        print(f"⚠️ 数据库文件不存在: {db_path}")
        print("💡 数据库文件会在首次运行时自动创建")
    
    print("\n" + "=" * 60)
    print("🔧 路径检查完成")
    print("=" * 60)

def test_imports():
    """测试关键模块的导入"""
    print("\n🧪 测试模块导入...")
    
    # 添加项目根目录到Python路径
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # 测试导入
    modules_to_test = [
        ('app', '主应用程序'),
        ('script.DouYinCommand', '抖音命令模块'),
        ('apiproxy.douyin.douyin', '抖音API模块'),
        ('apiproxy.common.utils', '工具模块'),
    ]
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {description} ({module_name})")
        except ImportError as e:
            print(f"❌ {description} ({module_name}): {e}")

def main():
    """主函数"""
    check_and_fix_paths()
    test_imports()
    
    print("\n💡 修复建议:")
    print("1. 如果配置文件不存在，请复制 settings/config.example.yml 为 settings/config.yml")
    print("2. 如果模块导入失败，请确保在项目根目录下运行脚本")
    print("3. 如果路径问题仍然存在，请检查文件权限和Python环境")

if __name__ == '__main__':
    main() 