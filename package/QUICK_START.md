# 🚀 快速打包指南

## 选择您的打包方式

### 🔨 PyInstaller（推荐新手）
```bash
cd package
python build.py pyinstaller
```

### ⚡ cx_Freeze（推荐性能）
```bash
cd package
python build.py cx_freeze
```

### 🚀 Nuitka（推荐生产）
```bash
cd package
python build.py nuitka
```

### 🔄 所有方式
```bash
cd package
python build.py all
```

## 📋 打包前检查清单

- [ ] Python 3.7+ 已安装
- [ ] pip 已安装
- [ ] 项目依赖已安装 (`pip install -r requirements.txt`)
- [ ] 项目结构完整（app.py, ui/, settings/, script/, apiproxy/）
- [ ] 图标文件已准备（可选：ui/static/favicon.ico）

## 🔧 常见问题解决

### 1. 依赖安装失败
```bash
# 升级pip
pip install --upgrade pip

# 安装打包工具
pip install pyinstaller cx_Freeze nuitka
```

### 2. 打包失败
```bash
# 检查Python版本
python --version

# 检查项目依赖
python -c "import flask, yaml, requests, PIL"
```

### 3. 文件过大
- 使用cx_Freeze或Nuitka
- 排除不必要的模块
- 优化数据文件

### 4. 启动失败
- 检查数据文件路径
- 验证依赖库
- 查看错误日志

## 📦 打包工具对比

| 工具 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| PyInstaller | 简单易用，单文件 | 文件大，启动慢 | 快速打包，简单分发 |
| cx_Freeze | 文件小，启动快 | 需要依赖库 | 性能要求高 |
| Nuitka | 性能最好，文件最小 | 编译时间长 | 生产环境 |

## 📤 输出文件

打包完成后，您将在 `package/dist/` 目录中找到：

- **可执行文件**: `DY下载器.exe` (Windows) 或 `DY下载器` (Linux/Mac)
- **数据文件**: UI模板、静态资源、配置文件等
- **安装脚本**: `install.bat` (Windows) 或 `install.sh` (Linux/Mac)

## 🎯 使用建议

### 开发测试
使用 **PyInstaller**，快速打包测试功能

### 性能优化
使用 **cx_Freeze**，平衡文件大小和启动速度

### 生产发布
使用 **Nuitka**，获得最佳性能和最小文件大小

## 📞 获取帮助

如果遇到问题，请：

1. 查看打包日志：`package/build/`
2. 检查错误信息
3. 参考详细文档：[打包说明](README.md)
4. 提交Issue：[问题反馈](https://github.com/CmeiLYL/DYDownload/issues) 