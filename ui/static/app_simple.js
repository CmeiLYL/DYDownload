// 文件管理相关变量
let fileAllFiles = [];
let fileFilteredFiles = [];
let fileCurrentPage = 1;
let fileItemsPerPage = 15;
let fileSources = new Set();

// 刷新文件列表
async function fileRefreshFiles() {
    try {
        console.log('开始获取文件列表...');
        const response = await fetch('/api/files');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const files = await response.json();
        console.log(`成功获取 ${files.length} 个文件`);
        
        // 处理文件数据
        fileAllFiles = files.map(file => {
            const fileInfo = {
                ...file,
                fileType: fileGetFileType(file.name),
                source: fileExtractSourceFromPath(file.path)
            };
            return fileInfo;
        });
        
        // 收集文件来源
        fileSources.clear();
        fileAllFiles.forEach(file => {
            if (file.source && file.source !== '未知来源') {
                fileSources.add(file.source);
            }
        });
        
        console.log(`发现 ${fileSources.size} 个文件来源:`, Array.from(fileSources));
        
        fileUpdateSourceFilter();
        fileFilterFiles();
        document.getElementById('totalFiles').textContent = fileAllFiles.length;
        
        console.log('文件列表刷新完成');
    } catch (error) {
        console.error('获取文件列表失败:', error);
        fileShowError(`获取文件列表失败: ${error.message}`);
    }
}

// 获取文件类型
function fileGetFileType(filename) {
    const ext = fileGetFileExtension(filename).toLowerCase();
    if (['mp4', 'avi', 'mov', 'mkv', 'flv', 'webm'].includes(ext)) return 'video';
    if (['mp3', 'wav', 'aac', 'flac', 'm4a'].includes(ext)) return 'audio';
    if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(ext)) return 'image';
    if (['json', 'txt', 'log'].includes(ext)) return 'data';
    return 'other';
}

// 从路径提取来源
function fileExtractSourceFromPath(path) {
    try {
        // 处理Windows和Unix路径分隔符
        const normalizedPath = path.replace(/\\/g, '/');
        const parts = normalizedPath.split('/');
        
        // 查找包含用户信息的目录
        for (let i = 0; i < parts.length; i++) {
            const part = parts[i];
            // 检查是否是用户目录（通常包含用户ID或特殊标识）
            if (part && part !== '.' && part !== '..' && 
                (part.includes('user_') || part.includes('MS4w') || 
                 part.includes('合集') || part.includes('用户') ||
                 part.length > 10)) {
                return part;
            }
        }
        
        // 如果没有找到特殊目录，返回第一级目录
        if (parts.length >= 2 && parts[0] && parts[0] !== '.') {
            return parts[0];
        }
        
        return '未知来源';
    } catch (error) {
        console.error('解析文件路径失败:', path, error);
        return '未知来源';
    }
}

// 更新来源筛选器
function fileUpdateSourceFilter() {
    const sourceFilter = document.getElementById('sourceFilter');
    if (!sourceFilter) {
        console.error('找不到来源筛选器元素');
        return;
    }
    
    const currentValue = sourceFilter.value;
    sourceFilter.innerHTML = '<option value="all">全部来源</option>';
    
    Array.from(fileSources).sort().forEach(source => {
        const option = document.createElement('option');
        option.value = source;
        option.textContent = source;
        sourceFilter.appendChild(option);
    });
    
    // 恢复之前的选择
    if (currentValue && Array.from(fileSources).includes(currentValue)) {
        sourceFilter.value = currentValue;
    }
}

// 筛选文件
function fileFilterFiles() {
    const typeFilter = document.getElementById('fileTypeFilter')?.value || 'all';
    const sourceFilter = document.getElementById('sourceFilter')?.value || 'all';
    const sortFilter = document.getElementById('sortFilter')?.value || 'date-desc';
    const searchInput = document.getElementById('searchInput')?.value?.toLowerCase() || '';
    
    console.log('开始筛选文件:', { typeFilter, sourceFilter, sortFilter, searchInput });
    
    fileFilteredFiles = fileAllFiles.filter(file => {
        if (typeFilter !== 'all' && file.fileType !== typeFilter) return false;
        if (sourceFilter !== 'all' && file.source !== sourceFilter) return false;
        if (searchInput && !file.name.toLowerCase().includes(searchInput)) return false;
        return true;
    });
    
    console.log(`筛选结果: ${fileFilteredFiles.length} 个文件`);
    
    fileSortFiles(sortFilter);
    fileUpdateFileStats();
    fileCurrentPage = 1;
    fileRenderFiles();
    fileUpdatePagination();
}

// 排序文件
function fileSortFiles(sortType) {
    switch (sortType) {
        case 'date-desc': fileFilteredFiles.sort((a, b) => new Date(b.modified) - new Date(a.modified)); break;
        case 'date-asc': fileFilteredFiles.sort((a, b) => new Date(a.modified) - new Date(b.modified)); break;
        case 'name-asc': fileFilteredFiles.sort((a, b) => a.name.localeCompare(b.name)); break;
        case 'name-desc': fileFilteredFiles.sort((a, b) => b.name.localeCompare(a.name)); break;
        case 'size-desc': fileFilteredFiles.sort((a, b) => b.size - a.size); break;
    }
}

// 更新统计信息
function fileUpdateFileStats() {
    const stats = {
        total: fileAllFiles.length,
        video: fileAllFiles.filter(f => f.fileType === 'video').length,
        image: fileAllFiles.filter(f => f.fileType === 'image').length,
        audio: fileAllFiles.filter(f => f.fileType === 'audio').length,
        other: fileAllFiles.filter(f => !['video', 'image', 'audio'].includes(f.fileType)).length
    };
    
    // 安全地更新统计信息
    const elements = {
        'totalFileCount': stats.total,
        'videoCount': stats.video,
        'imageCount': stats.image,
        'audioCount': stats.audio,
        'otherCount': stats.other
    };
    
    Object.entries(elements).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    });
}

// 渲染文件
function fileRenderFiles() {
    const container = document.getElementById('filesContainer');
    if (!container) {
        console.error('找不到文件容器元素');
        return;
    }
    
    container.innerHTML = '';
    
    if (fileFilteredFiles.length === 0) {
        container.innerHTML = '<div class="text-center py-5" style="grid-column: 1 / -1;"><i class="bi bi-folder-x" style="font-size: 3rem; color: #cbd5e1;"></i><p class="text-muted mt-3">没有找到符合条件的文件</p></div>';
        return;
    }
    
    const startIndex = (fileCurrentPage - 1) * fileItemsPerPage;
    const endIndex = startIndex + fileItemsPerPage;
    const currentPageFiles = fileFilteredFiles.slice(startIndex, endIndex);
    
    console.log(`渲染第 ${fileCurrentPage} 页，显示 ${currentPageFiles.length} 个文件`);
    
    currentPageFiles.forEach(file => {
        const fileCard = document.createElement('div');
        fileCard.className = 'file-card';
        
        const fileExt = fileGetFileExtension(file.name).toLowerCase();
        const isImage = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(fileExt);
        const isVideo = ['mp4', 'avi', 'mov', 'mkv', 'flv', 'webm'].includes(fileExt);
        
        let thumbnailContent = '';
        if (isImage || isVideo) {
            const imagePath = file.path.replace(/\\/g, '/');
            const thumbnailUrl = `/api/file/thumbnail?path=${encodeURIComponent(imagePath)}`;
            
            if (isVideo) {
                // 视频文件：先显示默认图标，然后检查缩略图状态
                thumbnailContent = `
                    <div class="file-thumbnail-container" data-video-path="${imagePath}">
                        <div class="file-icon video-placeholder">
                            <i class="bi bi-camera-video-fill"></i>
                            <div class="thumbnail-status">检查中...</div>
                        </div>
                    </div>
                `;
            } else {
                // 图片文件：使用懒加载
                thumbnailContent = `
                    <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 150'%3E%3Crect width='200' height='150' fill='%23f8fafc'/%3E%3C/svg%3E" 
                         data-src="${thumbnailUrl}" 
                         alt="${file.name}" 
                         class="lazy-thumbnail"
                         onerror="this.parentElement.innerHTML='<div class=\\'file-icon\\'><i class=\\'bi bi-image\\'></i></div>'"
                         onload="this.classList.add('loaded')">
                `;
            }
        } else {
            thumbnailContent = `<div class="file-icon"><i class="bi ${fileGetFileIcon(file.name)}"></i></div>`;
        }
        
        fileCard.innerHTML = `
            <div class="file-type-badge">${fileExt.toUpperCase()}</div>
            <div class="file-source-badge" title="${file.source}">${fileTruncateText(file.source, 10)}</div>
            <div class="file-thumbnail">${thumbnailContent}</div>
            <div class="file-name" title="${file.name}">${fileTruncateFileName(file.name, 20)}</div>
            <div class="file-meta">
                <span>${fileFormatFileSize(file.size)}</span>
                <span>${fileFormatDate(file.modified)}</span>
            </div>
        `;
        
        // 添加点击事件
        fileCard.onclick = (event) => {
            // 检查是否点击了缩略图（避免与懒加载冲突）
            if (event.target.closest('.file-thumbnail')) {
                return;
            }
            // 使用原文件路径进行预览
            filePreviewFile(event, file.path, fileExt);
        };
        
        // 添加右键菜单事件
        fileCard.oncontextmenu = (event) => {
            event.preventDefault();
            fileOpenFileInFolder(event, file);
        };
        
        container.appendChild(fileCard);
    });
    
    // 初始化懒加载
    fileInitLazyLoading();
    
    // 初始化视频缩略图检查
    fileInitVideoThumbnailCheck();
}

// 视频缩略图状态检查
function fileInitVideoThumbnailCheck() {
    // 延迟一点时间再开始检查，避免页面加载时阻塞
    setTimeout(() => {
        fileCheckVideoThumbnails();
    }, 1000);
}

function fileCheckVideoThumbnails() {
    const containers = document.querySelectorAll('.file-thumbnail-container[data-video-path]');
    
    containers.forEach(container => {
        const videoPath = container.dataset.videoPath;
        if (videoPath) {
            fileCheckVideoThumbnailStatus(container, videoPath);
        }
    });
}

async function fileCheckVideoThumbnailStatus(container, videoPath) {
    try {
        const response = await fetch(`/api/file/thumbnail/status?path=${encodeURIComponent(videoPath)}`);
        const data = await response.json();
        
        if (data.status === 'ready') {
            // 缩略图已生成，显示缩略图
            fileShowVideoThumbnail(container, videoPath);
        } else if (data.status === 'not_generated' || data.status === 'outdated') {
            // 请求生成缩略图
            fileRequestVideoThumbnail(container, videoPath);
        } else {
            // 其他状态，显示错误
            fileShowVideoThumbnailError(container, data.status);
        }
    } catch (error) {
        console.error('检查视频缩略图状态失败:', error);
        fileShowVideoThumbnailError(container, 'error');
    }
}

async function fileRequestVideoThumbnail(container, videoPath) {
    try {
        // 更新状态显示
        const statusDiv = container.querySelector('.thumbnail-status');
        if (statusDiv) {
            statusDiv.textContent = '生成中...';
        }
        
        // 请求缩略图
        const response = await fetch(`/api/file/thumbnail?path=${encodeURIComponent(videoPath)}`);
        
        if (response.status === 202) {
            // 正在后台生成，开始轮询
            fileStartThumbnailPolling(container, videoPath);
        } else if (response.ok) {
            // 缩略图已存在，直接显示
            fileShowVideoThumbnail(container, videoPath);
        } else {
            // 生成失败
            fileShowVideoThumbnailError(container, 'generation_failed');
        }
    } catch (error) {
        console.error('请求视频缩略图失败:', error);
        fileShowVideoThumbnailError(container, 'request_failed');
    }
}

function fileStartThumbnailPolling(container, videoPath) {
    let pollCount = 0;
    const maxPolls = 30; // 最多轮询30次（30秒）
    
    const pollInterval = setInterval(async () => {
        pollCount++;
        
        try {
            const response = await fetch(`/api/file/thumbnail/status?path=${encodeURIComponent(videoPath)}`);
            const data = await response.json();
            
            if (data.status === 'ready') {
                // 缩略图生成完成
                clearInterval(pollInterval);
                fileShowVideoThumbnail(container, videoPath);
            } else if (pollCount >= maxPolls) {
                // 超时
                clearInterval(pollInterval);
                fileShowVideoThumbnailError(container, 'timeout');
            } else {
                // 更新状态显示
                const statusDiv = container.querySelector('.thumbnail-status');
                if (statusDiv) {
                    statusDiv.textContent = `生成中...(${pollCount}s)`;
                }
            }
        } catch (error) {
            console.error('轮询缩略图状态失败:', error);
            if (pollCount >= maxPolls) {
                clearInterval(pollInterval);
                fileShowVideoThumbnailError(container, 'poll_error');
            }
        }
    }, 1000);
}

function fileShowVideoThumbnail(container, videoPath) {
    const thumbnailUrl = `/api/file/thumbnail?path=${encodeURIComponent(videoPath)}`;
    
    container.innerHTML = `
        <img src="${thumbnailUrl}" 
             alt="视频缩略图" 
             class="video-thumbnail"
             onerror="this.parentElement.innerHTML='<div class=\\'file-icon\\'><i class=\\'bi bi-camera-video-fill\\'></i></div>'"
             onload="this.classList.add('loaded')">
    `;
}

function fileShowVideoThumbnailError(container, errorType) {
    let errorMessage = '缩略图生成失败';
    
    switch (errorType) {
        case 'file_not_found':
            errorMessage = '文件不存在';
            break;
        case 'generation_failed':
            errorMessage = '生成失败';
            break;
        case 'request_failed':
            errorMessage = '请求失败';
            break;
        case 'timeout':
            errorMessage = '生成超时';
            break;
        case 'poll_error':
            errorMessage = '状态检查失败';
            break;
        default:
            errorMessage = '未知错误';
    }
    
    container.innerHTML = `
        <div class="file-icon video-error">
            <i class="bi bi-camera-video-fill"></i>
            <div class="thumbnail-status">${errorMessage}</div>
        </div>
    `;
}

// 更新分页
function fileUpdatePagination() {
    const totalPages = Math.ceil(fileFilteredFiles.length / fileItemsPerPage);
    const pagination = document.getElementById('pagination');
    const currentPageInfo = document.getElementById('currentPageInfo');
    const totalPagesSpan = document.getElementById('totalPages');
    
    if (!pagination || !currentPageInfo || !totalPagesSpan) {
        console.error('找不到分页相关元素');
        return;
    }
    
    const startItem = (fileCurrentPage - 1) * fileItemsPerPage + 1;
    const endItem = Math.min(fileCurrentPage * fileItemsPerPage, fileFilteredFiles.length);
    currentPageInfo.textContent = `${startItem}-${endItem}`;
    totalPagesSpan.textContent = totalPages;
    
    pagination.innerHTML = '';
    if (totalPages <= 1) return;
    
    // 上一页
    const prevLi = document.createElement('li');
    prevLi.className = `page-item ${fileCurrentPage === 1 ? 'disabled' : ''}`;
    prevLi.innerHTML = `<a class="page-link" href="#" onclick="fileChangePage(${fileCurrentPage - 1})">上一页</a>`;
    pagination.appendChild(prevLi);
    
    // 页码
    const maxVisiblePages = 5;
    let startPage = Math.max(1, fileCurrentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
    
    if (endPage - startPage + 1 < maxVisiblePages) {
        startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }
    
    if (startPage > 1) {
        pagination.appendChild(fileCreatePageItem(1));
        if (startPage > 2) pagination.appendChild(fileCreateEllipsisItem());
    }
    
    for (let i = startPage; i <= endPage; i++) {
        pagination.appendChild(fileCreatePageItem(i, i === fileCurrentPage));
    }
    
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) pagination.appendChild(fileCreateEllipsisItem());
        pagination.appendChild(fileCreatePageItem(totalPages));
    }
    
    // 下一页
    const nextLi = document.createElement('li');
    nextLi.className = `page-item ${fileCurrentPage === totalPages ? 'disabled' : ''}`;
    nextLi.innerHTML = `<a class="page-link" href="#" onclick="fileChangePage(${fileCurrentPage + 1})">下一页</a>`;
    pagination.appendChild(nextLi);
}

// 创建分页项
function fileCreatePageItem(page, active = false) {
    const li = document.createElement('li');
    li.className = `page-item ${active ? 'active' : ''}`;
    li.innerHTML = `<a class="page-link" href="#" onclick="fileChangePage(${page})">${page}</a>`;
    return li;
}

// 创建省略号项
function fileCreateEllipsisItem() {
    const li = document.createElement('li');
    li.className = 'page-item disabled';
    li.innerHTML = '<span class="page-link">...</span>';
    return li;
}

// 切换页面
function fileChangePage(page) {
    const totalPages = Math.ceil(fileFilteredFiles.length / fileItemsPerPage);
    if (page >= 1 && page <= totalPages) {
        fileCurrentPage = page;
        fileRenderFiles();
        fileUpdatePagination();
    }
}

// 工具函数
function fileGetFileExtension(filename) {
    return filename.split('.').pop();
}

function fileTruncateText(text, maxLength) {
    return text.length <= maxLength ? text : text.substring(0, maxLength - 2) + '..';
}

function fileTruncateFileName(filename, maxLength) {
    if (filename.length <= maxLength) return filename;
    const ext = fileGetFileExtension(filename);
    const nameWithoutExt = filename.substring(0, filename.lastIndexOf('.'));
    const maxNameLength = maxLength - ext.length - 4;
    return maxNameLength <= 0 ? filename.substring(0, maxLength - 3) + '...' : nameWithoutExt.substring(0, maxNameLength) + '...' + ext;
}

function fileGetFileIcon(filename) {
    const ext = fileGetFileExtension(filename).toLowerCase();
    if (['mp4', 'avi', 'mov', 'mkv', 'flv', 'webm'].includes(ext)) return 'bi-camera-video-fill';
    if (['mp3', 'wav', 'aac', 'flac', 'm4a'].includes(ext)) return 'bi-music-note-beamed';
    if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(ext)) return 'bi-image-fill';
    if (['json'].includes(ext)) return 'bi-filetype-json';
    if (['txt', 'log'].includes(ext)) return 'bi-file-text-fill';
    return 'bi-file-earmark-fill';
}

function fileFormatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function fileFormatDate(dateString) {
    return new Date(dateString).toLocaleString('zh-CN');
}

function fileOpenFileInFolder(event, file) {
    event.stopPropagation(); // 阻止事件冒泡
    
    const downloadPath = document.getElementById('downloadPath')?.value || './Downloaded/';
    const fullPath = `${downloadPath}/${file.path}`;
    
    try {
        if (navigator.platform.indexOf('Win') !== -1) {
            const command = `explorer /select,"${fullPath.replace(/\//g, '\\')}"`;
            window.open(`cmd://${command}`, '_blank');
        } else {
            window.open(`file://${fullPath}`, '_blank');
        }
        fileShowToast(`已在文件夹中打开: ${file.name}`, 'success');
    } catch (error) {
        fileShowToast('无法打开文件，请手动访问', 'warning');
    }
}

function filePreviewFile(event, filePath, fileExt) {
    event.stopPropagation(); // 阻止事件冒泡
    
    const isVideo = ['mp4', 'avi', 'mov', 'mkv', 'flv', 'webm'].includes(fileExt.toLowerCase());
    const isImage = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(fileExt.toLowerCase());
    
    if (!isVideo && !isImage) {
        fileShowToast('不支持预览此文件类型', 'warning');
        return;
    }
    
    // 确保使用原文件路径，不是缩略图路径
    // 检查路径是否包含temp，如果包含则跳过
    if (filePath.includes('temp')) {
        fileShowToast('无法预览临时文件', 'warning');
        return;
    }
    
    const previewUrl = `/api/file/preview?path=${encodeURIComponent(filePath)}`;
    
    // 创建或获取模态框
    let modal = document.getElementById('filePreviewModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'filePreviewModal';
        modal.className = 'modal fade';
        modal.setAttribute('tabindex', '-1');
        modal.innerHTML = `
            <div class="modal-dialog modal-fullscreen modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">文件预览</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center">
                        <div id="previewContent"></div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                        <button type="button" class="btn btn-primary" onclick="fileDownloadFile()">下载</button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }
    
    // 显示加载状态
    const previewContent = document.getElementById('previewContent');
    previewContent.innerHTML = `
        <div class="d-flex justify-content-center align-items-center" style="height: 400px;">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
        </div>
    `;
    
    // 显示模态框
    const modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();
    
    // 加载文件内容
    if (isVideo) {
        // 使用专门的视频API
        const videoUrl = `/api/file/video?path=${encodeURIComponent(filePath)}`;
        
        previewContent.innerHTML = `
            <div class="video-container" style="width: 100%; height: calc(100vh - 200px); display: flex; align-items: center; justify-content: center; background: #000;">
                <video controls preload="metadata" 
                       style="width: 100%; height: 100%; object-fit: contain;"
                       crossorigin="anonymous"
                       playsinline
                       webkit-playsinline>
                    <source src="${videoUrl}" type="video/${fileExt.toLowerCase()}" />
                    您的浏览器不支持视频播放。
                </video>
            </div>
        `;
        
        // 添加视频加载事件监听
        setTimeout(() => {
            const video = previewContent.querySelector('video');
            if (video) {
                video.addEventListener('loadedmetadata', function() {
                    console.log('视频元数据加载完成');
                });
                
                video.addEventListener('error', function(e) {
                    console.error('视频加载错误:', e);
                    previewContent.innerHTML = `
                        <div class="alert alert-danger">
                            <i class="bi bi-exclamation-triangle"></i>
                            视频加载失败，请检查文件格式或稍后重试
                        </div>
                    `;
                });
                
                video.addEventListener('loadstart', function() {
                    console.log('开始加载视频');
                });
                
                video.addEventListener('canplay', function() {
                    console.log('视频可以播放');
                });
            }
        }, 100);
    } else if (isImage) {
        previewContent.innerHTML = `
            <div class="image-container" style="width: 100%; height: calc(100vh - 200px); display: flex; align-items: center; justify-content: center; background: #f8f9fa;">
                <img src="${previewUrl}" 
                     style="max-width: 100%; max-height: 100%; object-fit: contain; cursor: zoom-in; transition: all 0.3s ease; border-radius: 8px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);" 
                     alt="图片预览" 
                     onclick="fileToggleImageZoom(this)"
                     onerror="this.parentElement.innerHTML='<div style=\\'display: flex; align-items: center; justify-content: center; height: 100%;\\'><p class=\\'text-danger\\'>图片加载失败</p></div>'"
                     title="点击放大/缩小">
            </div>
        `;
    }
    
    // 保存当前文件信息用于下载
    window.currentPreviewFile = {
        path: filePath,
        ext: fileExt,
        url: previewUrl
    };
}

// 图片缩放功能
function fileToggleImageZoom(img) {
    if (img.style.maxWidth === '100%') {
        // 放大到原始大小
        img.style.maxWidth = 'none';
        img.style.maxHeight = 'none';
        img.style.width = 'auto';
        img.style.height = 'auto';
        img.style.cursor = 'zoom-out';
        img.title = '点击缩小';
    } else {
        // 缩小到适应容器
        img.style.maxWidth = '100%';
        img.style.maxHeight = '100%';
        img.style.width = 'auto';
        img.style.height = 'auto';
        img.style.cursor = 'zoom-in';
        img.title = '点击放大';
    }
}

function fileDownloadFile() {
    if (window.currentPreviewFile) {
        const link = document.createElement('a');
        link.href = window.currentPreviewFile.url;
        link.download = window.currentPreviewFile.path.split('/').pop();
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        fileShowToast('开始下载文件', 'success');
    }
}

function fileOpenDownloadFolder() {
    const downloadPath = document.getElementById('downloadPath')?.value || './Downloaded/';
    try {
        if (navigator.platform.indexOf('Win') !== -1) {
            const command = `explorer "${downloadPath.replace(/\//g, '\\')}"`;
            window.open(`cmd://${command}`, '_blank');
        } else {
            window.open(`file://${downloadPath}`, '_blank');
        }
        fileShowToast('已打开下载文件夹', 'success');
    } catch (error) {
        fileShowToast('无法打开文件夹，请手动访问下载目录', 'warning');
    }
}

function fileShowError(message) {
    const container = document.getElementById('filesContainer');
    if (container) {
        container.innerHTML = `
            <div class="text-center py-5" style="grid-column: 1 / -1;">
                <i class="bi bi-exclamation-triangle" style="font-size: 3rem; color: #f59e0b;"></i>
                <p class="text-muted mt-3">${message}</p>
                <small class="text-muted">请检查网络连接或稍后重试</small>
            </div>
        `;
    }
}

function fileShowToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    document.body.appendChild(toast);
    setTimeout(() => { if (toast.parentNode) toast.parentNode.removeChild(toast); }, 3000);
}

// 懒加载相关函数
function fileInitLazyLoading() {
    // 使用 Intersection Observer API 实现懒加载
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.remove('lazy-thumbnail');
                        img.removeAttribute('data-src');
                        observer.unobserve(img);
                    }
                }
            });
        }, {
            rootMargin: '50px 0px', // 提前50px开始加载
            threshold: 0.01
        });
        
        // 观察所有懒加载图片
        document.querySelectorAll('.lazy-thumbnail').forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // 降级处理：直接加载所有图片
        document.querySelectorAll('.lazy-thumbnail').forEach(img => {
            if (img.dataset.src) {
                img.src = img.dataset.src;
                img.classList.remove('lazy-thumbnail');
                img.removeAttribute('data-src');
            }
        });
    }
}

// 页面滚动时重新检查懒加载
function fileCheckLazyLoading() {
    if ('IntersectionObserver' in window) {
        // Intersection Observer 会自动处理，不需要手动检查
        return;
    }
    
    // 降级处理：检查可见的图片
    const lazyImages = document.querySelectorAll('.lazy-thumbnail');
    lazyImages.forEach(img => {
        const rect = img.getBoundingClientRect();
        const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
        
        if (isVisible && img.dataset.src) {
            img.src = img.dataset.src;
            img.classList.remove('lazy-thumbnail');
            img.removeAttribute('data-src');
        }
    });
}

// 添加滚动事件监听器
document.addEventListener('DOMContentLoaded', function() {
    // 使用节流函数优化滚动事件
    let scrollTimeout;
    window.addEventListener('scroll', function() {
        if (scrollTimeout) {
            clearTimeout(scrollTimeout);
        }
        scrollTimeout = setTimeout(fileCheckLazyLoading, 100);
    });
}); 