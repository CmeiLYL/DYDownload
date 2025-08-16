#!/bin/bash

# DY下载器 - 部署脚本
# 支持多种部署方式

set -e

echo "🚀 DY下载器部署脚本"
echo "=================="

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "📁 项目根目录: $PROJECT_ROOT"
echo "📁 脚本目录: $SCRIPT_DIR"

# 检查参数
if [ $# -eq 0 ]; then
    echo "用法: $0 [local|docker|server|heroku|vercel|railway]"
    echo ""
    echo "部署选项:"
    echo "  local    - 本地部署"
    echo "  docker   - Docker部署"
    echo "  server   - 服务器部署"
    echo "  heroku   - Heroku部署"
    echo "  vercel   - Vercel部署"
    echo "  railway  - Railway部署"
    exit 1
fi

DEPLOY_TYPE=$1

# 检查依赖
check_dependencies() {
    echo "📋 检查依赖..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 未安装"
        exit 1
    fi
    
    # 检查pip
    if ! command -v pip &> /dev/null; then
        echo "❌ pip 未安装"
        exit 1
    fi
    
    echo "✅ 基本依赖检查通过"
}

# 安装Python依赖
install_dependencies() {
    echo "📦 安装Python依赖..."
    cd "$PROJECT_ROOT"
    pip install -r requirements.txt
    echo "✅ 依赖安装完成"
}

# 本地部署
deploy_local() {
    echo "🏠 开始本地部署..."
    
    check_dependencies
    install_dependencies
    
    echo "🚀 启动应用..."
    cd "$PROJECT_ROOT"
    python app.py
}

# Docker部署
deploy_docker() {
    echo "🐳 开始Docker部署..."
    
    # 检查Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker 未安装"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose 未安装"
        exit 1
    fi
    
    echo "🔨 构建Docker镜像..."
    cd "$SCRIPT_DIR"
    docker-compose build
    
    echo "🚀 启动Docker容器..."
    docker-compose up -d
    
    echo "✅ Docker部署完成"
    echo "🌐 访问地址: http://localhost:5000"
}

# 服务器部署
deploy_server() {
    echo "🖥️  开始服务器部署..."
    
    check_dependencies
    install_dependencies
    
    # 检查Gunicorn
    if ! python -c "import gunicorn" &> /dev/null; then
        echo "📦 安装Gunicorn..."
        pip install gunicorn
    fi
    
    echo "🚀 使用Gunicorn启动应用..."
    cd "$PROJECT_ROOT"
    gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 --max-requests 1000 start_server:app
}

# Heroku部署
deploy_heroku() {
    echo "☁️  开始Heroku部署..."
    
    # 检查Heroku CLI
    if ! command -v heroku &> /dev/null; then
        echo "❌ Heroku CLI 未安装"
        echo "请访问: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    # 检查Git
    if ! command -v git &> /dev/null; then
        echo "❌ Git 未安装"
        exit 1
    fi
    
    echo "🔐 登录Heroku..."
    heroku login
    
    echo "📝 创建Heroku应用..."
    read -p "请输入应用名称 (或按回车使用默认名称): " app_name
    if [ -z "$app_name" ]; then
        app_name="dy-downloader-$(date +%s)"
    fi
    
    heroku create $app_name
    
    echo "🔧 添加构建包..."
    heroku buildpacks:add https://github.com/heroku/heroku-buildpack-ffmpeg-latest.git
    heroku buildpacks:add heroku/python
    
    echo "📤 部署到Heroku..."
    cd "$PROJECT_ROOT"
    # 复制Heroku配置文件到根目录
    cp "$SCRIPT_DIR/Procfile" .
    cp "$SCRIPT_DIR/runtime.txt" .
    
    git add .
    git commit -m "Deploy to Heroku"
    git push heroku main
    
    echo "🌐 打开应用..."
    heroku open
    
    echo "✅ Heroku部署完成"
}

# Vercel部署
deploy_vercel() {
    echo "☁️  开始Vercel部署..."
    
    # 检查Vercel CLI
    if ! command -v vercel &> /dev/null; then
        echo "📦 安装Vercel CLI..."
        npm install -g vercel
    fi
    
    echo "🔐 登录Vercel..."
    vercel login
    
    echo "📤 部署到Vercel..."
    cd "$PROJECT_ROOT"
    # 复制Vercel配置文件到根目录
    cp "$SCRIPT_DIR/vercel.json" .
    
    vercel --prod
    
    echo "✅ Vercel部署完成"
}

# Railway部署
deploy_railway() {
    echo "☁️  开始Railway部署..."
    
    # 检查Railway CLI
    if ! command -v railway &> /dev/null; then
        echo "📦 安装Railway CLI..."
        npm install -g @railway/cli
    fi
    
    echo "🔐 登录Railway..."
    railway login
    
    echo "📤 部署到Railway..."
    cd "$PROJECT_ROOT"
    # 复制Railway配置文件到根目录
    cp "$SCRIPT_DIR/railway.json" .
    
    railway up
    
    echo "✅ Railway部署完成"
}

# 主函数
main() {
    case $DEPLOY_TYPE in
        "local")
            deploy_local
            ;;
        "docker")
            deploy_docker
            ;;
        "server")
            deploy_server
            ;;
        "heroku")
            deploy_heroku
            ;;
        "vercel")
            deploy_vercel
            ;;
        "railway")
            deploy_railway
            ;;
        *)
            echo "❌ 未知的部署类型: $DEPLOY_TYPE"
            echo "支持的部署类型: local, docker, server, heroku, vercel, railway"
            exit 1
            ;;
    esac
}

# 执行主函数
main 