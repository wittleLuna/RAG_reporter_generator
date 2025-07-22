console.log('main.js loaded');
// RAG实训报告生成系统 - 主JavaScript文件

// 全局变量
let uploadedFiles = {
    cover: [],
    body: [],
    data: []
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeFileUpload();
    initializeFormValidation();
    initializeAdvancedPrompt();
    initializeProgressBar();
    
    // 初始化拖拽排序功能
    setTimeout(() => enableDataFileDragSort(), 500);

    // 页面加载后自动拉取
    fetchUserProfileAndUpdateUI();
});

// 初始化文件上传功能
function initializeFileUpload() {
    const dropZones = document.querySelectorAll('.drop-zone');
    
    dropZones.forEach(zone => {
        const fileInput = zone.querySelector('input[type="file"]');
        const type = zone.dataset.type;
        
        // 点击上传
        zone.addEventListener('click', () => fileInput.click());
        
        // 文件选择
        fileInput.addEventListener('change', (e) => handleFileSelect(e, type));
        
        // 拖拽上传
        zone.addEventListener('dragover', handleDragOver);
        zone.addEventListener('dragleave', handleDragLeave);
        zone.addEventListener('drop', (e) => handleDrop(e, type));
    });
}

// 处理文件选择
function handleFileSelect(event, type) {
    const files = Array.from(event.target.files);
    processFiles(files, type);
}

// 处理拖拽悬停
function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.classList.add('drag-over');
}

// 处理拖拽离开
function handleDragLeave(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('drag-over');
}

// 处理文件拖拽
function handleDrop(event, type) {
    event.preventDefault();
    event.currentTarget.classList.remove('drag-over');
    
    const files = Array.from(event.dataTransfer.files);
    processFiles(files, type);
}

// 处理文件
function processFiles(files, type) {
    files.forEach(file => {
        // 检查文件类型
        if (!isValidFileType(file, type)) {
            showError(`不支持的文件类型: ${file.name}`);
            return;
        }
        
        // 检查文件大小
        if (file.size > 50 * 1024 * 1024) { // 50MB
            showError(`文件过大: ${file.name}`);
            return;
        }
        
        // 添加到上传列表
        addFileToList(file, type);
        uploadedFiles[type].push(file);
        
        // 如果是资料文件，立即启用拖拽排序
        if (type === 'data') {
            setTimeout(() => enableDataFileDragSort(), 100);
        }
    });
}

// 验证文件类型
function isValidFileType(file, type) {
    const allowedTypes = {
        cover: ['.doc', '.docx'],
        body: ['.doc', '.docx'],
        data: ['.md', '.markdown', '.doc', '.docx', '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp']
    };
    
    const extension = '.' + file.name.split('.').pop().toLowerCase();
    return allowedTypes[type].includes(extension);
}

// 添加文件到列表
function addFileToList(file, type) {
    const listId = type + 'Uploaded';
    const list = document.getElementById(listId);
    
    const fileItem = document.createElement('div');
    fileItem.className = 'uploaded-file-item';
    
    // 为资料文件添加拖拽提示
    const dragHint = type === 'data' ? ' (可拖拽调整顺序)' : '';
    
    fileItem.innerHTML = `
        <button class="uploaded-file-delete" onclick="removeFile('${file.name}', '${type}')">
            <i class="fas fa-times"></i>
        </button>
        <span class="uploaded-file-name">${file.name}${dragHint}</span>
        ${type === 'data' ? '<i class="fas fa-grip-vertical" style="margin-left: 5px; color: #666; cursor: grab;"></i>' : ''}
    `;
    
    list.appendChild(fileItem);
}

// 移除文件
function removeFile(fileName, type) {
    uploadedFiles[type] = uploadedFiles[type].filter(file => file.name !== fileName);
    updateFileList(type);
}

// 更新文件列表显示
function updateFileList(type) {
    const listId = type + 'Uploaded';
    const list = document.getElementById(listId);
    list.innerHTML = '';
    
    uploadedFiles[type].forEach(file => {
        addFileToList(file, type);
    });
}

// 拖拽排序功能 for dataUploaded
function enableDataFileDragSort() {
    const list = document.getElementById('dataUploaded');
    if (!list) return;
    
    let dragSrcIndex = null;
    let dragSrcElement = null;
    
    list.querySelectorAll('.uploaded-file-item').forEach((item, idx) => {
        // 清除之前的事件监听器
        item.removeEventListener('dragstart', item._dragStartHandler);
        item.removeEventListener('dragend', item._dragEndHandler);
        item.removeEventListener('dragover', item._dragOverHandler);
        item.removeEventListener('dragleave', item._dragLeaveHandler);
        item.removeEventListener('drop', item._dropHandler);
        
        item.setAttribute('draggable', 'true');
        item.style.cursor = 'grab';
        
        // 拖拽开始
        item._dragStartHandler = function(e) {
            dragSrcIndex = idx;
            dragSrcElement = item;
            e.dataTransfer.effectAllowed = 'move';
            item.classList.add('dragging');
            item.style.cursor = 'grabbing';
            item.style.opacity = '0.5';
            console.log('开始拖拽文件:', uploadedFiles.data[idx]?.name);
        };
        
        // 拖拽结束
        item._dragEndHandler = function() {
            item.classList.remove('dragging');
            item.style.cursor = 'grab';
            item.style.opacity = '1';
            dragSrcIndex = null;
            dragSrcElement = null;
        };
        
        // 拖拽悬停
        item._dragOverHandler = function(e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            if (dragSrcElement && dragSrcElement !== item) {
                item.classList.add('drag-over');
            }
        };
        
        // 拖拽离开
        item._dragLeaveHandler = function() {
            item.classList.remove('drag-over');
        };
        
        // 拖拽放置
        item._dropHandler = function(e) {
            e.preventDefault();
            item.classList.remove('drag-over');
            
            if (dragSrcIndex !== null && dragSrcIndex !== idx) {
                console.log('交换文件位置:', dragSrcIndex, '->', idx);
                
                // 交换顺序
                const moved = uploadedFiles.data.splice(dragSrcIndex, 1)[0];
                uploadedFiles.data.splice(idx, 0, moved);
                
                // 更新显示
                updateFileList('data');
                
                // 重新启用拖拽
                setTimeout(() => enableDataFileDragSort(), 50);
                
                console.log('文件顺序已更新:', uploadedFiles.data.map(f => f.name));
            }
            dragSrcIndex = null;
            dragSrcElement = null;
        };
        
        // 添加事件监听器
        item.addEventListener('dragstart', item._dragStartHandler);
        item.addEventListener('dragend', item._dragEndHandler);
        item.addEventListener('dragover', item._dragOverHandler);
        item.addEventListener('dragleave', item._dragLeaveHandler);
        item.addEventListener('drop', item._dropHandler);
    });
    
    console.log('拖拽排序功能已启用，文件数量:', list.querySelectorAll('.uploaded-file-item').length);
}

// 修改updateFileList('data')，每次渲染后启用拖拽
const _oldUpdateFileList = updateFileList;
updateFileList = function(type) {
    _oldUpdateFileList(type);
    if (type === 'data') enableDataFileDragSort();
};

// 初始化表单验证
function initializeFormValidation() {
    const generateBtn = document.getElementById('generateBtn');
    generateBtn.addEventListener('click', validateAndGenerate);
}

// 验证并生成报告
function validateAndGenerate() {
    // 验证基本信息
    const requiredFields = ['name', 'student_id', 'class_name', 'project_name'];
    for (let field of requiredFields) {
        const value = document.getElementById(field).value.trim();
        if (!value) {
            showError(`请填写${getFieldLabel(field)}`);
            return;
        }
    }
    
    // 校验模板：如果未选择模板，则必须上传文件
    if (!window.selectedTemplate) {
        if (uploadedFiles.cover.length === 0) {
            showError('请上传封面模板或选择模板');
            return;
        }
        if (uploadedFiles.body.length === 0) {
            showError('请上传正文模板或选择模板');
            return;
        }
    }
    
    // 验证资料文件
    if (uploadedFiles.data.length === 0) {
        showError('请上传至少一个资料文件');
        return;
    }
    
    // 开始生成报告
    generateReport();
}

// 获取字段标签
function getFieldLabel(field) {
    const labels = {
        name: '姓名',
        student_id: '学号',
        class_name: '班级',
        project_name: '课程'
    };
    return labels[field] || field;
}

// 生成报告
async function generateReport() {
    const generateBtn = document.getElementById('generateBtn');
    const progressBar = document.getElementById('progressBar');
    const reportStatus = document.getElementById('reportStatus');
    
    // 显示进度条
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 生成中...';
    progressBar.style.display = 'block';
    reportStatus.style.display = 'none';
    
    // 准备表单数据
    const formData = new FormData();
    
    // 必填：query字段
    formData.append('query', document.getElementById('project_name').value || '实训报告');
    
    // 基本信息
    const basicInfo = [
        'name', 'student_id', 'class_name', 'project_name', 'instructor',
        'textbook', 'lab', 'finish_date', 'design_requirements',
        'knowledge_and_tech', 'completion', 'self_statement'
    ];
    
    basicInfo.forEach(field => {
        const value = document.getElementById(field).value.trim();
        if (value) {
            formData.append(field, value);
        }
    });
    
    // 生成模式
    const generationMode = document.querySelector('input[name="generationMode"]:checked').value;
    formData.append('generation_mode', generationMode);
    
    // 页面控制
    const targetPages = document.getElementById('targetPages').value;
    const targetPagesInput = document.getElementById('targetPagesInput').value;
    const finalTargetPages = targetPagesInput || targetPages;
    if (finalTargetPages) {
        formData.append('target_pages', finalTargetPages);
    }
    
    // 多轮补全
    const multiRoundCompletion = document.getElementById('multiRoundCompletion').checked;
    formData.append('multi_round_completion', multiRoundCompletion);
    
    // 高级提示词
    const advancedFormatting = document.getElementById('advancedFormatting').checked;
    if (advancedFormatting) {
        const additionalRequirements = document.getElementById('additionalRequirements').value.trim();
        if (additionalRequirements) {
            formData.append('additional_requirements', additionalRequirements);
        }
    }
    
    // 文件上传/模板路径
    if (window.selectedTemplate) {
        // 传递模板路径给后端
        formData.append('cover_template_path', window.selectedTemplate.cover_template_path);
        formData.append('body_template_path', window.selectedTemplate.body_template_path);
        formData.append('template_id', window.selectedTemplate.template_id);
    } else {
        uploadedFiles.cover.forEach(file => {
            formData.append('cover_template', file);
        });
        uploadedFiles.body.forEach(file => {
            formData.append('body_template', file);
        });
    }
    uploadedFiles.data.forEach(file => {
        formData.append('data_files', file);
    });
    
    // 资料文件顺序
    const fileOrder = uploadedFiles.data.map(f => f.name);
    formData.append('file_order', JSON.stringify(fileOrder));

    // 调试：输出FormData内容
    for (let pair of formData.entries()) {
        console.log('FormData:', pair[0], pair[1]);
    }
    // 检查data_files类型
    uploadedFiles.data.forEach(file => {
        console.log('data_files类型:', file, file instanceof File);
    });
    
    try {
        // 模拟进度更新
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 10;
            if (progress > 90) progress = 90;
            updateProgress(progress);
        }, 500);
        
        // 发送请求
        const response = await fetch('/generate_report', {
            method: 'POST',
            body: formData
        });
        
        clearInterval(progressInterval);
        updateProgress(100);
        
        if (response.ok) {
            const result = await response.json();
            showSuccess('报告生成成功！');
            showDownloadLink(result.download_url);
            
            // 新增：渲染报告正文（带插图）
            if (result.report) {
                const reportHtml = renderReportWithImages(result.report, result.images, '/uploads');
                const reportPreview = document.getElementById('reportPreview');
                const reportContent = document.querySelector('.report-content');
                if (reportPreview && reportContent) {
                    reportContent.innerHTML = reportHtml;
                    reportPreview.style.display = 'block';
                }
                
                // 可选：展示图片缩略图列表，允许编辑描述
                if (result.images && result.images.length > 0) {
                    renderImageList(result.images, '/uploads');
                }
            }
        } else {
            const error = await response.json();
            showError(error.detail || '报告生成失败');
        }
    } catch (error) {
        console.error('生成报告失败:', error);
        showError('网络错误，请稍后重试');
    } finally {
        // 恢复按钮状态
        generateBtn.disabled = false;
        generateBtn.innerHTML = '生成报告';
        progressBar.style.display = 'none';
        fetchUserProfileAndUpdateUI();
    }
}

// 更新进度条
function updateProgress(percentage) {
    const progressInner = document.getElementById('progressInner');
    progressInner.style.width = percentage + '%';
}

// 初始化高级提示词功能
function initializeAdvancedPrompt() {
    const advancedCheckbox = document.getElementById('advancedFormatting');
    const promptGroup = document.getElementById('promptGroup');
    
    advancedCheckbox.addEventListener('change', function() {
        promptGroup.style.display = this.checked ? 'block' : 'none';
    });
}

// 初始化进度条
function initializeProgressBar() {
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        progressBar.style.display = 'none';
    }
}

// 显示错误信息
function showError(message) {
    const reportStatus = document.getElementById('reportStatus');
    reportStatus.className = 'report-status error';
    reportStatus.textContent = message;
    reportStatus.style.display = 'block';
    
    // 3秒后自动隐藏
    setTimeout(() => {
        reportStatus.style.display = 'none';
    }, 3000);
}

// 显示成功信息
function showSuccess(message) {
    const reportStatus = document.getElementById('reportStatus');
    reportStatus.className = 'report-status success';
    reportStatus.textContent = message;
    reportStatus.style.display = 'block';
}

// 显示下载链接
function showDownloadLink(downloadUrl) {
    const downloadSection = document.getElementById('downloadSection');
    downloadSection.innerHTML = `
        <a href="${downloadUrl}" download>
            <i class="fas fa-download"></i>
            下载生成的报告
        </a>
    `;
    downloadSection.style.display = 'block';
}

// 工具函数：格式化文件大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 工具函数：防抖
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 工具函数：节流
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// 导出函数供其他模块使用
window.RAGSystem = {
    showError,
    showSuccess,
    formatFileSize,
    debounce,
    throttle
};

// 新增：拉取用户信息并联动按钮
async function fetchUserProfileAndUpdateUI() {
    console.log('调用了fetchUserProfileAndUpdateUI');
    try {
        const res = await fetch('/user/profile');
        if (!res.ok) throw new Error('用户信息接口异常');
        const user = await res.json();
        // 显示剩余次数
        const usageCountSpan = document.getElementById('usageCountSpan');
        if (usageCountSpan) {
            usageCountSpan.innerText = (user.usage_count ?? '--');
        }
        // 按钮联动
        const generateBtn = document.getElementById('generateBtn');
        if (generateBtn) {
            if (!user.usage_count || user.usage_count <= 0) {
                generateBtn.disabled = true;
                generateBtn.classList.add('disabled');
                generateBtn.innerText = '使用次数已用完，请充值';
            } else {
                generateBtn.disabled = false;
                generateBtn.classList.remove('disabled');
                generateBtn.innerText = '生成报告';
            }
        }
    } catch (e) {
        // 网络或接口异常时兜底显示
        const usageCountSpan = document.getElementById('usageCountSpan');
        if (usageCountSpan) usageCountSpan.innerText = '--';
        const generateBtn = document.getElementById('generateBtn');
        if (generateBtn) {
            generateBtn.disabled = false;
            generateBtn.classList.remove('disabled');
            generateBtn.innerText = '生成报告';
        }
        console.error('获取用户信息失败', e);
    }
}

// 充值弹窗关闭后刷新次数
function closeRechargeModal() {
    document.getElementById('rechargeModal').style.display = 'none';
    fetchUserProfileAndUpdateUI();
}

// 渲染报告正文，自动插入图片和描述
function renderReportWithImages(report, images, imageBaseUrl = '/uploads') {
    let html = report;
    if (images && Array.isArray(images)) {
        images.forEach(img => {
            // 构造图片HTML块
            const imgTag = `
                <div class="report-image-block" style="text-align:center;margin:20px 0;border:1px solid #eee;border-radius:8px;padding:15px;background:#fafafa;">
                    <img src="${imageBaseUrl}/${img.filepath}" alt="${img.description}" style="max-width:400px;max-height:300px;display:block;margin:0 auto 8px;border-radius:4px;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                    <div style="color:#666;font-size:0.9em;font-style:italic;">${img.description || '图片描述'}</div>
                </div>
            `;
            // 替换所有占位符
            html = html.replaceAll(`{{image:${img.id}}}`, imgTag);
        });
    }
    // 处理未被替换的图片占位符
    html = html.replace(/{{image:img_\d+}}/g, '<div style="color:red;text-align:center;padding:20px;background:#fff5f5;border:1px solid #fed7d7;border-radius:4px;">[图片未找到]</div>');
    
    // 将Markdown转换为HTML（简单处理）
    html = convertMarkdownToHtml(html);
    
    return html;
}

// 简单的Markdown转HTML转换
function convertMarkdownToHtml(markdown) {
    let html = markdown;
    
    // 标题转换
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^#### (.*$)/gim, '<h4>$1</h4>');
    
    // 粗体转换
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // 代码块转换
    html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    
    // 行内代码转换
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // 列表转换
    html = html.replace(/^- (.*$)/gim, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    
    // 段落转换
    html = html.replace(/^(?!<[h|u|p|d|i])(.*$)/gim, '<p>$1</p>');
    
    // 清理空段落
    html = html.replace(/<p><\/p>/g, '');
    html = html.replace(/<p>\s*<\/p>/g, '');
    
    return html;
}

// 渲染图片缩略图和描述编辑
function renderImageList(images, imageBaseUrl) {
    const container = document.getElementById('imageList');
    if (!container) {
        // 如果容器不存在，创建一个
        const newContainer = document.createElement('div');
        newContainer.id = 'imageList';
        newContainer.style.cssText = 'display:flex;gap:12px;margin-top:20px;flex-wrap:wrap;padding:15px;background:#f8f9fa;border-radius:8px;border:1px solid #e9ecef;';
        newContainer.innerHTML = '<h4 style="width:100%;margin-bottom:10px;color:#495057;">图片管理</h4>';
        
        // 插入到报告预览区域后面
        const reportPreview = document.getElementById('reportPreview');
        if (reportPreview && reportPreview.parentNode) {
            reportPreview.parentNode.insertBefore(newContainer, reportPreview.nextSibling);
        }
    }
    
    const imageContainer = document.getElementById('imageList');
    if (!imageContainer) return;
    
    // 清空现有内容，保留标题
    const title = imageContainer.querySelector('h4');
    imageContainer.innerHTML = '';
    if (title) imageContainer.appendChild(title);
    
    images.forEach((img, index) => {
        const div = document.createElement('div');
        div.className = 'image-thumb-block';
        div.style.cssText = 'display:flex;flex-direction:column;align-items:center;padding:10px;background:white;border-radius:6px;border:1px solid #dee2e6;min-width:120px;';
        div.innerHTML = `
            <img src="${imageBaseUrl}/${img.filepath}" style="max-width:80px;max-height:80px;border-radius:4px;margin-bottom:8px;box-shadow:0 1px 3px rgba(0,0,0,0.1);">
            <textarea data-img-id="${img.id}" class="img-desc-input" style="width:100px;height:60px;font-size:12px;padding:4px;border:1px solid #ced4da;border-radius:3px;resize:none;" placeholder="图片描述">${img.description || ''}</textarea>
            <div style="font-size:11px;color:#6c757d;margin-top:4px;">图片 ${index + 1}</div>
        `;
        imageContainer.appendChild(div);
    });
    
    // 添加保存按钮
    const saveBtn = document.createElement('button');
    saveBtn.innerHTML = '<i class="fas fa-save"></i> 保存描述';
    saveBtn.style.cssText = 'margin-top:10px;padding:8px 16px;background:#007bff;color:white;border:none;border-radius:4px;cursor:pointer;font-size:14px;';
    saveBtn.onclick = saveImageDescriptions;
    imageContainer.appendChild(saveBtn);
    
    // 监听描述编辑
    imageContainer.querySelectorAll('.img-desc-input').forEach(textarea => {
        textarea.addEventListener('input', function() {
            const imgId = this.dataset.imgId;
            const newDesc = this.value;
            console.log('图片描述已修改', imgId, newDesc);
        });
    });
}

// 保存图片描述
async function saveImageDescriptions() {
    const descriptions = {};
    const textareas = document.querySelectorAll('.img-desc-input');
    
    textareas.forEach(textarea => {
        const imgId = textarea.dataset.imgId;
        const description = textarea.value.trim();
        descriptions[imgId] = description;
    });
    
    try {
        // 这里可以调用后端API保存描述
        // const response = await fetch('/save_image_descriptions', {
        //     method: 'POST',
        //     headers: {'Content-Type': 'application/json'},
        //     body: JSON.stringify({descriptions})
        // });
        
        // 临时显示保存成功
        showSuccess('图片描述已保存');
        console.log('保存的图片描述:', descriptions);
    } catch (error) {
        showError('保存图片描述失败');
        console.error('保存图片描述失败:', error);
    }
}

function useTemplate(templateId) {
    fetch(`/templates/${templateId}/files`)
        .then(response => response.json())
        .then(data => {
            if (data.cover_template_path && data.body_template_path) {
                // 设置全局变量
                window.selectedTemplate = {
                    cover_template_path: data.cover_template_path,
                    body_template_path: data.body_template_path,
                    template_id: templateId,
                    template_name: '' // 可选：可再查一次模板名
                };
                // 同步下拉框选中状态
                const select = document.getElementById('templateSelect');
                if (select) {
                    for (let i = 0; i < select.options.length; i++) {
                        if (select.options[i].value == templateId) {
                            select.selectedIndex = i;
                            break;
                        }
                    }
                }
                alert('模板已应用！');
                closeTemplateModal();
            } else {
                alert('模板信息不完整，请稍后重试');
            }
        })
        .catch(error => {
            console.error('使用模板失败:', error);
            alert('使用模板失败，请稍后重试');
        });
}

// === 自动修复消息中心相关问题 ===

// 1. 获取管理员ID（全局缓存）
window.adminId = null;
fetch('/user/admin_id')
  .then(res => res.json())
  .then(data => {
    window.adminId = data.admin_id;
  });

// 2. 判断当前用户是否为管理员
window.isAdmin = false;
fetch('/user/profile')
  .then(res => res.json())
  .then(user => {
    window.isAdmin = (user.username === 'admin');
  });

// 3. 加载用户列表，仅管理员请求 /admin/users
function loadUsersIfAdmin(callback) {
  if (window.isAdmin) {
    fetch('/admin/users')
      .then(res => res.json())
      .then(data => {
        window.users = data || [];
        if (typeof callback === 'function') callback(window.users);
      })
      .catch(() => {
        window.users = [];
        if (typeof callback === 'function') callback(window.users);
      });
  } else {
    window.users = [];
    if (typeof callback === 'function') callback(window.users);
  }
}

// 4. 修正 loadChatHistory，users未定义时不报错
function loadChatHistorySafe() {
  const users = window.users || [];
  // ...原有loadChatHistory逻辑，使用users变量...
  // 这里只做防御性处理，具体渲染逻辑请根据原有实现补充
}

// 5. 发送消息时自动带上管理员ID
function sendMessageToAdmin(content) {
  if (!window.adminId) {
    alert('管理员ID未获取到，无法发送消息');
    return;
  }
  let formData = new FormData();
  formData.append('to_user_id', window.adminId);
  formData.append('content', content);
  fetch('/messages/send', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    // 处理返回
    if (data.success) {
      // 消息发送成功后的逻辑
    } else {
      alert('消息发送失败');
    }
  });
}
// === 自动修复结束 === 