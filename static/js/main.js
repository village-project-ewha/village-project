document.addEventListener('DOMContentLoaded', () => {

    // =========================================
    // 1. 메인 배너 슬라이더 설정 (home.html)
    // =========================================
    const mainSliderElement = document.querySelector('.main-slider');
    if (mainSliderElement) {
        new Swiper(".main-slider", {
            loop: true,
            effect: "fade",
            fadeEffect: { crossFade: true },
            pagination: {
                el: ".fraction-pagination",
                type: "fraction",
                formatFractionCurrent: function (number) {
                    return String(number).padStart(2, '0');
                },
                formatFractionTotal: function (number) {
                    return String(number).padStart(2, '0');
                },
                renderFraction: function (currentClass, totalClass) {
                    return '<span class="' + currentClass + '"></span>' +
                        '<span class="page-sep">/</span>' +
                        '<span class="' + totalClass + '"></span>';
                }
            },
            navigation: {
                nextEl: ".control-btn.next",
                prevEl: ".control-btn.prev",
            },
        });
    }

    // =========================================
    // 2. 드롭다운 메뉴 로직 (index.html)
    // =========================================
    const profileButton = document.getElementById('profile-menu-button');
    const profileDropdown = document.getElementById('profile-dropdown');

    if (profileButton && profileDropdown) {
        profileButton.addEventListener('click', (event) => {
            event.preventDefault();
            profileDropdown.classList.toggle('show');
        });

        window.addEventListener('click', (event) => {
            if (!profileButton.contains(event.target) && !profileDropdown.contains(event.target)) {
                profileDropdown.classList.remove('show');
            }
        });
    }

    // =========================================
    // 3. 소형 배너 슬라이더 설정 (products.html)
    // =========================================
    const bannerContainer = document.querySelector('.banner-container');

    // 이 요소가 존재하는 페이지에서만 실행 (에러 방지)
    if (bannerContainer) {
        const slides = document.querySelectorAll('.mini-banner-slide');
        const totalSlides = slides.length;

        const prevBtn = document.querySelector('.small-banner-section .prev');
        const nextBtn = document.querySelector('.small-banner-section .next');
        const fractionBox = document.querySelector('.small-banner-section .fraction-pagination');

        let currentSlide = 0;
        let autoSlideInterval;

        function updateSlider() {
            // 1. 슬라이드 이동
            bannerContainer.style.transform = `translateX(-${currentSlide * 100 / totalSlides}%)`;

            // 2. 숫자 텍스트 업데이트 (01 / 03 형식 + 구분선 클래스 적용)
            const currentStr = String(currentSlide + 1).padStart(2, '0'); // 1 -> "01"
            const totalStr = String(totalSlides).padStart(2, '0');        // 3 -> "03"

            // HTML 태그(span)를 포함해야 하므로 textContent가 아닌 innerHTML 사용
            fractionBox.innerHTML = `${currentStr}<span class="page-sep">/</span>${totalStr}`;
        }

        function nextSlide() {
            currentSlide = (currentSlide + 1) % totalSlides;
            updateSlider();
        }

        function prevSlide() {
            currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
            updateSlider();
        }

        function startAutoSlide() {
            autoSlideInterval = setInterval(nextSlide, 4000);
        }

        function resetAutoSlide() {
            clearInterval(autoSlideInterval);
            startAutoSlide();
        }

        if (nextBtn && prevBtn) {
            nextBtn.addEventListener('click', () => {
                nextSlide();
                resetAutoSlide();
            });

            prevBtn.addEventListener('click', () => {
                prevSlide();
                resetAutoSlide();
            });
        }

        // 초기 실행
        updateSlider();
        startAutoSlide();
    }

    // =========================================
    // 4. 텍스트 더보기/숨기기 (review_detail.html)
    // =========================================
    const reviewItems = document.querySelectorAll('.review-item');
    if (reviewItems.length > 0) {
        reviewItems.forEach(item => {
            const reviewText = item.querySelector('.review-content');
            const toggleButton = item.querySelector('.show-more-button');

            if (reviewText && toggleButton) {
                if (reviewText.scrollHeight <= reviewText.clientHeight) {
                    toggleButton.style.display = 'none';
                }

                toggleButton.addEventListener('click', () => {
                    reviewText.classList.toggle('expanded');
                    if (reviewText.classList.contains('expanded')) {
                        toggleButton.textContent = '숨기기';
                    } else {
                        toggleButton.textContent = '더보기';
                    }
                });
            }
        });
    }

    // =========================================
    // 5. 구해드림 슬라이더 설정
    // =========================================
    const findSliderElement = document.querySelector('.find-slider');
    if (findSliderElement) {
        new Swiper(".find-slider", {
            slidesPerView: "auto",
            spaceBetween: 20,
            freeMode: true,
            grabCursor: true,
            scrollbar: {
                el: ".swiper-scrollbar",
                draggable: true,
                hide: false,
            },
        });
    }

    // =========================================
    // 6. 포토 리뷰 슬라이더 설정
    // =========================================
    const reviewSliderElement = document.querySelector('.review-slider');
    if (reviewSliderElement) {
        new Swiper(".review-slider", {
            slidesPerView: "auto",
            spaceBetween: 15,
            loop: true,
            speed: 5000,
            autoplay: {
                delay: 0,
                disableOnInteraction: false,
                pauseOnMouseEnter: true,
            },
            navigation: {
                nextEl: ".review-slider-wrapper .swiper-button-next",
                prevEl: ".review-slider-wrapper .swiper-button-prev",
            },
            freeMode: true,
        });
    }

    
});