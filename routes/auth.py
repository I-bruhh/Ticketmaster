from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import routes.auth_db as auth_db
from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    recaptcha = RecaptchaField(validators=[Recaptcha(message="You are detected to possibly be a bot!")])
    submit = SubmitField()


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        data, status_code = auth_db.get_user_by_username(username)
        user_data = data.get_json()
        if status_code == 200:
            if user_data and check_password_hash(user_data['password'], password):
                session['username'] = user_data['username']
                return redirect(url_for('concert.concerts'))
            else:
                return "Login failed"

    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    message = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        data, status_code = auth_db.get_user_by_username(username)

        if status_code == 200:
            message = "Username already exists"
        else:
            user_data = {
                'username': username,
                'password': generate_password_hash(password, method='pbkdf2:sha256')
            }

            data, status_code = auth_db.create_user(user_data)

            if status_code == 200:
                return redirect(url_for('auth.login'))
            else:
                message = "User registration failed"

    return render_template('register.html', message=message)


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Clear the user's session
    return redirect(url_for('auth.login'))
