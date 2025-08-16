# DY下载器 Web UI

一个基于 Flask 的DY下载器 Web 界面，提供图形化界面来管理和下载DY内容。

## 项目结构

```
DYDownload/
├── docs/                    # 文档目录
│   ├── README.md           # 项目主要说明文档
│   ├── PROJECT_STRUCTURE.md # 项目结构说明
│   ├── FINAL_SUMMARY.md    # 项目总结
│   ├── VIDEO_THUMBNAILS.md # 视频缩略图功能说明
│   ├── README_WEB_UI.md    # Web UI说明
│   ├── PAGINATION_FEATURES.md # 分页功能说明
│   ├── OPTIMIZATION_SUMMARY.md # 优化总结
│   ├── WEB_UI_SUMMARY.md   # Web UI总结
│   └── examples.md         # 使用示例
├── ui/                      # UI相关文件目录
│   ├── static/             # 静态资源文件
│   │   ├── app.js          # 主要JavaScript文件
│   │   ├── app_new.js      # 新版JavaScript文件
│   │   └── app_simple.js   # 简化版JavaScript文件
│   ├── templates/          # HTML模板文件
│   │   └── index.html      # 主页面模板
│   ├── demo_web_ui.py      # Web UI演示脚本
│   ├── run_web.py          # Web服务器启动脚本
│   └── start_web_ui.bat    # Windows启动脚本
├── script/                  # 脚本文件目录
│   ├── quick_start.py      # 快速启动脚本
│   └── DouYinCommand.py    # DY命令处理脚本
├── settings/                # 配置和数据库文件目录
│   ├── config.yml          # 主配置文件
│   ├── config.yml.backup   # 配置文件备份
│   ├── config.example.yml  # 配置示例文件
│   └── data.db             # 数据库文件
├── utils/                   # 工具函数
├── test/                    # 测试文件
├── logs/                    # 日志文件
├── img/                     # 图片资源
├── apiproxy/               # API代理
├── app.py                  # 主应用程序
├── requirements.txt        # Python依赖
├── .gitignore             # Git忽略文件
└── .gitmessage            # Git提交信息模板
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置项目

复制配置文件示例并编辑：

```bash
cp settings/config.example.yml settings/config.yml
# 编辑 settings/config.yml 文件，配置下载链接和选项
```

### 3. 启动Web UI

#### 方法一：直接启动
```bash
python app.py
```

#### 方法二：使用启动脚本
```bash
python script/quick_start.py
```

#### 方法三：使用UI目录下的脚本
```bash
cd ui
python run_web.py
```

#### 方法四：Windows批处理
```bash
# 双击 ui/start_web_ui.bat
```

### 4. 访问界面

启动后访问：`http://localhost:5000`

## 主要功能

- **下载管理**: 支持用户主页、单个视频、合集、音乐、直播链接下载
- **文件管理**: 文件列表、分页、分类、预览功能
- **视频缩略图**: 自动生成视频缩略图
- **配置管理**: 实时配置更新和备份
- **日志系统**: 详细的日志记录和显示

## 文件说明

### 文档文件 (docs/)
- 所有项目文档和使用说明
- 功能特性说明和优化总结

### UI文件 (ui/)
- Web界面相关的所有文件
- 静态资源、HTML模板、UI脚本
- Web服务器启动脚本

### 脚本文件 (script/)
- 独立的Python脚本文件
- 命令行工具和辅助脚本

### 配置文件 (settings/)
- 所有配置相关文件
- 主配置文件、备份文件、示例文件
- 数据库文件

### 核心文件 (根目录)
- 主应用程序文件 (`app.py`)
- 依赖管理文件 (`requirements.txt`)

## 注意事项

- 确保Python 3.7+环境
- 安装所有必要的依赖包
- 配置正确的下载路径
- 确保网络连接正常
- 视频缩略图功能需要安装ffmpeg

## 故障排除

如果遇到问题，请：

1. 检查日志文件：`logs/douyin.log`
2. 运行诊断脚本：`python test/diagnose_web.py`
3. 查看测试脚本：`test/` 目录下的各种测试文件

## 开发说明

- 添加新功能时，注意更新相应的路径引用
- UI相关文件放在 `ui/` 目录下
- 脚本文件放在 `script/` 目录下
- 文档文件放在 `docs/` 目录下 

