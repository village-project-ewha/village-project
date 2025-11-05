document.addEventListener("DOMContentLoaded", function() {

    // 1. 아이디 중복 확인 (시뮬레이션)
    // -------------------------------------
    const idInput = document.getElementById("userid");
    const idCheckBtn = document.getElementById("id-check-btn");
    const idMessage = document.getElementById("id-message");

    // [수정] null 체크 추가: idCheckBtn이 페이지에 있을 때만 실행
    if (idCheckBtn) {
        idCheckBtn.addEventListener("click", function() {
            const userId = idInput.value;

            if (userId === "") {
                // [수정] showMessage 함수를 사용하도록 통일
                showMessage(idMessage, "* 아이디를 입력해주세요.", "error");
            } else if (userId === "admin") {
                // 'admin'이라는 아이디는 이미 사용 중이라고 가정
                showMessage(idMessage, "* 이미 사용 중인 아이디입니다.", "error");
            } else {
                showMessage(idMessage, "* 사용 가능한 아이디입니다.", "success");
            }
        });
    }


    // 2. 비밀번호 유효성 검사 설정
    // -------------------------------------
    const pwInput = document.getElementById("password");
    const pwConfirmInput = document.getElementById("password-confirm");
    
    // 메시지 ID 가져오기
    const pwRuleMessage = document.getElementById("password-rule-message"); // (규칙 메시지)
    const pwMatchMessage = document.getElementById("password-message"); // (일치 여부 메시지)

    /* 비밀번호 8자 규칙을 실시간으로 검사 */
    function checkPasswordRule() {
        if (!pwInput || !pwRuleMessage) return; // 요소가 없으면 중단

        const pw = pwInput.value;

        if (pw.length > 0 && pw.length < 8) {
            // 1. 입력 중 + 8자 미만일 때: 빨간색 경고 표시
            showMessage(pwRuleMessage, "* 8자 이상의 비밀번호를 입력해주세요.", "error");
        
        } else if (pw.length >= 8) {
            // 2. 8자 이상일 때: 메시지 숨김 (성공으로 간주)
            showMessage(pwRuleMessage, "", null);

        } else {
            // 3. 아무것도 입력하지 않았을 때: 기본 회색 안내 문구
            showMessage(pwRuleMessage, "* 영문, 숫자를 포함한 8자 이상의 비밀번호를 입력해주세요.", null);
        }
    }

    /* 두 비밀번호 필드의 일치 여부를 실시간으로 확인 */
    function checkPasswordMatch() {
        if (!pwInput || !pwConfirmInput || !pwMatchMessage) return; // 요소가 없으면 중단
        
        const pw = pwInput.value;
        const pwConfirm = pwConfirmInput.value;

        // pwConfirm이 비어있으면 메시지 삭제
        if (pwConfirm === "") {
             showMessage(pwMatchMessage, "", null);
             return;
        }

        if (pw !== "" && pwConfirm !== "") {
            if (pw === pwConfirm) {
                showMessage(pwMatchMessage, "* 비밀번호가 일치합니다.", "success");
            } else {
                showMessage(pwMatchMessage, "* 비밀번호가 일치하지 않습니다.", "error");
            }
        } else {
            showMessage(pwMatchMessage, "", null); // 비어있으면 메시지 숨김
        }
    }

    // [수정] null 체크 추가: pwInput이 페이지에 있을 때만 실행
    if (pwInput) {
        // 비밀번호(pwInput) 입력 시, 2개 함수(규칙, 일치)를 모두 실행
        pwInput.addEventListener("keyup", function() {
            checkPasswordRule();  // 8자 규칙 검사
            checkPasswordMatch(); // 일치 여부 검사
        });
    }
    
    // [수정] null 체크 추가: pwConfirmInput이 페이지에 있을 때만 실행
    if (pwConfirmInput) {
        // 비밀번호 확인(pwConfirmInput) 입력 시, 일치 여부만 검사
        pwConfirmInput.addEventListener("keyup", checkPasswordMatch);
    }

    
    // 3. 헬퍼(Helper) 함수 
    // -------------------------------------
    /**
     * 지정된 요소에 유효성 검사 메시지를 표시합니다.
     * @param {HTMLElement} element - 메시지를 표시할 <p> 태그
     * @param {string} text - 표시할 텍스트
     * @param {'success' | 'error' | null} type - 메시지 유형 (CSS 클래스명)
     */
    function showMessage(element, text, type) {
        if (element) { // element가 null이 아닌지 확인
            element.textContent = text;
            
            if (type === "success") {
                element.className = "help-text success";
            } else if (type === "error") {
                element.className = "help-text error";
            } else {
                element.className = "help-text"; // 기본 클래스
            }
        } else {
            // 만약 HTML에 id가 잘못된 경우를 대비해 콘솔에 경고
            console.warn("showMessage: 대상 element를 찾을 수 없습니다.");
        }
    }

});