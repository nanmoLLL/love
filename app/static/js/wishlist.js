document.addEventListener('DOMContentLoaded', () => {
    // 元素获取
    const pendingDetailModal = document.getElementById('pendingDetailModal');
    const completedDetailModal = document.getElementById('completedDetailModal');
    const toast = document.getElementById('toast');
    let currentWishIndex = -1; // 当前操作的愿望索引

    // 1. 点击未完成愿望卡片 - 显示详情输入对话框
    document.querySelectorAll('.pending-wishes .wish-card').forEach(card => {
        card.addEventListener('click', (e) => {
            if (!e.target.closest('.toggle-btn')) { // 点击按钮不触发
                currentWishIndex = parseInt(card.dataset.index);
                pendingDetailModal.classList.add('show');
            }
        });
    });

    // 2. 确认详情提交（未完成愿望）
    document.querySelector('.confirm-detail-btn').addEventListener('click', async () => {
        const detailText = document.querySelector('.detail-text-input').value.trim();
        const imageInput = document.querySelector('.image-input');

        if (currentWishIndex !== -1) {
            // 构建FormData（支持文件上传）
            const formData = new FormData();
            formData.append('index', currentWishIndex);
            formData.append('detail_text', detailText);

            // 添加图片
            for (let i = 0; i < imageInput.files.length; i++) {
                formData.append('images', imageInput.files[i]);
            }

            // 提交到后端
            const response = await fetch('/wishlist/update-detail', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                showToast('详情已保存');
                pendingDetailModal.classList.remove('show');
                // 重置表单
                document.querySelector('.detail-text-input').value = '';
                imageInput.value = '';
                // 刷新页面
                setTimeout(() => window.location.reload(), 800);
            }
        }
    });

    // 3. 点击已完成愿望卡片 - 显示详情对话框
    document.querySelectorAll('.completed-wishes .wish-card').forEach(card => {
        card.addEventListener('click', (e) => {
            if (!e.target.closest('.toggle-btn')) { // 点击按钮不触发
                currentWishIndex = parseInt(card.dataset.index);
                loadCompletedWishDetail(currentWishIndex);
                completedDetailModal.classList.add('show');
            }
        });
    });

    // 加载已完成愿望详情
    async function loadCompletedWishDetail(index) {
        const response = await fetch(`/wishlist/get-detail?index=${index}`);
        if (response.ok) {
            const wish = await response.json();
            // 填充详情内容
            document.querySelector('.wish-full-content').innerHTML = `
                <p><strong>愿望：</strong>${wish.content}</p>
                ${wish.detail_text ? `<p><strong>详情：</strong>${wish.detail_text}</p>` : ''}
                <p><strong>创建时间：</strong>${wish.time}</p>
                ${wish.images ? `
                    <div><strong>图片：</strong></div>
                    <div class="detail-images">
                        ${wish.images.split(',').map(img => `<img src="${img}" alt="图片">`).join('')}
                    </div>
                ` : ''}
            `;
            // 加载备注
            const notesList = document.querySelector('.notes-list');
            notesList.innerHTML = wish.notes ?
                wish.notes.split(';').map(note => {
                    const [time, content] = note.split('|');
                    return `
                        <div class="note-item">
                            <div>${content}</div>
                            <div class="note-time">${time}</div>
                        </div>
                    `;
                }).join('') :
                '<div class="empty-note">暂无备注</div>';
        }
    }

    // 4. 添加备注（已完成愿望）
    document.querySelector('.add-note-btn').addEventListener('click', async () => {
        const noteContent = document.querySelector('.note-input').value.trim();
        if (noteContent && currentWishIndex !== -1) {
            const response = await fetch('/wishlist/add-note', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `index=${currentWishIndex}&note=${encodeURIComponent(noteContent)}`
            });
            if (response.ok) {
                showToast('备注已添加');
                document.querySelector('.note-input').value = '';
                loadCompletedWishDetail(currentWishIndex); // 刷新备注列表
            }
        }
    });

    // 辅助：显示提示框
    function showToast(text) {
        toast.textContent = text;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 2000);
    }

    // 取消按钮逻辑
    document.querySelector('.cancel-btn').addEventListener('click', () => {
        pendingDetailModal.classList.remove('show');
    });

    document.querySelector('.close-detail-btn').addEventListener('click', () => {
        completedDetailModal.classList.remove('show');
    });

    // 原有功能：添加愿望
    document.querySelector('.add-btn').addEventListener('click', async () => {
        const input = document.querySelector('.wish-input');
        const content = input.value.trim();
        if (content) {
            const response = await fetch('/wishlist', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `wish=${encodeURIComponent(content)}`
            });
            if (response.ok) {
                input.value = '';
                showToast('愿望添加成功');
                setTimeout(() => window.location.reload(), 800);
            }
        }
    });

    // 原有功能：切换愿望状态
    document.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation(); // 防止触发卡片点击事件
            const card = btn.closest('.wish-card');
            const index = parseInt(card.dataset.index);
            const response = await fetch('/wishlist/toggle', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `index=${index}`
            });
            if (response.ok) {
                showToast('状态已更新');
                setTimeout(() => window.location.reload(), 800);
            }
        });
    });
});