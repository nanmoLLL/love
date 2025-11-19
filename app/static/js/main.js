// 爱心点击与跳转逻辑
let clickCount = 0;
const totalClicks = 10;

function handleClick() {
    clickCount++;
    createHearts(80); // 生成爱心动画
    // 点击10次跳转至爱的留言页
    if (clickCount >= totalClicks) {
        window.location.href = "/love-popup";
    }
}

// 生成漂浮爱心
function createHearts(num) {
    for (let i = 0; i < num; i++) {
        const heart = document.createElement('div');
        heart.className = 'heart';

        // 随机位置
        heart.style.left = `${Math.random() * 100}%`;
        heart.style.top = `${Math.random() * 100}%`;

        // 随机大小
        const size = 5 + Math.random() * 20;
        heart.style.setProperty('--size', `${size}px`);

        // 随机颜色
        const colors = ['#e91e63', '#9c27b0', '#f06292', '#ff69b4', '#ff80ab'];
        const color = colors[Math.floor(Math.random() * colors.length)];
        heart.style.background = color;
        heart.style.boxShadow = `0 0 8px ${color}`;

        // 随机漂浮动画
        const duration = 1 + Math.random() * 3;
        heart.style.animation = `float ${duration}s linear forwards`;

        document.body.appendChild(heart);

        // 动画结束后移除元素
        setTimeout(() => {
            heart.remove();
        }, duration * 1000);
    }
}

// 图片切换功能
let photoIndex = 0;
const photos = [
    '/static/images/1.jpg',
    '/static/images/2.jpg',
    '/static/images/3.jpg'
];

function showMorePhotos() {
    photoIndex = (photoIndex + 1) % photos.length;
    const photoElement = document.querySelector('.photo');
    if (photoElement) {
        photoElement.src = photos[photoIndex];
    }
}

// 留言提交功能（不刷新页面）
document.getElementById('messageForm').addEventListener('submit', async function(e) {
    e.preventDefault(); // 阻止默认提交（关键）

    const textarea = this.querySelector('.message-input');
    const message = textarea.value.trim();

    if (message) {
        try {
            // 发送POST请求
            const response = await fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `message=${encodeURIComponent(message)}`
            });

            if (response.ok) {
                textarea.value = ''; // 清空输入框
                // 显示成功提示
                const successModal = document.getElementById('messageSuccessModal');
                successModal.classList.add('show');

                // 3秒后自动关闭提示
                setTimeout(() => {
                    successModal.classList.remove('show');
                }, 3000);
            }
        } catch (error) {
            console.error('留言提交失败:', error);
        }
    }
});

// 页面加载时初始化
window.onload = () => {
    createHearts(10); // 初始显示10个爱心
};