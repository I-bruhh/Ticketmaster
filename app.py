from flask import Flask, redirect, url_for
from config import Config
from routes.auth import auth_bp
from routes.concert import concerts_bp
from routes.profile import profile_bp
from routes.purchase import purchase_bp
from routes.auth_db import auth_db_bp
from routes.concert_db import concert_db_bp
from routes.purchase_db import purchase_db_bp

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key'


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(concerts_bp, url_prefix='/concerts')
app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(purchase_bp, url_prefix='/purchase')

app.register_blueprint(auth_db_bp)
app.register_blueprint(concert_db_bp)
app.register_blueprint(purchase_db_bp)


@app.route('/')
def index():
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
