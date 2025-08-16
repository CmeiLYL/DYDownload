#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DY下载器 - 生产环境启动脚本
用于Gunicorn等WSGI服务器启动
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置生产环境
os.environ['FLASK_ENV'] = 'production'

# 导入应用
from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 