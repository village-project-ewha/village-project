// 좋아요 함수
function toggleHeart(productName) {
    const heartIcon = document.getElementById('heart-icon');
    const isLiked = heartIcon.classList.contains('fas'); // 현재 채워진 하트인지 확인 (좋아요 상태인지)

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
    const productWay = document.getElementById('product-way-data').value;

    if (productName) {
        checkHeartStatus(productName); // 좋아요
        updateRentalButton(productName, productWay); // 대여 신청
    }
});

// 대여 신청 상태 업데이트
function updateRentalButton(productName, productWay) {
    const rentalButtonSpan = document.getElementById('rental-button');
    const perDay = document.getElementById('per-day');

    if (productWay === "판매") {
        if (perDay) perDay.style.display = "none";
    }

    if (productWay === "판매") {
        rentalButtonSpan.textContent = "구매 신청하기";
    } else {
        rentalButtonSpan.textContent = "대여 신청하기";
    }

    rentalButtonSpan.onclick = () => requestAction(productName, productWay);
}

function requestAction(productName, productWay) {
    const action = productWay === "판매" ? "구매" : "대여";
    const confirmResult = confirm(`이 상품의 ${action}를 신청하시겠습니까?`);

    if (!confirmResult) return;

    fetch(`/request_rental/${productName}/`, {
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert(data.message);
            } else {
                alert(`${action} 신청이 완료되었습니다!`);
                location.reload();
            }
        })
        .catch(error => console.error(`${action} 신청 오류:`, error));
}