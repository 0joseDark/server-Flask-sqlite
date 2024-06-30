// static/js/











































































































































































































































































// Função para exibir mensagens na página
function showMessage(message, elementId, isError = false) {
    const messageDiv = document.getElementById(elementId);
    messageDiv.textContent = message;
    messageDiv.style.color = isError ? 'red' : 'green';
}

// Função para buscar e exibir a lista de arquivos do usuário
async function fetchFiles() {
    try {
        const response = await fetch('/files/list');
        if (!response.ok) {
            throw new Error('Failed to fetch files');
        }
        const files = await response.json();
        const fileList = document.getElementById('file-list');
        fileList.innerHTML = '';
        files.forEach(file => {
            const li = document.createElement('li');
            li.innerHTML = `
                <a href="#" onclick="downloadFile('${file}')">${file}</a>
                <button onclick="deleteFile('${file}')">Delete</button>
            `;
            fileList.appendChild(li);
        });
    } catch (error) {
        console.error('Error fetching files:', error.message);
    }
}

// Função para lidar com o envio de arquivos
document.getElementById('upload-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById('file-input');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) {
            throw new Error('Failed to upload file');
        }
        const result = await response.json();
        showMessage(result.message, 'message');
        fileInput.value = ''; // Limpa o input de arquivo
        fetchFiles(); // Atualiza a lista de arquivos
    } catch (error) {
        console.error('Error uploading file:', error.message);
        showMessage('Failed to upload file', 'message', true);
    }
});

// Função para lidar com a exclusão de arquivos
async function deleteFile(filename) {
    if (!confirm(`Are you sure you want to delete ${filename}?`)) {
        return;
    }
    try {
        const response = await fetch(`/delete/${filename}`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Failed to delete file');
        }
        const result = await response.json();
        showMessage(result.message, 'message');
        fetchFiles(); // Atualiza a lista de arquivos após exclusão
    } catch (error) {
        console.error('Error deleting file:', error.message);
        showMessage('Failed to delete file', 'message', true);
    }
}

// Função para fazer o download de um arquivo
function downloadFile(filename) {
    window.location.href = `/download/${filename}`;
}

// Inicializa a página buscando e exibindo os arquivos do usuário
fetchFiles();
