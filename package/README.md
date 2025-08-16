# 打包文件说明

本文件夹包含DY下载器应用的所有打包相关文件，用于将Python应用打包成可执行程序。

## 📁 文件说明

### 打包脚本
- `build.py` - Python打包脚本（跨平台）
- `build.sh` - Linux/Mac打包脚本
- `build.bat` - Windows打包脚本

### 输出目录
- `dist/` - 打包后的可执行文件输出目录
- `build/` - 临时构建文件目录

## 🔨 支持的打包方式

### 1. PyInstaller
- **优点**: 简单易用，支持单文件打包
- **缺点**: 文件较大，启动较慢
- **适用**: 快速打包，简单分发

### 2. cx_Freeze
- **优点**: 文件较小，启动较快
- **缺点**: 需要依赖库
- **适用**: 性能要求较高的场景

### 3. Nuitka
- **优点**: 性能最好，文件最小
- **缺点**: 编译时间长，依赖C编译器
- **适用**: 生产环境，性能要求极高

## 🚀 快速打包

### 使用Python脚本（推荐）
```bash
cd package
python build.py pyinstaller    # 使用PyInstaller
python build.py cx_freeze      # 使用cx_Freeze
python build.py nuitka         # 使用Nuitka
python build.py all            # 使用所有方式
```

### 使用Shell脚本（Linux/Mac）
```bash
cd package
chmod +x build.sh
./build.sh pyinstaller
./build.sh cx_freeze
./build.sh nuitka
./build.sh all
```

### 使用批处理脚本（Windows）
```bash
cd package
build.bat pyinstaller
build.bat cx_freeze
build.bat nuitka
build.bat all
```

## 📋 打包前准备

1. **确保项目依赖已安装**：
   ```bash
   pip install -r requirements.txt
   ```

2. **检查项目结构**：
   - `app.py` - 主应用程序
   - `ui/templates/` - HTML模板
   - `ui/static/` - 静态资源
   - `settings/` - 配置文件
   - `script/` - 脚本文件
   - `apiproxy/` - API代理

3. **准备图标文件**（可选）：
   - 将图标文件放在 `ui/static/favicon.ico`

## 📦 打包选项说明

### PyInstaller选项
- `--onefile`: 打包成单个可执行文件
- `--windowed`: 无控制台窗口（Windows）
- `--icon`: 设置应用图标
- `--add-data`: 添加数据文件

### cx_Freeze选项
- `--packages`: 包含的Python包
- `--excludes`: 排除的模块
- `--include_files`: 包含的文件
- `--optimize`: 优化级别

### Nuitka选项
- `--standalone`: 独立可执行文件
- `--include-data-dir`: 包含数据目录
- `--remove-output`: 移除输出文件
- `--assume-yes-for-downloads`: 自动下载依赖

## 🔧 自定义打包

### 修改打包配置
编辑对应的打包脚本文件：
- `build.py` - 修改Python脚本中的配置
- `build.sh` - 修改Shell脚本中的命令
- `build.bat` - 修改批处理脚本中的命令

### 添加自定义数据文件
在打包脚本中添加 `--add-data` 或 `--include-data-dir` 参数：
```bash
--add-data "path/to/file:destination"
--include-data-dir "path/to/dir=destination"
```

### 设置应用图标
确保图标文件存在，打包脚本会自动检测并使用：
```
ui/static/favicon.ico
```

## 📤 输出文件说明

### 打包后的文件结构
```
package/dist/
├── DY下载器.exe          # Windows可执行文件
├── DY下载器              # Linux/Mac可执行文件
├── ui/                   # UI文件
│   ├── templates/        # HTML模板
│   └── static/          # 静态资源
├── settings/            # 配置文件
├── script/              # 脚本文件
├── apiproxy/            # API代理
├── install.bat          # Windows安装脚本
└── install.sh           # Linux/Mac安装脚本
```

### 安装程序
- `install.bat` - Windows安装脚本
- `install.sh` - Linux/Mac安装脚本

## 🔍 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   # 升级pip
   pip install --upgrade pip
   
   # 重新安装依赖
   pip install pyinstaller cx_Freeze nuitka
   ```

2. **打包失败**
   ```bash
   # 检查Python版本
   python --version
   
   # 检查依赖
   python -c "import flask, yaml, requests, PIL"
   ```

3. **文件过大**
   - 使用cx_Freeze或Nuitka
   - 排除不必要的模块
   - 优化数据文件

4. **启动失败**
   - 检查数据文件路径
   - 验证依赖库
   - 查看错误日志

### 调试方法

1. **查看详细输出**：
   ```bash
   python build.py pyinstaller --debug
   ```

2. **检查打包日志**：
   ```bash
   # PyInstaller日志
   cat build/build.log
   
   # cx_Freeze日志
   cat build/build.log
   ```

3. **测试可执行文件**：
   ```bash
   # 直接运行
   ./dist/DY下载器
   
   # 查看依赖
   ldd dist/DY下载器  # Linux
   otool -L dist/DY下载器  # Mac
   ```

## 📚 相关文档

- [PyInstaller文档](https://pyinstaller.org/)
- [cx_Freeze文档](https://cx-freeze.readthedocs.io/)
- [Nuitka文档](https://nuitka.net/)
- [项目README](../README.md) 