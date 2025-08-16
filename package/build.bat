@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo 🔨 DY下载器 - 打包脚本
echo ====================

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

echo 📁 项目根目录: %PROJECT_ROOT%
echo 📁 脚本目录: %SCRIPT_DIR%

REM 检查参数
if "%~1"=="" (
    echo 用法: %0 [pyinstaller^|cx_freeze^|nuitka^|all]
    echo.
    echo 打包选项:
    echo   pyinstaller - 使用 PyInstaller 打包
    echo   cx_freeze   - 使用 cx_Freeze 打包
    echo   nuitka      - 使用 Nuitka 打包
    echo   all         - 使用所有方式打包
    exit /b 1
)

set BUILD_TYPE=%~1

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

echo 📋 检查打包依赖...

REM 检查并安装PyInstaller
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 📦 安装 PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ PyInstaller 安装失败
        exit /b 1
    )
) else (
    echo ✅ PyInstaller 已安装
)

REM 检查并安装cx_Freeze
python -c "import cx_Freeze" >nul 2>&1
if errorlevel 1 (
    echo 📦 安装 cx_Freeze...
    pip install cx_Freeze
    if errorlevel 1 (
        echo ❌ cx_Freeze 安装失败
        exit /b 1
    )
) else (
    echo ✅ cx_Freeze 已安装
)

REM 检查并安装Nuitka
python -c "import nuitka" >nul 2>&1
if errorlevel 1 (
    echo 📦 安装 Nuitka...
    pip install nuitka
    if errorlevel 1 (
        echo ❌ Nuitka 安装失败
        exit /b 1
    )
) else (
    echo ✅ Nuitka 已安装
)

echo ✅ 所有依赖检查完成

REM 创建输出目录
if not exist "%SCRIPT_DIR%dist" mkdir "%SCRIPT_DIR%dist"
if not exist "%SCRIPT_DIR%build" mkdir "%SCRIPT_DIR%build"

REM 根据参数执行打包
if "%BUILD_TYPE%"=="pyinstaller" (
    call :build_pyinstaller
) else if "%BUILD_TYPE%"=="cx_freeze" (
    call :build_cx_freeze
) else if "%BUILD_TYPE%"=="nuitka" (
    call :build_nuitka
) else if "%BUILD_TYPE%"=="all" (
    echo 🔨 使用所有方式打包...
    call :build_pyinstaller
    call :build_cx_freeze
    call :build_nuitka
) else (
    echo ❌ 未知的打包类型: %BUILD_TYPE%
    echo 支持的打包类型: pyinstaller, cx_freeze, nuitka, all
    exit /b 1
)

REM 创建安装程序
call :create_installer

echo.
echo 🎉 打包完成！
echo 📁 输出目录: %SCRIPT_DIR%dist
goto :eof

REM PyInstaller打包
:build_pyinstaller
echo 🔨 使用 PyInstaller 打包...
cd /d "%SCRIPT_DIR%"

REM 构建PyInstaller命令
set PYINSTALLER_CMD=pyinstaller --distpath dist --workpath build --specpath . --clean --noconfirm --onefile

REM 添加数据文件
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --add-data "%PROJECT_ROOT%\ui\templates;ui\templates"
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --add-data "%PROJECT_ROOT%\ui\static;ui\static"
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --add-data "%PROJECT_ROOT%\settings;settings"
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --add-data "%PROJECT_ROOT%\script;script"
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --add-data "%PROJECT_ROOT%\apiproxy;apiproxy"

REM 添加图标（如果存在）
if exist "%PROJECT_ROOT%\ui\static\favicon.ico" (
    set PYINSTALLER_CMD=%PYINSTALLER_CMD% --icon "%PROJECT_ROOT%\ui\static\favicon.ico"
)

REM 添加主程序
set PYINSTALLER_CMD=%PYINSTALLER_CMD% "%PROJECT_ROOT%\app.py"

echo 执行命令: %PYINSTALLER_CMD%
%PYINSTALLER_CMD%
if errorlevel 1 (
    echo ❌ PyInstaller 打包失败
    exit /b 1
)

echo ✅ PyInstaller 打包完成
goto :eof

REM cx_Freeze打包
:build_cx_freeze
echo 🔨 使用 cx_Freeze 打包...
cd /d "%SCRIPT_DIR%"

REM 创建setup.py
echo import sys > setup_cx_freeze.py
echo import os >> setup_cx_freeze.py
echo from cx_Freeze import setup, Executable >> setup_cx_freeze.py
echo. >> setup_cx_freeze.py
echo project_root = r"%PROJECT_ROOT%" >> setup_cx_freeze.py
echo sys.path.insert(0, project_root) >> setup_cx_freeze.py
echo. >> setup_cx_freeze.py
echo include_files = [ >> setup_cx_freeze.py
echo     (os.path.join(project_root, "ui/templates"), "ui/templates"), >> setup_cx_freeze.py
echo     (os.path.join(project_root, "ui/static"), "ui/static"), >> setup_cx_freeze.py
echo     (os.path.join(project_root, "settings"), "settings"), >> setup_cx_freeze.py
echo     (os.path.join(project_root, "script"), "script"), >> setup_cx_freeze.py
echo     (os.path.join(project_root, "apiproxy"), "apiproxy"), >> setup_cx_freeze.py
echo ] >> setup_cx_freeze.py
echo. >> setup_cx_freeze.py
echo build_options = { >> setup_cx_freeze.py
echo     "packages": ["flask", "yaml", "requests", "PIL"], >> setup_cx_freeze.py
echo     "excludes": ["tkinter", "matplotlib", "numpy", "pandas"], >> setup_cx_freeze.py
echo     "include_files": include_files, >> setup_cx_freeze.py
echo     "optimize": 2, >> setup_cx_freeze.py
echo } >> setup_cx_freeze.py
echo. >> setup_cx_freeze.py
echo base = None >> setup_cx_freeze.py
echo if sys.platform == "win32": >> setup_cx_freeze.py
echo     base = "Win32GUI" >> setup_cx_freeze.py
echo. >> setup_cx_freeze.py
echo executables = [ >> setup_cx_freeze.py
echo     Executable( >> setup_cx_freeze.py
echo         os.path.join(project_root, "app.py"), >> setup_cx_freeze.py
echo         base=base, >> setup_cx_freeze.py
echo         target_name="DY下载器.exe", >> setup_cx_freeze.py
echo         icon=os.path.join(project_root, "ui/static/favicon.ico") if os.path.exists(os.path.join(project_root, "ui/static/favicon.ico")) else None >> setup_cx_freeze.py
echo     ) >> setup_cx_freeze.py
echo ] >> setup_cx_freeze.py
echo. >> setup_cx_freeze.py
echo setup( >> setup_cx_freeze.py
echo     name="DY下载器", >> setup_cx_freeze.py
echo     version="1.0.0", >> setup_cx_freeze.py
echo     description="DY内容下载器", >> setup_cx_freeze.py
echo     options={"build_exe": build_options}, >> setup_cx_freeze.py
echo     executables=executables >> setup_cx_freeze.py
echo ) >> setup_cx_freeze.py

REM 执行打包
python setup_cx_freeze.py build
if errorlevel 1 (
    echo ❌ cx_Freeze 打包失败
    del setup_cx_freeze.py
    exit /b 1
)

REM 清理临时文件
del setup_cx_freeze.py

echo ✅ cx_Freeze 打包完成
goto :eof

REM Nuitka打包
:build_nuitka
echo 🔨 使用 Nuitka 打包...
cd /d "%SCRIPT_DIR%"

REM 构建Nuitka命令
set NUITKA_CMD=python -m nuitka --output-dir dist --remove-output --assume-yes-for-downloads --standalone

REM 添加数据文件
set NUITKA_CMD=%NUITKA_CMD% --include-data-dir "%PROJECT_ROOT%\ui\templates=ui\templates"
set NUITKA_CMD=%NUITKA_CMD% --include-data-dir "%PROJECT_ROOT%\ui\static=ui\static"
set NUITKA_CMD=%NUITKA_CMD% --include-data-dir "%PROJECT_ROOT%\settings=settings"
set NUITKA_CMD=%NUITKA_CMD% --include-data-dir "%PROJECT_ROOT%\script=script"
set NUITKA_CMD=%NUITKA_CMD% --include-data-dir "%PROJECT_ROOT%\apiproxy=apiproxy"

REM 添加主程序
set NUITKA_CMD=%NUITKA_CMD% "%PROJECT_ROOT%\app.py"

echo 执行命令: %NUITKA_CMD%
%NUITKA_CMD%
if errorlevel 1 (
    echo ❌ Nuitka 打包失败
    exit /b 1
)

echo ✅ Nuitka 打包完成
goto :eof

REM 创建安装程序
:create_installer
echo 🔨 创建安装程序...

REM 创建安装脚本
echo @echo off > "%SCRIPT_DIR%dist\install.bat"
echo chcp 65001 ^>nul >> "%SCRIPT_DIR%dist\install.bat"
echo echo DY下载器 - 安装程序 >> "%SCRIPT_DIR%dist\install.bat"
echo echo ==================== >> "%SCRIPT_DIR%dist\install.bat"
echo. >> "%SCRIPT_DIR%dist\install.bat"
echo set INSTALL_DIR=%%PROGRAMFILES%%\DY下载器 >> "%SCRIPT_DIR%dist\install.bat"
echo set START_MENU_DIR=%%APPDATA%%\Microsoft\Windows\Start Menu\Programs\DY下载器 >> "%SCRIPT_DIR%dist\install.bat"
echo. >> "%SCRIPT_DIR%dist\install.bat"
echo echo 正在安装到: %%INSTALL_DIR%% >> "%SCRIPT_DIR%dist\install.bat"
echo. >> "%SCRIPT_DIR%dist\install.bat"
echo if not exist "%%INSTALL_DIR%%" mkdir "%%INSTALL_DIR%%" >> "%SCRIPT_DIR%dist\install.bat"
echo xcopy /E /I /Y "dist\*" "%%INSTALL_DIR%%" >> "%SCRIPT_DIR%dist\install.bat"
echo. >> "%SCRIPT_DIR%dist\install.bat"
echo if not exist "%%START_MENU_DIR%%" mkdir "%%START_MENU_DIR%%" >> "%SCRIPT_DIR%dist\install.bat"
echo. >> "%SCRIPT_DIR%dist\install.bat"
echo echo 安装完成！ >> "%SCRIPT_DIR%dist\install.bat"
echo echo 您可以在桌面和开始菜单中找到 DY下载器 >> "%SCRIPT_DIR%dist\install.bat"
echo pause >> "%SCRIPT_DIR%dist\install.bat"

echo ✅ 安装程序创建完成
goto :eof 