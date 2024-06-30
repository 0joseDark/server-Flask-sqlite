# app.py

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chave secreta para sessões

# Simulação de um banco de dados de usuários
users = {
    1: {'id': 1, 'username': 'user1', 'password_hash': generate_password_hash('password1'), 'email': 'user1@example.com'},
    2: {'id': 2, 'username': 'user2', 'password_hash': generate_password_hash('password2'), 'email': 'user2@example.com'}
}

# Função para verificar se um usuário já existe
def user_exists(username):
    return any(user['username'] == username for user in users.values())

# Rota para a página inicial (login/register)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para autenticar o usuário
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = next((u for u in users.values() if u['username'] == username), None)
    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        return jsonify({'redirect': url_for('files')})  # Redireciona para /files após login
    
    return jsonify({'error': 'Invalid credentials'}), 401

# Rota para criar uma nova conta de usuário
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    # Verifica se o usuário já existe
    if user_exists(username):
        return jsonify({'error': 'Username already exists'}), 400

    # Cria um novo usuário
    user_id = max(users.keys()) + 1
    users[user_id] = {
        'id': user_id,
        'username': username,
        'password_hash': generate_password_hash(password),
        'email': email
    }

    return jsonify({'redirect': url_for('files')})  # Redireciona para /files após registro

# Rota para a página de arquivos
@app.route('/files')
def files():
    if 'user_id' in session:
        # Aqui você pode implementar a lógica para listar os arquivos do usuário
        user_id = session['user_id']
        # Supondo que você tenha uma função para obter os arquivos do usuário
        user_files = []  # Implemente a lógica para obter os arquivos do usuário
        return render_template('files.html', user_files=user_files)
    else:
        return redirect(url_for('index'))

# Rota para fazer logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
