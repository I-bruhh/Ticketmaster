from flask import Flask
from config import Config
from models import db
from routes.auth import auth_bp
from routes.concerts import concerts_bp
from routes.views import views_bp
from routes.profile import profile_bp
from routes.purchase import purchase_bp

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key'

# Initialize the 'ticketmaster' database using the SQLAlchemy instance 'db'
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(concerts_bp, url_prefix='/concerts')
app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(purchase_bp, url_prefix='/purchase')
app.register_blueprint(views_bp)

if __name__ == '__main__':
    app.run(debug=True)
