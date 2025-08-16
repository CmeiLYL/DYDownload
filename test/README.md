# 测试脚本目录

本目录包含抖音下载器 Web UI 的所有测试脚本和工具。

## 目录结构

```
test/
├── README.md                           # 本文件
├── install_dependencies.py             # 依赖安装脚本
├── install_ffmpeg.py                   # ffmpeg 安装脚本
├── fix_tqdm.py                         # tqdm 依赖修复脚本
├── diagnose_web.py                     # Web UI 诊断脚本
├── test_download.py                    # 下载功能测试
├── test_web_ui.py                      # Web UI 基础功能测试
├── test_pagination.py                  # 分页功能测试
├── test_thumbnail.py                   # 缩略图功能测试
├── test_file_preview.py                # 文件预览功能测试
├── test_video_thumbnails.py            # 视频缩略图测试
├── test_background_thumbnails.py       # 后台缩略图生成测试
├── test_ffmpeg_encoding.py             # ffmpeg 编码测试
├── test_path_fix.py                    # 路径修复测试
├── test_preview_fix.py                 # 预览修复测试
├── test_preview_enhancement.py         # 预览增强测试
├── test_video_api.py                   # 视频API测试
├── test_video_image_fix.py             # 视频图片修复测试
├── test_fullscreen_preview.py          # 全屏预览测试
├── test_debug_info.py                  # 调试信息测试
├── test_file_filtering.py              # 文件过滤测试
├── test_web_fix.py                     # Web修复测试
├── test_file_functions.py              # 文件功能测试
├── test_pagination_update.py           # 分页更新测试
└── test_thumbnail.py                   # 缩略图测试
```

## 脚本分类

### 安装和修复脚本
- `install_dependencies.py` - 安装所有必要的依赖包
- `install_ffmpeg.py` - 安装和配置 ffmpeg
- `fix_tqdm.py` - 修复 tqdm 依赖问题

### 诊断脚本
- `diagnose_web.py` - 诊断 Web UI 的问题

### 功能测试脚本
- `test_download.py` - 测试下载功能
- `test_web_ui.py` - 测试 Web UI 基础功能
- `test_pagination.py` - 测试分页功能
- `test_thumbnail.py` - 测试缩略图功能
- `test_file_preview.py` - 测试文件预览功能

### 视频相关测试
- `test_video_thumbnails.py` - 测试视频缩略图
- `test_background_thumbnails.py` - 测试后台缩略图生成
- `test_video_api.py` - 测试视频API
- `test_video_image_fix.py` - 测试视频图片修复

### 修复验证测试
- `test_ffmpeg_encoding.py` - 验证 ffmpeg 编码修复
- `test_path_fix.py` - 验证路径修复
- `test_preview_fix.py` - 验证预览修复
- `test_preview_enhancement.py` - 验证预览增强
- `test_fullscreen_preview.py` - 验证全屏预览
- `test_debug_info.py` - 验证调试信息
- `test_file_filtering.py` - 验证文件过滤
- `test_web_fix.py` - 验证Web修复
- `test_file_functions.py` - 验证文件功能
- `test_pagination_update.py` - 验证分页更新

## 使用方法

### 1. 安装依赖
```bash
cd test
python install_dependencies.py
```

### 2. 安装 ffmpeg
```bash
python install_ffmpeg.py
```

### 3. 修复依赖问题
```bash
python fix_tqdm.py
```

### 4. 诊断问题
```bash
python diagnose_web.py
```

### 5. 运行功能测试
```bash
# 测试下载功能
python test_download.py

# 测试 Web UI
python test_web_ui.py

# 测试分页功能
python test_pagination.py

# 测试缩略图功能
python test_thumbnail.py
```

### 6. 运行修复验证测试
```bash
# 验证路径修复
python test_path_fix.py

# 验证预览修复
python test_preview_fix.py

# 验证视频API
python test_video_api.py
```

## 注意事项

1. 运行测试前确保 Web UI 服务器已启动
2. 某些测试需要网络连接
3. 视频相关测试需要安装 ffmpeg
4. 测试脚本会创建临时文件和目录
5. 建议按顺序运行测试脚本

## 故障排除

如果遇到问题，请按以下顺序检查：

1. 运行 `diagnose_web.py` 诊断问题
2. 运行 `install_dependencies.py` 安装依赖
3. 运行 `fix_tqdm.py` 修复依赖问题
4. 检查 Web UI 服务器是否正常运行
5. 查看日志文件获取详细错误信息 