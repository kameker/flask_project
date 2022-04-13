from os import environ
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validate import validate
from config import from_email, password
from flask import Flask, render_template
from werkzeug.utils import redirect
from werkzeug.security import check_password_hash
from data import db_session
from data.users import User
from forms.reg_user import RegisterForm
from forms.login_user import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/data.db")
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@app.route('/')
def _():
    return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.password.data,
            email=form.email.data,
        )
        print(f"{form.password.data} - {form.email.data}")
        user.set_password(form.password.data)
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        if check_password_hash(db_sess.query(User).filter(User.email.like(form.email.data)).first().hashed_password, form.password.data):
            return redirect('/')
        else:
            return render_template('login.html', title='Вход',
                                       form=form,
                                       message="Неверные данные")
    return render_template('login.html', title='Вход', form=form)


if __name__ == '__main__':
    main()
