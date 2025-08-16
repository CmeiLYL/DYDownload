#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import yaml
import shutil
import logging
import threading
import subprocess
import queue
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import io
import mimetypes
import hashlib
import tempfile
import re # Added for video preview API
import time # Added for retry logic

# 配置日志
def setup_logging():
    """设置日志配置"""
    # 确保logs目录存在
    os.makedirs('logs', exist_ok=True)
    
    # 创建logger
    logger = logging.getLogger('douyin_web')
    logger.setLevel(logging.INFO)
    
    # 创建文件处理器
    file_handler = logging.FileHandler('logs/douyin.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 创建格式器
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 设置格式器
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# 初始化日志
logger = setup_logging()

app = Flask(__name__)
CORS(app)

# 全局变量
config_file = "config.yml"
download_queue = queue.Queue()
download_status = {"running": False, "current_task": None, "progress": 0}

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path="config.yml"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                logger.info(f"成功加载配置文件: {self.config_path}")
                return config
            else:
                logger.info("配置文件不存在，使用默认配置")
                return self.get_default_config()
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return self.get_default_config()
    
    def save_config(self, config_data):
        """保存配置文件"""
        try:
            # 备份原配置文件
            if self.config_path.exists():
                backup_path = self.config_path.with_suffix('.yml.backup')
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    with open(backup_path, 'w', encoding='utf-8') as bf:
                        bf.write(f.read())
                logger.info(f"配置文件已备份到: {backup_path}")
            
            # 保存新配置
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            self.config = config_data
            logger.info("配置文件保存成功")
            return True
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
            return False
    
    def get_default_config(self):
        """获取默认配置"""
        return {
            "link": [],
            "path": "./Downloaded/",
            "music": False,
            "cover": False,
            "avatar": False,
            "json": False,
            "folderstyle": False,
            "mode": ["post", "mix"],
            "number": {
                "post": 0,
                "like": 0,
                "allmix": 0,
                "mix": 0,
                "music": 0
            },
            "database": True,
            "increase": {
                "post": True,
                "like": False,
                "allmix": True,
                "mix": True,
                "music": False
            },
            "thread": 5,
            "cookies": {}
        }

# 视频缩略图管理类
class VideoThumbnailManager:
    def __init__(self, download_path='./Downloaded/'):
        # 确保使用绝对路径
        self.download_path = Path(download_path).resolve()
        self.cache_dir = self.download_path / 'temp' / 'thumbnails'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ffmpeg_available = self._check_ffmpeg()
        self.generation_queue = queue.Queue()
        self.is_generating = False
        
        logger.info(f"视频缩略图缓存目录: {self.cache_dir}")
        if self.ffmpeg_available:
            logger.info("✓ ffmpeg 可用，支持视频缩略图生成")
            # 启动后台生成线程
            self.start_background_generator()
        else:
            logger.warning("⚠ ffmpeg 不可用，视频缩略图功能将不可用")
    
    def _check_ffmpeg(self):
        """检查ffmpeg是否可用"""
        try:
            result = self._execute_ffmpeg_safe(['ffmpeg', '-version'], timeout=5)
            return result is not None and result.returncode == 0
        except Exception as e:
            logger.error(f"检查ffmpeg失败: {e}")
            return False
    
    def start_background_generator(self):
        """启动后台缩略图生成线程"""
        if not self.ffmpeg_available:
            return
            
        def background_generator():
            while True:
                try:
                    # 从队列中获取视频路径
                    video_path = self.generation_queue.get(timeout=1)
                    if video_path is None:  # 停止信号
                        break
                    
                    self._generate_thumbnail_sync(video_path)
                    self.generation_queue.task_done()
                    
                except queue.Empty:
                    continue
                except Exception as e:
                    logger.error(f"后台缩略图生成出错: {e}")
        
        self.generator_thread = threading.Thread(target=background_generator, daemon=True)
        self.generator_thread.start()
        logger.info("后台缩略图生成线程已启动")
    
    def get_thumbnail_path(self, video_path):
        """获取视频缩略图缓存路径"""
        # 使用视频路径的MD5作为缓存文件名
        video_hash = hashlib.md5(video_path.encode()).hexdigest()
        return self.cache_dir / f"{video_hash}.jpg"
    
    def request_thumbnail_generation(self, video_path):
        """请求生成缩略图（异步）"""
        if not self.ffmpeg_available:
            return False
        
        try:
            video_full_path = self.download_path / video_path
            if not video_full_path.exists():
                logger.error(f"视频文件不存在: {video_full_path}")
                return False
            
            thumbnail_path = self.get_thumbnail_path(video_path)
            
            # 如果缩略图已存在且较新，不需要重新生成
            if thumbnail_path.exists():
                video_mtime = video_full_path.stat().st_mtime
                thumb_mtime = thumbnail_path.stat().st_mtime
                if thumb_mtime > video_mtime:
                    logger.debug(f"缩略图已存在且较新: {thumbnail_path}")
                    return True
            
            # 添加到生成队列
            self.generation_queue.put(video_path)
            logger.info(f"已添加到缩略图生成队列: {video_path}")
            return True
            
        except Exception as e:
            logger.error(f"请求缩略图生成失败: {e}")
            return False
    
    def _generate_thumbnail_sync(self, video_path):
        """同步生成缩略图（在后台线程中调用）"""
        try:
            video_full_path = self.download_path / video_path
            thumbnail_path = self.get_thumbnail_path(video_path)
            
            logger.info(f"开始生成视频缩略图: {video_path}")
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_thumb_path = temp_file.name
            
            try:
                # 使用ffmpeg提取第1秒的帧
                cmd = [
                    'ffmpeg', '-i', str(video_full_path),
                    '-ss', '00:00:01',  # 从第1秒开始
                    '-vframes', '1',    # 提取1帧
                    '-vf', 'scale=200:150:force_original_aspect_ratio=decrease,pad=200:150:(ow-iw)/2:(oh-ih)/2',  # 缩放到200x150
                    '-y',  # 覆盖输出文件
                    temp_thumb_path
                ]
                
                logger.debug(f"执行ffmpeg命令: {' '.join(cmd)}")
                result = self._execute_ffmpeg_safe(cmd)
                
                if result and result.returncode == 0 and os.path.exists(temp_thumb_path):
                    # 移动到缓存目录
                    shutil.move(temp_thumb_path, thumbnail_path)
                    logger.info(f"视频缩略图生成成功: {thumbnail_path}")
                    return True
                else:
                    logger.error(f"ffmpeg执行失败: {result.stderr if result else '未知错误'}")
                    return False
                    
            except subprocess.TimeoutExpired:
                logger.error(f"ffmpeg执行超时: {video_path}")
                return False
            except FileNotFoundError:
                logger.error(f"ffmpeg未找到，请安装ffmpeg")
                self.ffmpeg_available = False
                return False
            except Exception as e:
                logger.error(f"生成视频缩略图失败: {e}")
                return False
            finally:
                # 清理临时文件
                if os.path.exists(temp_thumb_path):
                    try:
                        os.unlink(temp_thumb_path)
                    except:
                        pass
                    
        except Exception as e:
            logger.error(f"处理视频缩略图失败: {e}")
            return False
    
    def get_thumbnail_status(self, video_path):
        """获取缩略图状态"""
        try:
            video_full_path = self.download_path / video_path
            if not video_full_path.exists():
                return "file_not_found"
            
            thumbnail_path = self.get_thumbnail_path(video_path)
            
            if thumbnail_path.exists():
                video_mtime = video_full_path.stat().st_mtime
                thumb_mtime = thumbnail_path.stat().st_mtime
                if thumb_mtime > video_mtime:
                    return "ready"
                else:
                    return "outdated"
            else:
                return "not_generated"
                
        except Exception as e:
            logger.error(f"获取缩略图状态失败: {e}")
            return "error"
    
    def cleanup_old_thumbnails(self, max_age_days=30):
        """清理旧的缩略图缓存"""
        try:
            cutoff_time = datetime.now().timestamp() - (max_age_days * 24 * 3600)
            cleaned_count = 0
            
            for thumb_file in self.cache_dir.glob('*.jpg'):
                if thumb_file.stat().st_mtime < cutoff_time:
                    thumb_file.unlink()
                    cleaned_count += 1
            
            if cleaned_count > 0:
                logger.info(f"清理了 {cleaned_count} 个旧缩略图")
                
        except Exception as e:
            logger.error(f"清理缩略图缓存失败: {e}")

    def _execute_ffmpeg_safe(self, cmd, timeout=30):
        """安全执行ffmpeg命令，处理编码问题"""
        try:
            # 尝试使用UTF-8编码
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                encoding='utf-8',
                errors='ignore'
            )
            return result
        except UnicodeDecodeError:
            # 如果UTF-8失败，尝试使用系统默认编码
            try:
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=timeout,
                    errors='ignore'
                )
                return result
            except Exception as e:
                logger.error(f"ffmpeg执行编码错误: {e}")
                return None
        except Exception as e:
            logger.error(f"ffmpeg执行失败: {e}")
            return None

# 初始化缩略图管理器
thumbnail_manager = VideoThumbnailManager()

def get_user_info_from_link(link):
    """从链接中获取用户信息"""
    try:
        logger.info(f"开始解析链接: {link}")
        
        # 导入抖音API
        from apiproxy.douyin.douyin import Douyin
        from apiproxy.common import utils
        
        dy = Douyin()
        key_type, key = dy.getKey(link)
        
        if key_type == "user" and key:
            # 获取用户详细信息
            data = dy.getUserDetailInfo(sec_uid=key)
            if data and data.get('user'):
                nickname = utils.replaceStr(data['user']['nickname'])
                logger.info(f"成功获取用户信息: {nickname} (用户ID: {key})")
                return {
                    "success": True,
                    "nickname": nickname,
                    "sec_uid": key,
                    "link_type": "user"
                }
        elif key_type == "aweme" and key:
            # 获取视频信息
            aweme_info = dy.getAwemeInfo(key)
            if aweme_info and aweme_info.get('author'):
                nickname = utils.replaceStr(aweme_info['author']['nickname'])
                logger.info(f"成功获取视频信息: {nickname} (视频ID: {key})")
                return {
                    "success": True,
                    "nickname": nickname,
                    "aweme_id": key,
                    "link_type": "video"
                }
        elif key_type == "mix" and key:
            # 获取合集信息
            mix_info = dy.getMixInfo(key, 1, 1, False)
            if mix_info and mix_info[0].get('mix_info'):
                mix_name = utils.replaceStr(mix_info[0]['mix_info']['mix_name'])
                logger.info(f"成功获取合集信息: {mix_name} (合集ID: {key})")
                return {
                    "success": True,
                    "nickname": mix_name,
                    "mix_id": key,
                    "link_type": "mix"
                }
        
        logger.warning(f"无法解析链接或获取用户信息: {link}")
        return {
            "success": False,
            "message": "无法解析链接或获取用户信息"
        }
        
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        return {
            "success": False,
            "message": f"获取用户信息失败: {str(e)}"
        }

# 初始化配置管理器
config_manager = ConfigManager()

@app.route('/')
def index():
    """首页"""
    logger.info("访问首页")
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取配置"""
    logger.info("获取配置")
    return jsonify(config_manager.config)

@app.route('/api/config', methods=['POST'])
def update_config():
    """更新配置"""
    try:
        data = request.get_json()
        logger.info("更新配置")
        if config_manager.save_config(data):
            return jsonify({"success": True, "message": "配置保存成功"})
        else:
            return jsonify({"success": False, "message": "配置保存失败"}), 500
    except Exception as e:
        logger.error(f"更新配置失败: {e}")
        return jsonify({"success": False, "message": f"更新配置失败: {str(e)}"}), 500

@app.route('/api/link/parse', methods=['POST'])
def parse_link():
    """解析链接并获取用户信息"""
    try:
        data = request.get_json()
        link = data.get('link', '').strip()
        
        if not link:
            logger.warning("链接为空")
            return jsonify({"success": False, "message": "链接不能为空"})
        
        logger.info(f"解析链接: {link}")
        user_info = get_user_info_from_link(link)
        return jsonify(user_info)
        
    except Exception as e:
        logger.error(f"解析链接失败: {e}")
        return jsonify({"success": False, "message": f"解析链接失败: {str(e)}"}), 500

@app.route('/api/download/start', methods=['POST'])
def start_download():
    """开始下载"""
    try:
        data = request.get_json()
        
        if download_status["running"]:
            logger.warning("已有下载任务正在运行")
            return jsonify({"success": False, "message": "已有下载任务正在运行"}), 400
        
        logger.info("开始下载任务")
        
        # 更新配置
        if not config_manager.save_config(data.get('config', config_manager.config)):
            return jsonify({"success": False, "message": "配置保存失败"}), 500
        
        # 启动下载线程
        download_status["running"] = True
        download_status["current_task"] = "准备下载..."
        download_status["progress"] = 0
        
        download_thread = threading.Thread(target=run_download, args=(data,))
        download_thread.daemon = True
        download_thread.start()
        
        logger.info("下载任务已启动")
        return jsonify({"success": True, "message": "下载任务已启动"})
    except Exception as e:
        logger.error(f"启动下载失败: {e}")
        return jsonify({"success": False, "message": f"启动下载失败: {str(e)}"}), 500

@app.route('/api/download/status', methods=['GET'])
def get_download_status():
    """获取下载状态"""
    return jsonify(download_status)

@app.route('/api/download/stop', methods=['POST'])
def stop_download():
    """停止下载"""
    logger.info("停止下载任务")
    download_status["running"] = False
    download_status["current_task"] = "已停止"
    return jsonify({"success": True, "message": "下载已停止"})

def run_download(data):
    """运行下载任务"""
    try:
        logger.info("开始执行下载任务")
        config = data.get('config', config_manager.config)
        
        # 检查是否有链接
        links = config.get('link', [])
        if not links:
            logger.error("没有配置下载链接")
            download_status["current_task"] = "错误：没有配置下载链接"
            return
        
        logger.info(f"开始下载 {len(links)} 个链接")
        
        # 更新下载路径
        download_path = Path(config.get('path', './Downloaded/')).resolve()
        download_path.mkdir(parents=True, exist_ok=True)
        
        download_status["current_task"] = "正在初始化下载..."
        download_status["progress"] = 5
        logger.info(f"下载路径: {download_path}")
        
        # 导入DouYinCommand模块
        try:
            import DouYinCommand
            logger.info("✓ 成功导入DouYinCommand模块")
        except ImportError as e:
            logger.error(f"✗ 导入DouYinCommand模块失败: {e}")
            download_status["current_task"] = "错误：无法导入DouYinCommand模块"
            return
        
        # 更新DouYinCommand的配置
        try:
            # 更新全局配置
            DouYinCommand.configModel["link"] = links
            DouYinCommand.configModel["path"] = str(download_path)
            DouYinCommand.configModel["music"] = config.get('music', True)
            DouYinCommand.configModel["cover"] = config.get('cover', True)
            DouYinCommand.configModel["avatar"] = config.get('avatar', True)
            DouYinCommand.configModel["json"] = config.get('json', True)
            DouYinCommand.configModel["folderstyle"] = config.get('folderstyle', True)
            DouYinCommand.configModel["mode"] = config.get('mode', ['post'])
            DouYinCommand.configModel["thread"] = config.get('thread', 5)
            DouYinCommand.configModel["database"] = config.get('database', True)
            
            # 更新数量限制
            numbers = config.get('number', {})
            DouYinCommand.configModel["number"]["post"] = numbers.get('post', 0)
            DouYinCommand.configModel["number"]["like"] = numbers.get('like', 0)
            DouYinCommand.configModel["number"]["allmix"] = numbers.get('allmix', 0)
            DouYinCommand.configModel["number"]["mix"] = numbers.get('mix', 0)
            DouYinCommand.configModel["number"]["music"] = numbers.get('music', 0)
            
            # 更新增量下载设置
            increase = config.get('increase', {})
            DouYinCommand.configModel["increase"]["post"] = increase.get('post', False)
            DouYinCommand.configModel["increase"]["like"] = increase.get('like', False)
            DouYinCommand.configModel["increase"]["allmix"] = increase.get('allmix', False)
            DouYinCommand.configModel["increase"]["mix"] = increase.get('mix', False)
            DouYinCommand.configModel["increase"]["music"] = increase.get('music', False)
            
            # 设置Cookie
            cookies = config.get('cookies', {})
            if cookies:
                cookie_str = "; ".join(f"{k}={v}" for k, v in cookies.items())
                DouYinCommand.configModel["cookie"] = cookie_str
                logger.info("✓ 已设置Cookie")
            
            logger.info("✓ 成功更新配置")
        except Exception as e:
            logger.error(f"✗ 更新配置失败: {e}")
            download_status["current_task"] = "错误：配置更新失败"
            return
        
        # 开始下载
        try:
            download_status["current_task"] = "正在启动下载..."
            download_status["progress"] = 10
            logger.info("正在启动DouYinCommand下载...")
            
            # 调用DouYinCommand的main函数
            DouYinCommand.main()
            
            download_status["current_task"] = "✓ 下载完成"
            download_status["progress"] = 100
            logger.info("✓ DouYinCommand下载完成")
            
        except Exception as e:
            logger.error(f"✗ DouYinCommand下载失败: {e}")
            download_status["current_task"] = f"✗ 下载失败: {str(e)}"
        
    except Exception as e:
        logger.error(f"✗ 下载过程出错: {e}")
        download_status["current_task"] = f"✗ 下载失败: {str(e)}"
    finally:
        download_status["running"] = False
        logger.info("下载任务结束")

@app.route('/api/files', methods=['GET'])
def get_downloaded_files():
    """获取已下载的文件列表"""
    try:
        download_path = Path(config_manager.config.get('path', './Downloaded/')).resolve()
        if not download_path.exists():
            logger.info("下载目录不存在")
            return jsonify([])
        
        files = []
        for item in download_path.rglob('*'):
            if item.is_file():
                # 排除temp文件夹中的文件
                if 'temp' in item.parts:
                    continue
                    
                files.append({
                    'name': item.name,
                    'path': str(item.relative_to(download_path)),
                    'size': item.stat().st_size,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                })
        
        logger.info(f"获取到 {len(files)} 个文件（已排除temp文件夹）")
        return jsonify(files)
    except Exception as e:
        logger.error(f"获取文件列表失败: {e}")
        return jsonify([])

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """获取日志"""
    try:
        log_file = Path("logs/douyin.log")
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = f.readlines()[-100:]  # 获取最后100行
            logger.info(f"获取到 {len(logs)} 条日志")
            return jsonify(logs)
        else:
            logger.info("日志文件不存在")
            return jsonify([])
    except Exception as e:
        logger.error(f"获取日志失败: {e}")
        return jsonify([])

@app.route('/api/file/thumbnail', methods=['GET'])
def get_file_thumbnail():
    """获取文件缩略图"""
    try:
        file_path = request.args.get('path', '')
        if not file_path:
            logger.error("缩略图API: 文件路径为空")
            return jsonify({"error": "文件路径不能为空"}), 400
        
        logger.info(f"缩略图API: 开始处理请求，路径: {file_path}")
        
        # 构建完整文件路径
        download_path = Path(config_manager.config.get('path', './Downloaded/')).resolve()
        # 修复路径分隔符问题
        file_path = file_path.replace('\\', '/')
        full_path = download_path / file_path
        
        logger.info(f"缩略图API: 下载路径: {download_path}")
        logger.info(f"缩略图API: 原始文件路径: {file_path}")
        logger.info(f"缩略图API: 完整文件路径: {full_path}")
        
        if not full_path.exists():
            logger.error(f"缩略图API: 文件不存在: {full_path}")
            return jsonify({"error": "文件不存在"}), 404
        
        # 检查文件类型
        file_ext = full_path.suffix.lower()
        
        # 处理图片文件
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            logger.info("缩略图API: 处理图片文件")
            try:
                with Image.open(full_path) as img:
                    # 转换为RGB模式（处理RGBA等）
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    # 计算缩略图尺寸
                    max_size = (200, 150)
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # 保存到内存
                    img_io = io.BytesIO()
                    img.save(img_io, 'JPEG', quality=85)
                    img_io.seek(0)
                    
                    logger.info(f"缩略图API: 生成图片缩略图成功: {file_path}")
                    return send_file(img_io, mimetype='image/jpeg')
                    
            except Exception as e:
                logger.error(f"缩略图API: 生成图片缩略图失败: {e}")
                return jsonify({"error": "生成图片缩略图失败"}), 500
        
        # 处理视频文件
        elif file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm']:
            logger.info("缩略图API: 处理视频文件")
            try:
                # 检查缩略图状态
                status = thumbnail_manager.get_thumbnail_status(file_path)
                logger.info(f"缩略图API: 视频缩略图状态: {status}")
                
                if status == "ready":
                    # 缩略图已存在，直接返回
                    thumbnail_path = thumbnail_manager.get_thumbnail_path(file_path)
                    logger.info(f"缩略图API: 返回现有视频缩略图: {thumbnail_path}")
                    return send_file(thumbnail_path, mimetype='image/jpeg')
                
                elif status in ["not_generated", "outdated"]:
                    # 请求后台生成缩略图
                    if thumbnail_manager.request_thumbnail_generation(file_path):
                        logger.info(f"缩略图API: 已请求后台生成视频缩略图: {file_path}")
                        # 返回默认图标或占位符
                        return jsonify({
                            "status": "generating",
                            "message": "缩略图正在后台生成中"
                        }), 202
                    else:
                        logger.error(f"缩略图API: 请求视频缩略图生成失败: {file_path}")
                        return jsonify({"error": "无法生成视频缩略图"}), 500
                
                else:
                    logger.error(f"缩略图API: 视频文件状态异常: {status}")
                    return jsonify({"error": "视频文件状态异常"}), 500
                    
            except Exception as e:
                logger.error(f"缩略图API: 处理视频缩略图失败: {e}")
                return jsonify({"error": "处理视频缩略图失败"}), 500
        
        else:
            logger.error(f"缩略图API: 不支持的文件类型: {file_ext}")
            return jsonify({"error": "不支持的文件类型"}), 400
            
    except Exception as e:
        logger.error(f"缩略图API: 获取缩略图失败: {e}")
        return jsonify({"error": "获取缩略图失败"}), 500

@app.route('/api/file/thumbnail/status', methods=['GET'])
def get_thumbnail_status():
    """获取缩略图生成状态"""
    try:
        file_path = request.args.get('path', '')
        if not file_path:
            return jsonify({"error": "文件路径不能为空"}), 400
        
        # 检查文件类型
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm']:
            status = thumbnail_manager.get_thumbnail_status(file_path)
            return jsonify({
                "status": status,
                "path": file_path
            })
        else:
            return jsonify({
                "status": "not_video",
                "message": "不是视频文件"
            })
            
    except Exception as e:
        logger.error(f"获取缩略图状态失败: {e}")
        return jsonify({"error": "获取缩略图状态失败"}), 500

@app.route('/api/file/preview', methods=['GET'])
def preview_file():
    """预览文件（视频或图片）"""
    try:
        file_path = request.args.get('path', '')
        if not file_path:
            logger.error("预览API: 文件路径为空")
            return jsonify({"error": "文件路径不能为空"}), 400
        
        logger.info(f"预览API: 开始处理请求，路径: {file_path}")
        
        # 构建完整文件路径
        download_path = Path(config_manager.config.get('path', './Downloaded/')).resolve()
        # 修复路径分隔符问题
        file_path = file_path.replace('\\', '/')
        full_path = download_path / file_path
        
        logger.info(f"预览API: 下载路径: {download_path}")
        logger.info(f"预览API: 原始文件路径: {file_path}")
        logger.info(f"预览API: 完整文件路径: {full_path}")
        
        if not full_path.exists():
            logger.error(f"预览API: 文件不存在: {full_path}")
            return jsonify({"error": "文件不存在"}), 404
        
        # 检查文件类型
        file_ext = full_path.suffix.lower()
        logger.info(f"预览API: 文件扩展名: {file_ext}")
        
        # 支持的文件类型
        supported_types = {
            # 视频文件
            '.mp4': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.mov': 'video/quicktime',
            '.mkv': 'video/x-matroska',
            '.flv': 'video/x-flv',
            '.webm': 'video/webm',
            # 图片文件
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp'
        }
        
        if file_ext not in supported_types:
            logger.error(f"预览API: 不支持的文件类型: {file_ext}")
            return jsonify({"error": "不支持的文件类型"}), 400
        
        # 获取MIME类型
        mime_type = supported_types[file_ext]
        logger.info(f"预览API: MIME类型: {mime_type}")
        
        # 获取文件大小
        file_size = full_path.stat().st_size
        logger.info(f"预览API: 文件大小: {file_size} bytes")
        
        logger.info(f"预览API: 预览文件: {file_path} (类型: {mime_type})")
        
        # 对于视频文件，支持范围请求（Range requests）
        if file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm']:
            logger.info("预览API: 处理视频文件")
            response = send_file(
                full_path, 
                mimetype=mime_type,
                as_attachment=False,
                conditional=True  # 启用条件请求支持
            )
            
            # 添加必要的响应头以确保视频正确播放
            response.headers['Accept-Ranges'] = 'bytes'
            response.headers['Cache-Control'] = 'public, max-age=3600'
            response.headers['Content-Disposition'] = 'inline'
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Range, Accept-Ranges, Content-Range'
            
            # 对于MP4文件，添加特殊的响应头
            if file_ext == '.mp4':
                response.headers['Content-Type'] = 'video/mp4'
                response.headers['X-Content-Type-Options'] = 'nosniff'
            
            logger.info("预览API: 视频文件处理完成")
            return response
        else:
            logger.info("预览API: 处理图片文件")
            # 对于图片文件，直接返回
            response = send_file(
                full_path, 
                mimetype=mime_type,
                as_attachment=False
            )
            logger.info("预览API: 图片文件处理完成")
            return response
        
    except Exception as e:
        logger.error(f"预览API: 预览文件失败: {e}")
        return jsonify({"error": "预览文件失败"}), 500

@app.route('/api/file/video', methods=['GET'])
def serve_video():
    """专门用于视频文件的API"""
    try:
        file_path = request.args.get('path', '')
        if not file_path:
            logger.error("视频API: 文件路径为空")
            return jsonify({"error": "文件路径不能为空"}), 400
        
        logger.info(f"视频API: 开始处理请求，路径: {file_path}")
        
        # 构建完整文件路径
        download_path = Path(config_manager.config.get('path', './Downloaded/')).resolve()
        # 修复路径分隔符问题
        file_path = file_path.replace('\\', '/')
        full_path = download_path / file_path
        
        logger.info(f"视频API: 下载路径: {download_path}")
        logger.info(f"视频API: 原始文件路径: {file_path}")
        logger.info(f"视频API: 完整文件路径: {full_path}")
        
        if not full_path.exists():
            logger.error(f"视频API: 文件不存在: {full_path}")
            return jsonify({"error": "文件不存在"}), 404
        
        # 检查文件类型
        file_ext = full_path.suffix.lower()
        logger.info(f"视频API: 文件扩展名: {file_ext}")
        
        if file_ext not in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm']:
            logger.error(f"视频API: 不支持的文件类型: {file_ext}")
            return jsonify({"error": "不是视频文件"}), 400
        
        # 获取文件大小
        file_size = full_path.stat().st_size
        logger.info(f"视频API: 文件大小: {file_size} bytes")
        
        # 处理Range请求
        range_header = request.headers.get('Range', None)
        logger.info(f"视频API: Range请求头: {range_header}")
        
        if range_header:
            logger.info("视频API: 处理Range请求")
            byte1, byte2 = 0, None
            m = re.search('(\d+)-(\d*)', range_header)
            if m:
                g = m.groups()
                
                if g[0]: byte1 = int(g[0])
                if g[1]: byte2 = int(g[1])
                
                if byte2 is None:
                    byte2 = file_size - 1
                
                length = byte2 - byte1 + 1
                
                logger.info(f"视频API: Range请求 - 开始字节: {byte1}, 结束字节: {byte2}, 长度: {length}")
                
                try:
                    with open(full_path, 'rb') as f:
                        f.seek(byte1)
                        data = f.read(length)
                    
                    logger.info(f"视频API: 成功读取Range数据，实际读取: {len(data)} bytes")
                    
                    response = app.response_class(
                        data,
                        206,
                        mimetype='video/mp4',
                        direct_passthrough=True
                    )
                    
                    response.headers.add('Content-Range', f'bytes {byte1}-{byte2}/{file_size}')
                    response.headers.add('Accept-Ranges', 'bytes')
                    response.headers.add('Content-Length', str(length))
                    response.headers.add('Cache-Control', 'public, max-age=3600')
                    response.headers.add('Content-Disposition', 'inline')
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
                    response.headers['Access-Control-Allow-Headers'] = 'Range, Accept-Ranges, Content-Range'
                    
                    # For MP4 files, add specific headers
                    if file_ext == '.mp4':
                        response.headers['Content-Type'] = 'video/mp4'
                        response.headers['X-Content-Type-Options'] = 'nosniff'
                    
                    logger.info(f"视频API: Range请求成功，状态码: 206")
                    return response
                    
                except Exception as e:
                    logger.error(f"视频API: Range请求读取文件失败: {e}")
                    return jsonify({"error": "读取文件失败"}), 500
            else:
                logger.error(f"视频API: Range请求格式无效: {range_header}")
                return jsonify({"error": "Range请求格式无效"}), 400
        else:
            logger.info("视频API: 处理完整文件请求")
            try:
                # 完整文件请求
                with open(full_path, 'rb') as f:
                    data = f.read()
                
                logger.info(f"视频API: 成功读取完整文件，大小: {len(data)} bytes")
                
                response = app.response_class(
                    data,
                    200,
                    mimetype='video/mp4',
                    direct_passthrough=True
                )
                
                response.headers.add('Accept-Ranges', 'bytes')
                response.headers.add('Content-Length', str(file_size))
                response.headers.add('Cache-Control', 'public, max-age=3600')
                response.headers.add('Content-Disposition', 'inline')
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Range, Accept-Ranges, Content-Range'
                
                # For MP4 files, add specific headers
                if file_ext == '.mp4':
                    response.headers['Content-Type'] = 'video/mp4'
                    response.headers['X-Content-Type-Options'] = 'nosniff'
                
                logger.info(f"视频API: 完整文件请求成功，状态码: 200")
                return response
                
            except Exception as e:
                logger.error(f"视频API: 完整文件请求读取失败: {e}")
                return jsonify({"error": "读取文件失败"}), 500
            
    except Exception as e:
        logger.error(f"视频API: 处理请求时发生异常: {e}")
        return jsonify({"error": "视频服务失败"}), 500

if __name__ == '__main__':
    # 确保必要的目录存在
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    logger.info("Web UI 启动中...")
    app.run(debug=True, host='0.0.0.0', port=5000) 