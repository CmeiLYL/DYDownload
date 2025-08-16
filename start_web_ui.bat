@echo off
chcp 65001 >nul
title 抖音下载器 Web UI

echo ================================================
echo 抖音下载器 Web UI 启动器
echo ================================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo 正在检查依赖包...
python -c "import flask, flask_cors, yaml" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install flask flask-cors pyyaml
    if errorlevel 1 (
        echo 错误: 依赖包安装失败
        pause
        exit /b 1
    )
)

echo 正在启动Web界面...
echo.
echo 启动后浏览器将自动打开 http://localhost:5000
echo 按 Ctrl+C 停止服务器
echo.

python run_web.py

echo.
echo 服务器已停止
pause 