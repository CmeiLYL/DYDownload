// 全局变量
let currentConfig = {};
let downloadStatus = { running: false, current_task: null, progress: 0 };
let statusUpdateInterval = null;
let linksData = []; // 存储链接和用户信息

// 文件管理相关变量
let allFiles = []; // 所有文件
let filteredFiles = []; // 筛选后的文件
let currentPage = 1; // 当前页码
let itemsPerPage = 12; // 每页显示的文件数量
let fileSources = new Set(); // 文件来源集合

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadConfig();
    startStatusUpdate();
    refreshFiles();
    refreshLogs();
});

// 加载配置
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();
        currentConfig = config;
        updateUIFromConfig(config);
        updateStatistics();
    } catch (error) {
        console.error('加载配置失败:', error);
        showToast('加载配置失败', 'error');
    }
}

// 从配置更新UI
function updateUIFromConfig(config) {
    // 更新链接列表
    updateLinksDisplay(config.link || []);
    
    // 更新下载选项
    document.getElementById('musicSwitch').checked = config.music || false;
    document.getElementById('coverSwitch').checked = config.cover || false;
    document.getElementById('avatarSwitch').checked = config.avatar || false;
    document.getElementById('jsonSwitch').checked = config.json || false;
    
    // 更新下载模式
    const modeSelect = document.getElementById('modeSelect');
    modeSelect.innerHTML = '';
    const modes = config.mode || ['post'];
    const allModes = [
        { value: 'post', label: '发布作品' },
        { value: 'like', label: '喜欢作品' },
        { value: 'mix', label: '合集' }
    ];
    
    allModes.forEach(mode => {
        const option = document.createElement('option');
        option.value = mode.value;
        option.textContent = mode.label;
        option.selected = modes.includes(mode.value);
        modeSelect.appendChild(option);
    });
    
    // 更新线程数
    document.getElementById('threadInput').value = config.thread || 5;
    
    // 更新设置页面
    document.getElementById('downloadPath').value = config.path || './Downloaded/';
    document.getElementById('folderStyleSwitch').checked = config.folderstyle || false;
    document.getElementById('databaseSwitch').checked = config.database !== false;
    
    // 更新增量下载设置
    const increase = config.increase || {};
    document.getElementById('increasePostSwitch').checked = increase.post || false;
    document.getElementById('increaseLikeSwitch').checked = increase.like || false;
    document.getElementById('increaseMixSwitch').checked = increase.mix || false;
    document.getElementById('increaseAllMixSwitch').checked = increase.allmix || false;
    
    // 更新Cookie设置
    const cookies = config.cookies || {};
    document.getElementById('msTokenInput').value = cookies.msToken || '';
    document.getElementById('ttwidInput').value = cookies.ttwid || '';
    document.getElementById('odinTtInput').value = cookies.odin_tt || '';
    document.getElementById('passportCsrfTokenInput').value = cookies.passport_csrf_token || '';
    document.getElementById('sidGuardInput').value = cookies.sid_guard || '';
}

// 更新链接显示
function updateLinksDisplay(links) {
    linksData = [];
    const tbody = document.getElementById('linksTableBody');
    tbody.innerHTML = '';
    
    links.forEach((link, index) => {
        if (link.trim()) {
            // 先添加一个占位行
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>
                    <input type="text" class="form-control form-control-sm" value="${link}" 
                           onchange="updateLink(${index}, this.value)" placeholder="请输入抖音链接">
                </td>
                <td>
                    <span class="text-muted">正在获取...</span>
                </td>
                <td>
                    <span class="badge bg-secondary">未知</span>
                </td>
                <td>
                    <button class="btn btn-outline-danger btn-sm" onclick="removeLink(${index})">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(row);
            
            // 异步获取用户信息
            parseLinkInfo(link, index);
        }
    });
    
    document.getElementById('totalLinks').textContent = links.length;
}

// 解析链接信息
async function parseLinkInfo(link, index) {
    try {
        const response = await fetch('/api/link/parse', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ link })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 更新表格行
            const tbody = document.getElementById('linksTableBody');
            const row = tbody.children[index];
            if (row) {
                const nameCell = row.children[2];
                const typeCell = row.children[3];
                
                nameCell.innerHTML = `<span class="fw-bold">${result.nickname}</span>`;
                
                let typeBadge = '';
                switch (result.link_type) {
                    case 'user':
                        typeBadge = '<span class="badge bg-primary">用户主页</span>';
                        break;
                    case 'video':
                        typeBadge = '<span class="badge bg-success">视频</span>';
                        break;
                    case 'mix':
                        typeBadge = '<span class="badge bg-warning">合集</span>';
                        break;
                    default:
                        typeBadge = '<span class="badge bg-secondary">未知</span>';
                }
                typeCell.innerHTML = typeBadge;
                
                // 保存链接信息
                linksData[index] = {
                    link: link,
                    nickname: result.nickname,
                    link_type: result.link_type,
                    id: result.sec_uid || result.aweme_id || result.mix_id
                };
            }
        } else {
            // 显示错误信息
            const tbody = document.getElementById('linksTableBody');
            const row = tbody.children[index];
            if (row) {
                const nameCell = row.children[2];
                const typeCell = row.children[3];
                
                nameCell.innerHTML = `<span class="text-danger">${result.message}</span>`;
                typeCell.innerHTML = '<span class="badge bg-danger">解析失败</span>';
            }
        }
    } catch (error) {
        console.error('解析链接信息失败:', error);
        const tbody = document.getElementById('linksTableBody');
        const row = tbody.children[index];
        if (row) {
            const nameCell = row.children[2];
            const typeCell = row.children[3];
            
            nameCell.innerHTML = '<span class="text-danger">网络错误</span>';
            typeCell.innerHTML = '<span class="badge bg-danger">解析失败</span>';
        }
    }
}

// 解析并添加链接
async function parseAndAddLink() {
    const linkInput = document.getElementById('newLinkInput');
    const link = linkInput.value.trim();
    
    if (!link) {
        showToast('请输入链接', 'error');
        return;
    }
    
    // 检查链接是否已存在
    const existingLinks = currentConfig.link || [];
    if (existingLinks.includes(link)) {
        showToast('链接已存在', 'warning');
        return;
    }
    
    // 添加到配置
    existingLinks.push(link);
    currentConfig.link = existingLinks;
    
    // 更新显示
    updateLinksDisplay(existingLinks);
    
    // 清空输入框
    linkInput.value = '';
    
    showToast('链接添加成功', 'success');
}

// 处理链接输入框回车事件
function handleLinkKeyPress(event) {
    if (event.key === 'Enter') {
        parseAndAddLink();
    }
}

// 清空所有链接
function clearAllLinks() {
    if (confirm('确定要清空所有链接吗？')) {
        currentConfig.link = [];
        linksData = [];
        updateLinksDisplay([]);
        showToast('已清空所有链接', 'success');
    }
}

// 更新链接
function updateLink(index, value) {
    if (!currentConfig.link) currentConfig.link = [];
    currentConfig.link[index] = value;
    
    // 重新解析链接信息
    if (value.trim()) {
        parseLinkInfo(value, index);
    }
}

// 删除链接
function removeLink(index) {
    if (!currentConfig.link) return;
    currentConfig.link.splice(index, 1);
    linksData.splice(index, 1);
    updateLinksDisplay(currentConfig.link);
    showToast('链接已删除', 'success');
}

// 开始下载
async function startDownload() {
    try {
        // 收集当前配置
        const config = collectCurrentConfig();
        
        const response = await fetch('/api/download/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ config })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast('下载任务已启动', 'success');
            updateDownloadControls(true);
        } else {
            showToast(result.message || '启动下载失败', 'error');
        }
    } catch (error) {
        console.error('启动下载失败:', error);
        showToast('启动下载失败', 'error');
    }
}

// 停止下载
async function stopDownload() {
    try {
        const response = await fetch('/api/download/stop', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast('下载已停止', 'success');
            updateDownloadControls(false);
        } else {
            showToast(result.message || '停止下载失败', 'error');
        }
    } catch (error) {
        console.error('停止下载失败:', error);
        showToast('停止下载失败', 'error');
    }
}

// 收集当前配置
function collectCurrentConfig() {
    const config = { ...currentConfig };
    
    // 收集链接（从表格中获取）
    const linkInputs = document.querySelectorAll('#linksTableBody input');
    config.link = Array.from(linkInputs).map(input => input.value).filter(link => link.trim());
    
    // 收集下载选项
    config.music = document.getElementById('musicSwitch').checked;
    config.cover = document.getElementById('coverSwitch').checked;
    config.avatar = document.getElementById('avatarSwitch').checked;
    config.json = document.getElementById('jsonSwitch').checked;
    
    // 收集下载模式
    const modeSelect = document.getElementById('modeSelect');
    config.mode = Array.from(modeSelect.selectedOptions).map(option => option.value);
    
    // 收集线程数
    config.thread = parseInt(document.getElementById('threadInput').value) || 5;
    
    // 收集设置
    config.path = document.getElementById('downloadPath').value || './Downloaded/';
    config.folderstyle = document.getElementById('folderStyleSwitch').checked;
    config.database = document.getElementById('databaseSwitch').checked;
    
    // 收集增量下载设置
    config.increase = {
        post: document.getElementById('increasePostSwitch').checked,
        like: document.getElementById('increaseLikeSwitch').checked,
        mix: document.getElementById('increaseMixSwitch').checked,
        allmix: document.getElementById('increaseAllMixSwitch').checked,
        music: false
    };
    
    // 收集Cookie设置
    config.cookies = {
        msToken: document.getElementById('msTokenInput').value,
        ttwid: document.getElementById('ttwidInput').value,
        odin_tt: document.getElementById('odinTtInput').value,
        passport_csrf_token: document.getElementById('passportCsrfTokenInput').value,
        sid_guard: document.getElementById('sidGuardInput').value
    };
    
    return config;
}

// 更新下载控制按钮
function updateDownloadControls(running) {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const statusBadge = document.getElementById('statusBadge');
    
    if (running) {
        startBtn.disabled = true;
        stopBtn.disabled = false;
        statusBadge.textContent = '运行中';
        statusBadge.className = 'status-badge status-running';
    } else {
        startBtn.disabled = false;
        stopBtn.disabled = true;
        statusBadge.textContent = '已停止';
        statusBadge.className = 'status-badge status-stopped';
    }
}

// 开始状态更新
function startStatusUpdate() {
    statusUpdateInterval = setInterval(updateDownloadStatus, 1000);
}

// 更新下载状态
async function updateDownloadStatus() {
    try {
        const response = await fetch('/api/download/status');
        const status = await response.json();
        
        if (status.running !== downloadStatus.running) {
            updateDownloadControls(status.running);
        }
        
        downloadStatus = status;
        
        // 更新进度条
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const currentTask = document.getElementById('currentTask');
        
        progressBar.style.width = `${status.progress}%`;
        progressText.textContent = `${status.progress}%`;
        currentTask.textContent = status.current_task || '等待开始...';
        
    } catch (error) {
        console.error('获取下载状态失败:', error);
    }
}

// 保存配置
async function saveConfig() {
    try {
        const config = collectCurrentConfig();
        
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentConfig = config;
            showToast('配置保存成功', 'success');
        } else {
            showToast(result.message || '配置保存失败', 'error');
        }
    } catch (error) {
        console.error('保存配置失败:', error);
        showToast('保存配置失败', 'error');
    }
}

// 重置配置
function resetConfig() {
    if (confirm('确定要重置配置吗？这将恢复默认设置。')) {
        currentConfig = {
            link: [],
            path: './Downloaded/',
            music: false,
            cover: false,
            avatar: false,
            json: false,
            folderstyle: false,
            mode: ['post', 'mix'],
            number: {
                post: 0,
                like: 0,
                allmix: 0,
                mix: 0,
                music: 0
            },
            database: true,
            increase: {
                post: true,
                like: false,
                allmix: true,
                mix: true,
                music: false
            },
            thread: 5,
            cookies: {}
        };
        
        updateUIFromConfig(currentConfig);
        showToast('配置已重置', 'success');
    }
}

// 刷新文件列表
async function refreshFiles() {
    try {
        const response = await fetch('/api/files');
        const files = await response.json();
        
        // 处理文件数据，添加来源信息
        allFiles = files.map(file => {
            const fileInfo = {
                ...file,
                fileType: getFileType(file.name),
                source: extractSourceFromPath(file.path)
            };
            return fileInfo;
        });
        
        // 收集所有文件来源
        fileSources.clear();
        allFiles.forEach(file => {
            if (file.source) {
                fileSources.add(file.source);
            }
        });
        
        // 更新来源筛选器
        updateSourceFilter();
        
        // 应用筛选和分页
        filterFiles();
        
        document.getElementById('totalFiles').textContent = allFiles.length;
    } catch (error) {
        console.error('获取文件列表失败:', error);
        const container = document.getElementById('filesContainer');
        container.innerHTML = `
            <div class="text-center py-5" style="grid-column: 1 / -1;">
                <i class="bi bi-exclamation-triangle" style="font-size: 3rem; color: #f59e0b;"></i>
                <p class="text-muted mt-3">获取文件列表失败</p>
                <small class="text-muted">请检查网络连接或稍后重试</small>
            </div>
        `;
    }
}

// 获取文件类型
function getFileType(filename) {
    const ext = getFileExtension(filename).toLowerCase();
    
    if (['mp4', 'avi', 'mov', 'mkv', 'flv', 'webm'].includes(ext)) {
        return 'video';
    } else if (['mp3', 'wav', 'aac', 'flac', 'm4a'].includes(ext)) {
        return 'audio';
    } else if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(ext)) {
        return 'image';
    } else if (['json', 'txt', 'log'].includes(ext)) {
        return 'data';
    } else {
        return 'other';
    }
}

// 从路径中提取来源信息
function extractSourceFromPath(path) {
    // 假设路径格式为: 用户名称/文件名 或 合集名称/文件名
    const pathParts = path.split(/[\\\/]/);
    if (pathParts.length >= 2) {
        return pathParts[0]; // 返回第一级目录名作为来源
    }
    return '未知来源';
}

// 更新来源筛选器
function updateSourceFilter() {
    const sourceFilter = document.getElementById('sourceFilter');
    const currentValue = sourceFilter.value;
    
    // 清空现有选项（保留"全部来源"）
    sourceFilter.innerHTML = '<option value="all">全部来源</option>';
    
    // 添加来源选项
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
function filterFiles() {
    const typeFilter = document.getElementById('fileTypeFilter').value;
    const sourceFilter = document.getElementById('sourceFilter').value;
    const sortFilter = document.getElementById('sortFilter').value;
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    
    // 应用筛选
    filteredFiles = allFiles.filter(file => {
        // 类型筛选
        if (typeFilter !== 'all' && file.fileType !== typeFilter) {
            return false;
        }
        
        // 来源筛选
        if (sourceFilter !== 'all' && file.source !== sourceFilter) {
            return false;
        }
        
        // 搜索筛选
        if (searchInput && !file.name.toLowerCase().includes(searchInput)) {
            return false;
        }
        
        return true;
    });
    
    // 应用排序
    sortFiles(sortFilter);
    
    // 更新统计信息
    updateFileStats();
    
    // 重置到第一页
    currentPage = 1;
    
    // 渲染文件
    renderFiles();
    
    // 更新分页
    updatePagination();
}

// 排序文件
function sortFiles(sortType) {
    switch (sortType) {
        case 'date-desc':
            filteredFiles.sort((a, b) => new Date(b.modified) - new Date(a.modified));
            break;
        case 'date-asc':
            filteredFiles.sort((a, b) => new Date(a.modified) - new Date(b.modified));
            break;
        case 'name-asc':
            filteredFiles.sort((a, b) => a.name.localeCompare(b.name));
            break;
        case 'name-desc':
            filteredFiles.sort((a, b) => b.name.localeCompare(a.name));
            break;
        case 'size-desc':
            filteredFiles.sort((a, b) => b.size - a.size);
            break;
    }
}

// 更新文件统计信息
function updateFileStats() {
    const stats = {
        total: allFiles.length,
        video: allFiles.filter(f => f.fileType === 'video').length,
        image: allFiles.filter(f => f.fileType === 'image').length,
        audio: allFiles.filter(f => f.fileType === 'audio').length,
        other: allFiles.filter(f => !['video', 'image', 'audio'].includes(f.fileType)).length
    };
    
    document.getElementById('totalFileCount').textContent = stats.total;
    document.getElementById('videoCount').textContent = stats.video;
    document.getElementById('imageCount').textContent = stats.image;
    document.getElementById('audioCount').textContent = stats.audio;
    document.getElementById('otherCount').textContent = stats.other;
}

// 渲染文件
function renderFiles() {
    const container = document.getElementById('filesContainer');
    container.innerHTML = '';
    
    if (filteredFiles.length === 0) {
        container.innerHTML = `
            <div class="text-center py-5" style="grid-column: 1 / -1;">
                <i class="bi bi-folder-x" style="font-size: 3rem; color: #cbd5e1;"></i>
                <p class="text-muted mt-3">没有找到符合条件的文件</p>
                <small class="text-muted">请尝试调整筛选条件</small>
            </div>
        `;
        return;
    }
    
    // 计算当前页的文件
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const currentPageFiles = filteredFiles.slice(startIndex, endIndex);
    
    // 渲染文件卡片
    currentPageFiles.forEach(file => {
        const fileCard = document.createElement('div');
        fileCard.className = 'file-card';
        fileCard.onclick = () => openFileInFolder(file);
        
        const fileExt = getFileExtension(file.name).toLowerCase();
        const isImage = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(fileExt);
        const isVideo = ['mp4', 'avi', 'mov', 'mkv', 'flv', 'webm'].includes(fileExt);
        
        let thumbnailContent = '';
        if (isImage) {
            // 图片文件显示缩略图
            const imagePath = file.path.replace(/\\/g, '/');
            thumbnailContent = `<img src="/api/file/thumbnail?path=${encodeURIComponent(imagePath)}" alt="${file.name}" onerror="this.parentElement.innerHTML='<div class=\\'file-icon\\'><i class=\\'bi bi-image\\'></i></div>'">`;
        } else if (isVideo) {
            // 视频文件显示视频图标
            thumbnailContent = `<div class="file-icon"><i class="bi bi-camera-video-fill"></i></div>`;
        } else {
            // 其他文件显示对应图标
            thumbnailContent = `<div class="file-icon"><i class="bi ${getFileIcon(file.name)}"></i></div>`;
        }
        
        fileCard.innerHTML = `
            <div class="file-type-badge">${fileExt.toUpperCase()}</div>
            <div class="file-source-badge" title="${file.source}">${truncateText(file.source, 10)}</div>
            <div class="file-thumbnail">
                ${thumbnailContent}
            </div>
            <div class="file-name" title="${file.name}">${truncateFileName(file.name, 20)}</div>
            <div class="file-meta">
                <span>${formatFileSize(file.size)}</span>
                <span>${formatDate(file.modified)}</span>
            </div>
        `;
        container.appendChild(fileCard);
    });
}

// 更新分页
function updatePagination() {
    const totalPages = Math.ceil(filteredFiles.length / itemsPerPage);
    const pagination = document.getElementById('pagination');
    const currentPageInfo = document.getElementById('currentPageInfo');
    const totalPagesSpan = document.getElementById('totalPages');
    
    // 更新页码信息
    const startItem = (currentPage - 1) * itemsPerPage + 1;
    const endItem = Math.min(currentPage * itemsPerPage, filteredFiles.length);
    currentPageInfo.textContent = `${startItem}-${endItem}`;
    totalPagesSpan.textContent = totalPages;
    
    // 清空分页按钮
    pagination.innerHTML = '';
    
    if (totalPages <= 1) {
        return;
    }
    
    // 上一页按钮
    const prevLi = document.createElement('li');
    prevLi.className = `page-item ${currentPage === 1 ? 'disabled' : ''}`;
    prevLi.innerHTML = `<a class="page-link" href="#" onclick="changePage(${currentPage - 1})">上一页</a>`;
    pagination.appendChild(prevLi);
    
    // 页码按钮
    const maxVisiblePages = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
    
    if (endPage - startPage + 1 < maxVisiblePages) {
        startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }
    
    // 第一页
    if (startPage > 1) {
        const firstLi = document.createElement('li');
        firstLi.className = 'page-item';
        firstLi.innerHTML = `<a class="page-link" href="#" onclick="changePage(1)">1</a>`;
        pagination.appendChild(firstLi);
        
        if (startPage > 2) {
            const ellipsisLi = document.createElement('li');
            ellipsisLi.className = 'page-item disabled';
            ellipsisLi.innerHTML = '<span class="page-link">...</span>';
            pagination.appendChild(ellipsisLi);
        }
    }
    
    // 页码
    for (let i = startPage; i <= endPage; i++) {
        const pageLi = document.createElement('li');
        pageLi.className = `page-item ${i === currentPage ? 'active' : ''}`;
        pageLi.innerHTML = `<a class="page-link" href="#" onclick="changePage(${i})">${i}</a>`;
        pagination.appendChild(pageLi);
    }
    
    // 最后一页
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            const ellipsisLi = document.createElement('li');
            ellipsisLi.className = 'page-item disabled';
            ellipsisLi.innerHTML = '<span class="page-link">...</span>';
            pagination.appendChild(ellipsisLi);
        }
        
        const lastLi = document.createElement('li');
        lastLi.className = 'page-item';
        lastLi.innerHTML = `<a class="page-link" href="#" onclick="changePage(${totalPages})">${totalPages}</a>`;
        pagination.appendChild(lastLi);
    }
    
    // 下一页按钮
    const nextLi = document.createElement('li');
    nextLi.className = `page-item ${currentPage === totalPages ? 'disabled' : ''}`;
    nextLi.innerHTML = `<a class="page-link" href="#" onclick="changePage(${currentPage + 1})">下一页</a>`;
    pagination.appendChild(nextLi);
}

// 切换页面
function changePage(page) {
    const totalPages = Math.ceil(filteredFiles.length / itemsPerPage);
    if (page >= 1 && page <= totalPages) {
        currentPage = page;
        renderFiles();
        updatePagination();
    }
}

// 截断文本
function truncateText(text, maxLength) {
    if (text.length <= maxLength) {
        return text;
    }
    return text.substring(0, maxLength - 2) + '..';
}

// 截断文件名
function truncateFileName(filename, maxLength) {
    if (filename.length <= maxLength) {
        return filename;
    }
    
    const ext = getFileExtension(filename);
    const nameWithoutExt = filename.substring(0, filename.lastIndexOf('.'));
    const maxNameLength = maxLength - ext.length - 4; // 4 for "..."
    
    if (maxNameLength <= 0) {
        return filename.substring(0, maxLength - 3) + '...';
    }
    
    return nameWithoutExt.substring(0, maxNameLength) + '...' + ext;
}

// 在文件夹中打开并高亮文件
function openFileInFolder(file) {
    const downloadPath = document.getElementById('downloadPath').value || './Downloaded/';
    const fullPath = `${downloadPath}/${file.path}`;
    
    try {
        // 在Windows上使用explorer并高亮文件
        if (navigator.platform.indexOf('Win') !== -1) {
            // Windows: 使用explorer /select命令高亮文件
            const command = `explorer /select,"${fullPath.replace(/\//g, '\\')}"`;
            window.open(`cmd://${command}`, '_blank');
        } else if (navigator.platform.indexOf('Mac') !== -1) {
            // macOS: 使用open命令
            window.open(`file://${fullPath}`, '_blank');
        } else {
            // Linux: 尝试使用默认文件管理器
            window.open(`file://${fullPath}`, '_blank');
        }
        
        showToast(`已在文件夹中打开: ${file.name}`, 'success');
    } catch (error) {
        console.error('打开文件失败:', error);
        showToast('无法打开文件，请手动访问', 'warning');
    }
}

// 打开下载文件夹
function openDownloadFolder() {
    const downloadPath = document.getElementById('downloadPath').value || './Downloaded/';
    
    try {
        // 在Windows上使用explorer
        if (navigator.platform.indexOf('Win') !== -1) {
            const command = `explorer "${downloadPath.replace(/\//g, '\\')}"`;
            window.open(`cmd://${command}`, '_blank');
        } else if (navigator.platform.indexOf('Mac') !== -1) {
            // macOS: 使用open命令
            window.open(`file://${downloadPath}`, '_blank');
        } else {
            // Linux: 尝试使用默认文件管理器
            window.open(`file://${downloadPath}`, '_blank');
        }
        
        showToast('已打开下载文件夹', 'success');
    } catch (error) {
        console.error('打开文件夹失败:', error);
        showToast('无法打开文件夹，请手动访问下载目录', 'warning');
    }
}

// 刷新日志
async function refreshLogs() {
    try {
        const response = await fetch('/api/logs');
        const logs = await response.json();
        
        const container = document.getElementById('logsContainer');
        
        if (logs.length === 0) {
            container.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-journal-x" style="font-size: 3rem; color: #64748b;"></i>
                    <p class="text-muted mt-3">暂无日志记录</p>
                    <small class="text-muted">系统日志将显示在这里</small>
                </div>
            `;
        } else {
            // 创建带颜色的日志内容
            const logContent = document.createElement('div');
            logContent.className = 'log-content';
            
            logs.forEach(log => {
                const logLine = document.createElement('div');
                logLine.className = 'log-line';
                
                // 解析日志级别并添加颜色
                let logClass = '';
                if (log.includes('[ERROR]') || log.includes('错误')) {
                    logClass = 'log-error';
                } else if (log.includes('[WARNING]') || log.includes('警告')) {
                    logClass = 'log-warning';
                } else if (log.includes('[SUCCESS]') || log.includes('成功')) {
                    logClass = 'log-success';
                } else if (log.includes('[INFO]') || log.includes('信息')) {
                    logClass = 'log-info';
                } else {
                    logClass = 'log-default';
                }
                
                logLine.className = `log-line ${logClass}`;
                logLine.textContent = log.trim();
                logContent.appendChild(logLine);
            });
            
            container.innerHTML = '';
            container.appendChild(logContent);
            
            // 滚动到底部
            container.scrollTop = container.scrollHeight;
        }
    } catch (error) {
        console.error('获取日志失败:', error);
        const container = document.getElementById('logsContainer');
        container.innerHTML = `
            <div class="text-center py-5">
                <i class="bi bi-exclamation-triangle" style="font-size: 3rem; color: #f59e0b;"></i>
                <p class="text-muted mt-3">获取日志失败</p>
                <small class="text-muted">请检查网络连接或稍后重试</small>
            </div>
        `;
    }
}

// 更新统计信息
function updateStatistics() {
    const links = currentConfig.link || [];
    document.getElementById('totalLinks').textContent = links.length;
}

// 选择路径（模拟）
function selectPath() {
    // 在实际应用中，这里可以调用文件选择对话框
    // 由于浏览器安全限制，这里只是提示用户手动输入
    alert('请手动输入下载路径，或使用相对路径如: ./Downloaded/');
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN');
}

// 显示提示消息
function showToast(message, type = 'info') {
    // 创建toast元素
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // 3秒后自动移除
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 3000);
}

// 页面卸载时清理
window.addEventListener('beforeunload', function() {
    if (statusUpdateInterval) {
        clearInterval(statusUpdateInterval);
    }
}); 