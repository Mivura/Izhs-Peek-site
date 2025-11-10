class PhotoSlider {
    constructor() {
        this.currentSlide = 0;
        this.slides = document.querySelectorAll('.slide');
        this.totalSlides = this.slides.length;
        this.slidesContainer = document.querySelector('.slides');
        this.dots = document.querySelectorAll('.dot');

        this.init();
    }

    init() {
        this.updateDots();
        this.bindEvents();
        this.startAutoplay();
    }

    bindEvents() {
        // Кнопки навигации
        document.querySelector('.prev-btn').addEventListener('click', () => this.prevSlide());
        document.querySelector('.next-btn').addEventListener('click', () => this.nextSlide());

        // Точки индикаторы
        this.dots.forEach((dot, index) => {
            dot.addEventListener('click', () => this.goToSlide(index));
        });

        // Свайпы для мобильных
        let startX = 0;
        let endX = 0;

        this.slidesContainer.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        });

        this.slidesContainer.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            if (startX - endX > 50) this.nextSlide();
            if (endX - startX > 50) this.prevSlide();
        });

        // Пауза автопролистывания при наведении
        this.slidesContainer.addEventListener('mouseenter', () => {
            clearInterval(this.autoplayInterval);
        });

        this.slidesContainer.addEventListener('mouseleave', () => {
            this.startAutoplay();
        });
    }

    goToSlide(slideIndex) {
        this.currentSlide = slideIndex;
        this.slidesContainer.style.transform = `translateX(-${slideIndex * 100}%)`;
        this.updateDots();
    }

    nextSlide() {
        this.currentSlide = (this.currentSlide + 1) % this.totalSlides;
        this.goToSlide(this.currentSlide);
    }

    prevSlide() {
        this.currentSlide = this.currentSlide === 0 ? this.totalSlides - 1 : this.currentSlide - 1;
        this.goToSlide(this.currentSlide);
    }

    updateDots() {
        this.dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === this.currentSlide);
        });
    }

    startAutoplay() {
        this.autoplayInterval = setInterval(() => {
            this.nextSlide();
        }, 4000); // автопролистывание каждые 4 секунды
    }
}

// Инициализация после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    new PhotoSlider();
});