#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试分页更新脚本
"""

import requests
import json

def test_pagination_update():
    """测试分页更新"""
    print("=" * 60)
    print("测试分页更新 - 每页15个文件")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # 测试文件API
    print("\n1. 测试文件API...")
    try:
        response = requests.get(f"{base_url}/api/files", timeout=10)
        if response.status_code == 200:
            files = response.json()
            print(f"✓ 文件API正常，获取到 {len(files)} 个文件")
            
            # 计算分页信息
            items_per_page = 15
            total_pages = (len(files) + items_per_page - 1) // items_per_page
            
            print(f"\n分页信息:")
            print(f"  - 每页显示: {items_per_page} 个文件")
            print(f"  - 总页数: {total_pages} 页")
            print(f"  - 总文件数: {len(files)} 个")
            
            # 显示每页的文件数量
            for page in range(1, min(total_pages + 1, 6)):  # 只显示前5页
                start_idx = (page - 1) * items_per_page
                end_idx = min(start_idx + items_per_page, len(files))
                page_files = files[start_idx:end_idx]
                print(f"  - 第 {page} 页: {len(page_files)} 个文件")
            
            if total_pages > 5:
                print(f"  - ... 还有 {total_pages - 5} 页")
                
        else:
            print(f"✗ 文件API异常: {response.status_code}")
    except Exception as e:
        print(f"✗ 文件API测试失败: {e}")
    
    # 测试静态文件
    print("\n2. 测试静态文件...")
    try:
        response = requests.get(f"{base_url}/static/app_simple.js", timeout=5)
        if response.status_code == 200:
            content = response.text
            if 'fileItemsPerPage = 15' in content:
                print("✓ app_simple.js 已更新为每页15个文件")
            else:
                print("⚠ app_simple.js 可能未正确更新")
        else:
            print(f"✗ 静态文件访问失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 静态文件测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n下一步:")
    print("1. 打开浏览器访问 http://localhost:5000")
    print("2. 切换到'文件'标签页")
    print("3. 检查每页是否显示15个文件")
    print("4. 测试分页功能是否正常工作")

if __name__ == '__main__':
    test_pagination_update() 