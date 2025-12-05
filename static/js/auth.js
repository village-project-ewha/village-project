let idChecked = false;

document.addEventListener("DOMContentLoaded", function () {
    // 1. 전체 동의 체크박스 기능 (이 부분은 변경 없음)
    const agreeAll = document.getElementById("agree-all");
    const agreeTerms = document.getElementById("agree-terms");
    const agreePrivacy = document.getElementById("agree-privacy");
    const agreeEvents = document.getElementById("agree-events");

    agreeAll.addEventListener("change", function () {
        const isChecked = this.checked;
        agreeTerms.checked = isChecked;
        agreePrivacy.checked = isChecked;
        agreeEvents.checked = isChecked;
    });

    // 개별 체크박스 중 하나라도 해제되면 전체 동의 해제
    [agreeTerms, agreePrivacy, agreeEvents].forEach(checkbox => {
        checkbox.addEventListener("change", function () {
            if (!this.checked) {
                agreeAll.checked = false;
            } else {
                // 모두 체크되어 있으면 전체 동의도 체크
                if (agreeTerms.checked && agreePrivacy.checked && agreeEvents.checked) {
                    agreeAll.checked = true;
                }
            }
        });
    });

    // 2. 이용약관 모달 기능 (이 부분은 변경 없음)
    const termsIcons = document.querySelectorAll(".icon-view");
    
    // 이용약관 보기
    termsIcons[0].addEventListener("click", function () {
        showModal("이용 약관", `
            <h3>제1조 (목적)</h3>
            <p>본 약관은 빌리지(이하 "회사")가 제공하는 서비스의 이용과 관련하여 회사와 회원 간의 권리, 의무 및 책임사항을 규정함을 목적으로 합니다.</p>
            
            <h3>제2조 (용어의 정의)</h3>
            <p>1. "서비스"란 회사가 제공하는 물품 대여 및 거래 플랫폼을 의미합니다.</p>
            <p>2. "회원"이란 본 약관에 동의하고 회사와 서비스 이용계약을 체결한 자를 말합니다.</p>
            
            <h3>제3조 (서비스의 제공)</h3>
            <p>회사는 다음과 같은 서비스를 제공합니다:</p>
            <p>- 물품 등록 및 대여/판매 중개</p>
            <p>- 회원 간 채팅 기능</p>
            <p>- 거래 내역 관리</p>
            
            <h3>제4조 (회원의 의무)</h3>
            <p>회원은 다음 행위를 하여서는 안됩니다:</p>
            <p>- 타인의 정보 도용</p>
            <p>- 허위 정보 등록</p>
            <p>- 불법 물품 거래</p>
        `);
    });

    // 개인정보 수집 및 이용 동의 보기
    termsIcons[1].addEventListener("click", function () {
        showModal("개인정보 수집 및 이용 동의", `
            <h3>1. 개인정보의 수집 및 이용 목적</h3>
            <p>회사는 다음의 목적을 위하여 개인정보를 처리합니다:</p>
            <p>- 회원 가입 및 관리</p>
            <p>- 물품 거래 서비스 제공</p>
            <p>- 고객 문의 응대</p>
            
            <h3>2. 수집하는 개인정보 항목</h3>
            <p>필수항목: 아이디, 비밀번호, 이메일</p>
            <p>선택항목: 휴대폰 번호</p>
            
            <h3>3. 개인정보의 보유 및 이용기간</h3>
            <p>회원 탈퇴 시까지 보유하며, 관계 법령에 따라 일정 기간 보관할 수 있습니다.</p>
            
            <h3>4. 동의를 거부할 권리</h3>
            <p>귀하는 개인정보 수집 및 이용에 대한 동의를 거부할 권리가 있으나, 필수항목 동의를 거부하실 경우 회원가입이 제한됩니다.</p>
        `);
    });

    // 모달 생성 함수 (이 부분은 변경 없음)
    function showModal(title, content) {
        const modal = document.createElement("div");
        modal.className = "terms-modal";
        modal.innerHTML = `
            <div class="terms-modal-content">
                <div class="terms-modal-header">
                    <h2>${title}</h2>
                    <button class="terms-modal-close">&times;</button>
                </div>
                <div class="terms-modal-body">
                    ${content}
                </div>
                <div class="terms-modal-footer">
                    <button class="terms-modal-confirm">확인</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        // 모달 닫기 이벤트
        modal.querySelector(".terms-modal-close").addEventListener("click", () => modal.remove());
        modal.querySelector(".terms-modal-confirm").addEventListener("click", () => modal.remove());
        modal.addEventListener("click", (e) => {
            if (e.target === modal) modal.remove();
        });
    }

    // 3. 비밀번호 검증 로직 (이 부분은 변경 없음)
    const password = document.getElementById("password");
    const passwordConfirm = document.getElementById("password-confirm");
    const passwordRuleMessage = document.getElementById("password-rule-message");
    const passwordMessage = document.getElementById("password-message");

    // 비밀번호 입력 시 실시간 검증
    password.addEventListener("input", function () {
        const pw = this.value;
        const hasLetter = /[a-zA-Z]/.test(pw);
        const hasNumber = /[0-9]/.test(pw);
        const isLongEnough = pw.length >= 8;

        if (pw.length === 0) {
            passwordRuleMessage.innerText = "* 영문, 숫자를 포함한 8자 이상의 비밀번호를 입력해주세요.";
            passwordRuleMessage.style.color = "#666";
        } else if (!hasLetter || !hasNumber || !isLongEnough) {
            passwordRuleMessage.innerText = "✗ 영문, 숫자를 포함한 8자 이상이어야 합니다.";
            passwordRuleMessage.style.color = "red";
        } else {
            passwordRuleMessage.innerText = "✓ 사용 가능한 비밀번호입니다.";
            passwordRuleMessage.style.color = "green";
        }

        // 비밀번호 확인란에 값이 있으면 일치 여부 체크
        if (passwordConfirm.value) {
            checkPasswordMatch();
        }
    });

    // 비밀번호 확인 실시간 검증
    passwordConfirm.addEventListener("input", checkPasswordMatch);

    function checkPasswordMatch() {
        const pw = password.value;
        const pwConfirm = passwordConfirm.value;

        if (pwConfirm.length === 0) {
            passwordMessage.innerText = "";
            return;
        }

        if (pw === pwConfirm) {
            passwordMessage.innerText = "✓ 비밀번호가 일치합니다.";
            passwordMessage.style.color = "green";
        } else {
            passwordMessage.innerText = "✗ 비밀번호가 일치하지 않습니다.";
            passwordMessage.style.color = "red";
        }
    }

    // 아이디 중복 확인 (이 부분은 변경 없음)
    document.getElementById("id-check-btn").addEventListener("click", function () {
        const userId = document.getElementById("userid").value;
        const msg = document.getElementById("id-message");

        if (!userId) {
            alert("아이디를 입력하세요!");
            return;
        }

        fetch("/signup_post", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: "mode=id_check&id=" + userId
        })
        .then(res => res.json())
        .then(data => {
            if (data.result === "ok") {
                msg.innerText = "✓ 사용 가능한 아이디입니다.";
                msg.style.color = "green";
                idChecked = true;
            } else {
                msg.innerText = "✗ 이미 사용 중인 아이디입니다.";
                msg.style.color = "red";
                idChecked = false;
            }
        });
    });

    // 아이디 입력값 변경 시 중복확인 초기화 (이 부분은 변경 없음)
    document.getElementById("userid").addEventListener("input", function () {
        idChecked = false;
        document.getElementById("id-message").innerText = "";
    });
});

// 최종 submit 검증 (수정된 부분)
function finalCheck() {
    const pw = document.getElementById("password").value;
    const pwConfirm = document.getElementById("password-confirm").value;
    // finalCheck 함수 내에서 약관 체크박스 요소를 다시 가져와야 합니다!
    const agreeTerms = document.getElementById("agree-terms"); 
    const agreePrivacy = document.getElementById("agree-privacy");

    // 1. 아이디 중복 확인 체크
    if (!idChecked) {
        alert("아이디 중복 확인을 먼저 해주세요!");
        return false;
    }

    // 2. 비밀번호 규칙 검증
    const hasLetter = /[a-zA-Z]/.test(pw);
    const hasNumber = /[0-9]/.test(pw);
    const isLongEnough = pw.length >= 8;

    if (!hasLetter || !hasNumber || !isLongEnough) {
        alert("비밀번호는 영문, 숫자를 포함한 8자 이상이어야 합니다.");
        return false;
    }

    // 3. 비밀번호 일치 확인
    if (pw !== pwConfirm) {
        alert("비밀번호가 일치하지 않습니다.");
        return false;
    }

    // 4. 필수 약관 동의 확인 (agreeTerms 변수가 이 함수 안에서 정의되었는지 확인하세요)
    // 이용 약관이 체크되지 않았을 경우
    if (!agreeTerms.checked) {
        alert("이용 약관 동의는 필수입니다.");
        return false;
    }

    // 개인정보 수집 및 이용 동의가 체크되지 않았을 경우
    if (!agreePrivacy.checked) {
        alert("개인정보 수집 및 이용 동의는 필수입니다.");
        return false;
    }

    return true;
}