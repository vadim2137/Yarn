import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://yarny:Zgikizoli1180!@localhost:5432/user_registration')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-here')
    
    # Настройки почты (пример для Mailtrap)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.mailtrap.io')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 2525))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'no-reply@example.com')
    
    # Настройки приложения
    APP_NAME = "User Registration API"
    EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
