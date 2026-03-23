// Простая реализация анимаций при скролле
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('aos-animate');
            }
        });
    }, observerOptions);

    // Наблюдаем за всеми элементами с data-aos
    document.querySelectorAll('[data-aos]').forEach(el => {
        observer.observe(el);
    });
}

// Функция для модального окна контактов
function openContactModal() {
    // Здесь можно реализовать открытие модального окна
    alert('Свяжитесь с нами по телефону: +7 (XXX) XXX-XX-XX\nили email: info@pic-dom.ru');
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initAnimations();
});