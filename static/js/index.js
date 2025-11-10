// Index Page Main Slider - Optimized

document.addEventListener('DOMContentLoaded', function () {
    initIndexSlider();
});

function initIndexSlider() {
    const slides = document.querySelectorAll('.baltic-slide');
    if (slides.length === 0) return;

    let currentIndex = 0;
    let autoPlayInterval;
    let isHovering = false;

    // Activate a specific slide
    function activateSlide(index) {
        slides.forEach(slide => {
            slide.classList.remove('active');
            slide.style.opacity = '0';
        });
        
        currentIndex = (index + slides.length) % slides.length;
        slides[currentIndex].classList.add('active');
        
        // Smooth fade-in effect
        setTimeout(() => {
            slides[currentIndex].style.opacity = '1';
        }, 50);
    }

    // Auto-play functionality
    function startAutoPlay() {
        autoPlayInterval = setInterval(() => {
            if (!isHovering) {
                currentIndex = (currentIndex + 1) % slides.length;
                activateSlide(currentIndex);
            }
        }, 4000);
    }

    function stopAutoPlay() {
        clearInterval(autoPlayInterval);
    }

    // Mouse hover on individual slides
    slides.forEach((slide, index) => {
        slide.addEventListener('mouseenter', () => {
            isHovering = true;
            activateSlide(index);
        });

        slide.addEventListener('mouseleave', () => {
            isHovering = false;
        });

        // Add smooth transition
        slide.style.transition = 'opacity 0.8s ease-in-out';
    });

    // Touch support for mobile
    let touchStartX = 0;
    let touchEndX = 0;
    const slider = document.querySelector('.baltic-slider');

    if (slider) {
        slider.addEventListener('touchstart', function (e) {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        slider.addEventListener('touchend', function (e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, { passive: true });
    }

    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;

        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                // Swipe left - next slide
                currentIndex = (currentIndex + 1) % slides.length;
            } else {
                // Swipe right - previous slide
                currentIndex = (currentIndex - 1 + slides.length) % slides.length;
            }
            activateSlide(currentIndex);
        }
    }

    // Keyboard navigation
    document.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') {
            stopAutoPlay();
            currentIndex = (currentIndex - 1 + slides.length) % slides.length;
            activateSlide(currentIndex);
            setTimeout(startAutoPlay, 3000);
        } else if (e.key === 'ArrowRight') {
            stopAutoPlay();
            currentIndex = (currentIndex + 1) % slides.length;
            activateSlide(currentIndex);
            setTimeout(startAutoPlay, 3000);
        }
    });

    // Start auto-play
    startAutoPlay();

    // Pause auto-play when page is not visible
    document.addEventListener('visibilitychange', function () {
        if (document.hidden) {
            stopAutoPlay();
        } else {
            startAutoPlay();
        }
    });
}
