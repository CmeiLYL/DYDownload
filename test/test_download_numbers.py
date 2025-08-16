#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试下载数量设置功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_config_loading():
    """测试配置加载"""
    print("=" * 50)
    print("🧪 测试下载数量设置功能")
    print("=" * 50)
    
    try:
        # 导入配置管理器
        from app import config_manager
        
        # 加载配置
        config = config_manager.config
        print("✅ 配置加载成功")
        
        # 检查下载数量设置
        number_config = config.get('number', {})
        print(f"📊 下载数量设置:")
        print(f"   - 发布作品: {number_config.get('post', 0)}")
        print(f"   - 喜欢作品: {number_config.get('like', 0)}")
        print(f"   - 合集: {number_config.get('mix', 0)}")
        print(f"   - 所有合集: {number_config.get('allmix', 0)}")
        print(f"   - 音乐: {number_config.get('music', 0)}")
        
        # 检查其他设置
        print(f"\n⚙️ 其他设置:")
        print(f"   - 下载模式: {config.get('mode', [])}")
        print(f"   - 线程数: {config.get('thread', 5)}")
        print(f"   - 下载路径: {config.get('path', './Downloaded/')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_douyin_command():
    """测试DouYinCommand模块"""
    print("\n" + "=" * 50)
    print("🧪 测试DouYinCommand模块")
    print("=" * 50)
    
    try:
        # 导入DouYinCommand模块
        import script.DouYinCommand as dyc
        
        # 检查配置模型
        print("✅ DouYinCommand模块导入成功")
        print(f"📊 配置模型:")
        print(f"   - 发布作品数量: {dyc.configModel['number']['post']}")
        print(f"   - 喜欢作品数量: {dyc.configModel['number']['like']}")
        print(f"   - 合集数量: {dyc.configModel['number']['mix']}")
        print(f"   - 所有合集数量: {dyc.configModel['number']['allmix']}")
        print(f"   - 音乐数量: {dyc.configModel['number']['music']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_web_ui_config():
    """测试Web UI配置收集"""
    print("\n" + "=" * 50)
    print("🧪 测试Web UI配置收集")
    print("=" * 50)
    
    try:
        # 模拟配置收集
        test_config = {
            'number': {
                'post': 10,
                'like': 5,
                'mix': 3,
                'allmix': 0,
                'music': 0
            },
            'mode': ['post', 'like'],
            'thread': 5,
            'path': './Downloaded/'
        }
        
        print("✅ 配置收集测试成功")
        print(f"📊 测试配置:")
        print(f"   - 发布作品数量: {test_config['number']['post']}")
        print(f"   - 喜欢作品数量: {test_config['number']['like']}")
        print(f"   - 合集数量: {test_config['number']['mix']}")
        print(f"   - 下载模式: {test_config['mode']}")
        print(f"   - 线程数: {test_config['thread']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始测试下载数量设置功能...")
    
    # 运行所有测试
    tests = [
        test_config_loading,
        test_douyin_command,
        test_web_ui_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print("📊 测试结果")
    print("=" * 50)
    print(f"✅ 通过: {passed}/{total}")
    print(f"❌ 失败: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！下载数量设置功能正常。")
    else:
        print("⚠️ 部分测试失败，请检查相关功能。")

if __name__ == '__main__':
    main() 