from flask import Flask
from config import Config
from models import db
from blueprints import create_app

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key'

# Initialize the 'ticketmaster' database using the SQLAlchemy instance 'db'
db.init_app(app)

with app.app_context():
    db.create_all()

main_app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
