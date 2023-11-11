from flask import Flask, redirect, url_for
from flask_session import Session
from config import Config
from routes.auth import auth_bp
from routes.concert import concert_bp
from routes.profile import profile_bp
from routes.purchase import purchase_bp
from routes.fairness import fairness_bp

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_KEY_PREFIX'] = 'your_prefix'
Session(app)
app.config.from_object(Config)
app.secret_key = 'your_secret_key'

app.config["RECAPTCHA_PUBLIC_KEY"] = "6LcTesEoAAAAAIsnUXGhtHwFIa5zsLeWMrdUX86S"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6LcTesEoAAAAAKkqkiPP9Zfw3b_Byki5VIn0RiKS"

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(concert_bp, url_prefix='/concerts')
app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(purchase_bp, url_prefix='/purchase')
app.register_blueprint(fairness_bp, url_prefix='/fairness')


@app.route('/')
def index():
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
