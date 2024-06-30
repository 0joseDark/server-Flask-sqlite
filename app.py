# app.py

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chave secreta para sessões

# Configurações do Flask-Mail (substitua com suas próprias configurações)
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'

mail = Mail(app)

# Simulação de um banco de dados de usuários
users = {}

# Função para verificar se um usuário já existe
def user_exists(username, email):
    return any(user['username'] == username or user['email'] == email for user in users.values())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = next((u for u in users.values() if u['username'] == username), None)
    if user and check_password_hash(user['password_hash'], password):
        if user['confirmed']:
            session['user_id'] = user['id']
            return jsonify({'redirect': url_for('files')})
        else:
            return jsonify({'error': 'Email not confirmed'}), 401
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    if user_exists(username, email):
        return jsonify({'error': 'Username or email already exists'}), 400

    user_id = len(users) + 1
    confirmation_token = secrets.token_urlsafe(24)
    users[user_id] = {
        'id': user_id,
        'username': username,
        'password_hash': generate_password_hash(password),
        'email': email,
        'confirmed': False,
        'confirmation_token': confirmation_token
    }

    confirm_url = url_for('confirm_email', token=confirmation_token, _external=True)
    msg = Message('Confirm your email', recipients=[email])
    msg.body = f'Click the link to confirm your email: {confirm_url}'
    mail.send(msg)

    return jsonify({'message': 'Registration successful. Please check your email for confirmation.'}), 200

@app.route('/confirm/<token>')
def confirm_email(token):
    for user in users.values():
        if user.get('confirmation_token') == token:
            user['confirmed'] = True
            session['user_id'] = user['id']
            return redirect(url_for('files'))
    
    return 'Invalid confirmation link', 400

@app.route('/files')
def files():
    if 'user_id' in session:
        user_files = ['file1.txt', 'file2.txt']
        return render_template('files.html', user_files=user_files)
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
