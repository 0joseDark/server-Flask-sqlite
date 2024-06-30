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
            document.getElementById('login-message').textContent = 'Failed to login';
        }
    });

    // Event listener para o formulário de registro
    document.getElementById('register-form').addEventListener('submit', async (event) => {
        event.preventDefault(); // Evita o envio tradicional do formulário
        
        const username = document.getElementById('reg-username').value;
        const password = document.getElementById('reg-password').value;
        const email = document.getElementById('email').value;
        
        // Faz uma requisição POST para /register
        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password, email })
            });

            if (!response.ok) {
                throw new Error('Failed to register');
            }

            const result = await response.json();
            // Redireciona para a URL fornecida pelo servidor após o registro
            window.location.href = result.redirect;

        } catch (error) {
            console.error('Registration error:', error.message);
            document.getElementById('register-message').textContent = '
