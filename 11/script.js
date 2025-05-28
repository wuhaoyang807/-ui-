// 基本交互功能
document.addEventListener('DOMContentLoaded', function() {
    // 处理底部导航点击
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            navItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // 处理分类导航点击
    const categories = document.querySelectorAll('.category');
    categories.forEach(category => {
        category.addEventListener('click', function() {
            categories.forEach(c => c.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // 处理标签导航点击
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // 处理返回按钮点击
    const backButton = document.querySelector('.back-button');
    if (backButton) {
        backButton.addEventListener('click', function() {
            window.location.href = 'index.html';
        });
    }

    // 初始化滑动卡片
    initSwiper();
});

// 初始化滑动卡片功能
function initSwiper() {
    const swiperContainer = document.querySelector('.swiper-container');
    if (!swiperContainer) return;
    
    const swiperWrapper = swiperContainer.querySelector('.swiper-wrapper');
    const slides = swiperContainer.querySelectorAll('.swiper-slide');
    const pagination = swiperContainer.querySelector('.swiper-pagination');
    
    // 生成分页指示器
    slides.forEach((_, index) => {
        const bullet = document.createElement('span');
        bullet.classList.add('swiper-pagination-bullet');
        if (index === 0) bullet.classList.add('swiper-pagination-bullet-active');
        pagination.appendChild(bullet);
    });

    const bullets = pagination.querySelectorAll('.swiper-pagination-bullet');
    
    // 设置卡片宽度为容器宽度的80%
    const containerWidth = swiperContainer.offsetWidth;
    const slideWidth = containerWidth * 0.8;
    
    // 设置每个卡片的初始位置和样式
    slides.forEach((slide, index) => {
        slide.style.width = `${slideWidth}px`;
        slide.style.marginRight = `${containerWidth * 0.05}px`; // 5%的间距
        
        // 初始化第一个卡片为活动状态
        if (index === 0) {
            slide.classList.add('swiper-slide-active');
        } else if (index === 1) {
            slide.classList.add('swiper-slide-next');
        } else if (index === slides.length - 1) {
            slide.classList.add('swiper-slide-prev');
        }
        
        // 点击卡片跳转到详情页
        slide.addEventListener('click', function() {
            window.location.href = 'detail.html';
        });
    });
    
    // 计算布局参数
    let currentIndex = 0;
    const totalSlides = slides.length;
    const slidePositions = Array.from(slides).map((_, index) => {
        // 计算每个卡片的偏移量
        return -index * (slideWidth + containerWidth * 0.05);
    });
    
    // 设置初始偏移量，让三张卡片同时显示
    let offsetX = (containerWidth - slideWidth * 3 - containerWidth * 0.1) / 2;
    swiperWrapper.style.transform = `translateX(${offsetX}px)`;
    
    // 触摸滑动相关变量
    let startX = 0;
    let currentX = 0;
    let isDragging = false;
    
    // 触摸事件处理
    swiperContainer.addEventListener('touchstart', handleStart);
    swiperContainer.addEventListener('touchmove', handleMove);
    swiperContainer.addEventListener('touchend', handleEnd);
    
    // 鼠标事件处理
    swiperContainer.addEventListener('mousedown', handleStart);
    swiperContainer.addEventListener('mousemove', handleMove);
    swiperContainer.addEventListener('mouseup', handleEnd);
    swiperContainer.addEventListener('mouseleave', handleEnd);
    
    function handleStart(e) {
        startX = getPositionX(e);
        isDragging = true;
        swiperWrapper.style.transition = 'none';
    }
    
    function handleMove(e) {
        if (!isDragging) return;
        
        const x = getPositionX(e);
        const diff = x - startX;
        currentX = offsetX + diff;
        
        swiperWrapper.style.transform = `translateX(${currentX}px)`;
        e.preventDefault();
    }
    
    function handleEnd(e) {
        if (!isDragging) return;
        isDragging = false;
        
        const endX = getPositionX(e);
        const diff = endX - startX;
        
        // 判断滑动方向和距离
        if (Math.abs(diff) > slideWidth / 4) {
            if (diff > 0 && currentIndex > 0) {
                // 向右滑动，显示前一张
                currentIndex--;
            } else if (diff < 0 && currentIndex < totalSlides - 1) {
                // 向左滑动，显示后一张
                currentIndex++;
            }
        }
        
        // 更新活动卡片状态
        updateActiveSlide();
    }
    
    // 更新活动卡片状态
    function updateActiveSlide() {
        // 计算新的偏移量
        offsetX = (containerWidth - slideWidth * 3 - containerWidth * 0.1) / 2 + slidePositions[currentIndex];
        
        // 使用过渡效果移动卡片
        swiperWrapper.style.transition = 'transform 0.3s ease';
        swiperWrapper.style.transform = `translateX(${offsetX}px)`;
        
        // 更新卡片类名
        slides.forEach((slide, index) => {
            slide.classList.remove('swiper-slide-active', 'swiper-slide-prev', 'swiper-slide-next');
            if (index === currentIndex) {
                slide.classList.add('swiper-slide-active');
            } else if (index === currentIndex - 1) {
                slide.classList.add('swiper-slide-prev');
            } else if (index === currentIndex + 1) {
                slide.classList.add('swiper-slide-next');
            }
        });
        
        // 更新分页指示器
        bullets.forEach((bullet, index) => {
            bullet.classList.toggle('swiper-pagination-bullet-active', index === currentIndex);
        });
    }
    
    // 点击分页指示器切换卡片
    bullets.forEach((bullet, index) => {
        bullet.addEventListener('click', () => {
            currentIndex = index;
            updateActiveSlide();
        });
    });
    
    // 获取触摸或鼠标事件的X坐标
    function getPositionX(e) {
        return e.type.includes('mouse') ? e.pageX : e.touches[0].clientX;
    }
}
