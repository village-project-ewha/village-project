
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

