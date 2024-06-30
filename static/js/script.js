// static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    // Event listener para o formulário de login
    document.getElementById('login-form').addEventListener('submit', async (event) => {
        event.preventDefault(); // Evita o envio tradicional do formulário
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        // Faz uma requisição POST para /login
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                throw new Error('Failed to login');
            }

            const result = await response.json();
            // Redireciona para a URL fornecida pelo servidor após o login
            window.location.href = result.redirect;

        } catch (error) {
            console.error('Login error:', error.message);
            document.getElementById('message').textContent = 'Failed to login';
        }
    });
});
