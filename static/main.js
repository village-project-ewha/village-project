
document.addEventListener('DOMContentLoaded', () => {
    
    // --- Swiper 캐러셀 초기화 (home.html) ---
    const swiperContainer = document.querySelector(".mySwiper");
    if (swiperContainer) {
        const swiper = new Swiper(".mySwiper", {
            loop: true,
            slidesPerView: 1,
            centeredSlides: true,
            spaceBetween: 30, 
            autoplay: {
                delay: 3000, 
                disableOnInteraction: false,
            },
            pagination: { 
                el: ".swiper-pagination",
                clickable: true,
            },
            navigation: { 
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
        });
    }

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

    

    
    // --- 4. 상품 선택 시뮬레이션 로직 (reg_reviews.html) ---
    const selectProductBtn = document.getElementById('select-product-btn');
    
    if (selectProductBtn) {
        selectProductBtn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // (시뮬레이션) 가짜 상품 데이터
            const product = {
                name: "샘플 상품 1 (공학용계산기)",
                image_url: "{{ url_for('static', filename='resource/products_png/공학용계산기.png') }}", // 실제로는 JS가 url_for를 못 쓰므로, 백엔드에서 경로를 받아와야 함
                price: 2000
            };

            // (시뮬레이션) 상품 정보를 화면에 채워넣기
            const productInfoBox = document.getElementById('selected-product-info');
            productInfoBox.innerHTML = `
                <img src="${product.image_url.replace('{{ url_for(\'static\', filename=\'', '').replace('\') }}', '')}" alt="${product.name}" class="product-image">
                <div class="product-details">
                    <span class="product-name">${product.name}</span>
                    <span class="product-price">${product.price.toLocaleString()}원 / 일</span>
                </div>
            `;
            productInfoBox.style.display = 'flex';
        });
    }
});