// 全局变量
let currentConfig = {};
let downloadStatus = { running: false, current_task: null, progress: 0 };
let statusUpdateInterval = null;
let linksData = []; // 存储链接和用户信息

// 下载信息相关变量
let downloadInfo = {
    downloadedCount: 0,
    failedCount: 0,
    remainingCount: 0,
    downloadSpeed: 0,
    startTime: null,
    recentDownloads: [],
    currentFile: null
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadConfig();
    startStatusUpdate();
    // 移除refreshFiles调用，由app_simple.js处理
    refreshLogs();
    // 异步更新统计信息
    updateStatistics();
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
    console.log("🔄 更新UI配置:", config);
    
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
    
    // 更新下载数量设置 - 从配置文件读取
    const number = config.number || {};
    console.log("📊 配置文件中的下载数量设置:", number);
    
    // 更新首页下载数量输入框
    if (document.getElementById('postNumberInput')) {
        document.getElementById('postNumberInput').value = number.post || 0;
        console.log("✅ 更新首页发布作品数量:", number.post || 0);
    }
    if (document.getElementById('likeNumberInput')) {
        document.getElementById('likeNumberInput').value = number.like || 0;
        console.log("✅ 更新首页喜欢作品数量:", number.like || 0);
    }
    if (document.getElementById('mixNumberInput')) {
        document.getElementById('mixNumberInput').value = number.mix || 0;
        console.log("✅ 更新首页合集数量:", number.mix || 0);
    }
    
    // 更新设置页面下载数量输入框
    if (document.getElementById('settingsPostNumberInput')) {
        document.getElementById('settingsPostNumberInput').value = number.post || 0;
        console.log("✅ 更新设置页面发布作品数量:", number.post || 0);
    }
    if (document.getElementById('settingsLikeNumberInput')) {
        document.getElementById('settingsLikeNumberInput').value = number.like || 0;
        console.log("✅ 更新设置页面喜欢作品数量:", number.like || 0);
    }
    if (document.getElementById('settingsMixNumberInput')) {
        document.getElementById('settingsMixNumberInput').value = number.mix || 0;
        console.log("✅ 更新设置页面合集数量:", number.mix || 0);
    }
    
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
    
    console.log("✅ UI配置更新完成");
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
                <td>
                    <input type="checkbox" class="form-check-input link-checkbox" value="${index}" checked>
                </td>
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
                    <span class="text-muted">-</span>
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
    updateSelectAllCheckbox();
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
                const nameCell = row.children[3];
                const typeCell = row.children[4];
                const countCell = row.children[5];
                
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
                
                // 显示作品数量
                let countText = '-';
                if (result.work_count !== undefined) {
                    countText = result.work_count.toString();
                } else if (result.link_type === 'user') {
                    countText = '<span class="text-muted">获取中...</span>';
                }
                countCell.innerHTML = `<span class="fw-bold text-primary">${countText}</span>`;
                
                // 保存链接信息
                linksData[index] = {
                    link: link,
                    nickname: result.nickname,
                    link_type: result.link_type,
                    id: result.sec_uid || result.aweme_id || result.mix_id,
                    work_count: result.work_count
                };
                
                // 如果是用户主页，异步获取作品数量
                if (result.link_type === 'user' && result.sec_uid) {
                    fetchUserWorkCount(result.sec_uid, index);
                }
            }
        } else {
            // 显示错误信息
            const tbody = document.getElementById('linksTableBody');
            const row = tbody.children[index];
            if (row) {
                const nameCell = row.children[3];
                const typeCell = row.children[4];
                const countCell = row.children[5];
                
                nameCell.innerHTML = `<span class="text-danger">${result.message}</span>`;
                typeCell.innerHTML = '<span class="badge bg-danger">解析失败</span>';
                countCell.innerHTML = '<span class="text-danger">-</span>';
            }
        }
    } catch (error) {
        console.error('解析链接信息失败:', error);
        const tbody = document.getElementById('linksTableBody');
        const row = tbody.children[index];
        if (row) {
            const nameCell = row.children[3];
            const typeCell = row.children[4];
            const countCell = row.children[5];
            
            nameCell.innerHTML = '<span class="text-danger">网络错误</span>';
            typeCell.innerHTML = '<span class="badge bg-danger">解析失败</span>';
            countCell.innerHTML = '<span class="text-danger">-</span>';
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
    
    // 保存配置到服务器
    saveConfigToServer();
    
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
        
        // 保存配置到服务器
        saveConfigToServer();
        
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
    
    // 保存配置到服务器
    saveConfigToServer();
}

// 删除链接
function removeLink(index) {
    if (!currentConfig.link) return;
    
    console.log(`🗑️ 删除链接 ${index}: ${currentConfig.link[index]}`);
    
    currentConfig.link.splice(index, 1);
    linksData.splice(index, 1);
    updateLinksDisplay(currentConfig.link);
    
    // 保存配置到服务器
    saveConfigToServer();
    
    showToast('链接已删除', 'success');
}

// 开始下载
async function startDownload() {
    try {
        // 获取选中的链接
        const selectedLinks = getSelectedLinks();
        
        if (selectedLinks.length === 0) {
            showToast('请至少选择一个链接进行下载', 'warning');
            return;
        }
        
        // 计算选中链接的总作品数量
        let totalWorks = 0;
        const selectedLinkData = [];
        
        for (let i = 0; i < selectedLinks.length; i++) {
            const link = selectedLinks[i];
            const linkIndex = currentConfig.link.indexOf(link);
            const linkData = linksData[linkIndex];
            
            if (linkData && linkData.work_count) {
                totalWorks += parseInt(linkData.work_count) || 0;
                selectedLinkData.push({
                    link: link,
                    work_count: parseInt(linkData.work_count) || 0,
                    nickname: linkData.nickname || '未知用户'
                });
            } else {
                // 如果没有作品数量信息，假设每个用户有10个作品作为默认值
                totalWorks += 10;
                selectedLinkData.push({
                    link: link,
                    work_count: 10,
                    nickname: linkData?.nickname || '未知用户'
                });
            }
        }
        
        console.log(`📊 选中链接总作品数量: ${totalWorks}`);
        console.log(`📋 选中链接详情:`, selectedLinkData);
        
        // 收集当前配置
        const config = collectCurrentConfig();
        
        // 创建一个下载专用的配置副本，不影响原始配置
        const downloadConfig = { ...config };
        downloadConfig.link = selectedLinks;
        downloadConfig.total_works = totalWorks;
        downloadConfig.selected_link_data = selectedLinkData;
        
        console.log(`📥 准备下载 ${selectedLinks.length} 个选中的链接，预计总作品数: ${totalWorks}`);
        
        const response = await fetch('/api/download/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ config: downloadConfig })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(`下载任务已启动，将下载 ${selectedLinks.length} 个链接，预计 ${totalWorks} 个作品`, 'success');
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
    
    console.log("🔍 开始收集配置...");
    console.log("📄 当前配置文件:", config);
    
    // 收集链接（从表格中获取，只获取链接输入框）
    // 使用更精确的选择器，只选择表格中第3列（链接列）的输入框
    const linkInputs = document.querySelectorAll('#linksTableBody tr td:nth-child(3) input[type="text"]');
    config.link = Array.from(linkInputs).map(input => input.value).filter(link => link.trim());
    
    console.log("🔗 收集到的链接:", config.link);
    
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
    
    // 收集下载数量设置 - 优先使用配置文件中的值
    console.log("📊 收集下载数量配置...");
    
    // 获取页面输入框的值
    const postNumberInput = document.getElementById('postNumberInput');
    const likeNumberInput = document.getElementById('likeNumberInput');
    const mixNumberInput = document.getElementById('mixNumberInput');
    
    const settingsPostNumberInput = document.getElementById('settingsPostNumberInput');
    const settingsLikeNumberInput = document.getElementById('settingsLikeNumberInput');
    const settingsMixNumberInput = document.getElementById('settingsMixNumberInput');
    
    // 优先使用首页设置，如果首页没有设置则使用设置页面，最后使用配置文件默认值
    const postValue = (postNumberInput && postNumberInput.value !== '') ? 
        parseInt(postNumberInput.value) : 
        (settingsPostNumberInput && settingsPostNumberInput.value !== '') ? 
            parseInt(settingsPostNumberInput.value) : 
            (config.number && config.number.post !== undefined) ? 
                config.number.post : 0;
    
    const likeValue = (likeNumberInput && likeNumberInput.value !== '') ? 
        parseInt(likeNumberInput.value) : 
        (settingsLikeNumberInput && settingsLikeNumberInput.value !== '') ? 
            parseInt(settingsLikeNumberInput.value) : 
            (config.number && config.number.like !== undefined) ? 
                config.number.like : 0;
    
    const mixValue = (mixNumberInput && mixNumberInput.value !== '') ? 
        parseInt(mixNumberInput.value) : 
        (settingsMixNumberInput && settingsMixNumberInput.value !== '') ? 
            parseInt(settingsMixNumberInput.value) : 
            (config.number && config.number.mix !== undefined) ? 
                config.number.mix : 0;
    
    config.number = {
        post: postValue,
        like: likeValue,
        mix: mixValue,
        allmix: config.number ? config.number.allmix : 0,
        music: config.number ? config.number.music : 0
    };
    
    console.log("📊 最终收集的下载数量配置:", config.number);
    console.log("📊 页面输入框值:");
    console.log("  - 首页发布作品:", postNumberInput ? postNumberInput.value : "元素不存在");
    console.log("  - 首页喜欢作品:", likeNumberInput ? likeNumberInput.value : "元素不存在");
    console.log("  - 首页合集:", mixNumberInput ? mixNumberInput.value : "元素不存在");
    console.log("  - 设置页面发布作品:", settingsPostNumberInput ? settingsPostNumberInput.value : "元素不存在");
    console.log("  - 设置页面喜欢作品:", settingsLikeNumberInput ? settingsLikeNumberInput.value : "元素不存在");
    console.log("  - 设置页面合集:", settingsMixNumberInput ? settingsMixNumberInput.value : "元素不存在");
    
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
    
    console.log("✅ 配置收集完成:", config);
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
        
        // 检查下载状态是否发生变化
        if (status.running !== downloadStatus.running) {
            updateDownloadControls(status.running);
            if (status.running) {
                // 开始下载时显示面板并初始化信息
                showDownloadInfoPanel();
                downloadInfo.startTime = new Date();
                // 初始化下载信息
                downloadInfo.totalLinks = status.total_links || 0;
                downloadInfo.completedLinks = status.completed_links || 0;
                downloadInfo.currentLinkIndex = status.current_link_index || 0;
                downloadInfo.currentLink = status.current_link || null;
                downloadInfo.totalWorks = status.total_works || 0;
                // 重置下载统计
                downloadInfo.downloadedCount = 0;
                downloadInfo.failedCount = 0;
                downloadInfo.downloadSpeed = 0;
                downloadInfo.estimatedTime = '--:--';
            } else {
                // 下载停止时隐藏面板
                hideDownloadInfoPanel();
                // 重置下载信息
                downloadInfo = {
                    downloadedCount: 0,
                    failedCount: 0,
                    remainingCount: 0,
                    downloadSpeed: 0,
                    startTime: null,
                    recentDownloads: [],
                    currentFile: null
                };
                
                // 下载完成后自动刷新文件列表和统计信息
                if (downloadStatus.running) {  // 之前是运行状态，现在停止了
                    console.log("🔄 下载完成，自动刷新文件列表和统计信息...");
                    
                    // 立即刷新统计信息
                    updateStatistics();
                    
                    // 延迟一下再刷新文件列表，确保文件系统更新完成
                    setTimeout(async () => {
                        // 刷新文件列表（使用app_simple.js中的函数）
                        if (typeof fileRefreshFiles === 'function') {
                            fileRefreshFiles();
                        }
                        
                        // 再次刷新统计信息，确保文件数量正确
                        await updateStatistics();
                        
                        // 显示完成提示
                        showToast('下载完成，文件列表已更新', 'success');
                    }, 1000);  // 减少延迟到1秒
                }
            }
        }
        
        downloadStatus = status;
        
        // 更新进度条 - 基于文件数量和总作品数量
        let progressPercent = 0;
        const downloaded_files = status.downloaded_files || 0;
        const total_works = status.total_works || 0;
        const total_links = status.total_links || 0;
        const completed_links = status.completed_links || 0;
        
        if (total_works > 0 && downloaded_files > 0) {
            // 如果有总作品数量，基于文件数量计算进度
            progressPercent = Math.min(100, Math.round((downloaded_files / total_works) * 1000) / 10);
        } else if (downloaded_files > 0) {
            // 如果没有总作品数量但有文件数量，假设每个链接平均10个作品
            const estimated_total_files = total_links * 10;
            progressPercent = Math.min(100, Math.round((downloaded_files / estimated_total_files) * 1000) / 10);
        } else if (total_links > 0) {
            // 如果没有文件数量，使用链接进度
            progressPercent = Math.round((completed_links / total_links) * 1000) / 10;
        }
        
        // 如果下载完成，进度条显示100%
        if (!status.running && completed_links >= total_links && total_links > 0) {
            progressPercent = 100;
        }
        
        // 更新进度条
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const currentTask = document.getElementById('currentTask');
        
        if (progressBar && progressText && currentTask) {
            progressBar.style.width = `${progressPercent}%`;
            progressText.textContent = `${progressPercent.toFixed(1)}%`;
            
            // 更新当前任务信息
            let taskText = status.current_task || '等待开始...';
            if (total_works > 0 && downloaded_files > 0) {
                // 显示基于作品数量的进度
                taskText = `已下载 ${downloaded_files}/${total_works} 个作品 (${progressPercent.toFixed(1)}%)`;
            } else if (downloaded_files > 0) {
                // 显示文件数量
                taskText = `已下载 ${downloaded_files} 个文件`;
            } else if (total_links > 0) {
                // 显示链接进度
                taskText = `链接 ${status.current_link_index + 1}/${total_links}: ${taskText}`;
            }
            currentTask.textContent = taskText;
        }
        
        // 更新下载信息面板
        updateDownloadInfoPanel(status);
        
    } catch (error) {
        console.error('获取下载状态失败:', error);
    }
}

// 显示下载信息面板
function showDownloadInfoPanel() {
    const panel = document.getElementById('downloadInfoPanel');
    if (panel) {
        panel.style.display = 'block';
        // 重置下载信息
        downloadInfo = {
            downloadedCount: 0,
            failedCount: 0,
            remainingCount: 0,
            downloadSpeed: 0,
            startTime: new Date(),
            recentDownloads: [],
            currentFile: null
        };
        // 不在这里调用updateDownloadInfoDisplay，等待状态更新
    }
}

// 隐藏下载信息面板
function hideDownloadInfoPanel() {
    const panel = document.getElementById('downloadInfoPanel');
    if (panel) {
        panel.style.display = 'none';
    }
}

// 更新下载信息面板显示
function updateDownloadInfoPanel(status) {
    // 解析当前任务信息
    if (status.current_task) {
        parseCurrentTask(status.current_task);
    }
    
    // 更新统计信息
    updateDownloadStats(status);
    
    // 更新速度和时间
    updateDownloadSpeedAndTime(status);
    
    // 更新显示
    updateDownloadInfoDisplay(status);
}

// 解析当前任务信息
function parseCurrentTask(taskText) {
    // 尝试从任务文本中提取文件名和类型
    const fileNameMatch = taskText.match(/下载[：:]\s*(.+)/);
    if (fileNameMatch) {
        downloadInfo.currentFile = {
            name: fileNameMatch[1],
            type: getFileType(fileNameMatch[1])
        };
    } else {
        downloadInfo.currentFile = {
            name: taskText,
            type: 'unknown'
        };
    }
}

// 获取文件类型
function getFileType(fileName) {
    const ext = fileName.split('.').pop().toLowerCase();
    if (['mp4', 'avi', 'mov', 'mkv'].includes(ext)) return 'video';
    if (['jpg', 'jpeg', 'png', 'gif'].includes(ext)) return 'image';
    if (['mp3', 'wav', 'aac'].includes(ext)) return 'audio';
    return 'file';
}

// 更新下载统计
function updateDownloadStats(status) {
    // 使用真实的下载状态信息
    downloadInfo.downloadedCount = status.downloaded_files || 0;
    downloadInfo.failedCount = status.failed_files || 0;
    downloadInfo.completedLinks = status.completed_links || 0;
    downloadInfo.totalLinks = status.total_links || 0;
    downloadInfo.currentLinkIndex = status.current_link_index || 0;
    downloadInfo.currentLink = status.current_link || null;
    downloadInfo.totalWorks = status.total_works || 0;
    
    // 计算剩余数量
    if (downloadInfo.totalWorks > 0) {
        // 如果有作品数量信息，按作品计算
        downloadInfo.remainingCount = Math.max(0, downloadInfo.totalWorks - downloadInfo.downloadedCount);
    } else {
        // 否则按链接计算
        downloadInfo.remainingCount = Math.max(0, downloadInfo.totalLinks - downloadInfo.completedLinks);
    }
}

// 更新下载速度和时间
function updateDownloadSpeedAndTime(status) {
    if (downloadInfo.startTime && status.start_time) {
        const elapsed = (new Date() - downloadInfo.startTime) / 1000; // 秒
        const downloaded_files = status.downloaded_files || 0;
        const total_works = status.total_works || 0;
        
        if (downloaded_files > 0 && elapsed > 0) {
            // 计算下载速度（基于作品数量）
            const worksPerSecond = downloaded_files / elapsed;
            downloadInfo.downloadSpeed = Math.round(worksPerSecond * 100) / 100; // 作品/秒
            
            // 计算剩余时间
            if (total_works > 0) {
                const remaining = Math.max(0, total_works - downloaded_files);
                const estimatedSeconds = remaining / worksPerSecond;
                downloadInfo.estimatedTime = formatTime(estimatedSeconds);
            } else {
                downloadInfo.estimatedTime = '--:--';
            }
        } else {
            downloadInfo.downloadSpeed = 0;
            downloadInfo.estimatedTime = '--:--';
        }
    }
}

// 格式化时间
function formatTime(seconds) {
    if (seconds < 60) {
        return `${Math.floor(seconds)}s`;
    } else if (seconds < 3600) {
        const minutes = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    } else {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        return `${hours}:${minutes.toString().padStart(2, '0')}`;
    }
}

// 更新下载信息显示
function updateDownloadInfoDisplay(status) {
    // 检查status参数是否存在
    if (!status) {
        console.warn('updateDownloadInfoDisplay: status参数为空');
        return;
    }
    
    // 更新当前下载状态
    const statusElement = document.getElementById('currentDownloadStatus');
    const fileNameElement = document.getElementById('currentFileName');
    const fileTypeElement = document.getElementById('currentFileType');
    
    if (status.running) {
        statusElement.textContent = '下载中';
        statusElement.className = 'badge bg-success';
    } else {
        statusElement.textContent = '已停止';
        statusElement.className = 'badge bg-secondary';
    }
    
    // 显示当前下载信息
    if (status.downloaded_files > 0) {
        // 如果有文件数量信息，显示文件信息
        fileNameElement.textContent = `已下载 ${status.downloaded_files} 个文件`;
        fileTypeElement.textContent = '抖音文件';
    } else if (status.current_link) {
        // 显示当前链接信息
        fileNameElement.textContent = status.current_link;
        fileTypeElement.textContent = '抖音链接';
    } else if (status.total_links > 0) {
        fileNameElement.textContent = `链接 ${status.current_link_index + 1}/${status.total_links}`;
        fileTypeElement.textContent = '等待开始...';
    } else {
        fileNameElement.textContent = '等待开始...';
        fileTypeElement.textContent = '-';
    }
    
    // 更新统计
    document.getElementById('downloadedCount').textContent = status.downloaded_files || 0;
    document.getElementById('failedCount').textContent = status.failed_files || 0;
    
    // 显示剩余数量
    const total_works = status.total_works || 0;
    const downloaded_files = status.downloaded_files || 0;
    if (total_works > 0) {
        const remaining = Math.max(0, total_works - downloaded_files);
        document.getElementById('remainingCount').textContent = remaining;
    } else {
        document.getElementById('remainingCount').textContent = '-';
    }
    
    // 更新速度和时间
    const speedUnit = '作品/秒';
    document.getElementById('downloadSpeed').textContent = `${downloadInfo.downloadSpeed} ${speedUnit}`;
    document.getElementById('estimatedTime').textContent = downloadInfo.estimatedTime || '--:--';
    
    // 更新最近下载列表
    updateRecentDownloadsList();
}

// 更新最近下载列表
function updateRecentDownloadsList() {
    const listElement = document.getElementById('recentDownloadsList');
    
    if (downloadInfo.recentDownloads.length === 0) {
        listElement.innerHTML = `
            <div class="text-muted text-center py-2">
                <small>暂无下载记录</small>
            </div>
        `;
        return;
    }
    
    const recentItems = downloadInfo.recentDownloads.slice(-5).map(item => `
        <div class="recent-item">
            <div class="recent-item-name">${item.name}</div>
            <div class="recent-item-status ${item.status}">${item.status}</div>
        </div>
    `).join('');
    
    listElement.innerHTML = recentItems;
}

// 添加下载记录
function addDownloadRecord(name, status) {
    downloadInfo.recentDownloads.push({
        name: name,
        status: status,
        time: new Date()
    });
    
    // 保持最近10条记录
    if (downloadInfo.recentDownloads.length > 10) {
        downloadInfo.recentDownloads = downloadInfo.recentDownloads.slice(-10);
    }
    
    updateRecentDownloadsList();
}

// 保存配置
async function saveConfig() {
    try {
        syncDownloadNumbers(); // 同步设置
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
            showToast('配置保存成功', 'success');
            currentConfig = config;
        } else {
            showToast(result.message || '保存配置失败', 'error');
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
async function updateStatistics() {
    const links = currentConfig.link || [];
    document.getElementById('totalLinks').textContent = links.length;
    
    // 如果有文件统计元素，也更新文件统计
    const totalFilesElement = document.getElementById('totalFiles');
    if (totalFilesElement) {
        try {
            // 从后端获取最新的文件列表来更新统计
            const response = await fetch('/api/files');
            if (response.ok) {
                const files = await response.json();
                totalFilesElement.textContent = files.length;
                console.log(`📊 更新文件统计: ${files.length} 个文件`);
            }
        } catch (error) {
            console.error('获取文件统计失败:', error);
            // 如果获取失败，尝试使用本地变量
            if (typeof fileAllFiles !== 'undefined') {
                totalFilesElement.textContent = fileAllFiles.length;
            }
        }
    }
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

// 同步下载数量设置
function syncDownloadNumbers() {
    // 从设置页面同步到首页
    const settingsPost = document.getElementById('settingsPostNumberInput')?.value || 0;
    const settingsLike = document.getElementById('settingsLikeNumberInput')?.value || 0;
    const settingsMix = document.getElementById('settingsMixNumberInput')?.value || 0;
    
    if (document.getElementById('postNumberInput')) {
        document.getElementById('postNumberInput').value = settingsPost;
    }
    if (document.getElementById('likeNumberInput')) {
        document.getElementById('likeNumberInput').value = settingsLike;
    }
    if (document.getElementById('mixNumberInput')) {
        document.getElementById('mixNumberInput').value = settingsMix;
    }
} 

// 调试函数：检查页面配置读取
function debugConfigReading() {
    console.log("🔍 调试配置读取...");
    
    // 检查首页下载数量输入框
    const postNumberInput = document.getElementById('postNumberInput');
    const likeNumberInput = document.getElementById('likeNumberInput');
    const mixNumberInput = document.getElementById('mixNumberInput');
    
    console.log("首页下载数量输入框:");
    console.log("  - postNumberInput:", postNumberInput ? postNumberInput.value : "元素不存在");
    console.log("  - likeNumberInput:", likeNumberInput ? likeNumberInput.value : "元素不存在");
    console.log("  - mixNumberInput:", mixNumberInput ? mixNumberInput.value : "元素不存在");
    
    // 检查设置页面下载数量输入框
    const settingsPostNumberInput = document.getElementById('settingsPostNumberInput');
    const settingsLikeNumberInput = document.getElementById('settingsLikeNumberInput');
    const settingsMixNumberInput = document.getElementById('settingsMixNumberInput');
    
    console.log("设置页面下载数量输入框:");
    console.log("  - settingsPostNumberInput:", settingsPostNumberInput ? settingsPostNumberInput.value : "元素不存在");
    console.log("  - settingsLikeNumberInput:", settingsLikeNumberInput ? settingsLikeNumberInput.value : "元素不存在");
    console.log("  - settingsMixNumberInput:", settingsMixNumberInput ? settingsMixNumberInput.value : "元素不存在");
    
    // 检查当前配置
    console.log("当前配置:", currentConfig);
    
    // 测试收集配置
    const collectedConfig = collectCurrentConfig();
    console.log("收集的配置:", collectedConfig);
    console.log("收集的下载数量:", collectedConfig.number);
}

// 在页面加载完成后添加调试按钮（仅在开发模式下）
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    document.addEventListener('DOMContentLoaded', function() {
        // 添加调试按钮到页面
        const debugBtn = document.createElement('button');
        debugBtn.textContent = '🔍 调试配置';
        debugBtn.style.cssText = 'position: fixed; top: 10px; right: 10px; z-index: 9999; padding: 5px 10px; background: #ff6b6b; color: white; border: none; border-radius: 4px; cursor: pointer;';
        debugBtn.onclick = debugConfigReading;
        document.body.appendChild(debugBtn);
    });
} 

// 全选/取消全选链接
function toggleAllLinks() {
    const selectAllCheckbox = document.getElementById('selectAllLinks');
    const linkCheckboxes = document.querySelectorAll('.link-checkbox');
    
    linkCheckboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });
}

// 更新全选复选框状态
function updateSelectAllCheckbox() {
    const selectAllCheckbox = document.getElementById('selectAllLinks');
    const linkCheckboxes = document.querySelectorAll('.link-checkbox');
    
    if (linkCheckboxes.length === 0) {
        selectAllCheckbox.checked = false;
        selectAllCheckbox.indeterminate = false;
        document.getElementById('selectedLinksCount').textContent = '0';
        return;
    }
    
    const checkedCount = Array.from(linkCheckboxes).filter(cb => cb.checked).length;
    
    // 更新选中链接数量显示
    document.getElementById('selectedLinksCount').textContent = checkedCount;
    
    if (checkedCount === 0) {
        selectAllCheckbox.checked = false;
        selectAllCheckbox.indeterminate = false;
    } else if (checkedCount === linkCheckboxes.length) {
        selectAllCheckbox.checked = true;
        selectAllCheckbox.indeterminate = false;
    } else {
        selectAllCheckbox.checked = false;
        selectAllCheckbox.indeterminate = true;
    }
}

// 获取选中的链接
function getSelectedLinks() {
    const linkCheckboxes = document.querySelectorAll('.link-checkbox:checked');
    const selectedLinks = [];
    
    linkCheckboxes.forEach(checkbox => {
        const index = parseInt(checkbox.value);
        // 直接从当前配置中获取链接，确保索引正确
        if (currentConfig.link && currentConfig.link[index]) {
            selectedLinks.push(currentConfig.link[index]);
        }
    });
    
    console.log(`📋 选中的链接数量: ${selectedLinks.length}`);
    return selectedLinks;
}

// 监听复选框变化
document.addEventListener('change', function(e) {
    if (e.target.classList.contains('link-checkbox')) {
        updateSelectAllCheckbox();
        // 移除自动删除链接的逻辑，只更新选中状态
    }
}); 

// 从配置中移除链接（仅在删除按钮点击时调用）
function removeLinkFromConfig(index) {
    if (currentConfig.link && currentConfig.link[index]) {
        console.log(`🗑️ 从配置中移除链接 ${index}: ${currentConfig.link[index]}`);
        
        // 从配置中移除链接
        currentConfig.link.splice(index, 1);
        
        // 从链接数据中移除
        if (linksData[index]) {
            linksData.splice(index, 1);
        }
        
        // 重新渲染链接列表
        updateLinksDisplay(currentConfig.link);
        
        // 保存配置到服务器
        saveConfigToServer();
    }
}

// 保存配置到服务器
async function saveConfigToServer() {
    try {
        console.log('💾 保存配置到服务器...');
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(currentConfig)
        });
        
        const result = await response.json();
        if (result.success) {
            console.log('✅ 配置保存成功');
        } else {
            console.error('❌ 配置保存失败:', result.message);
            showToast('配置保存失败', 'error');
        }
    } catch (error) {
        console.error('❌ 保存配置失败:', error);
        showToast('保存配置失败', 'error');
    }
}

// 获取用户作品数量
async function fetchUserWorkCount(secUid, index) {
    try {
        const response = await fetch('/api/user/work-count', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sec_uid: secUid })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 更新表格中的作品数量
            const tbody = document.getElementById('linksTableBody');
            const row = tbody.children[index];
            if (row) {
                const countCell = row.children[5];
                countCell.innerHTML = `<span class="fw-bold text-primary">${result.work_count}</span>`;
                
                // 更新链接数据
                if (linksData[index]) {
                    linksData[index].work_count = result.work_count;
                }
            }
        } else {
            // 显示获取失败
            const tbody = document.getElementById('linksTableBody');
            const row = tbody.children[index];
            if (row) {
                const countCell = row.children[5];
                countCell.innerHTML = '<span class="text-warning">获取失败</span>';
            }
        }
    } catch (error) {
        console.error('获取用户作品数量失败:', error);
        const tbody = document.getElementById('linksTableBody');
        const row = tbody.children[index];
        if (row) {
            const countCell = row.children[5];
            countCell.innerHTML = '<span class="text-warning">网络错误</span>';
        }
    }
} 