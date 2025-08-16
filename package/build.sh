#!/bin/bash

# DY下载器 - 打包脚本
# 支持多种打包方式：PyInstaller、cx_Freeze、Nuitka

set -e

echo "🔨 DY下载器 - 打包脚本"
echo "===================="

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "📁 项目根目录: $PROJECT_ROOT"
echo "📁 脚本目录: $SCRIPT_DIR"

# 检查参数
if [ $# -eq 0 ]; then
    echo "用法: $0 [pyinstaller|cx_freeze|nuitka|all]"
    echo ""
    echo "打包选项:"
    echo "  pyinstaller - 使用 PyInstaller 打包"
    echo "  cx_freeze   - 使用 cx_Freeze 打包"
    echo "  nuitka      - 使用 Nuitka 打包"
    echo "  all         - 使用所有方式打包"
    exit 1
fi

BUILD_TYPE=$1

# 检查依赖
check_dependencies() {
    echo "📋 检查依赖..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 未安装"
        exit 1
    fi
    
    # 检查pip
    if ! command -v pip3 &> /dev/null; then
        echo "❌ pip3 未安装"
        exit 1
    fi
    
    # 检查并安装PyInstaller
    if ! python3 -c "import PyInstaller" &> /dev/null; then
        echo "📦 安装 PyInstaller..."
        pip3 install pyinstaller
    else
        echo "✅ PyInstaller 已安装"
    fi
    
    # 检查并安装cx_Freeze
    if ! python3 -c "import cx_Freeze" &> /dev/null; then
        echo "📦 安装 cx_Freeze..."
        pip3 install cx_Freeze
    else
        echo "✅ cx_Freeze 已安装"
    fi
    
    # 检查并安装Nuitka
    if ! python3 -c "import nuitka" &> /dev/null; then
        echo "📦 安装 Nuitka..."
        pip3 install nuitka
    else
        echo "✅ Nuitka 已安装"
    fi
    
    echo "✅ 所有依赖检查完成"
}

# 创建目录
create_directories() {
    echo "📁 创建目录..."
    mkdir -p "$SCRIPT_DIR/dist"
    mkdir -p "$SCRIPT_DIR/build"
}

# PyInstaller打包
build_pyinstaller() {
    echo "🔨 使用 PyInstaller 打包..."
    cd "$SCRIPT_DIR"
    
    # 构建命令
    cmd=(
        pyinstaller
        --distpath dist
        --workpath build
        --specpath .
        --clean
        --noconfirm
        --onefile
    )
    
    # 添加数据文件
    cmd+=(
        --add-data "$PROJECT_ROOT/ui/templates:ui/templates"
        --add-data "$PROJECT_ROOT/ui/static:ui/static"
        --add-data "$PROJECT_ROOT/settings:settings"
        --add-data "$PROJECT_ROOT/script:script"
        --add-data "$PROJECT_ROOT/apiproxy:apiproxy"
    )
    
    # 添加图标（如果存在）
    if [ -f "$PROJECT_ROOT/ui/static/favicon.ico" ]; then
        cmd+=(--icon "$PROJECT_ROOT/ui/static/favicon.ico")
    fi
    
    # 添加主程序
    cmd+=("$PROJECT_ROOT/app.py")
    
    echo "执行命令: ${cmd[*]}"
    "${cmd[@]}"
    
    echo "✅ PyInstaller 打包完成"
}

# cx_Freeze打包
build_cx_freeze() {
    echo "🔨 使用 cx_Freeze 打包..."
    cd "$SCRIPT_DIR"
    
    # 创建setup.py
    cat > setup_cx_freeze.py << EOF
import sys
import os
from cx_Freeze import setup, Executable

# 添加项目根目录到路径
project_root = r"$PROJECT_ROOT"
sys.path.insert(0, project_root)

# 包含的数据文件
include_files = [
    (os.path.join(project_root, "ui/templates"), "ui/templates"),
    (os.path.join(project_root, "ui/static"), "ui/static"),
    (os.path.join(project_root, "settings"), "settings"),
    (os.path.join(project_root, "script"), "script"),
    (os.path.join(project_root, "apiproxy"), "apiproxy"),
]

# 排除的模块
excludes = ["tkinter", "matplotlib", "numpy", "pandas"]

# 构建选项
build_options = {
    "packages": ["flask", "yaml", "requests", "PIL"],
    "excludes": excludes,
    "include_files": include_files,
    "optimize": 2,
}

# 可执行文件
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(
        os.path.join(project_root, "app.py"),
        base=base,
        target_name="DY下载器" if sys.platform != "win32" else "DY下载器.exe",
        icon=os.path.join(project_root, "ui/static/favicon.ico") if os.path.exists(os.path.join(project_root, "ui/static/favicon.ico")) else None
    )
]

setup(
    name="DY下载器",
    version="1.0.0",
    description="DY内容下载器",
    options={"build_exe": build_options},
    executables=executables
)
EOF
    
    # 执行打包
    python3 setup_cx_freeze.py build
    
    # 清理临时文件
    rm setup_cx_freeze.py
    
    echo "✅ cx_Freeze 打包完成"
}

# Nuitka打包
build_nuitka() {
    echo "🔨 使用 Nuitka 打包..."
    cd "$SCRIPT_DIR"
    
    # 构建命令
    cmd=(
        python3 -m nuitka
        --output-dir dist
        --remove-output
        --assume-yes-for-downloads
        --standalone
    )
    
    # 添加数据文件
    cmd+=(
        --include-data-dir "$PROJECT_ROOT/ui/templates=ui/templates"
        --include-data-dir "$PROJECT_ROOT/ui/static=ui/static"
        --include-data-dir "$PROJECT_ROOT/settings=settings"
        --include-data-dir "$PROJECT_ROOT/script=script"
        --include-data-dir "$PROJECT_ROOT/apiproxy=apiproxy"
    )
    
    # 添加主程序
    cmd+=("$PROJECT_ROOT/app.py")
    
    echo "执行命令: ${cmd[*]}"
    "${cmd[@]}"
    
    echo "✅ Nuitka 打包完成"
}

# 创建安装程序
create_installer() {
    echo "🔨 创建安装程序..."
    
    # 创建安装脚本
    cat > "$SCRIPT_DIR/dist/install.sh" << 'EOF'
#!/bin/bash

echo "DY下载器 - 安装程序"
echo "==================="

# 安装目录
INSTALL_DIR="/usr/local/DY下载器"
DESKTOP_DIR="$HOME/Desktop"
APP_DIR="$HOME/.local/share/applications"

echo "正在安装到: $INSTALL_DIR"

# 创建安装目录
sudo mkdir -p "$INSTALL_DIR"

# 复制文件
sudo cp -r dist/* "$INSTALL_DIR/"

# 创建桌面快捷方式
cat > "$DESKTOP_DIR/DY下载器.desktop" << 'DESKTOP_EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=DY下载器
Comment=DY内容下载器
Exec=/usr/local/DY下载器/DY下载器
Icon=/usr/local/DY下载器/ui/static/favicon.ico
Terminal=false
Categories=Network;
DESKTOP_EOF

# 创建应用程序菜单项
mkdir -p "$APP_DIR"
cat > "$APP_DIR/DY下载器.desktop" << 'APP_EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=DY下载器
Comment=DY内容下载器
Exec=/usr/local/DY下载器/DY下载器
Icon=/usr/local/DY下载器/ui/static/favicon.ico
Terminal=false
Categories=Network;
APP_EOF

# 设置权限
chmod +x "$DESKTOP_DIR/DY下载器.desktop"
chmod +x "$APP_DIR/DY下载器.desktop"
chmod +x "$INSTALL_DIR/DY下载器"

echo "安装完成！"
echo "您可以在桌面和应用程序菜单中找到 DY下载器"
EOF
    
    chmod +x "$SCRIPT_DIR/dist/install.sh"
    
    echo "✅ 安装程序创建完成"
}

# 清理构建文件
clean_build() {
    echo "🧹 清理构建文件..."
    
    # 清理PyInstaller文件
    if [ -f "$SCRIPT_DIR/app.spec" ]; then
        rm "$SCRIPT_DIR/app.spec"
    fi
    
    # 清理构建目录
    if [ -d "$SCRIPT_DIR/build" ]; then
        rm -rf "$SCRIPT_DIR/build"
    fi
    
    echo "✅ 清理完成"
}

# 主函数
main() {
    check_dependencies
    create_directories
    
    case $BUILD_TYPE in
        "pyinstaller")
            build_pyinstaller
            ;;
        "cx_freeze")
            build_cx_freeze
            ;;
        "nuitka")
            build_nuitka
            ;;
        "all")
            echo "🔨 使用所有方式打包..."
            build_pyinstaller
            build_cx_freeze
            build_nuitka
            ;;
        *)
            echo "❌ 未知的打包类型: $BUILD_TYPE"
            echo "支持的打包类型: pyinstaller, cx_freeze, nuitka, all"
            exit 1
            ;;
    esac
    
    create_installer
    clean_build
    
    echo ""
    echo "🎉 打包完成！"
    echo "📁 输出目录: $SCRIPT_DIR/dist"
}

# 执行主函数
main 