/* static/js/reg_items.js */

document.addEventListener('DOMContentLoaded', function () {

    /* =========================================
       1. 파일 업로드 (기본 alert로 복구)
       ========================================= */
    const fileInput = document.getElementById('file');
    const preview = document.getElementById('preview');
    // const uploadText = document.getElementById('upload_text'); 
    const iconContainer = document.getElementById('default_content');

    if (fileInput) {
        fileInput.addEventListener('change', function () {
            const file = this.files[0];
            if (!file) return;


            const maxSize = 20 * 1024 * 1024;
            if (file.size > maxSize) {
                alert("파일 용량이 너무 큽니다. (20MB 이상)\n서버 전송 및 미리보기가 느려질 수 있습니다.");
            }

            // 에러 빨간줄 있으면 삭제 
            clearError(document.getElementById('image_box'));

            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
                if (iconContainer) iconContainer.style.display = 'none';
            };
            reader.readAsDataURL(file);
        });
    }

    /* =========================================
       2. 기능 로직 (글자수, 체크박스 등)
       ========================================= */

    // 글자수 세기
    const nameInput = document.getElementById('name');
    const charCount = document.getElementById('charCount');
    if (nameInput && charCount) {
        nameInput.addEventListener('input', () => charCount.innerText = `[${nameInput.value.length}/40]`);
    }

    const explainInput = document.getElementById('explain');
    const charCount_explain = document.getElementById('charCount_explain');
    if (explainInput && charCount_explain) {
        explainInput.addEventListener('input', () => charCount_explain.innerText = `[${explainInput.value.length}/2000]`);
    }

    // 체크박스 하나만 선택 (status 방식)
    function setupSingleCheck(name) {
        const checkboxes = document.querySelectorAll(`input[name="${name}"]`);
        checkboxes.forEach((cb) => {
            cb.addEventListener('click', function () {
                // 1. 하나만 선택 로직
                this.checked = true;
                checkboxes.forEach((other) => {
                    if (other !== this) other.checked = false;
                });

                // 2. 클릭하는 순간 빨간색 에러 스타일 제거

                // (1) 모든 박스 에러 제거
                checkboxes.forEach(box => box.classList.remove('input-error'));

                // (2) 아래 메시지와 박스 에러 제거
                const parentBox = this.closest('.way_box') || this.closest('.status_box') || this.closest('div');
                if (parentBox) {
                    clearError(parentBox);
                }
            });
        });
    }

    setupSingleCheck('way');
    setupSingleCheck('method');
    setupSingleCheck('status');

    // 대면/비대면 장소 보이기 로직
    const checkbox_method = document.querySelectorAll('input[name="method"]');
    const placeDiv = document.querySelector('.product_place');
    const placeInput = document.getElementById('place');

    checkbox_method.forEach((cb) => {
        cb.addEventListener('click', function () {
            if (this.value === '대면') {
                if (placeDiv) placeDiv.style.display = 'block';

            } else {
                if (placeDiv) placeDiv.style.display = 'none';
                if (placeInput) {
                    placeInput.value = '';
                    clearError(placeInput);
                }
            }
        });
    });

    // 모든 입력창 입력 시 에러 지우기
    const allInputs = document.querySelectorAll('input, textarea, select');

    allInputs.forEach(input => {
       
        input.addEventListener('input', handleClearError);
        input.addEventListener('change', handleClearError);
    });

    function handleClearError() {
        if (this.type !== 'checkbox' && this.type !== 'radio') {
            clearError(this);
        }
    }

}); // DOMContentLoaded 끝


/* =========================================
   3. 폼 제출 검사 (HTML에서 호출해야 하므로 밖에 둠)
   ========================================= */

// 에러 표시 함수
function showError(element, message) {
    if (!element) return;
    element.classList.add('input-error');

    // 에러 메시지 박스 찾기 (없으면 생성)
    let msgNode = element.parentNode.querySelector('.error-msg');
    if (!msgNode) {
        msgNode = document.createElement('div');
        msgNode.className = 'error-msg';
        element.parentNode.appendChild(msgNode);
    }
    msgNode.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> ${message}`;

    element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    element.focus();
}

// 에러 지우기 함수
function clearError(element) {
    if (!element) return;
    element.classList.remove('input-error');
    const msgNode = element.parentNode.querySelector('.error-msg');
    if (msgNode) msgNode.remove();
}

function validateForm() {
    // 1. 사진
    const fileInput = document.getElementById('file');
    if (!fileInput.value) {
        showError(document.getElementById('image_box'), "상품 사진을 등록해주세요.");
        return false;
    }

    // 2. 이름
    const nameInput = document.getElementById('name');
    if (nameInput.value.trim() === "") {
        showError(nameInput, "상품 이름을 입력해주세요.");
        return false;
    }

    // 3. 카테고리 확인 
    const categoryInput = document.getElementById('category');
    if (categoryInput.value === "") {
        showError(categoryInput, "카테고리를 선택해주세요.");
        return false;
    }

    // 4. 상품 상태 
    const statusCheckboxes = document.querySelectorAll('input[name="status"]');
    const checkedStatus = document.querySelector('input[name="status"]:checked');
    if (!checkedStatus) {
        statusCheckboxes.forEach(cb => cb.classList.add('input-error'));
        const statusBox = document.querySelector('.status_box');
        showError(statusBox, "상품 상태를 선택해주세요.");
        return false;
    }

    // 5. 거래 방식
    const wayCheckboxes = document.querySelectorAll('input[name="way"]');
    const checkedWay = document.querySelector('input[name="way"]:checked');
    if (!checkedWay) {
        wayCheckboxes.forEach(cb => cb.classList.add('input-error'));
        showError(document.querySelector('.way_box'), "거래 방식을 선택해주세요.");
        return false;
    }

    // 6. 가격
    const priceInput = document.getElementById('price');
    if (priceInput.value.trim() === "") {
        showError(priceInput, "가격을 입력해주세요.");
        return false;
    }

    // 7. 수령 방법
    const methodCheckboxes = document.querySelectorAll('input[name="method"]');
    const checkedMethod = document.querySelector('input[name="method"]:checked');
    if (!checkedMethod) {
        methodCheckboxes.forEach(cb => cb.classList.add('input-error'));
        const methodBox = document.querySelector('input[name="method"]').closest('.way_box');
        showError(methodBox, "수령 방법을 선택해주세요.");
        return false;
    }

    // 8. 거래 장소
    const placeInput = document.getElementById('place');
    if (checkedMethod.value === '대면' && placeInput.value.trim() === "") {
        showError(placeInput, "거래 장소를 입력해주세요.");
        return false;
    }

    // 9. 상세 설명
    const explainInput = document.getElementById('explain');
    if (explainInput.value.trim() === "") {
        showError(explainInput, "상세 설명을 입력해주세요.");
        return false;
    }

    return true;
}