// 좋아요 함수
function toggleHeart(productName) {
    const heartIcon = document.getElementById('heart-icon');
    const isLiked = heartIcon.classList.contains('fas'); // 현재 채워진 하트인지 확인 (좋아요 상태인지)git add
    
    // 좋아요 상태 -> 취소
    const actionUrl = isLiked ? `/unlike/${productName}/` : `/like/${productName}/`;
    
    fetch(actionUrl, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.msg);
        if (isLiked) {
            heartIcon.classList.remove('fas');
            heartIcon.classList.add('far'); // 빈 하트로 변경
        } else {
            heartIcon.classList.add('fas'); // 채워진 하트로 변경
            heartIcon.classList.remove('far');
        }
    })
    .catch(error => console.error('좋아요 토글 오류:', error));
}


function checkHeartStatus(productName) {
    const heartIcon = document.getElementById('heart-icon');
    
    fetch(`/show_heart/${productName}/`)
        .then(response => response.json())
        .then(data => {
            if (data.my_heart === 'Y') {
                heartIcon.classList.add('fas');    // 채워진 하트
                heartIcon.classList.remove('far');
            } else {
                heartIcon.classList.add('far');    // 빈 하트
                heartIcon.classList.remove('fas');
            }
        })
        .catch(error => console.error('좋아요 상태 조회 오류:', error));
}

document.addEventListener('DOMContentLoaded', () => {
    const productName = document.getElementById('product-name-data').value;
    
    if (productName) {
        checkHeartStatus(productName);
    }
});

// 대여 신청하기 함수
function requestRental(productName) {
    const rentalButton = document.getElementById('rental-button');
    
    // 이미 신청이 완료된 상태라면 중복 신청 방지
    if (rentalButton.textContent === '신청 완료') {
        alert('이미 대여 신청을 완료했습니다.');
        return;
    }

    fetch(`/request_rental/${productName}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.status === 401) {
            alert("대여 신청을 위해서는 로그인이 필요합니다.");
            window.location.href = '/login';
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            rentalButton.textContent = '신청 완료';
            
            // 2. 스타일 변경 (예: 배경색을 회색으로)
            rentalButton.parentElement.style.backgroundColor = '#ccc';
            rentalButton.style.cursor = 'default';
            
            alert(data.message); // "대여 신청이 완료되었습니다."
        } else {
            alert('신청 실패: ' + data.message);
        }
    })
    .catch(error => console.error('대여 신청 오류:', error));
}