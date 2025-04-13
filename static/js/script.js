document.querySelectorAll('.file-input').forEach(input => {
    input.addEventListener('change', function () {
        const parent = this.closest('.image-item');
        parent.classList.toggle('selected', this.checked);
    });
});
const downloadBtn = document.getElementById('downloadBtn');
const fileInputs = document.querySelectorAll('.file-input');
const imageItems = document.querySelectorAll('.image-item');

// 更新按钮状态
function updateButtonState() {
    const hasSelected = [...fileInputs].some(input => input.checked);
    downloadBtn.disabled = !hasSelected;
}

// 处理文件选择变化
fileInputs.forEach(input => {
    input.addEventListener('change', () => {
        const parent = input.closest('.image-item');
        parent.classList.toggle('selected', input.checked);
        updateButtonState();
    });
});

async function handleDownload() {
    const selectedCheckboxes = [];
    fileInputs.forEach(checkbox => {
        if (checkbox.checked) {
            selectedCheckboxes.push(checkbox.id);
        }
    });
    const response = await fetch('/api/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(selectedCheckboxes)
    });

    if (response.ok) {
        const result = await response.json();
        console.log(result);
    } else {
        console.error('Error:', response.status, response.statusText);
    }

    // 重置选择状态
    imageItems.forEach(item => item.classList.remove('selected'));
    updateButtonState();
}
// 绑定下载按钮事件
downloadBtn.addEventListener('click', handleDownload);
