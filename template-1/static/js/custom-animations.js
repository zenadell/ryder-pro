document.addEventListener("DOMContentLoaded", function() {
    // 1. Mobile Menu Fallback
    const menuButtons = document.querySelectorAll('.w-nav-button');
    menuButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const nav = this.closest('.w-nav');
            if (!nav) return;
            const menu = nav.querySelector('.w-nav-menu');
            if (!menu) return;

            // Use class toggling only, to avoid stuck inline styles on window resize
            menu.classList.toggle('menu-expanded');
        });
    });

    // 2. Slider Fallback
    const sliders = document.querySelectorAll('.w-slider');
    sliders.forEach(slider => {
        const mask = slider.querySelector('.w-slider-mask');
        const leftArrow = slider.querySelector('.w-slider-arrow-left');
        const rightArrow = slider.querySelector('.w-slider-arrow-right');
        const slides = slider.querySelectorAll('.w-slide');
        
        if (!mask || slides.length === 0) return;

        let currentSlide = 0;
        
        // Remove ANY inline styles we added previously to mask
        mask.style.display = '';
        mask.style.flexWrap = '';
        mask.style.overflow = '';
        
        // Let slides remain inline-block, we just translate them horizontally
        slides.forEach(slide => {
            slide.style.transition = 'transform 0.4s cubic-bezier(0.25, 1, 0.5, 1)';
            slide.style.minWidth = ''; // remove bad inline style
            slide.style.flexShrink = ''; // remove bad inline style
        });

        function updateSlider() {
            slides.forEach(slide => {
                // Calculate percentage based on current slide, plus accounting for margin-right if any
                // 100% here means 100% of the slide's width
                // We use CSS calc to add the gap (e.g., 50px for car-slide)
                slide.style.transform = `translateX(calc(-${currentSlide * 100}% - ${currentSlide * 50}px))`;
            });
        }

        if (leftArrow) {
            leftArrow.addEventListener('click', function(e) {
                e.preventDefault();
                currentSlide = (currentSlide > 0) ? currentSlide - 1 : slides.length - 1;
                updateSlider();
            });
        }

        if (rightArrow) {
            rightArrow.addEventListener('click', function(e) {
                e.preventDefault();
                currentSlide = (currentSlide < slides.length - 1) ? currentSlide + 1 : 0;
                updateSlider();
            });
        }
    });
});
