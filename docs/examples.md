# 使用示例

本文档提供了DY下载器的详细使用示例，帮助你更好地使用工具。

## 基本使用

### 1. 启动Web界面

```bash
# 方法一：直接启动
python app.py

# 方法二：使用启动脚本
python script/quick_start.py

# 方法三：使用UI目录下的脚本
cd ui
python run_web.py
```

### 2. 访问界面

启动后访问：`http://localhost:5000`

## 配置示例

### 基本配置

```yaml
# settings/config.yml
link:
  - "https://www.douyin.com/user/MS4wLjABAAAAxxxxx"
  - "https://v.douyin.com/xxxxx/"

path: "./Downloaded/"
music: true
cover: true
avatar: true
json: true
folderstyle: false

mode: ["post", "mix"]

number:
  post: 10
  like: 0
  allmix: 0
  mix: 0
  music: 0

database: true
thread: 5

cookies:
  msToken: "your_ms_token"
  ttwid: "your_ttwid"
  odin_tt: "your_odin_tt"
```

### 高级配置

```yaml
# 增量下载配置
increase:
  post: true
  like: false
  allmix: true
  mix: true
  music: false

# 下载路径配置
path: "/path/to/download/folder"

# 线程配置
thread: 10

# Cookie配置
cookies:
  msToken: "your_ms_token"
  ttwid: "your_ttwid"
  odin_tt: "your_odin_tt"
  passport_csrf_token: "your_csrf_token"
  sid_guard: "your_sid_guard"
```

## 链接格式示例

### 用户主页链接

```
https://www.douyin.com/user/MS4wLjABAAAAxxxxx
```

### 视频链接

```
https://v.douyin.com/xxxxx/
https://www.douyin.com/video/xxxxx
```

### 合集链接

```
https://www.douyin.com/collection/xxxxx
```

## 使用场景

### 场景1：下载用户所有作品

1. 获取用户主页链接
2. 配置下载选项：
   - 音乐：开启
   - 封面：开启
   - 头像：开启
   - JSON：开启
3. 设置下载模式：发布作品
4. 设置下载数量：0（全部下载）
5. 开始下载

### 场景2：下载用户喜欢的作品

1. 获取用户主页链接
2. 配置下载选项
3. 设置下载模式：喜欢作品
4. 设置下载数量限制
5. 开始下载

### 场景3：下载合集内容

1. 获取合集链接
2. 配置下载选项
3. 设置下载模式：合集
4. 设置下载数量
5. 开始下载

### 场景4：增量下载

1. 配置增量下载选项
2. 启用数据库功能
3. 运行下载任务
4. 后续运行时会自动跳过已下载的内容

## 常见问题解决

### 问题1：下载失败

**原因**：Cookie过期或无效
**解决**：
1. 重新获取Cookie
2. 更新配置文件中的Cookie信息

### 问题2：下载速度慢

**原因**：线程数设置过低
**解决**：
1. 增加线程数设置
2. 检查网络连接

### 问题3：文件重复下载

**原因**：未启用增量下载
**解决**：
1. 启用数据库功能
2. 配置增量下载选项

### 问题4：文件路径错误

**原因**：路径配置不正确
**解决**：
1. 检查路径是否存在
2. 确保有写入权限
3. 使用绝对路径

## 高级技巧

### 1. 批量下载

```yaml
link:
  - "https://www.douyin.com/user/user1"
  - "https://www.douyin.com/user/user2"
  - "https://www.douyin.com/user/user3"
```

### 2. 分类下载

```yaml
# 只下载视频
music: false
cover: false
avatar: false
json: true

# 只下载音乐
music: true
cover: false
avatar: false
json: false
```

### 3. 限制下载数量

```yaml
number:
  post: 5    # 只下载5个发布作品
  like: 10   # 只下载10个喜欢作品
  mix: 3     # 只下载3个合集
```

### 4. 优化性能

```yaml
# 增加线程数
thread: 10

# 启用增量下载
database: true
increase:
  post: true
  like: true
  mix: true
```

## 监控和日志

### 查看下载进度

在Web界面中实时查看：
- 下载进度百分比
- 已下载文件数量
- 当前处理的链接
- 下载速度

### 查看日志

```bash
# 查看实时日志
tail -f logs/douyin.log

# 查看错误日志
grep "ERROR" logs/douyin.log

# 查看下载完成日志
grep "下载完成" logs/douyin.log
```

## 故障排除

### 1. 检查配置

```bash
# 验证配置文件格式
python -c "import yaml; yaml.safe_load(open('settings/config.yml'))"
```

### 2. 检查依赖

```bash
# 安装依赖
pip install -r requirements.txt

# 检查ffmpeg
ffmpeg -version
```

### 3. 检查权限

```bash
# 检查下载目录权限
ls -la ./Downloaded/

# 检查日志目录权限
ls -la ./logs/
```

### 4. 网络检查

```bash
# 测试网络连接
ping www.douyin.com

# 测试API连接
curl -I https://www.douyin.com
```

## 最佳实践

### 1. 配置管理

- 定期备份配置文件
- 使用版本控制管理配置
- 为不同环境创建不同配置

### 2. 性能优化

- 根据网络情况调整线程数
- 启用增量下载避免重复下载
- 定期清理日志文件

### 3. 监控和维护

- 定期检查下载目录空间
- 监控日志文件大小
- 及时更新Cookie信息

### 4. 安全考虑

- 不要在配置文件中存储敏感信息
- 定期更新依赖包
- 使用防火墙保护服务

## 扩展使用

### 1. 自动化脚本

```bash
#!/bin/bash
# 自动下载脚本
cd /path/to/dy-downloader
python app.py &
sleep 5
# 添加下载任务
curl -X POST http://localhost:5000/api/download/start \
  -H "Content-Type: application/json" \
  -d '{"config": {...}}'
```

### 2. 定时任务

```bash
# crontab 示例
0 2 * * * cd /path/to/dy-downloader && python app.py
```

### 3. 监控脚本

```bash
#!/bin/bash
# 监控下载状态
while true; do
  status=$(curl -s http://localhost:5000/api/download/status)
  echo "$(date): $status"
  sleep 60
done
```

这些示例涵盖了DY下载器的主要使用场景和高级功能，帮助你更好地使用这个工具。 