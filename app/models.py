from datetime import datetime
from app import db, flask_bcrypt
import jwt
from config import Config

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def generate_email_confirmation_token(self, expires_in=86400):
        return jwt.encode(
            {'email_confirmation': self.id, 'exp': datetime.utcnow() + timedelta(seconds=expires_in)},
            Config.SECRET_KEY,
            algorithm='HS256'
        )

    @staticmethod
    def verify_email_confirmation_token(token):
        try:
            id = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])['email_confirmation']
        except:
            return None
        return User.query.get(id)
