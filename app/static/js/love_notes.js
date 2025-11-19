let messagePool = [...loveMessages];

const colors = [
    '#e91e63', '#9c27b0', '#f06292', '#ff69b4', '#ff80ab',
    '#d81b60', '#8e24aa', '#c2185b', '#ad1457', '#880e4f',
    '#ffb6c1', '#dDA0DD', '#ffc0cb', '#db7093', '#ff6347',
    '#ff9999', '#cc66cc', '#ff66b3'
];
const heartColors = ['#e91e63', '#9c27b0', '#f06292', '#ff69b4', '#ff80ab'];
const isMobile = window.innerWidth <= 600;
const maxNoteWidth = isMobile ? 130 : 160;
const noteHeight = isMobile ? 50 : 55;
const spacing = isMobile ? 15 : 20;
let existingNotes = [];

// 爱心生成函数
function createHearts(num) {
    for (let i = 0; i < num; i++) {
        const heart = document.createElement('div');
        heart.className = 'heart';

        // 全屏分布
        heart.style.left = `${Math.random() * 100}%`;
        heart.style.top = `${Math.random() * 100}%`;

        // 适中的爱心尺寸
        const size = 4 + Math.random() * 16; // 4-20px
        heart.style.setProperty('--size', `${size}px`);

        heart.style.background = heartColors[Math.floor(Math.random() * heartColors.length)];
        heart.style['box-shadow'] = `0 0 6px ${heart.style.background}`;

        // 随机方向
        const direction = Math.random() > 0.7 ? 'floatDown' : 'float';
        const duration = 3 + Math.random() * 4; // 3-7秒
        heart.style.animation = `${direction} ${duration}s linear forwards`;

        document.body.appendChild(heart);
        setTimeout(() => heart.remove(), duration * 1000);
    }
}

// 减少生成频率和数量
setInterval(() => {
    // 手机端3-5个/次，电脑端5-8个/次
    const count = isMobile ? 3 + Math.floor(Math.random() * 3) : 5 + Math.floor(Math.random() * 4);
    createHearts(count);
}, 200); // 200ms生成一次

// 爱心留言位置逻辑
function getEdgeBiasedPosition() {
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;
    const minSafeLeft = -30;
    const maxSafeLeft = windowWidth - maxNoteWidth + 20;
    const minSafeTop = 35;
    const maxSafeTop = windowHeight - noteHeight - 60;

    let left, top;
    let attempts = 0;
    const maxAttempts = 100;

    if (isMobile) {
        do {
            left = minSafeLeft + Math.random() * (maxSafeLeft - minSafeLeft);
            top = minSafeTop + Math.random() * (maxSafeTop - minSafeTop);
            attempts++;
        } while (isOverlapping(left, top) && attempts < maxAttempts);
    } else {
        const randomX = Math.random();
        if (randomX < 0.35) {
            const leftRange = 0.3 * windowWidth;
            left = minSafeLeft + 0.1 * windowWidth + Math.random() * leftRange;
        } else if (randomX < 0.95) {
            const leftRange = 0.4 * windowWidth;
            left = 0.6 * windowWidth + Math.random() * leftRange;
        } else {
            const leftRange = 0.2 * windowWidth - maxNoteWidth;
            left = 0.4 * windowWidth + Math.random() * leftRange;
        }

        top = minSafeTop + Math.random() * (maxSafeTop - minSafeTop);

        while (isOverlapping(left, top) && attempts < maxAttempts) {
            left += (Math.random() > 0.7 ? 1 : -1) * (spacing + Math.random() * 15);
            if (attempts % 4 === 0) {
                top += (Math.random() > 0.5 ? 1 : -1) * (spacing + Math.random() * 15);
            }
            left = Math.max(minSafeLeft, Math.min(left, maxSafeLeft));
            top = Math.max(minSafeTop, Math.min(top, maxSafeTop));
            attempts++;
        }
    }

    return { left, top };
}

function isOverlapping(newLeft, newTop) {
    return existingNotes.some(note => {
        const overlapX = Math.abs(newLeft - note.left) < (maxNoteWidth + spacing) * 1.2;
        const overlapY = Math.abs(newTop - note.top) < (noteHeight + spacing) * 1.2;
        return overlapX && overlapY;
    });
}

function getUniqueMessage() {
    if (messagePool.length === 0) {
        messagePool = [...loveMessages];
    }
    const randomIndex = Math.floor(Math.random() * messagePool.length);
    const message = messagePool[randomIndex];
    messagePool.splice(randomIndex, 1);
    return message;
}

function createLoveNotes() {
    const totalNotes = isMobile ? 40 : 50;
    for (let i = 0; i < totalNotes; i++) {
        setTimeout(() => {
            const note = document.createElement('div');
            note.className = 'love-note';

            const message = getUniqueMessage();
            note.textContent = message;

            const { left, top } = getEdgeBiasedPosition();
            note.style.left = `${left}px`;
            note.style.top = `${top}px`;

            existingNotes.push({ left, top, element: note });

            note.style.background = colors[Math.floor(Math.random() * colors.length)];
            note.style['box-shadow'] = `0 0 10px ${note.style.background}80`;

            const rotate = (Math.random() - 0.5) * 8;
            note.style.transform = `scale(0.8) rotate(${rotate}deg)`;

            document.body.appendChild(note);

            setTimeout(() => {
                note.classList.add('show');
            }, 30);

            note.addEventListener('click', () => {
                note.classList.remove('show');
                note.classList.add('hide');
                existingNotes = existingNotes.filter(item => item.element !== note);
                setTimeout(() => note.remove(), 200);
            });

            const autoRemoveTime = 7000 + Math.random() * 5000;
            setTimeout(() => {
                note.classList.remove('show');
                note.classList.add('hide');
                existingNotes = existingNotes.filter(item => item.element !== note);
                setTimeout(() => note.remove(), 200);
            }, autoRemoveTime);
        }, i * 150);
    }
}

// 初始生成适量爱心
window.onload = () => {
    createLoveNotes();
    // 初始爱心数量减少
    createHearts(isMobile ? 20 : 30);
};