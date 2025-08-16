#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试Web UI配置读取
"""

import sys
import os
import yaml
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 切换到项目根目录
os.chdir(project_root)

def test_current_config():
    """测试当前配置"""
    print("=" * 60)
    print("🧪 测试当前配置")
    print("=" * 60)
    
    try:
        # 导入配置管理器
        from app import config_manager
        
        # 加载当前配置
        config = config_manager.load_config()
        
        print("📋 当前配置:")
        print(f"   - 链接数量: {len(config.get('link', []))}")
        print(f"   - 下载选项: music={config.get('music', False)}, cover={config.get('cover', False)}, avatar={config.get('avatar', False)}, json={config.get('json', True)}")
        
        number_config = config.get('number', {})
        print(f"   - 下载数量: post={number_config.get('post', 0)}, like={number_config.get('like', 0)}, mix={number_config.get('mix', 0)}")
        print(f"   - 下载模式: {config.get('mode', [])}")
        print(f"   - 线程数: {config.get('thread', 5)}")
        print(f"   - 下载路径: {config.get('path', './Downloaded/')}")
        
        # 检查下载数量是否为0
        if number_config.get('post', 0) == 0:
            print("✅ 发布作品数量已设置为0（全部下载）")
            return True
        else:
            print(f"❌ 发布作品数量为 {number_config.get('post', 0)}，应该为0")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_config_file():
    """测试配置文件内容"""
    print("\n" + "=" * 60)
    print("🧪 测试配置文件内容")
    print("=" * 60)
    
    try:
        config_path = Path("settings/config.yml")
        if not config_path.exists():
            print(f"❌ 配置文件不存在: {config_path}")
            return False
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print("📄 配置文件内容:")
        number_config = config.get('number', {})
        print(f"   - 发布作品数量: {number_config.get('post', 0)}")
        print(f"   - 喜欢作品数量: {number_config.get('like', 0)}")
        print(f"   - 合集数量: {number_config.get('mix', 0)}")
        
        if number_config.get('post', 0) == 0:
            print("✅ 配置文件中的发布作品数量为0")
            return True
        else:
            print(f"❌ 配置文件中的发布作品数量为 {number_config.get('post', 0)}，应该为0")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始测试Web UI配置...")
    
    # 运行所有测试
    tests = [
        test_current_config,
        test_config_file
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print("📊 测试结果")
    print("=" * 60)
    print(f"✅ 通过: {passed}/{total}")
    print(f"❌ 失败: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！配置已正确设置为0。")
        print("\n💡 现在请重新启动Web UI，然后在首页设置下载数量为0，再测试下载功能。")
    else:
        print("⚠️ 部分测试失败，请检查配置。")

if __name__ == '__main__':
    main() 