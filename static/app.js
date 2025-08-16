// 全局变量
let currentConfig = {};
let downloadStatus = { running: false, current_task: null, progress: 0 };
let statusUpdateInterval = null;
let linksData = []; // 存储链接和用户信息

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadConfig();
    startStatusUpdate();
    // 移除refreshFiles调用，由app_simple.js处理
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