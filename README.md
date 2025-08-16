# 抖音下载器 Web UI

一个基于 Flask 的抖音下载器 Web 界面，提供图形化操作来管理和下载抖音内容。

## 功能特性

- 🎯 **Web 界面** - 基于 Flask + Bootstrap 5 的现代化界面
- 📥 **批量下载** - 支持用户主页、单个视频、合集、音乐、直播链接
- 🎨 **文件预览** - 支持视频播放和图片查看
- 🖼️ **缩略图** - 自动生成视频和图片缩略图
- 📄 **分页管理** - 文件列表分页显示，支持搜索和过滤
- ⚙️ **配置管理** - YAML 配置文件，支持实时更新
- 📊 **日志系统** - 详细的日志记录和前端显示
- 🔄 **增量下载** - 支持增量更新，避免重复下载

## 快速开始

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 或者使用测试目录中的安装脚本
cd test
python install_dependencies.py
```

### 2. 配置设置

复制配置文件示例并修改：

```bash
cp config.example.yml config.yml
```

编辑 `config.yml` 文件，添加抖音链接和配置选项。

### 3. 启动应用

```bash
# 方式1：直接启动
python app.py

# 方式2：使用启动脚本
python run_web.py

# 方式3：Windows 批处理
start_web_ui.bat
```

### 4. 访问界面

打开浏览器访问：`http://localhost:5000`

## 项目结构

```
抖音下载器-Web-UI/
├── app.py                              # 主应用程序
├── DouYinCommand.py                    # 原始下载器
├── config.yml                          # 配置文件
├── requirements.txt                    # 依赖列表
├── templates/                          # HTML 模板
├── static/                             # 静态文件
├── test/                               # 测试脚本目录
├── apiproxy/                           # 抖音 API 模块
├── logs/                               # 日志目录
├── Downloaded/                         # 下载目录
└── docs/                               # 文档目录
```

详细的项目结构说明请查看：[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## 使用说明

### 1. 添加下载链接

在"首页"标签页中：
- 输入抖音链接（用户主页、视频、合集等）
- 点击"添加链接"按钮
- 系统会自动解析链接类型和用户信息

### 2. 配置下载选项

在"设置"标签页中：
- **下载路径** - 设置文件保存位置
- **下载选项** - 选择是否下载音乐、封面、头像等
- **下载模式** - 选择下载发布作品、喜欢作品或合集
- **数量限制** - 设置各类内容的下载数量
- **线程数** - 设置并发下载线程数

### 3. 开始下载

- 点击"开始下载"按钮
- 在"日志"标签页查看下载进度
- 下载完成后在"文件"标签页查看结果

### 4. 文件管理

在"文件"标签页中：
- 查看所有下载的文件
- 支持分页浏览和搜索
- 点击文件可直接预览
- 右键点击可在文件夹中打开

## 支持的链接类型

- **用户主页** - `https://www.douyin.com/user/...`
- **单个视频** - `https://v.douyin.com/...`
- **合集** - `https://www.douyin.com/collection/...`
- **音乐** - `https://www.douyin.com/music/...`
- **直播** - `https://live.douyin.com/...`

## 配置选项

### 基本设置
- `path` - 下载保存路径
- `thread` - 下载线程数
- `database` - 是否使用数据库

### 下载选项
- `music` - 是否下载音乐文件
- `cover` - 是否下载视频封面
- `avatar` - 是否下载用户头像
- `json` - 是否保存 JSON 数据
- `folderstyle` - 是否使用文件夹样式

### 下载模式
- `mode` - 下载模式：`post`（发布）、`like`（喜欢）、`mix`（合集）

### 数量限制
- `number.post` - 发布作品数量限制
- `number.like` - 喜欢作品数量限制
- `number.mix` - 合集数量限制

### 增量下载
- `increase.post` - 是否增量下载发布作品
- `increase.like` - 是否增量下载喜欢作品
- `increase.mix` - 是否增量下载合集

## 测试和调试

### 运行测试

```bash
cd test

# 安装依赖
python install_dependencies.py

# 诊断问题
python diagnose_web.py

# 测试下载功能
python test_download.py

# 测试 Web UI
python test_web_ui.py
```

### 常见问题

1. **依赖问题** - 运行 `test/install_dependencies.py`
2. **ffmpeg 问题** - 运行 `test/install_ffmpeg.py`
3. **tqdm 问题** - 运行 `test/fix_tqdm.py`
4. **网络问题** - 检查网络连接和防火墙设置

## 技术栈

### 后端
- **Flask** - Web 框架
- **Flask-CORS** - 跨域支持
- **Pillow** - 图片处理
- **PyYAML** - 配置文件处理

### 前端
- **Bootstrap 5** - UI 框架
- **Bootstrap Icons** - 图标库
- **原生 JavaScript** - 交互逻辑

### 下载器
- **apiproxy** - 抖音 API 代理
- **requests** - HTTP 请求
- **ffmpeg** - 视频处理（可选）

## 开发说明

### 添加新功能
1. 在 `app.py` 中添加新的 API 路由
2. 在 `templates/index.html` 中添加前端界面
3. 在 `static/app.js` 中添加交互逻辑
4. 在 `test/` 目录中添加测试脚本

### 测试
1. 进入 `test/` 目录
2. 运行相应的测试脚本
3. 查看测试结果和日志

## 更新日志

详细的更新日志请查看：[VIDEO_THUMBNAILS.md](VIDEO_THUMBNAILS.md)

## 许可证

本项目仅供学习和研究使用，请遵守相关法律法规。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关文档

- [项目结构说明](PROJECT_STRUCTURE.md)
- [视频缩略图功能](VIDEO_THUMBNAILS.md)
- [分页功能说明](PAGINATION_FEATURES.md)
- [优化总结](OPTIMIZATION_SUMMARY.md)
- [Web UI 使用说明](README_WEB_UI.md) 

