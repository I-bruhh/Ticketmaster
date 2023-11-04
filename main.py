from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///purchases.db'  # SQLite database
app.secret_key = 'your_secret_key'  # Set a secret key for session management
db = SQLAlchemy(app)

app.static_folder = 'static'

concerts_data = [
    {
        "name": "Concert 1",
        "dates": ["2023-11-10", "2023-11-15"],
        "venues": ["Venue 1", "Venue 2"],
        "categories": [100, 50],
        "start_ticket_sale": "2023-10-15 10:00:00",
        "end_ticket_sale": "2023-11-08 17:00:00",
        "limit_per_person": 5,
        "total_tickets_for_sale": 500,
        "waiting_room": [],
        "ticket_sales_started": False,
    },
    {
        "name": "Concert 2",
        "dates": ["2023-12-01", "2023-12-10"],
        "venues": ["Venue 3", "Venue 4"],
        "categories": [80, 60],
        "start_ticket_sale": "2023-11-15 09:00:00",
        "end_ticket_sale": "2023-11-28 18:00:00",
        "limit_per_person": 4,
        "total_tickets_for_sale": 300,
        "waiting_room": [],
        "ticket_sales_started": False,
    }
]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
    app.secret_key = 'your_secret_key'  # Set a secret key for session management
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create database tables
    return app

app = create_app()

def process_queue(concert):
    if concert["ticket_sales_started"]:
        return "Ticket sales have already started for this concert."

    concert["waiting_room"].sort(key=lambda user: user["arrival_time"])
    for user in concert["waiting_room"]:
        # Process users based on arrival time
        # For example, assign tickets to users or perform other actions here
        user_arrival_time = user["arrival_time"]
        # Process the user with arrival time `user_arrival_time`

    concert["ticket_sales_started"] = True
    return "Ticket sales started for this concert."

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/concerts')
def dashboard():
    return render_template('index.html', concerts=concerts_data)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/join_waiting_room/<int:concert_id>', methods=['POST'])
def join_waiting_room(concert_id):
    if request.method == 'POST':
        arrival_time = request.form.get('arrival_time')
        concert = concerts_data[concert_id]

        if not concert["ticket_sales_started"]:
            concert["waiting_room"].append({"arrival_time": arrival_time})
            return "You've joined the waiting room."
        else:
            return "Ticket sales have already started for this concert."

    return render_template('join_waiting_room.html')

@app.route('/start_sale/<int:concert_id>')
def start_sale(concert_id):
    concert = concerts_data[concert_id]
    process_queue(concert)  # Start the ticket sale process
    return "Ticket sales started for this concert."

@app.route('/concert/<int:concert_id>')
def concert_detail(concert_id):
    if 0 <= concert_id < len(concerts_data):
        concert = concerts_data[concert_id]
        return render_template('concert_detail.html', concert=concert)
    else:
        return "Concert not found"

@app.route('/purchase', methods=['POST'])
def purchase_tickets():
    date = request.form.get('date')
    venue = request.form.get('venue')
    category = request.form.get('category')

    # Create a new purchase and add it to the database
    purchase = Purchase(date=date, venue=venue, category=category)
    db.session.add(purchase)
    db.session.commit()

    # Display a popup message with the purchase details using JavaScript
    popup_message = f'Successful purchase! Your ticket summary: Date: {date}, Venue: {venue}, Category: {category}'

    return render_template('index.html', concerts=concerts_data, popup_message=popup_message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store user ID in session
            return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
        else:
            return "Login failed"

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            return "Username already exists"
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))  # Redirect to login after successful registration

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
