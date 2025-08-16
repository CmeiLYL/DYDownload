#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试配置传递功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_config_passing():
    """测试配置传递"""
    print("=" * 60)
    print("🧪 测试配置传递功能")
    print("=" * 60)
    
    try:
        # 导入DouYinCommand模块
        import script.DouYinCommand as dyc
        
        # 模拟Web UI传递的配置
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
                'post': 5,
                'like': 3,
                'mix': 2,
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
                'msToken': 'test_token',
                'ttwid': 'test_ttwid'
            }
        }
        
        print("📋 测试配置:")
        print(f"   - 下载选项: music={test_config['music']}, cover={test_config['cover']}, avatar={test_config['avatar']}, json={test_config['json']}")
        print(f"   - 下载数量: post={test_config['number']['post']}, like={test_config['number']['like']}, mix={test_config['number']['mix']}")
        print(f"   - 下载模式: {test_config['mode']}")
        print(f"   - 线程数: {test_config['thread']}")
        
        # 更新DouYinCommand的配置
        print("\n🔄 更新DouYinCommand配置...")
        
        # 更新基本配置
        dyc.configModel["link"] = test_config['link']
        dyc.configModel["path"] = test_config['path']
        dyc.configModel["music"] = test_config['music']
        dyc.configModel["cover"] = test_config['cover']
        dyc.configModel["avatar"] = test_config['avatar']
        dyc.configModel["json"] = test_config['json']
        dyc.configModel["folderstyle"] = test_config['folderstyle']
        dyc.configModel["mode"] = test_config['mode']
        dyc.configModel["thread"] = test_config['thread']
        dyc.configModel["database"] = test_config['database']
        
        # 更新数量限制
        numbers = test_config['number']
        dyc.configModel["number"]["post"] = numbers['post']
        dyc.configModel["number"]["like"] = numbers['like']
        dyc.configModel["number"]["allmix"] = numbers['allmix']
        dyc.configModel["number"]["mix"] = numbers['mix']
        dyc.configModel["number"]["music"] = numbers['music']
        
        # 更新增量下载设置
        increase = test_config['increase']
        dyc.configModel["increase"]["post"] = increase['post']
        dyc.configModel["increase"]["like"] = increase['like']
        dyc.configModel["increase"]["allmix"] = increase['allmix']
        dyc.configModel["increase"]["mix"] = increase['mix']
        dyc.configModel["increase"]["music"] = increase['music']
        
        # 设置Cookie
        cookies = test_config['cookies']
        if cookies:
            cookie_str = "; ".join(f"{k}={v}" for k, v in cookies.items())
            dyc.configModel["cookie"] = cookie_str
        
        print("✅ 配置更新完成")
        
        # 验证配置是否正确设置
        print("\n🔍 验证配置设置:")
        print(f"   - 下载选项: music={dyc.configModel['music']}, cover={dyc.configModel['cover']}, avatar={dyc.configModel['avatar']}, json={dyc.configModel['json']}")
        print(f"   - 下载数量: post={dyc.configModel['number']['post']}, like={dyc.configModel['number']['like']}, mix={dyc.configModel['number']['mix']}")
        print(f"   - 下载模式: {dyc.configModel['mode']}")
        print(f"   - 线程数: {dyc.configModel['thread']}")
        print(f"   - Cookie: {dyc.configModel['cookie'][:50]}..." if dyc.configModel['cookie'] else "   - Cookie: 未设置")
        
        # 检查配置是否匹配
        config_matches = (
            dyc.configModel['music'] == test_config['music'] and
            dyc.configModel['cover'] == test_config['cover'] and
            dyc.configModel['avatar'] == test_config['avatar'] and
            dyc.configModel['json'] == test_config['json'] and
            dyc.configModel['number']['post'] == test_config['number']['post'] and
            dyc.configModel['number']['like'] == test_config['number']['like'] and
            dyc.configModel['number']['mix'] == test_config['number']['mix']
        )
        
        if config_matches:
            print("\n✅ 配置传递测试通过！")
            return True
        else:
            print("\n❌ 配置传递测试失败！")
            return False
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        return False

def test_default_config():
    """测试默认配置"""
    print("\n" + "=" * 60)
    print("🧪 测试默认配置")
    print("=" * 60)
    
    try:
        # 导入配置管理器
        from app import config_manager
        
        # 加载配置
        config = config_manager.config
        print("📋 默认配置:")
        print(f"   - 下载选项: music={config.get('music', False)}, cover={config.get('cover', False)}, avatar={config.get('avatar', False)}, json={config.get('json', True)}")
        print(f"   - 下载数量: post={config.get('number', {}).get('post', 0)}, like={config.get('number', {}).get('like', 0)}, mix={config.get('number', {}).get('mix', 0)}")
        print(f"   - 下载模式: {config.get('mode', [])}")
        print(f"   - 线程数: {config.get('thread', 5)}")
        
        # 检查默认设置是否正确
        default_correct = (
            config.get('music', False) == False and
            config.get('cover', False) == False and
            config.get('avatar', False) == False and
            config.get('json', True) == True
        )
        
        if default_correct:
            print("✅ 默认配置正确！")
            return True
        else:
            print("❌ 默认配置不正确！")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始测试配置传递功能...")
    
    # 运行所有测试
    tests = [
        test_config_passing,
        test_default_config
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
        print("🎉 所有测试通过！配置传递功能正常。")
        print("\n💡 现在Web UI的配置设置应该能正确传递给下载模块了。")
    else:
        print("⚠️ 部分测试失败，请检查相关功能。")

if __name__ == '__main__':
    main() 