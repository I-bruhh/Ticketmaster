from flask import Blueprint
from routes.auth import auth_bp
from routes.concerts import concerts_bp
from routes.views import views_bp
from routes.profile import profile_bp
from routes.purchase import purchase_bp

def create_app():
    app = Blueprint('app', __name__)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(concerts_bp, url_prefix='/concerts')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(purchase_bp, url_prefix='/purchase')
    app.register_blueprint(views_bp)

    return app