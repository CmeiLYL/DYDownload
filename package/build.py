#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DY下载器 - 打包脚本
支持多种打包方式：PyInstaller、cx_Freeze、Nuitka
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

class PackageBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.package_dir = Path(__file__).parent
        self.dist_dir = self.package_dir / "dist"
        self.build_dir = self.package_dir / "build"
        
        # 确保目录存在
        self.dist_dir.mkdir(exist_ok=True)
        self.build_dir.mkdir(exist_ok=True)
        
        print(f"📁 项目根目录: {self.project_root}")
        print(f"📁 打包目录: {self.package_dir}")
        print(f"📁 输出目录: {self.dist_dir}")
    
    def check_dependencies(self):
        """检查打包依赖"""
        print("📋 检查打包依赖...")
        
        # 检查PyInstaller
        try:
            import PyInstaller
            print("✅ PyInstaller 已安装")
        except ImportError:
            print("📦 安装 PyInstaller...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        
        # 检查cx_Freeze
        try:
            import cx_Freeze
            print("✅ cx_Freeze 已安装")
        except ImportError:
            print("📦 安装 cx_Freeze...")
            subprocess.run([sys.executable, "-m", "pip", "install", "cx_Freeze"], check=True)
        
        # 检查Nuitka
        try:
            import nuitka
            print("✅ Nuitka 已安装")
        except ImportError:
            print("📦 安装 Nuitka...")
            subprocess.run([sys.executable, "-m", "pip", "install", "nuitka"], check=True)
    
    def build_with_pyinstaller(self, onefile=True, windowed=False):
        """使用PyInstaller打包"""
        print("🔨 使用 PyInstaller 打包...")
        
        # 清理输出目录
        print("🧹 清理输出目录...")
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        self.dist_dir.mkdir(exist_ok=True)
        
        # 临时重命名Downloaded目录以避免打包
        downloaded_dir = self.project_root / "script" / "Downloaded"
        temp_downloaded_dir = self.project_root / "script" / "Downloaded_temp"
        
        if downloaded_dir.exists():
            print("📁 临时重命名Downloaded目录...")
            downloaded_dir.rename(temp_downloaded_dir)
        
        try:
            # 构建命令
            cmd = [
                "pyinstaller",
                "--distpath", str(self.dist_dir),
                "--workpath", str(self.build_dir),
                "--specpath", str(self.package_dir),
                "--clean",
                "--noconfirm"
            ]
            
            if onefile:
                cmd.append("--onefile")
            
            if windowed:
                cmd.append("--windowed")
            
            # 添加数据文件
            cmd.extend([
                "--add-data", f"{self.project_root}/ui/templates{os.pathsep}ui/templates",
                "--add-data", f"{self.project_root}/ui/static{os.pathsep}ui/static",
                "--add-data", f"{self.project_root}/settings{os.pathsep}settings",
                "--add-data", f"{self.project_root}/script{os.pathsep}script",
                "--add-data", f"{self.project_root}/apiproxy{os.pathsep}apiproxy"
            ])
            
            # 添加图标（如果存在）
            icon_path = self.project_root / "ui" / "static" / "favicon.ico"
            if icon_path.exists():
                cmd.extend(["--icon", str(icon_path)])
            
            # 主程序
            cmd.append(str(self.project_root / "app.py"))
            
            print(f"执行命令: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            
            # 重命名可执行文件
            old_exe = self.dist_dir / "app.exe"
            new_exe = self.dist_dir / "DYDownload.exe"
            if old_exe.exists():
                old_exe.rename(new_exe)
                print("✅ 重命名可执行文件为 DYDownload.exe")
            
            print("✅ PyInstaller 打包完成")
            
        finally:
            # 恢复Downloaded目录
            if temp_downloaded_dir.exists():
                print("📁 恢复Downloaded目录...")
                temp_downloaded_dir.rename(downloaded_dir)
    
    def build_with_cx_freeze(self):
        """使用cx_Freeze打包"""
        print("🔨 使用 cx_Freeze 打包...")
        
        # 创建setup.py
        setup_content = f'''
import sys
import os
from cx_Freeze import setup, Executable

# 添加项目根目录到路径
project_root = r"{self.project_root}"
sys.path.insert(0, project_root)

# 包含的数据文件
include_files = [
    (os.path.join(project_root, "ui/templates"), "ui/templates"),
    (os.path.join(project_root, "ui/static"), "ui/static"),
    (os.path.join(project_root, "settings"), "settings"),
    (os.path.join(project_root, "script"), "script"),
    (os.path.join(project_root, "apiproxy"), "apiproxy"),
]

# 排除的模块和目录
excludes = ["tkinter", "matplotlib", "numpy", "pandas"]
exclude_dirs = ["script/Downloaded"]

# 构建选项
build_options = {{
    "packages": ["flask", "yaml", "requests", "PIL"],
    "excludes": excludes,
    "include_files": include_files,
    "optimize": 2,
}}

# 可执行文件
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(
        os.path.join(project_root, "app.py"),
        base=base,
        target_name="DY下载器.exe" if sys.platform == "win32" else "DY下载器",
        icon=os.path.join(project_root, "ui/static/favicon.ico") if os.path.exists(os.path.join(project_root, "ui/static/favicon.ico")) else None
    )
]

setup(
    name="DY下载器",
    version="1.0.0",
    description="DY内容下载器",
    options={{"build_exe": build_options}},
    executables=executables
)
'''
        
        setup_file = self.package_dir / "setup_cx_freeze.py"
        with open(setup_file, 'w', encoding='utf-8') as f:
            f.write(setup_content)
        
        # 执行打包
        cmd = [sys.executable, str(setup_file), "build"]
        print(f"执行命令: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
        # 清理临时文件
        setup_file.unlink()
        
        print("✅ cx_Freeze 打包完成")
    
    def build_with_nuitka(self, standalone=True):
        """使用Nuitka打包"""
        print("🔨 使用 Nuitka 打包...")
        
        # 构建命令
        cmd = [
            sys.executable, "-m", "nuitka",
            "--output-dir", str(self.dist_dir),
            "--remove-output",
            "--assume-yes-for-downloads"
        ]
        
        if standalone:
            cmd.append("--standalone")
        
        # 添加数据文件
        cmd.extend([
            "--include-data-dir", f"{self.project_root}/ui/templates=ui/templates",
            "--include-data-dir", f"{self.project_root}/ui/static=ui/static",
            "--include-data-dir", f"{self.project_root}/settings=settings",
            "--include-data-dir", f"{self.project_root}/script=script",
            "--include-data-dir", f"{self.project_root}/apiproxy=apiproxy"
        ])
        
        # 排除下载的文件目录
        cmd.extend([
            "--nofollow-import-to=script.Downloaded"
        ])
        
        # 主程序
        cmd.append(str(self.project_root / "app.py"))
        
        print(f"执行命令: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
        print("✅ Nuitka 打包完成")
    
    def create_installer(self):
        """创建安装程序"""
        print("🔨 创建安装程序...")
        
        # 这里可以集成NSIS、Inno Setup等工具
        # 暂时创建一个简单的批处理安装脚本
        
        installer_content = f'''@echo off
chcp 65001 >nul
echo DY下载器 - 安装程序
echo ====================

set INSTALL_DIR=%PROGRAMFILES%\\DY下载器
set START_MENU_DIR=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\DY下载器

echo 正在安装到: %INSTALL_DIR%

REM 创建安装目录
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM 复制文件
xcopy /E /I /Y "dist\\*" "%INSTALL_DIR%"

REM 创建开始菜单快捷方式
if not exist "%START_MENU_DIR%" mkdir "%START_MENU_DIR%"

REM 创建桌面快捷方式
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\\Desktop\\DY下载器.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\\DY下载器.exe" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

echo 安装完成！
echo 您可以在桌面和开始菜单中找到 DY下载器
pause
'''
        
        installer_file = self.dist_dir / "install.bat"
        with open(installer_file, 'w', encoding='utf-8') as f:
            f.write(installer_content)
        
        print("✅ 安装程序创建完成")
    
    def create_release_zip(self):
        """创建发布zip文件"""
        print("📦 创建发布zip文件...")
        
        import zipfile
        from datetime import datetime
        
        # 创建zip文件名（包含日期）
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"DYDownload_{date_str}.zip"
        zip_path = self.dist_dir / zip_name
        
        # 创建默认配置文件
        default_config = self.create_default_config()
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加可执行文件
            exe_file = self.dist_dir / "DYDownload.exe"
            if exe_file.exists():
                zipf.writestr(exe_file.name, open(exe_file, 'rb').read())
                print(f"📄 添加 {exe_file.name}")
            
            # 添加默认配置文件到settings目录
            zipf.writestr("settings/config.yml", default_config)
            print("📄 添加 settings/config.yml")
            
            # 添加README文件（如果存在）
            readme_file = self.project_root / "README.md"
            if readme_file.exists():
                zipf.writestr(readme_file.name, open(readme_file, 'r', encoding='utf-8').read())
                print(f"📄 添加 {readme_file.name}")
        
        print(f"✅ 发布包创建完成: {zip_path}")
        return zip_path
    
    def create_default_config(self):
        """创建默认配置文件"""
        default_config = """# DY下载器 - 默认配置文件

# 服务器配置
server:
  host: "127.0.0.1"
  port: 5000
  debug: false

# 下载配置
download:
  # 下载目录
  save_dir: "./downloads"
  # 最大并发下载数
  max_concurrent: 3
  # 下载超时时间（秒）
  timeout: 30
  # 重试次数
  retry_times: 3

# 日志配置
logging:
  level: "INFO"
  file: "./logs/dy_downloader.log"
  max_size: "10MB"
  backup_count: 5

# 用户代理配置
user_agent:
  # 默认用户代理
  default: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
  # 随机用户代理列表
  random_agents:
    - "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    - "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    - "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# 代理配置
proxy:
  enabled: false
  http: ""
  https: ""

# 视频质量配置
video_quality:
  # 优先下载质量
  preferred: "720p"
  # 可用质量列表
  available: ["1080p", "720p", "480p", "360p"]

# 音频配置
audio:
  # 音频格式
  format: "mp3"
  # 音频质量
  quality: "128k"

# 文件命名配置
naming:
  # 文件名模板
  template: "{title}_{date}_{time}"
  # 日期格式
  date_format: "%Y-%m-%d"
  # 时间格式
  time_format: "%H.%M.%S"
  # 最大文件名长度
  max_length: 100

# 安全配置
security:
  # 验证SSL证书
  verify_ssl: true
  # 允许不安全连接
  allow_insecure: false

# 性能配置
performance:
  # 缓存大小（MB）
  cache_size: 100
  # 清理缓存间隔（小时）
  cache_cleanup_interval: 24
  # 内存使用限制（MB）
  memory_limit: 512
"""
        return default_config
    
    def clean_build(self):
        """清理构建文件"""
        print("🧹 清理构建文件...")
        
        # 清理PyInstaller文件
        spec_file = self.package_dir / "app.spec"
        if spec_file.exists():
            spec_file.unlink()
        
        # 清理构建目录
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        
        print("✅ 清理完成")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python build.py [pyinstaller|cx_freeze|nuitka|all]")
        print("")
        print("打包选项:")
        print("  pyinstaller - 使用 PyInstaller 打包")
        print("  cx_freeze   - 使用 cx_Freeze 打包")
        print("  nuitka      - 使用 Nuitka 打包")
        print("  all         - 使用所有方式打包")
        return
    
    builder = PackageBuilder()
    builder.check_dependencies()
    
    build_type = sys.argv[1].lower()
    
    try:
        if build_type == "pyinstaller":
            builder.build_with_pyinstaller()
        elif build_type == "cx_freeze":
            builder.build_with_cx_freeze()
        elif build_type == "nuitka":
            builder.build_with_nuitka()
        elif build_type == "all":
            print("🔨 使用所有方式打包...")
            builder.build_with_pyinstaller()
            builder.build_with_cx_freeze()
            builder.build_with_nuitka()
        else:
            print(f"❌ 未知的打包类型: {build_type}")
            return
        
        # 创建安装程序
        builder.create_installer()
        
        # 创建发布zip文件
        zip_path = builder.create_release_zip()
        
        print(f"\n🎉 打包完成！")
        print(f"📁 输出目录: {builder.dist_dir}")
        print(f"📦 发布包: {zip_path}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
    except Exception as e:
        print(f"❌ 打包出错: {e}")
    finally:
        # 清理构建文件
        builder.clean_build()

if __name__ == "__main__":
    main() 