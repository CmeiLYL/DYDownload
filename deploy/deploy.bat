@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo 🚀 DY下载器部署脚本
echo ==================

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

echo 📁 项目根目录: %PROJECT_ROOT%
echo 📁 脚本目录: %SCRIPT_DIR%

REM 检查参数
if "%~1"=="" (
    echo 用法: %0 [local^|docker^|server]
    echo.
    echo 部署选项:
    echo   local    - 本地部署
    echo   docker   - Docker部署
    echo   server   - 服务器部署
    exit /b 1
)

set DEPLOY_TYPE=%~1

REM 检查依赖
:check_dependencies
echo 📋 检查依赖...

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装
    exit /b 1
)

REM 检查pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip 未安装
    exit /b 1
)

echo ✅ 基本依赖检查通过
goto :eof

REM 安装Python依赖
:install_dependencies
echo 📦 安装Python依赖...
cd /d "%PROJECT_ROOT%"
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    exit /b 1
)
echo ✅ 依赖安装完成
goto :eof

REM 本地部署
:deploy_local
echo 🏠 开始本地部署...

call :check_dependencies
call :install_dependencies

echo 🚀 启动应用...
cd /d "%PROJECT_ROOT%"
python app.py
goto :eof

REM Docker部署
:deploy_docker
echo 🐳 开始Docker部署...

REM 检查Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker 未安装
    exit /b 1
)

REM 检查Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose 未安装
    exit /b 1
)

echo 🔨 构建Docker镜像...
cd /d "%SCRIPT_DIR%"
docker-compose build
if errorlevel 1 (
    echo ❌ Docker构建失败
    exit /b 1
)

echo 🚀 启动Docker容器...
docker-compose up -d
if errorlevel 1 (
    echo ❌ Docker启动失败
    exit /b 1
)

echo ✅ Docker部署完成
echo 🌐 访问地址: http://localhost:5000
goto :eof

REM 服务器部署
:deploy_server
echo 🖥️  开始服务器部署...

call :check_dependencies
call :install_dependencies

REM 检查Gunicorn
python -c "import gunicorn" >nul 2>&1
if errorlevel 1 (
    echo 📦 安装Gunicorn...
    pip install gunicorn
)

echo 🚀 使用Gunicorn启动应用...
cd /d "%PROJECT_ROOT%"
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 --max-requests 1000 start_server:app
goto :eof

REM 主函数
:main
if "%DEPLOY_TYPE%"=="local" (
    call :deploy_local
) else if "%DEPLOY_TYPE%"=="docker" (
    call :deploy_docker
) else if "%DEPLOY_TYPE%"=="server" (
    call :deploy_server
) else (
    echo ❌ 未知的部署类型: %DEPLOY_TYPE%
    echo 支持的部署类型: local, docker, server
    exit /b 1
)

goto :eof

REM 执行主函数
call :main 