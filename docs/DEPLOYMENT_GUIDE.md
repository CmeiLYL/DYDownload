# DY下载器 - 部署指南

## 概述

本文档提供了DY下载器应用的多种部署方式，从简单的本地部署到生产环境的完整部署方案。

## 部署方式

### 1. 本地部署（推荐新手）

#### 1.1 直接运行
```bash
# 克隆或下载项目
git clone <your-repository-url>
cd DYDownload

# 安装依赖
pip install -r requirements.txt

# 启动应用
python app.py
```

#### 1.2 使用批处理文件（Windows）
```bash
# 双击运行
ui/start_web_ui.bat
```

#### 1.3 使用启动脚本
```bash
# 使用快速启动脚本
python script/quick_start.py

# 或使用UI目录下的脚本
cd ui
python run_web.py
```

### 2. 服务器部署

#### 2.1 使用Gunicorn（推荐）

**安装Gunicorn：**
```bash
pip install gunicorn
```

**创建启动脚本 `start_server.py`：**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 导入应用
from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**启动命令：**
```bash
# 开发环境
gunicorn -w 4 -b 0.0.0.0:5000 start_server:app

# 生产环境
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 --max-requests 1000 start_server:app
```

#### 2.2 使用Docker部署

**创建Dockerfile：**
```dockerfile
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p logs Downloaded ui/templates ui/static settings

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "app.py"]
```

**创建docker-compose.yml：**
```yaml
version: '3.8'

services:
  dy-downloader:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./Downloaded:/app/Downloaded
      - ./logs:/app/logs
      - ./settings:/app/settings
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

**启动Docker容器：**
```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 3. 云平台部署

#### 3.1 部署到Heroku

**创建Procfile：**
```
web: gunicorn start_server:app
```

**创建runtime.txt：**
```
python-3.9.18
```

**创建requirements.txt（确保包含）：**
```
Flask==2.3.3
gunicorn==21.2.0
PyYAML==6.0.1
Pillow==10.0.1
flask-cors==4.0.0
```

**部署命令：**
```bash
# 安装Heroku CLI
# 登录Heroku
heroku login

# 创建应用
heroku create your-app-name

# 添加构建包（如果需要ffmpeg）
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-ffmpeg-latest.git
heroku buildpacks:add heroku/python

# 部署
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# 打开应用
heroku open
```

#### 3.2 部署到Vercel

**创建vercel.json：**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "start_server.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "start_server.py"
    }
  ]
}
```

**部署命令：**
```bash
# 安装Vercel CLI
npm i -g vercel

# 部署
vercel
```

#### 3.3 部署到Railway

**创建railway.json：**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app.py",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 4. 生产环境配置

#### 4.1 使用Nginx反向代理

**安装Nginx：**
```bash
# Ubuntu/Debian
sudo apt-get install nginx

# CentOS/RHEL
sudo yum install nginx
```

**配置Nginx `/etc/nginx/sites-available/dy-downloader`：**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 支持WebSocket
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 静态文件缓存
    location /static/ {
        alias /path/to/your/app/ui/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # 文件下载优化
    location /api/file/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_buffering off;
        proxy_request_buffering off;
    }
}
```

**启用配置：**
```bash
sudo ln -s /etc/nginx/sites-available/dy-downloader /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 4.2 使用Systemd服务

**创建服务文件 `/etc/systemd/system/dy-downloader.service`：**
```ini
[Unit]
Description=DY Downloader Web Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/your/app
Environment=PATH=/path/to/your/venv/bin
ExecStart=/path/to/your/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 start_server:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**启动服务：**
```bash
sudo systemctl daemon-reload
sudo systemctl enable dy-downloader
sudo systemctl start dy-downloader
sudo systemctl status dy-downloader
```

### 5. 安全配置

#### 5.1 环境变量配置

**创建.env文件：**
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DEBUG=False
```

**修改app.py以使用环境变量：**
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
```

#### 5.2 SSL证书配置

**使用Let's Encrypt：**
```bash
# 安装Certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加：0 12 * * * /usr/bin/certbot renew --quiet
```

### 6. 监控和日志

#### 6.1 日志配置

**修改日志配置：**
```python
import logging
from logging.handlers import RotatingFileHandler

# 创建日志目录
os.makedirs('logs', exist_ok=True)

# 配置日志
file_handler = RotatingFileHandler(
    'logs/douyin.log', 
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s: %(message)s'
))
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
```

#### 6.2 健康检查

**添加健康检查端点：**
```python
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })
```

### 7. 性能优化

#### 7.1 数据库优化

**使用SQLite连接池：**
```python
import sqlite3
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
```

#### 7.2 缓存配置

**添加Redis缓存：**
```python
import redis

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

# 缓存文件列表
def get_cached_files():
    cache_key = 'files_list'
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    files = get_downloaded_files()
    redis_client.setex(cache_key, 300, json.dumps(files))  # 缓存5分钟
    return files
```

### 8. 备份策略

#### 8.1 自动备份脚本

**创建备份脚本 `backup.sh`：**
```bash
#!/bin/bash

BACKUP_DIR="/backup/dy-downloader"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份配置文件
cp -r settings/ $BACKUP_DIR/settings_$DATE/

# 备份数据库
cp settings/data.db $BACKUP_DIR/data_$DATE.db

# 备份日志
cp -r logs/ $BACKUP_DIR/logs_$DATE/

# 压缩备份
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz $BACKUP_DIR/settings_$DATE/ $BACKUP_DIR/data_$DATE.db $BACKUP_DIR/logs_$DATE/

# 清理旧备份（保留7天）
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "settings_*" -mtime +7 -exec rm -rf {} \;
find $BACKUP_DIR -name "logs_*" -mtime +7 -exec rm -rf {} \;
```

**设置定时备份：**
```bash
# 编辑crontab
crontab -e

# 添加每日备份任务
0 2 * * * /path/to/backup.sh
```

### 9. 故障排除

#### 9.1 常见问题

**问题1：端口被占用**
```bash
# 查看端口占用
netstat -tulpn | grep :5000

# 杀死进程
sudo kill -9 <PID>
```

**问题2：权限问题**
```bash
# 修复文件权限
sudo chown -R www-data:www-data /path/to/your/app
sudo chmod -R 755 /path/to/your/app
```

**问题3：内存不足**
```bash
# 查看内存使用
free -h

# 优化Gunicorn配置
gunicorn -w 2 -b 0.0.0.0:5000 --max-requests 100 --max-requests-jitter 10 start_server:app
```

#### 9.2 日志分析

**查看应用日志：**
```bash
# 实时查看日志
tail -f logs/douyin.log

# 查看错误日志
grep "ERROR" logs/douyin.log

# 查看最近的日志
tail -n 100 logs/douyin.log
```

### 10. 更新和维护

#### 10.1 自动更新脚本

**创建更新脚本 `update.sh`：**
```bash
#!/bin/bash

# 停止服务
sudo systemctl stop dy-downloader

# 备份当前版本
cp -r /path/to/your/app /path/to/backup/app_$(date +%Y%m%d_%H%M%S)

# 拉取最新代码
cd /path/to/your/app
git pull origin main

# 更新依赖
pip install -r requirements.txt

# 重启服务
sudo systemctl start dy-downloader

# 检查服务状态
sudo systemctl status dy-downloader
```

## 总结

选择合适的部署方式取决于您的需求：

- **个人使用**：本地部署或Docker部署
- **小团队使用**：服务器部署 + Nginx
- **生产环境**：云平台部署 + 监控
- **企业使用**：完整的生产环境配置

建议从简单的本地部署开始，随着需求的增长逐步升级到更复杂的部署方案。 