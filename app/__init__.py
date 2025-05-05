from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
flask_bcrypt = Bcrypt()
mail = Mail()

def create_app(config_class='config.Config'):  # Используем строку вместо класса
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    flask_bcrypt.init_app(app)
    mail.init_app(app)

    from app.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
