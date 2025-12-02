
document.addEventListener('DOMContentLoaded', () => {


    const bannerSwiper = new Swiper(".main-slider", {
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

    // --- 드롭다운 메뉴 로직 (index.html) ---
    const profileButton = document.getElementById('profile-menu-button');
    const profileDropdown = document.getElementById('profile-dropdown');

    if (profileButton && profileDropdown) {

        // 1. 프로필 버튼 클릭 시
        profileButton.addEventListener('click', (event) => {
            event.preventDefault();

            // 'show' 클래스를 붙이거나 떼서 메뉴를 열고 닫음
            profileDropdown.classList.toggle('show');
        });

        // 2. 페이지의 다른 곳을 클릭하면 드롭다운 닫기
        window.addEventListener('click', (event) => {
            // 클릭된 곳이 버튼(a)이나 버튼의 자식(i)이 아니고,
            // 메뉴(ul)나 메뉴의 자식(li, a)도 아니라면
            if (!profileButton.contains(event.target) && !profileDropdown.contains(event.target)) {
                profileDropdown.classList.remove('show');
            }
        });
    }


    // 텍스트 노출 로직 (review_detail.html)
    const reviewItems = document.querySelectorAll('.review-item');

    reviewItems.forEach(item => {
        const reviewText = item.querySelector('.review-content');
        const toggleButton = item.querySelector('.show-more-button');


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
    });


    // 구해드림 슬라이더 설정
    const findSlider = new Swiper(".find-slider", {
        slidesPerView: "auto", 
        spaceBetween: 20,      
        freeMode: true,         
        grabCursor: true,       

        // 스크롤바 설정
        scrollbar: {
            el: ".swiper-scrollbar",
            draggable: true,    
            hide: false,        
        },
    });

    // 포토 리뷰 슬라이더 설정
    const reviewSlider = new Swiper(".review-slider", {
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
});