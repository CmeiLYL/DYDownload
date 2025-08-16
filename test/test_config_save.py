#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试配置保存功能
"""

import sys
import os
import yaml
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_config_save():
    """测试配置保存功能"""
    print("=" * 60)
    print("🧪 测试配置保存功能")
    print("=" * 60)
    
    try:
        # 导入配置管理器
        from app import config_manager
        
        # 创建测试配置
        test_config = {
            'link': ['https://v.douyin.com/test1/', 'https://v.douyin.com/test2/'],
            'path': './Downloaded/',
            'music': False,
            'cover': False,
            'avatar': False,
            'json': True,
            'folderstyle': False,
            'mode': ['post', 'like'],
            'thread': 8,
            'database': True,
            'number': {
                'post': 10,
                'like': 5,
                'mix': 3,
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
            'cookies': {
                'msToken': 'test_token_123',
                'ttwid': 'test_ttwid_456'
            }
        }
        
        print("📋 测试配置:")
        print(f"   - 链接数量: {len(test_config['link'])}")
        print(f"   - 下载选项: music={test_config['music']}, cover={test_config['cover']}, avatar={test_config['avatar']}, json={test_config['json']}")
        print(f"   - 下载数量: post={test_config['number']['post']}, like={test_config['number']['like']}, mix={test_config['number']['mix']}")
        print(f"   - 下载模式: {test_config['mode']}")
        print(f"   - 线程数: {test_config['thread']}")
        
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
        
        print("📄 保存的配置内容:")
        print(f"   - 链接数量: {len(saved_config.get('link', []))}")
        print(f"   - 下载选项: music={saved_config.get('music', False)}, cover={saved_config.get('cover', False)}, avatar={saved_config.get('avatar', False)}, json={saved_config.get('json', True)}")
        print(f"   - 下载数量: post={saved_config.get('number', {}).get('post', 0)}, like={saved_config.get('number', {}).get('like', 0)}, mix={saved_config.get('number', {}).get('mix', 0)}")
        print(f"   - 下载模式: {saved_config.get('mode', [])}")
        print(f"   - 线程数: {saved_config.get('thread', 5)}")
        
        # 检查配置是否匹配
        config_matches = (
            saved_config.get('link') == test_config['link'] and
            saved_config.get('music') == test_config['music'] and
            saved_config.get('cover') == test_config['cover'] and
            saved_config.get('avatar') == test_config['avatar'] and
            saved_config.get('json') == test_config['json'] and
            saved_config.get('number', {}).get('post') == test_config['number']['post'] and
            saved_config.get('number', {}).get('like') == test_config['number']['like'] and
            saved_config.get('number', {}).get('mix') == test_config['number']['mix'] and
            saved_config.get('mode') == test_config['mode'] and
            saved_config.get('thread') == test_config['thread']
        )
        
        if config_matches:
            print("\n✅ 配置保存验证通过！")
            return True
        else:
            print("\n❌ 配置保存验证失败！")
            return False
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        return False

def test_config_reload():
    """测试配置重新加载功能"""
    print("\n" + "=" * 60)
    print("🧪 测试配置重新加载功能")
    print("=" * 60)
    
    try:
        # 导入配置管理器
        from app import config_manager
        
        # 重新加载配置
        print("🔄 重新加载配置文件...")
        reloaded_config = config_manager.load_config()
        
        print("📋 重新加载的配置:")
        print(f"   - 链接数量: {len(reloaded_config.get('link', []))}")
        print(f"   - 下载选项: music={reloaded_config.get('music', False)}, cover={reloaded_config.get('cover', False)}, avatar={reloaded_config.get('avatar', False)}, json={reloaded_config.get('json', True)}")
        print(f"   - 下载数量: post={reloaded_config.get('number', {}).get('post', 0)}, like={reloaded_config.get('number', {}).get('like', 0)}, mix={reloaded_config.get('number', {}).get('mix', 0)}")
        print(f"   - 下载模式: {reloaded_config.get('mode', [])}")
        print(f"   - 线程数: {reloaded_config.get('thread', 5)}")
        
        # 检查是否有测试配置
        if len(reloaded_config.get('link', [])) >= 2 and 'test1' in reloaded_config.get('link', [''])[0]:
            print("✅ 配置重新加载成功！")
            return True
        else:
            print("❌ 配置重新加载失败！")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_douyin_command_config():
    """测试DouYinCommand配置传递"""
    print("\n" + "=" * 60)
    print("🧪 测试DouYinCommand配置传递")
    print("=" * 60)
    
    try:
        # 导入DouYinCommand模块
        import script.DouYinCommand as dyc
        
        # 重新加载配置文件
        from app import config_manager
        config = config_manager.load_config()
        
        print("📋 从配置文件加载的配置:")
        print(f"   - 链接数量: {len(config.get('link', []))}")
        print(f"   - 下载选项: music={config.get('music', False)}, cover={config.get('cover', False)}, avatar={config.get('avatar', False)}, json={config.get('json', True)}")
        print(f"   - 下载数量: post={config.get('number', {}).get('post', 0)}, like={config.get('number', {}).get('like', 0)}, mix={config.get('number', {}).get('mix', 0)}")
        
        # 更新DouYinCommand配置
        print("\n🔄 更新DouYinCommand配置...")
        
        dyc.configModel["link"] = config.get('link', [])
        dyc.configModel["path"] = config.get('path', './Downloaded/')
        dyc.configModel["music"] = config.get('music', False)
        dyc.configModel["cover"] = config.get('cover', False)
        dyc.configModel["avatar"] = config.get('avatar', False)
        dyc.configModel["json"] = config.get('json', True)
        dyc.configModel["folderstyle"] = config.get('folderstyle', False)
        dyc.configModel["mode"] = config.get('mode', ['post'])
        dyc.configModel["thread"] = config.get('thread', 5)
        dyc.configModel["database"] = config.get('database', True)
        
        # 更新数量限制
        numbers = config.get('number', {})
        dyc.configModel["number"]["post"] = numbers.get('post', 0)
        dyc.configModel["number"]["like"] = numbers.get('like', 0)
        dyc.configModel["number"]["allmix"] = numbers.get('allmix', 0)
        dyc.configModel["number"]["mix"] = numbers.get('mix', 0)
        dyc.configModel["number"]["music"] = numbers.get('music', 0)
        
        print("✅ DouYinCommand配置更新完成")
        
        # 验证DouYinCommand配置
        print("\n🔍 DouYinCommand配置验证:")
        print(f"   - 下载选项: music={dyc.configModel['music']}, cover={dyc.configModel['cover']}, avatar={dyc.configModel['avatar']}, json={dyc.configModel['json']}")
        print(f"   - 下载数量: post={dyc.configModel['number']['post']}, like={dyc.configModel['number']['like']}, mix={dyc.configModel['number']['mix']}")
        print(f"   - 下载模式: {dyc.configModel['mode']}")
        print(f"   - 线程数: {dyc.configModel['thread']}")
        
        # 检查配置是否匹配
        config_matches = (
            dyc.configModel['music'] == config.get('music', False) and
            dyc.configModel['cover'] == config.get('cover', False) and
            dyc.configModel['avatar'] == config.get('avatar', False) and
            dyc.configModel['json'] == config.get('json', True) and
            dyc.configModel['number']['post'] == config.get('number', {}).get('post', 0) and
            dyc.configModel['number']['like'] == config.get('number', {}).get('like', 0) and
            dyc.configModel['number']['mix'] == config.get('number', {}).get('mix', 0)
        )
        
        if config_matches:
            print("\n✅ DouYinCommand配置传递成功！")
            return True
        else:
            print("\n❌ DouYinCommand配置传递失败！")
            return False
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始测试配置保存功能...")
    
    # 运行所有测试
    tests = [
        test_config_save,
        test_config_reload,
        test_douyin_command_config
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
        print("🎉 所有测试通过！配置保存功能正常。")
        print("\n💡 现在下载前会先保存配置到YAML文件，确保使用最新的配置设置。")
    else:
        print("⚠️ 部分测试失败，请检查相关功能。")

if __name__ == '__main__':
    main() 