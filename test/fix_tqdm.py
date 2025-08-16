#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
快速修复 tqdm 依赖问题
"""

import subprocess
import sys

def main():
    """安装 tqdm 依赖"""
    print("=" * 50)
    print("修复 tqdm 依赖问题")
    print("=" * 50)
    
    try:
        print("正在安装 tqdm...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm==4.66.1"])
        print("✓ tqdm 安装成功！")
        
        # 验证安装
        try:
            import tqdm
            print("✓ tqdm 模块导入成功")
            print(f"✓ tqdm 版本: {tqdm.__version__}")
        except ImportError:
            print("✗ tqdm 模块导入失败")
            return False
        
        print("\n现在可以重新启动下载功能了！")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ tqdm 安装失败: {e}")
        print("\n请尝试手动安装:")
        print("pip install tqdm==4.66.1")
        return False
    except Exception as e:
        print(f"✗ 安装过程出错: {e}")
        return False

if __name__ == '__main__':
    main() 