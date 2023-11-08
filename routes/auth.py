from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import requests

auth_bp = Blueprint('auth', __name__)


# Define the base URL for the auth_db_bp blueprint
auth_db_base_url = 'http://127.0.0.1:5432'  # Update with the correct URL


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Make a GET request to fetch the user data
        response = requests.get(f'{auth_db_base_url}/auth_db/users/{username}')

        if response.status_code == 200:
            user_data = response.json()

            if user_data and check_password_hash(user_data['password'], password):
                session['user_id'] = user_data['user_id']
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
        existing_user = requests.get(f'{auth_db_base_url}/auth_db/users/{username}')

        if existing_user.status_code == 200:
            return "Username already exists"
        else:
            user_data = {
                'username': username,
                'password': generate_password_hash(password, method='pbkdf2:sha256')
                # Add other user attributes as needed
            }

            # Make a POST request to create the user
            create_user_response = requests.post(f'{auth_db_base_url}/auth_db/users', json=user_data)

            if create_user_response.status_code == 200:
                return redirect(url_for('auth.login'))
            else:
                return "User registration failed"

    return render_template('register.html')


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Clear the user's session
    return redirect(url_for('auth.login'))
