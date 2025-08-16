# 抖音下载器 Web UI - 项目目录结构

## 项目概述

这是一个基于 Flask 的抖音下载器 Web UI，提供了图形化界面来管理和下载抖音内容。

## 目录结构

```
抖音下载器-Web-UI/
├── README.md                           # 项目主说明文档
├── PROJECT_STRUCTURE.md                # 项目目录结构说明（本文件）
├── VIDEO_THUMBNAILS.md                 # 视频缩略图功能说明
├── PAGINATION_FEATURES.md              # 分页功能说明
├── OPTIMIZATION_SUMMARY.md             # 优化总结
├── WEB_UI_SUMMARY.md                   # Web UI 总结
├── README_WEB_UI.md                    # Web UI 使用说明
├── config.example.yml                  # 配置文件示例
├── config.yml                          # 配置文件
├── config.yml.backup                   # 配置文件备份
├── requirements.txt                    # Python 依赖包列表
├── app.py                              # 主应用程序文件
├── DouYinCommand.py                    # 原始下载器命令行版本
├── run_web.py                          # Web UI 启动脚本
├── demo_web_ui.py                      # Web UI 演示脚本
├── start_web_ui.bat                    # Windows 启动脚本
├── data.db                             # 数据库文件
├── .gitignore                          # Git 忽略文件
├── .gitmessage                         # Git 提交信息模板
├── .pytest_cache/                      # pytest 缓存目录
├── .venv/                              # Python 虚拟环境
├── .idea/                              # IDE 配置目录
├── __pycache__/                        # Python 缓存目录
├── logs/                               # 日志文件目录
│   └── douyin.log                      # 应用日志文件
├── Downloaded/                         # 下载文件目录
│   ├── temp/                           # 临时文件目录
│   │   └── thumbnails/                 # 缩略图缓存目录
│   └── [用户目录]/                      # 用户下载内容
├── test/                               # 测试脚本目录
│   ├── README.md                       # 测试目录说明
│   ├── install_dependencies.py         # 依赖安装脚本
│   ├── install_ffmpeg.py               # ffmpeg 安装脚本
│   ├── fix_tqdm.py                     # tqdm 依赖修复脚本
│   ├── diagnose_web.py                 # Web UI 诊断脚本
│   ├── test_download.py                # 下载功能测试
│   ├── test_web_ui.py                  # Web UI 基础功能测试
│   ├── test_pagination.py              # 分页功能测试
│   ├── test_thumbnail.py               # 缩略图功能测试
│   ├── test_file_preview.py            # 文件预览功能测试
│   ├── test_video_thumbnails.py        # 视频缩略图测试
│   ├── test_background_thumbnails.py   # 后台缩略图生成测试
│   ├── test_ffmpeg_encoding.py         # ffmpeg 编码测试
│   ├── test_path_fix.py                # 路径修复测试
│   ├── test_preview_fix.py             # 预览修复测试
│   ├── test_preview_enhancement.py     # 预览增强测试
│   ├── test_video_api.py               # 视频API测试
│   ├── test_video_image_fix.py         # 视频图片修复测试
│   ├── test_fullscreen_preview.py      # 全屏预览测试
│   ├── test_debug_info.py              # 调试信息测试
│   ├── test_file_filtering.py          # 文件过滤测试
│   ├── test_web_fix.py                 # Web修复测试
│   ├── test_file_functions.py          # 文件功能测试
│   └── test_pagination_update.py       # 分页更新测试
├── templates/                          # HTML 模板目录
│   └── index.html                      # 主页面模板
├── static/                             # 静态文件目录
│   ├── app.js                          # 主要 JavaScript 文件
│   └── app_simple.js                   # 简化版 JavaScript 文件
├── apiproxy/                           # 抖音 API 代理模块
│   ├── __init__.py
│   ├── common/                         # 通用工具模块
│   │   ├── __init__.py
│   │   └── utils.py                    # 工具函数
│   └── douyin/                         # 抖音相关模块
│       ├── __init__.py
│       ├── douyin.py                   # 抖音 API 核心
│       ├── download.py                 # 下载功能
│       └── douyin_headers.py           # 请求头配置
├── utils/                              # 工具模块目录
├── img/                                # 图片资源目录
├── docs/                               # 文档目录
└── WEB_UI_SUMMARY.md                   # Web UI 总结文档
```

## 核心文件说明

### 主要应用文件
- `app.py` - Flask 主应用程序，包含所有 API 路由和业务逻辑
- `DouYinCommand.py` - 原始的命令行版本下载器
- `run_web.py` - Web UI 启动脚本

### 配置文件
- `config.yml` - 主配置文件，包含下载设置和链接
- `config.example.yml` - 配置文件示例
- `requirements.txt` - Python 依赖包列表

### 前端文件
- `templates/index.html` - 主页面 HTML 模板
- `static/app.js` - 主要 JavaScript 逻辑
- `static/app_simple.js` - 文件管理相关的 JavaScript

### 后端模块
- `apiproxy/` - 抖音 API 代理模块，包含所有下载逻辑
- `utils/` - 工具模块

### 测试和工具
- `test/` - 所有测试脚本和工具
- `logs/` - 日志文件目录
- `Downloaded/` - 下载文件存储目录

## 功能模块

### 1. Web UI 界面
- 基于 Flask + Bootstrap 5
- 响应式设计，支持移动端
- 标签页导航（首页、设置、文件、日志）

### 2. 下载功能
- 支持用户主页、单个视频、合集、音乐、直播链接
- 可配置下载选项（音乐、封面、头像、JSON等）
- 支持增量下载和数量限制
- 多线程下载

### 3. 文件管理
- 文件列表显示
- 分页功能
- 文件分类（视频、图片）
- 文件预览（视频播放、图片查看）
- 缩略图生成

### 4. 视频缩略图
- 后台异步生成
- 懒加载优化
- 缓存管理
- 支持多种视频格式

### 5. 配置管理
- YAML 配置文件
- 配置备份和恢复
- 实时配置更新

### 6. 日志系统
- 详细的日志记录
- 前端日志显示
- 彩色日志输出

## 技术栈

### 后端
- **Flask** - Web 框架
- **Flask-CORS** - 跨域支持
- **Pillow** - 图片处理
- **PyYAML** - 配置文件处理
- **pathlib** - 路径处理

### 前端
- **Bootstrap 5** - UI 框架
- **Bootstrap Icons** - 图标库
- **原生 JavaScript** - 交互逻辑

### 下载器
- **apiproxy** - 抖音 API 代理
- **requests** - HTTP 请求
- **ffmpeg** - 视频处理（可选）

## 启动方式

### 1. 直接启动
```bash
python app.py
```

### 2. 使用启动脚本
```bash
python run_web.py
```

### 3. Windows 批处理
```bash
start_web_ui.bat
```

## 访问地址

启动后访问：`http://localhost:5000`

## 开发说明

### 添加新功能
1. 在 `app.py` 中添加新的 API 路由
2. 在 `templates/index.html` 中添加前端界面
3. 在 `static/app.js` 或 `static/app_simple.js` 中添加交互逻辑
4. 在 `test/` 目录中添加相应的测试脚本

### 测试
1. 进入 `test/` 目录
2. 运行相应的测试脚本
3. 查看测试结果和日志

### 部署
1. 安装依赖：`pip install -r requirements.txt`
2. 配置 `config.yml`
3. 启动应用：`python app.py`
4. 访问 Web 界面

## 注意事项

1. 确保 Python 3.7+ 环境
2. 安装所有必要的依赖包
3. 配置正确的下载路径
4. 确保网络连接正常
5. 视频缩略图功能需要安装 ffmpeg
6. 定期备份配置文件 