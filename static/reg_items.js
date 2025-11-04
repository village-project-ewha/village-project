const fileInput = document.getElementById('file');
const imageBox = document.getElementById('image_box');
const uploadText = document.getElementById('upload_text');
const icon = imageBox.querySelector('a');
const preview = document.getElementById('preview');

fileInput.addEventListener('change', function () {
    const file = this.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        // 이미지 미리보기
        preview.src = e.target.result;
        preview.style.display = 'block';

        // 텍스트/아이콘 숨기기
        uploadText.style.display = 'none';
        icon.style.display = 'none';
    };
    reader.readAsDataURL(file);
});


const nameInput = document.getElementById('name');
const charCount = document.getElementById('charCount');

nameInput.addEventListener('input', () => {
    const len = nameInput.value.length;
    charCount.textContent = `[${len}/40]`;
});

const explainInput = document.getElementById('explain');
const charCount_explain = document.getElementById('charCount_explain');

explainInput.addEventListener('input', () => {
    const len = explainInput.value.length;
    charCount_explain.textContent = `[${len}/2000]`;
});

const checkbox_way = document.querySelectorAll('input[name="way"]');
checkbox_way.forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
            checkbox_way.forEach((cb) => {
                if (cb !== checkbox) cb.checked = false;
            });
        }
    });
});

const checkboxes = document.querySelectorAll('input[name="status"]');
checkboxes.forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
            checkboxes.forEach((cb) => {
                if (cb !== checkbox) cb.checked = false;
            });
        }
    });
});