# 项目结构

## 目录组织

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
│   └── DouYinCommand.py    # 抖音命令处理脚本
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

## 文件分类说明

### 文档文件 (docs/)
- 所有 `.md` 格式的文档文件
- 包含项目说明、使用指南、功能文档等

### UI文件 (ui/)
- Web界面相关的所有文件
- 包括静态资源、HTML模板、UI脚本等
- Web服务器启动和配置脚本

### 脚本文件 (script/)
- 独立的Python脚本文件
- 命令行工具和辅助脚本
- 快速启动和命令处理脚本

### 配置文件 (settings/)
- 所有配置相关文件
- 主配置文件、备份文件、示例文件
- 数据库文件

### 核心文件 (根目录)
- 主应用程序文件 (`app.py`)
- 依赖管理文件 (`requirements.txt`)

## 使用说明

1. **启动Web UI**: 进入 `ui/` 目录，运行 `python run_web.py` 或双击 `start_web_ui.bat`
2. **查看文档**: 所有文档都在 `docs/` 目录中
3. **运行脚本**: 独立的脚本文件都在 `script/` 目录中
4. **配置项目**: 编辑 `settings/config.yml` 文件

## 注意事项

- 移动文件后，可能需要更新一些文件中的相对路径引用
- 确保在运行脚本时使用正确的相对路径
- Web UI的静态资源和模板文件现在位于 `ui/` 目录下
- 配置文件和数据库文件现在位于 `settings/` 目录下 