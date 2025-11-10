// House Page JavaScript - Optimized Sliders and Calculator

document.addEventListener('DOMContentLoaded', function () {
    // ============ Floor Plan Slider ============
    initFloorPlanSlider();

    // ============ Photo Slider ============
    initPhotoSlider();

    // ============ Calculator ============
    initCalculator();
});

// Floor Plan Slider (for multi-floor houses)
function initFloorPlanSlider() {
    const floorPlans = document.querySelectorAll('.floor-plan');
    const floorDots = document.querySelectorAll('.floor-dot');
    const floorPrevBtn = document.querySelector('.floor-prev');
    const floorNextBtn = document.querySelector('.floor-next');

    if (floorPlans.length === 0) return;

    let currentFloor = 0;

    function showFloor(n) {
        // Hide all floor plans
        floorPlans.forEach(plan => plan.classList.remove('active'));
        floorDots.forEach(dot => dot.classList.remove('active'));

        // Update current floor with wrapping
        currentFloor = (n + floorPlans.length) % floorPlans.length;

        // Show active floor
        floorPlans[currentFloor].classList.add('active');
        floorDots[currentFloor].classList.add('active');
    }

    // Event handlers for navigation buttons
    if (floorPrevBtn) {
        floorPrevBtn.addEventListener('click', function () {
            showFloor(currentFloor - 1);
        });
    }

    if (floorNextBtn) {
        floorNextBtn.addEventListener('click', function () {
            showFloor(currentFloor + 1);
        });
    }

    // Event handlers for indicator dots
    floorDots.forEach(dot => {
        dot.addEventListener('click', function () {
            const floorIndex = parseInt(this.getAttribute('data-floor'));
            showFloor(floorIndex);
        });
    });

    // Keyboard navigation
    document.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') {
            showFloor(currentFloor - 1);
        } else if (e.key === 'ArrowRight') {
            showFloor(currentFloor + 1);
        }
    });
}

// Photo Slider
function initPhotoSlider() {
    const slider = document.querySelector('.slider');
    if (!slider) return;

    const slides = slider.querySelector('.slides');
    const slideElements = slider.querySelectorAll('.slide');
    const prevBtn = slider.querySelector('.prev-btn');
    const nextBtn = slider.querySelector('.next-btn');
    const dots = slider.querySelectorAll('.dot');

    let currentSlide = 0;
    let isTransitioning = false;

    function updateSlider() {
        if (isTransitioning) return;
        isTransitioning = true;

        // Update slide position
        slides.style.transform = `translateX(-${currentSlide * 100}%)`;

        // Update dots
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentSlide);
        });

        setTimeout(() => {
            isTransitioning = false;
        }, 500);
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slideElements.length;
        updateSlider();
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + slideElements.length) % slideElements.length;
        updateSlider();
    }

    function goToSlide(index) {
        currentSlide = index;
        updateSlider();
    }

    // Event listeners
    if (prevBtn) {
        prevBtn.addEventListener('click', prevSlide);
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', nextSlide);
    }

    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => goToSlide(index));
    });

    // Keyboard navigation
    document.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') {
            prevSlide();
        } else if (e.key === 'ArrowRight') {
            nextSlide();
        }
    });

    // Touch/swipe support
    let touchStartX = 0;
    let touchEndX = 0;

    slider.addEventListener('touchstart', function (e) {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    slider.addEventListener('touchend', function (e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });

    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;

        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                nextSlide();
            } else {
                prevSlide();
            }
        }
    }

    // Auto-play (optional - uncomment to enable)
    // let autoPlayInterval = setInterval(nextSlide, 5000);
    // slider.addEventListener('mouseenter', () => clearInterval(autoPlayInterval));
    // slider.addEventListener('mouseleave', () => {
    //     autoPlayInterval = setInterval(nextSlide, 5000);
    // });
}

// Calculator
function initCalculator() {
    const configOptions = document.querySelectorAll('.config-option');
    const checkboxes = document.querySelectorAll('.service-checkbox');
    const serviceItems = document.querySelectorAll('.service-item');
    const fixedTotalDisplay = document.getElementById('fixed-total-display');
    const configSummaryName = document.getElementById('config-summary-name');
    const totalAmountInput = document.getElementById('total_amount');
    const selectedConfigInput = document.getElementById('selected_config');

    if (!configOptions.length) return;

    let selectedConfigPrice = parseInt(configOptions[1]?.dataset.price || configOptions[0]?.dataset.price || 0);
    let selectedConfigName = configOptions[1]?.querySelector('.config-name')?.textContent || 
                             configOptions[0]?.querySelector('.config-name')?.textContent || '';

    // Format numbers with spaces
    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    }

    // Select configuration
    function selectConfiguration(option) {
        configOptions.forEach(opt => opt.classList.remove('selected'));
        option.classList.add('selected');

        selectedConfigPrice = parseInt(option.dataset.price);
        selectedConfigName = option.querySelector('.config-name').textContent;
        if (selectedConfigInput) {
            selectedConfigInput.value = selectedConfigName;
        }

        updateFixedTotal();
    }

    // Update fixed total
    function updateFixedTotal() {
        let servicesTotal = 0;

        checkboxes.forEach((checkbox, index) => {
            if (checkbox.checked && serviceItems[index]) {
                servicesTotal += parseInt(serviceItems[index].dataset.price);
            }
        });

        const total = selectedConfigPrice + servicesTotal;

        if (configSummaryName) {
            configSummaryName.textContent = selectedConfigName;
        }
        if (fixedTotalDisplay) {
            fixedTotalDisplay.textContent = formatNumber(total) + ' ₽';
        }
        if (totalAmountInput) {
            totalAmountInput.value = total;
        }

        updateSelectedStyles();
    }

    // Update selected styles
    function updateSelectedStyles() {
        serviceItems.forEach((item, index) => {
            if (checkboxes[index] && checkboxes[index].checked) {
                item.classList.add('selected');
            } else {
                item.classList.remove('selected');
            }
        });
    }

    // Event handlers for configuration selection
    configOptions.forEach(option => {
        option.addEventListener('click', function () {
            selectConfiguration(this);
        });
    });

    // Event handlers for checkboxes
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateFixedTotal);
    });

    // Event handlers for service items (click anywhere to toggle)
    serviceItems.forEach((item, index) => {
        item.addEventListener('click', function (e) {
            if (e.target !== checkboxes[index]) {
                checkboxes[index].checked = !checkboxes[index].checked;
                updateFixedTotal();
            }
        });
    });

    // Auto-select second configuration if available
    if (configOptions.length > 1) {
        selectConfiguration(configOptions[1]);
    } else if (configOptions.length === 1) {
        selectConfiguration(configOptions[0]);
    }
}
