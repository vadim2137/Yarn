from flask import Blueprint, request, jsonify, url_for
from datetime import datetime
from app import db, flask_bcrypt, mail
from app.models import User
from app.utils import send_confirmation_email
import jwt
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    required_fields = ['first_name', 'last_name', 'username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Все поля обязательны для заполнения'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Пользователь с таким email уже существует'}), 409
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Этот username уже занят'}), 409
    
    try:
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Пользователь успешно зарегистрирован',
            'user_id': user.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    """ Подтверждение email """
    user = User.verify_email_confirmation_token(token)
    if not user:
        return jsonify({'message': 'Неверный или просроченный токен'}), 400
    
    if user.email_confirmed:
        return jsonify({'message': 'Email уже подтвержден'}), 200
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Email успешно подтвержден'}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    """ Аутентификация пользователя """
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email и пароль обязательны'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.verify_password(data['password']):
        return jsonify({'message': 'Неверный email или пароль'}), 401
    
    if not user.email_confirmed:
        return jsonify({'message': 'Пожалуйста, подтвердите ваш email'}), 403
    
    return jsonify({
        'message': 'Успешный вход',
        'user_id': user.id,
        'email': user.email
    }), 200
