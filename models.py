from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON

# Create a single SQLAlchemy instance for the 'ticketmaster' database
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), default=None)  # Set a default value of None
    location = db.Column(db.String(120), default=None)
    phone = db.Column(db.String(20), default=None)
    about_me = db.Column(db.Text, default=None)
    education = db.Column(db.Text, default=None)
    work_experience = db.Column(db.Text, default=None)


class Concert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dates = db.Column(JSON, nullable=False)
    venues = db.Column(JSON, nullable=False)
    categories = db.Column(JSON, nullable=False)
    start_ticket_sale = db.Column(db.String(100), nullable=False)
    end_ticket_sale = db.Column(db.String(100), nullable=False)
    limit_per_person = db.Column(db.Integer, nullable=False)
    total_tickets_for_sale = db.Column(db.Integer, nullable=False)
    waiting_room = db.Column(JSON, nullable=False)
    ticket_sales_started = db.Column(db.Boolean, default=False)


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.id'), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='purchases')
    concert = db.relationship('Concert', back_populates='purchases')


# Define relationships for the models within the 'ticketmaster' database
User.purchases = db.relationship('Purchase', back_populates='user')
Concert.purchases = db.relationship('Purchase', back_populates='concert')
