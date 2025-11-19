document.addEventListener('DOMContentLoaded', function() {
    // 初始化功能
    initTabs();
    initAddWish();
    initToggleStatus();
    initWishCards();
    initModal();
    initToast();
});

// 当前编辑的愿望数据
let currentWishData = {};
let newImages = [];

/**
 * 初始化Tab标签切换
 */
function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            this.classList.add('active');
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
}

/**
 * 初始化添加愿望
 */
function initAddWish() {
    const addBtn = document.querySelector('.add-btn');
    const wishInput = document.querySelector('.wish-input');

    if (!addBtn || !wishInput) return;

    addBtn.addEventListener('click', async function() {
        await submitWish();
    });

    wishInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            submitWish();
        }
    });

    async function submitWish() {
        const content = wishInput.value.trim();

        if (!content) {
            showToast('请输入愿望内容！', 'warning');
            return;
        }

        try {
            const response = await fetch('/wishlist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `wish=${encodeURIComponent(content)}`
            });

            if (response.ok) {
                wishInput.value = '';
                showToast('愿望添加成功！', 'success');
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                showToast('添加失败，请重试！', 'error');
            }
        } catch (error) {
            console.error('添加愿望出错：', error);
            showToast('网络错误，请稍后重试！', 'error');
        }
    }
}

/**
 * 初始化愿望状态切换
 */
function initToggleStatus() {
    const toggleBtns = document.querySelectorAll('.toggle-btn');

    toggleBtns.forEach(btn => {
        btn.addEventListener('click', async function(e) {
            // 阻止事件冒泡到卡片点击
            e.stopPropagation();

            const index = this.getAttribute('data-index');
            const isCompleted = this.classList.contains('completed');

            try {
                const response = await fetch(`/wishlist/toggle/${index}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `checked=${!isCompleted}`
                });

                if (response.ok) {
                    showToast(isCompleted ? '已标记为未完成' : '已标记为已完成', 'success');
                    setTimeout(() => {
                        window.location.reload();
                    }, 800);
                } else {
                    showToast('状态更新失败', 'error');
                }
            } catch (error) {
                console.error('切换状态出错：', error);
                showToast('网络错误，状态更新失败', 'error');
            }
        });
    });
}

/**
 * 初始化愿望卡片点击事件
 */
function initWishCards() {
    const wishCards = document.querySelectorAll('.wish-card');

    wishCards.forEach(card => {
        card.addEventListener('click', function() {
            const index = this.getAttribute('data-index');
            const id = this.getAttribute('data-id');
            const title = this.querySelector('.wish-title').textContent;
            const desc = this.querySelector('.wish-desc').textContent;

            // 获取已上传的图片
            const imageElements = this.querySelectorAll('.wish-image img');
            const images = [];
            imageElements.forEach(img => {
                const src = img.getAttribute('src');
                if (src) {
                    images.push(src.split('/').pop());
                }
            });

            // 设置当前愿望数据
            currentWishData = {
                index,
                id,
                title,
                desc: desc,
                images
            };

            // 打开模态框
            openModal();
        });
    });
}

/**
 * 初始化模态框
 */
function initModal() {
    const modal = document.getElementById('wishModal');
    const closeBtn = document.querySelector('.close-btn');
    const cancelBtn = document.getElementById('cancelBtn');
    const saveBtn = document.getElementById('saveBtn');
    const wishImages = document.getElementById('wishImages');

    // 关闭模态框
    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);

    // 点击模态框外部关闭
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // 图片上传预览
    wishImages.addEventListener('change', function(e) {
        const files = e.target.files;
        if (!files.length) return;

        const previewContainer = document.getElementById('previewImages');

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            if (!file.type.startsWith('image/')) continue;

            const reader = new FileReader();
            reader.onload = function(event) {
                const previewItem = document.createElement('div');
                previewItem.className = 'preview-item';
                previewItem.innerHTML = `
                    <img src="${event.target.result}" alt="预览图片">
                    <span class="remove-img" data-index="${newImages.length}">&times;</span>
                `;

                previewContainer.appendChild(previewItem);

                // 添加到新图片数组
                newImages.push(file);

                // 添加删除事件
                previewItem.querySelector('.remove-img').addEventListener('click', function() {
                    const idx = this.getAttribute('data-index');
                    newImages.splice(idx, 1);
                    previewItem.remove();
                    updatePreviewIndices();
                });
            };
            reader.readAsDataURL(file);
        }

        // 清空input值，允许重复选择相同文件
        wishImages.value = '';
    });

    // 保存愿望详情
    saveBtn.addEventListener('click', async function() {
        await saveWishDetails();
    });
}

/**
 * 更新预览图片索引
 */
function updatePreviewIndices() {
    const removeBtns = document.querySelectorAll('#previewImages .remove-img');
    removeBtns.forEach((btn, idx) => {
        btn.setAttribute('data-index', idx);
    });
}

/**
 * 打开模态框
 */
function openModal() {
    const modal = document.getElementById('wishModal');
    const wishIndex = document.getElementById('wishIndex');
    const wishId = document.getElementById('wishId');
    const wishTitle = document.getElementById('wishTitle');
    const wishDesc = document.getElementById('wishDesc');
    const existingImages = document.getElementById('existingImages');

    // 设置表单值
    wishIndex.value = currentWishData.index;
    wishId.value = currentWishData.id;
    wishTitle.value = currentWishData.title;
    wishDesc.value = currentWishData.desc || '';

    // 显示已上传图片
    existingImages.innerHTML = '';
    if (currentWishData.images && currentWishData.images.length > 0) {
        currentWishData.images.forEach((img, idx) => {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';
            previewItem.innerHTML = `
                <img src="${window.location.origin}/static/uploads/${img}" alt="已上传图片">
                <span class="remove-img" data-img="${img}">&times;</span>
            `;
            existingImages.appendChild(previewItem);

            // 删除已上传图片
            previewItem.querySelector('.remove-img').addEventListener('click', function() {
                const imgName = this.getAttribute('data-img');
                previewItem.remove();
                currentWishData.images = currentWishData.images.filter(item => item !== imgName);
            });
        });
    }

    // 清空新图片预览
    document.getElementById('previewImages').innerHTML = '';
    newImages = [];

    // 显示模态框
    modal.style.display = 'flex';
}

/**
 * 关闭模态框
 */
function closeModal() {
    const modal = document.getElementById('wishModal');
    modal.style.display = 'none';
    currentWishData = {};
    newImages = [];
}

/**
 * 保存愿望详情
 */
async function saveWishDetails() {
    const index = document.getElementById('wishIndex').value;
    const id = document.getElementById('wishId').value;
    const title = document.getElementById('wishTitle').value.trim();
    const desc = document.getElementById('wishDesc').value.trim();

    if (!title) {
        showToast('请输入愿望标题！', 'warning');
        return;
    }

    // 创建FormData对象
    const formData = new FormData();
    formData.append('index', index);
    formData.append('id', id);
    formData.append('title', title);
    formData.append('description', desc);

    // 添加新图片
    newImages.forEach((img, idx) => {
        formData.append('images', img);
    });

    // 添加要删除的图片
    const existingImages = currentWishData.images || [];
    const originalImages = document.querySelectorAll('#existingImages .preview-item img');
    const originalImageNames = Array.from(originalImages).map(img => {
        const src = img.getAttribute('src');
        return src.split('/').pop();
    });

    const deletedImages = existingImages.filter(img => !originalImageNames.includes(img));
    if (deletedImages.length > 0) {
        formData.append('deleted_images', JSON.stringify(deletedImages));
    }

    try {
        const response = await fetch(`/wishlist/save/${index}`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            showToast('愿望详情保存成功！', 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showToast('保存失败，请重试！', 'error');
        }
    } catch (error) {
        console.error('保存愿望详情出错：', error);
        showToast('网络错误，请稍后重试！', 'error');
    }
}

/**
 * 初始化提示框
 */
function initToast() {
    if (!document.getElementById('toast-container')) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 10px;
        `;
        document.body.appendChild(container);
    }
}

/**
 * 显示提示框
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    toast.style.cssText = `
        padding: 10px 20px;
        border-radius: 4px;
        color: white;
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.3s;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    `;

    const bgColors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };
    toast.style.backgroundColor = bgColors[type] || bgColors.info;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
    }, 10);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
        setTimeout(() => {
            container.removeChild(toast);
        }, 300);
    }, 3000);
}