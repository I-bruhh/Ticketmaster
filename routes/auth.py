from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import requests

auth_bp = Blueprint('auth', __name__)

base_url = 'http://127.0.0.1:5000'


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Make a GET request to fetch the user data
        response = requests.get(f'{base_url}/users/{username}')

        if response.status_code == 200:
            user_data = response.json()

            if user_data and check_password_hash(user_data['password'], password):
                session['username'] = user_data['username']
                return redirect(url_for('concerts.concerts'))
            else:
                return "Login failed"

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Make a GET request to check if the username already exists
        existing_user = requests.get(f'{base_url}/create_users/{username}')

        if existing_user.status_code == 200:
            return "Username already exists"
        else:
            user_data = {
                'username': username,
                'password': generate_password_hash(password, method='pbkdf2:sha256')
                # Add other user attributes as needed
            }

            # Make a POST request to create the user
            create_user_response = requests.post(f'{base_url}/create_users', json=user_data)

            if create_user_response.status_code == 200:
                return redirect(url_for('auth.login'))
            else:
                return "User registration failed"

    return render_template('register.html')


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Clear the user's session
    return redirect(url_for('auth.login'))
