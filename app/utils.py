from flask_mail import Message
from app import mail
from config import Config

def send_email(to, subject, template):
    """ Отправка email """
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=Config.MAIL_DEFAULT_SENDER
    )
    mail.send(msg)

def send_confirmation_email(user_email, token):
    """ Отправка email с подтверждением """
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = f"""
    <p>Пожалуйста, подтвердите ваш email, перейдя по ссылке:</p>
    <p><a href="{confirm_url}">{confirm_url}</a></p>
    <br>
    <p>Спасибо!</p>
    """
    send_email(user_email, "Подтвердите ваш email", html)
