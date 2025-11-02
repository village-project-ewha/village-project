document.addEventListener('DOMContentLoaded', function () {
  const starRatingBox = document.querySelector('.rating-box');
  if (!starRatingBox) return;

  const stars = starRatingBox.querySelectorAll('.star-rating i');
  const ratingInput = document.querySelector('input[name="rating"]');
  const ratingText = starRatingBox.querySelector('.rating-text');

  let currentRating = 0;

  // 별 클릭
  stars.forEach((star) => {
    star.addEventListener('click', () => {
      const rating = parseInt(star.dataset.value);
      currentRating = rating;
      ratingInput.value = rating;
      updateStars(rating);
      updateRatingText(rating);
    });

    // 마우스 hover
    star.addEventListener('mouseenter', () => {
      const rating = parseInt(star.dataset.value);
      updateStars(rating);
      updateRatingText(rating);
    });
  });

  // 마우스가 별점 영역을 벗어나면 원래 값으로 복원
  starRatingBox.addEventListener('mouseleave', () => {
    updateStars(currentRating);
    updateRatingText(currentRating);
  });

  // 별 업데이트
  function updateStars(rating) {
    stars.forEach((star) => {
      const starValue = parseInt(star.dataset.value);
      if (starValue <= rating) {
        star.classList.add('selected');
      } else {
        star.classList.remove('selected');
      }
    });
  }

  // 텍스트 업데이트
  function updateRatingText(rating) {
    ratingText.textContent = `(${rating}.0 / 5.0)`;
  }

  // 초기화
  updateStars(currentRating);
  updateRatingText(currentRating);

  // --- 사진 미리보기 로직 ---
  const fileInput = document.querySelector('.photo-input');
  if (fileInput) {
    fileInput.addEventListener('change', function(event) {
      const placeholders = document.querySelectorAll('.photo-upload-box.placeholder');
      const files = event.target.files;
      let filesToProcess = Math.min(files.length, placeholders.length);

      for (let i = 0; i < filesToProcess; i++) {
        const file = files[i];
        const placeholder = placeholders[i];
        const reader = new FileReader();

        reader.onload = function(e) {
          placeholder.style.backgroundImage = `url(${e.target.result})`;
          placeholder.classList.remove('placeholder');
          placeholder.classList.add('thumbnail');
        }
        reader.readAsDataURL(file);
      }
    });
  }


  // --- 글자수 카운팅 및 유효성 검사 ---
    const reviewTextarea = document.querySelector('textarea[name="review_content"]');
    const charCountSpan = document.querySelector('.current-count');
    const errorMessage = document.querySelector('.error-message');
    const submitButton = document.querySelector('.submit-review-button');

    if (reviewTextarea && charCountSpan) {
    // 실시간 글자수 카운팅
    reviewTextarea.addEventListener('input', function() {
        const length = this.value.length;
        charCountSpan.textContent = length;
        
        // 20자 미만이면 에러 메시지 표시
        if (length > 0 && length < 20) {
        errorMessage.style.display = 'block';
        charCountSpan.style.color = '#e74c3c';
        } else {
        errorMessage.style.display = 'none';
        charCountSpan.style.color = '#00462A';
        }
    });
    }

    // 폼 제출 시 유효성 검사
    const reviewForm = document.querySelector('form');
    if (reviewForm) {
    reviewForm.addEventListener('submit', function(event) {
        const reviewContent = reviewTextarea.value.trim();
        
        // 리뷰 내용이 20자 미만이면 제출 막기
        if (reviewContent.length < 20) {
        event.preventDefault();
        errorMessage.style.display = 'block';
        reviewTextarea.focus();
        
        // 스크롤을 textarea 위치로 이동
        reviewTextarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return false;
        }
        
        // 별점이 0점이면 제출 막기
        if (currentRating === 0) {
        event.preventDefault();
        alert('별점을 선택해 주세요.');
        starRatingBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return false;
        }
    });
    }
});