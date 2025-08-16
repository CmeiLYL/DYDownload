#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试下载数量配置读取功能
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

def test_number_config_save():
    """测试下载数量配置保存"""
    print("=" * 60)
    print("🧪 测试下载数量配置保存")
    print("=" * 60)
    
    try:
        # 导入配置管理器
        from app import config_manager
        
        # 创建测试配置，重点测试下载数量
        test_config = {
            'link': ['https://v.douyin.com/test/'],
            'path': './Downloaded/',
            'music': False,
            'cover': False,
            'avatar': False,
            'json': True,
            'folderstyle': False,
            'mode': ['post'],
            'thread': 5,
            'database': True,
            'number': {
                'post': 15,      # 测试发布作品数量
                'like': 8,       # 测试喜欢作品数量
                'mix': 5,        # 测试合集数量
                'allmix': 0,
                'music': 0
            },
            'increase': {
                'post': False,
                'like': False,
                'mix': False,
                'allmix': False,
                'music': False
            },
            'cookies': {}
        }
        
        print("📋 测试配置（重点下载数量）:")
        print(f"   - 发布作品数量: {test_config['number']['post']}")
        print(f"   - 喜欢作品数量: {test_config['number']['like']}")
        print(f"   - 合集数量: {test_config['number']['mix']}")
        
        # 保存配置
        print("\n💾 保存配置到YAML文件...")
        if config_manager.save_config(test_config):
            print("✅ 配置保存成功")
        else:
            print("❌ 配置保存失败")
            return False
        
        # 验证配置文件
        print("\n🔍 验证配置文件...")
        config_path = config_manager.config_path
        if not config_path.exists():
            print(f"❌ 配置文件不存在: {config_path}")
            return False
        
        # 读取并验证保存的配置
        with open(config_path, 'r', encoding='utf-8') as f:
            saved_config = yaml.safe_load(f)
        
        print("📄 保存的下载数量配置:")
        saved_number = saved_config.get('number', {})
        print(f"   - 发布作品数量: {saved_number.get('post', 0)}")
        print(f"   - 喜欢作品数量: {saved_number.get('like', 0)}")
        print(f"   - 合集数量: {saved_number.get('mix', 0)}")
        
        # 检查下载数量是否匹配
        number_matches = (
            saved_number.get('post', 0) == test_config['number']['post'] and
            saved_number.get('like', 0) == test_config['number']['like'] and
            saved_number.get('mix', 0) == test_config['number']['mix']
        )
        
        if number_matches:
            print("\n✅ 下载数量配置保存验证通过！")
            return True
        else:
            print("\n❌ 下载数量配置保存验证失败！")
            return False
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        return False

def test_number_config_reload():
    """测试下载数量配置重新加载"""
    print("\n" + "=" * 60)
    print("🧪 测试下载数量配置重新加载")
    print("=" * 60)
    
    try:
        # 导入配置管理器
        from app import config_manager
        
        # 重新加载配置
        print("🔄 重新加载配置文件...")
        reloaded_config = config_manager.load_config()
        
        print("📋 重新加载的下载数量配置:")
        reloaded_number = reloaded_config.get('number', {})
        print(f"   - 发布作品数量: {reloaded_number.get('post', 0)}")
        print(f"   - 喜欢作品数量: {reloaded_number.get('like', 0)}")
        print(f"   - 合集数量: {reloaded_number.get('mix', 0)}")
        
        # 检查是否有测试配置
        if (reloaded_number.get('post', 0) == 15 and 
            reloaded_number.get('like', 0) == 8 and 
            reloaded_number.get('mix', 0) == 5):
            print("✅ 下载数量配置重新加载成功！")
            return True
        else:
            print("❌ 下载数量配置重新加载失败！")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_douyin_command_number_config():
    """测试DouYinCommand下载数量配置传递"""
    print("\n" + "=" * 60)
    print("🧪 测试DouYinCommand下载数量配置传递")
    print("=" * 60)
    
    try:
        # 导入DouYinCommand模块
        import script.DouYinCommand as dyc
        
        # 重新加载配置文件
        from app import config_manager
        config = config_manager.load_config()
        
        print("📋 从配置文件加载的下载数量配置:")
        config_number = config.get('number', {})
        print(f"   - 发布作品数量: {config_number.get('post', 0)}")
        print(f"   - 喜欢作品数量: {config_number.get('like', 0)}")
        print(f"   - 合集数量: {config_number.get('mix', 0)}")
        
        # 更新DouYinCommand配置
        print("\n🔄 更新DouYinCommand下载数量配置...")
        
        # 更新数量限制
        numbers = config.get('number', {})
        dyc.configModel["number"]["post"] = numbers.get('post', 0)
        dyc.configModel["number"]["like"] = numbers.get('like', 0)
        dyc.configModel["number"]["allmix"] = numbers.get('allmix', 0)
        dyc.configModel["number"]["mix"] = numbers.get('mix', 0)
        dyc.configModel["number"]["music"] = numbers.get('music', 0)
        
        print("✅ DouYinCommand下载数量配置更新完成")
        
        # 验证DouYinCommand配置
        print("\n🔍 DouYinCommand下载数量配置验证:")
        print(f"   - 发布作品数量: {dyc.configModel['number']['post']}")
        print(f"   - 喜欢作品数量: {dyc.configModel['number']['like']}")
        print(f"   - 合集数量: {dyc.configModel['number']['mix']}")
        print(f"   - 所有合集数量: {dyc.configModel['number']['allmix']}")
        print(f"   - 音乐数量: {dyc.configModel['number']['music']}")
        
        # 检查配置是否匹配
        number_matches = (
            dyc.configModel['number']['post'] == config_number.get('post', 0) and
            dyc.configModel['number']['like'] == config_number.get('like', 0) and
            dyc.configModel['number']['mix'] == config_number.get('mix', 0) and
            dyc.configModel['number']['allmix'] == config_number.get('allmix', 0) and
            dyc.configModel['number']['music'] == config_number.get('music', 0)
        )
        
        if number_matches:
            print("\n✅ DouYinCommand下载数量配置传递成功！")
            return True
        else:
            print("\n❌ DouYinCommand下载数量配置传递失败！")
            return False
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        return False

def test_web_ui_number_config():
    """测试Web UI下载数量配置模拟"""
    print("\n" + "=" * 60)
    print("🧪 测试Web UI下载数量配置模拟")
    print("=" * 60)
    
    try:
        # 模拟Web UI收集的配置
        web_ui_config = {
            'link': ['https://v.douyin.com/test/'],
            'path': './Downloaded/',
            'music': False,
            'cover': False,
            'avatar': False,
            'json': True,
            'folderstyle': False,
            'mode': ['post'],
            'thread': 5,
            'database': True,
            'number': {
                'post': 20,      # 模拟用户设置的发布作品数量
                'like': 10,      # 模拟用户设置的喜欢作品数量
                'mix': 7,        # 模拟用户设置的合集数量
                'allmix': 0,
                'music': 0
            },
            'increase': {
                'post': False,
                'like': False,
                'mix': False,
                'allmix': False,
                'music': False
            },
            'cookies': {}
        }
        
        print("📋 模拟Web UI配置:")
        print(f"   - 发布作品数量: {web_ui_config['number']['post']}")
        print(f"   - 喜欢作品数量: {web_ui_config['number']['like']}")
        print(f"   - 合集数量: {web_ui_config['number']['mix']}")
        
        # 模拟保存配置
        from app import config_manager
        if config_manager.save_config(web_ui_config):
            print("✅ Web UI配置保存成功")
        else:
            print("❌ Web UI配置保存失败")
            return False
        
        # 验证保存的配置
        reloaded_config = config_manager.load_config()
        reloaded_number = reloaded_config.get('number', {})
        
        print("📄 保存后的下载数量配置:")
        print(f"   - 发布作品数量: {reloaded_number.get('post', 0)}")
        print(f"   - 喜欢作品数量: {reloaded_number.get('like', 0)}")
        print(f"   - 合集数量: {reloaded_number.get('mix', 0)}")
        
        # 检查是否匹配
        if (reloaded_number.get('post', 0) == web_ui_config['number']['post'] and
            reloaded_number.get('like', 0) == web_ui_config['number']['like'] and
            reloaded_number.get('mix', 0) == web_ui_config['number']['mix']):
            print("✅ Web UI下载数量配置测试通过！")
            return True
        else:
            print("❌ Web UI下载数量配置测试失败！")
            return False
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始测试下载数量配置功能...")
    
    # 运行所有测试
    tests = [
        test_number_config_save,
        test_number_config_reload,
        test_douyin_command_number_config,
        test_web_ui_number_config
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
        print("🎉 所有测试通过！下载数量配置功能正常。")
        print("\n💡 现在Web UI的下载数量设置应该能正确保存和传递了。")
    else:
        print("⚠️ 部分测试失败，请检查相关功能。")

if __name__ == '__main__':
    main() 