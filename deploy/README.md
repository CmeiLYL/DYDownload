# 部署文件说明

本文件夹包含DY下载器应用的所有部署相关文件。

## 📁 文件说明

### Docker部署
- `Dockerfile` - Docker镜像构建文件
- `docker-compose.yml` - Docker Compose配置文件

### 云平台部署
- `Procfile` - Heroku部署配置
- `runtime.txt` - Python运行时版本
- `vercel.json` - Vercel部署配置
- `railway.json` - Railway部署配置

### 部署脚本
- `deploy.sh` - Linux/Mac部署脚本
- `deploy.bat` - Windows部署脚本

## 🚀 快速部署

### 1. 本地部署
```bash
# Linux/Mac
cd deploy
chmod +x deploy.sh
./deploy.sh local

# Windows
cd deploy
deploy.bat local
```

### 2. Docker部署
```bash
cd deploy
docker-compose up -d
```

### 3. 服务器部署
```bash
cd deploy
chmod +x deploy.sh
./deploy.sh server
```

### 4. 云平台部署

#### Heroku
```bash
cd deploy
# 确保Procfile和runtime.txt在根目录
cp Procfile ../
cp runtime.txt ../
cd ..
heroku create your-app-name
git push heroku main
```

#### Vercel
```bash
cd deploy
# 确保vercel.json在根目录
cp vercel.json ../
cd ..
vercel --prod
```

#### Railway
```bash
cd deploy
# 确保railway.json在根目录
cp railway.json ../
cd ..
railway up
```

## 📋 部署前准备

1. **确保项目根目录包含必要文件**：
   - `app.py` - 主应用程序
   - `start_server.py` - 生产环境启动脚本
   - `requirements.txt` - Python依赖
   - `settings/config.yml` - 配置文件

2. **检查依赖**：
   ```bash
   pip install -r requirements.txt
   ```

3. **配置应用**：
   - 编辑 `settings/config.yml` 添加下载链接
   - 在Web界面中配置Cookie信息

## 🔧 自定义部署

### 修改Docker配置
编辑 `Dockerfile` 或 `docker-compose.yml` 来调整Docker部署配置。

### 修改云平台配置
- Heroku: 编辑 `Procfile` 和 `runtime.txt`
- Vercel: 编辑 `vercel.json`
- Railway: 编辑 `railway.json`

### 修改部署脚本
编辑 `deploy.sh` 或 `deploy.bat` 来自定义部署流程。

## 📚 详细文档

更多部署信息请参考：
- [部署指南](../docs/DEPLOYMENT_GUIDE.md)
- [项目README](../README.md) 