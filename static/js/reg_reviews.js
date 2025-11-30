document.addEventListener('DOMContentLoaded', function () {
  
  // ==========================================
  // 1. 별점 (Star Rating) 기능
  // ==========================================
  const starRatingBox = document.querySelector('.rating-box');
  const ratingInput = document.querySelector('input[name="reviewStar"]'); 
  const ratingText = document.querySelector('.rating-text');
  
  // 현재 별점을 저장할 변수
  let currentRating = 0;

  if (starRatingBox && ratingInput) {
    const stars = starRatingBox.querySelectorAll('.star-rating i');

    // 별 클릭 이벤트
    stars.forEach((star) => {
      star.addEventListener('click', () => {
        const rating = parseInt(star.dataset.value);
        currentRating = rating;
        ratingInput.value = rating; // hidden input에 값 저장
        updateStars(rating);
        updateRatingText(rating);
      });

      // 마우스 오버 이벤트
      star.addEventListener('mouseenter', () => {
        const rating = parseInt(star.dataset.value);
        updateStars(rating);
        updateRatingText(rating);
      });
    });

    // 마우스가 영역을 벗어나면 확정된 점수(currentRating)로 복구
    starRatingBox.addEventListener('mouseleave', () => {
      updateStars(currentRating);
      updateRatingText(currentRating);
    });

    // 별 색상 채우기 함수
    function updateStars(rating) {
      stars.forEach((star) => {
        const starValue = parseInt(star.dataset.value);
        if (starValue <= rating) {
          star.classList.add('selected'); // CSS에서 .selected 색상 정의 필요
        } else {
          star.classList.remove('selected');
        }
      });
    }

    // 텍스트 업데이트 함수
    function updateRatingText(rating) {
      if (ratingText) {
        ratingText.textContent = `(${rating}.0 / 5.0)`;
      }
    }

    // 초기화
    updateStars(currentRating);
    updateRatingText(currentRating);
  }


  // ==========================================
  // 2. 사진 미리보기 로직
  // ==========================================
  const fileInput = document.querySelector('input[type="file"]'); // .photo-input 대신 일반적인 선택자 사용 추천
  if (fileInput) {
    fileInput.addEventListener('change', function (event) {
      // 미리보기 박스들 (.placeholder 클래스를 가진 요소들)
      const placeholders = document.querySelectorAll('.photo-upload-box');
      const files = event.target.files;
      
      // 파일 개수와 박스 개수 중 작은 것만큼 반복
      let filesToProcess = Math.min(files.length, placeholders.length);

      for (let i = 0; i < filesToProcess; i++) {
        const file = files[i];
        const placeholder = placeholders[i];
        
        // 이미지 파일인지 확인
        if (!file.type.startsWith('image/')) continue;

        const reader = new FileReader();

        reader.onload = function (e) {
          placeholder.style.backgroundImage = `url(${e.target.result})`;
          placeholder.style.backgroundSize = 'cover';
          placeholder.style.backgroundPosition = 'center';
          placeholder.classList.remove('placeholder');
          placeholder.classList.add('thumbnail');
        }
        reader.readAsDataURL(file);
      }
    });
  }


  // ==========================================
  // 3. 글자수 카운팅 및 유효성 검사
  // ==========================================
  const reviewTextarea = document.querySelector('textarea[name="reviewContents"]');
  const charCountSpan = document.querySelector('.current-count');
  const errorMessage = document.querySelector('.error-message');
  
  // [중요 수정] 폼을 ID로 정확하게 찾기 (HTML에 id="reviewForm" 필수!)
  const reviewForm = document.getElementById('reviewForm'); 

  if (reviewTextarea && charCountSpan) {
    // 실시간 글자수 카운팅
    reviewTextarea.addEventListener('input', function () {
      const length = this.value.length;
      charCountSpan.textContent = length;

      // 20자 미만이면 에러 메시지 표시
      if (length > 0 && length < 20) {
        if (errorMessage) errorMessage.style.display = 'block';
        charCountSpan.style.color = '#e74c3c'; // 빨간색
      } else {
        if (errorMessage) errorMessage.style.display = 'none';
        charCountSpan.style.color = '#00462A'; // 초록색
      }
    });
  }

  // ==========================================
  // 4. 폼 제출 시 최종 유효성 검사
  // ==========================================
  if (reviewForm) {
    reviewForm.addEventListener('submit', function (event) {
      
      // 1) 내용 글자수 검사
      const reviewContent = reviewTextarea.value.trim();
      
      if (reviewContent.length < 20) {
        event.preventDefault(); // 제출 막기
        alert("리뷰를 20자 이상 작성해 주세요.");
        
        if (errorMessage) errorMessage.style.display = 'block';
        reviewTextarea.focus();
        
        // 부드럽게 스크롤 이동
        reviewTextarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return false;
      }

      // 2) 별점 검사 (0점이면 막기)
      // currentRating 변수는 위에서 정의했으므로 접근 가능
      if (currentRating === 0) {
        event.preventDefault(); // 제출 막기
        alert('별점을 선택해 주세요.');
        
        if (starRatingBox) {
            starRatingBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        return false;
      }

      // 여기까지 오면 통과 -> 서버로 전송됨
    });
  } else {
    console.error("reviewForm을 찾을 수 없습니다. HTML <form> 태그에 id='reviewForm'을 추가했는지 확인하세요.");
  }
});