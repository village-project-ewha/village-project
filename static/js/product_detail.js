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
        if (isLiked) {
            heartIcon.classList.remove('fas');
            heartIcon.classList.add('far'); // 빈 하트로 변경
        } else {
            heartIcon.classList.add('fas'); // 채워진 하트로 변경
            heartIcon.classList.remove('far');
        }
        alert(data.msg);
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