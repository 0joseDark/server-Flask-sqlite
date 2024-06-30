# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import re
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Chave para criptografar a sessão
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'user_files'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
db = SQLAlchemy(app)

# Modelo de usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

# Inicializando o banco de dados
with app.app_context():
    db.create_all()

def get_user_folder(user_id):
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return user_folder

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email'}), 400

    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({'error': 'Email or username already exists'}), 409
    
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/files')
def files():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    return render_template('files.html')

@app.route('/files/list')
def list_files():
    if 'user_id' not in session:
        return jsonify([])  # Retorna uma lista vazia se não estiver autenticado
    
    user_folder = get_user_folder(session['user_id'])
    user_files = os.listdir(user_folder)
    return jsonify(user_files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filename = secure_filename(file.filename)
    user_folder = get_user_folder(session['user_id'])
    file.save(os.path.join(user_folder, filename))
    
    return jsonify({'message': 'File uploaded successfully'})

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_folder = get_user_folder(session['user_id'])
    file_path = os.path.join(user_folder, secure_filename(filename))
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'})
    return jsonify({'error': 'File not found'}), 404

@app.route('/download/<filename>')
def download_file(filename):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_folder = get_user_folder(session['user_id'])
    return send_from_directory(user_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)
