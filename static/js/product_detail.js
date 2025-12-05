function showToast(message) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast-message';
    toast.innerText = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('hide');
        setTimeout(() => { toast.remove(); }, 500);
    }, 3000);
}

function toggleHeart(productName) {
    const heartIcon = document.getElementById('heart-icon');
    if (!heartIcon) return;

    const isLiked = heartIcon.getAttribute('fill') === '#ff0000';

    const actionUrl = isLiked ? `/unlike/${productName}/` : `/like/${productName}/`;
    const toastMessage = isLiked ? "위시리스트에서 삭제됐습니다." : "위시리스트에 담겼습니다.";

    fetch(actionUrl, {
        method: 'POST'
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message || '찜 처리 중 오류가 발생했습니다.');
                });
            }
            return response.json();
        })
        .then(data => {
            if (isLiked) {
                heartIcon.setAttribute('fill', 'none');
                heartIcon.setAttribute('stroke', '#888888');
            } else {
                heartIcon.setAttribute('fill', '#ff0000');
                heartIcon.setAttribute('stroke', '#ff0000');
            }
            showToast(toastMessage);
        })
        .catch(error => {
            console.error('좋아요 토글 오류:', error.message);
            showToast(error.message);
        });
}

function checkHeartStatus(productName) {
    const heartIcon = document.getElementById('heart-icon');
    if (!heartIcon) return;

    fetch(`/show_heart/${productName}/`)
        .then(response => response.json())
        .then(data => {
            console.log('서버 좋아요 상태 응답:', data); 
            
            if (data.my_heart === 'Y') {
                heartIcon.setAttribute('fill', '#ff0000');
                heartIcon.setAttribute('stroke', '#ff0000');
            } else {
                heartIcon.setAttribute('fill', 'none');
                heartIcon.setAttribute('stroke', '#888888');
            }
        })
        .catch(error => console.error('좋아요 상태 조회 오류:', error));
}

function requestAction(productName, productWay) {
    const action = productWay === "판매" ? "구매" : "대여";
    const confirmResult = confirm(`이 상품을 ${action}하시겠습니까?`);

    if (!confirmResult) return;

    const rentalButton = document.getElementById('rental-button');
    const buttonContainer = document.getElementById('detail_chat_button_2');

    fetch(`/request_rental/${productName}/`, {
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                showToast(data.message);
            } else {
                // 버튼 텍스트 변경
                if (productWay === "판매") {
                    rentalButton.textContent = "구매완료!";
                } else {
                    rentalButton.textContent = "대여완료!";
                }
                
                // 버튼 비활성화 스타일 적용
                rentalButton.style.opacity = "0.6";
                rentalButton.style.cursor = "not-allowed";
                rentalButton.onclick = null; // 클릭 이벤트 제거
                
                // 컨테이너에도 포인터 이벤트 비활성화
                if (buttonContainer) {
                    buttonContainer.style.pointerEvents = "none";
                }
                
                showToast(`${action}가 완료되었습니다!`);
            }
        })
        .catch(error => console.error(`${action} 신청 오류:`, error));
}

function updateRentalButton(productName, productWay) {
    const rentalButtonSpan = document.getElementById('rental-button');
    const perDay = document.querySelector('.per_day');

    if (productWay === "판매" && perDay) {
        perDay.style.display = "none";
    }

    if (productWay === "판매") {
        rentalButtonSpan.textContent = "구매하기";
    } else {
        rentalButtonSpan.textContent = "대여하기";
    }

    rentalButtonSpan.onclick = () => requestAction(productName, productWay);
}

document.addEventListener('DOMContentLoaded', () => {
    const productNameInput = document.getElementById('product-name-data');
    const productWayInput = document.getElementById('product-way-data');

    if (productNameInput && productWayInput) {
        const productName = productNameInput.value;
        const productWay = productWayInput.value;

        checkHeartStatus(productName);
        updateRentalButton(productName, productWay);
    }
});