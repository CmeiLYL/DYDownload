# 🚀 快速部署指南

## 选择您的部署方式

### 🏠 本地部署（推荐新手）
```bash
cd deploy
chmod +x deploy.sh  # Linux/Mac
./deploy.sh local
```

### 🐳 Docker部署（推荐）
```bash
cd deploy
docker-compose up -d
```

### 🖥️ 服务器部署
```bash
cd deploy
chmod +x deploy.sh
./deploy.sh server
```

### ☁️ 云平台部署

#### Heroku
```bash
cd deploy
chmod +x deploy.sh
./deploy.sh heroku
```

#### Vercel
```bash
cd deploy
chmod +x deploy.sh
./deploy.sh vercel
```

#### Railway
```bash
cd deploy
chmod +x deploy.sh
./deploy.sh railway
```

## 📋 部署前检查清单

- [ ] Python 3.7+ 已安装
- [ ] pip 已安装
- [ ] 项目依赖已安装 (`pip install -r requirements.txt`)
- [ ] 配置文件已设置 (`settings/config.yml`)
- [ ] 下载目录已创建 (`Downloaded/`)

## 🔧 常见问题解决

### 1. 权限问题
```bash
# Linux/Mac
chmod +x deploy/deploy.sh

# Windows
# 右键点击 deploy.bat -> 以管理员身份运行
```

### 2. 端口被占用
```bash
# 查看端口占用
netstat -tulpn | grep :5000

# 杀死进程
sudo kill -9 <PID>
```

### 3. Docker问题
```bash
# 检查Docker状态
docker --version
docker-compose --version

# 重启Docker服务
sudo systemctl restart docker
```

## 📞 获取帮助

如果遇到问题，请：

1. 查看日志文件：`logs/douyin.log`
2. 检查部署状态：访问 `http://localhost:5000/health`
3. 参考详细文档：[部署指南](../docs/DEPLOYMENT_GUIDE.md)
4. 提交Issue：[问题反馈](https://github.com/your-username/DYDownload/issues) 