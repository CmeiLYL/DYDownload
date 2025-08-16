# DY下载器 Web UI

一个功能强大的DY内容下载器，提供现代化的Web界面来管理和下载DY内容。

## 🚀 快速开始

### 本地部署（推荐新手）

```bash
# 克隆项目
git clone <your-repository-url>
cd DYDownload

# 安装依赖
pip install -r requirements.txt

# 启动应用
python app.py
```

然后访问：http://localhost:5000

### 使用部署脚本

```bash
# Linux/Mac
cd deploy
chmod +x deploy.sh
./deploy.sh local

# Windows
cd deploy
deploy.bat local
```

### 打包成可执行程序

```bash
# 使用PyInstaller打包（推荐新手）
cd package
python build.py pyinstaller

# 使用cx_Freeze打包（推荐性能）
python build.py cx_freeze

# 使用Nuitka打包（推荐生产）
python build.py nuitka
```

## 📦 部署和打包方式

### 1. 本地部署
最简单的部署方式，适合个人使用：
```bash
python app.py
```

### 2. Docker部署
使用Docker容器化部署：
```bash
# 进入部署目录
cd deploy

# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 3. 服务器部署
使用Gunicorn生产服务器：
```bash
cd deploy
chmod +x deploy.sh
./deploy.sh server
```

### 4. 云平台部署

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

### 5. 打包成可执行程序

#### PyInstaller（推荐新手）
```bash
cd package
python build.py pyinstaller
```

#### cx_Freeze（推荐性能）
```bash
cd package
python build.py cx_freeze
```

#### Nuitka（推荐生产）
```bash
cd package
python build.py nuitka
```

## 🔧 配置说明

### 基本配置
编辑 `settings/config.yml` 文件：
```yaml
link:
  - "https://www.douyin.com/user/MS4wLjABAAAAxxxxx"

path: "./Downloaded/"
music: true
cover: true
avatar: true
json: true
folderstyle: false

mode: ["post", "mix"]
number:
  post: 0
  like: 0
  allmix: 0
  mix: 0
  music: 0

database: true
thread: 5
```

### Cookie配置
在Web界面中配置DY登录Cookie：
- msToken
- ttwid
- odin_tt
- passport_csrf_token
- sid_guard

## 🌟 主要功能

- **链接管理**: 支持用户主页、视频、合集链接
- **批量下载**: 同时处理多个链接
- **实时监控**: 显示下载进度和状态
- **文件管理**: 浏览、预览、下载已下载的文件
- **缩略图生成**: 自动为视频生成缩略图
- **配置管理**: 实时修改下载配置
- **日志系统**: 详细的日志记录

## 📁 项目结构

```
DYDownload/
├── app.py                 # 主应用程序
├── start_server.py        # 生产环境启动脚本
├── requirements.txt       # Python依赖
├── deploy/               # 部署相关文件
│   ├── Dockerfile        # Docker配置
│   ├── docker-compose.yml # Docker Compose配置
│   ├── Procfile          # Heroku配置
│   ├── runtime.txt       # Python运行时版本
│   ├── vercel.json       # Vercel配置
│   ├── railway.json      # Railway配置
│   ├── deploy.sh         # 部署脚本 (Linux/Mac)
│   ├── deploy.bat        # 部署脚本 (Windows)
│   └── README.md         # 部署说明
├── package/              # 打包相关文件
│   ├── build.py          # Python打包脚本
│   ├── build.sh          # Linux/Mac打包脚本
│   ├── build.bat         # Windows打包脚本
│   ├── dist/             # 打包输出目录
│   ├── build/            # 临时构建目录
│   └── README.md         # 打包说明
├── docs/                 # 文档目录
├── ui/                   # UI相关文件
│   ├── templates/        # HTML模板
│   └── static/          # 静态资源
├── script/              # 脚本文件
├── settings/            # 配置文件
├── logs/                # 日志文件
└── Downloaded/          # 下载目录
```

## 🔍 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查看端口占用
   netstat -tulpn | grep :5000
   # 杀死进程
   sudo kill -9 <PID>
   ```

2. **权限问题**
   ```bash
   # 修复文件权限
   sudo chown -R www-data:www-data /path/to/your/app
   sudo chmod -R 755 /path/to/your/app
   ```

3. **依赖安装失败**
   ```bash
   # 升级pip
   pip install --upgrade pip
   # 重新安装依赖
   pip install -r requirements.txt --force-reinstall
   ```

4. **打包失败**
   ```bash
   # 安装打包工具
   pip install pyinstaller cx_Freeze nuitka
   # 检查项目依赖
   python -c "import flask, yaml, requests, PIL"
   ```

### 查看日志
```bash
# 实时查看日志
tail -f logs/douyin.log

# 查看错误日志
grep "ERROR" logs/douyin.log
```

## 📚 详细文档

- [部署指南](docs/DEPLOYMENT_GUIDE.md) - 详细的部署说明
- [部署文件说明](deploy/README.md) - 部署文件使用说明
- [打包文件说明](package/README.md) - 打包文件使用说明
- [快速打包指南](package/QUICK_START.md) - 快速打包指南
- [使用示例](docs/examples.md) - 使用示例和最佳实践
- [项目结构](docs/PROJECT_STRUCTURE.md) - 项目结构说明
- [Web UI说明](docs/README_WEB_UI.md) - Web界面功能说明

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目遵循开源许可证。

## 🔗 相关链接

- [项目主页](https://github.com/CmeiLYL/DYDownload)
- [问题反馈](https://github.com/CmeiLYL/DYDownload/issues)
- [更新日志](CHANGELOG.md) 