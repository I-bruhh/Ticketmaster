from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session

# Import your Purchase model and database instance
from models import User, Concert, Purchase, db

# Create a Blueprint for purchase-related routes
purchase_bp = Blueprint("purchase", __name__)


@purchase_bp.route("/concert/<int:concert_id>/booth", methods=["GET", "POST"])
def booth(concert_id):
    concert = Concert.query.get(concert_id)

    # Handle GET request to render the booth page
    return render_template("booth.html", concert=concert)


@purchase_bp.route("/concert/<int:concert_id>/summary", methods=["POST"])
def summary(concert_id):
    concert = Concert.query.get(concert_id)
    user = User.query.get(session.get('user_id'))

    if request.method == "POST":
        date = request.form.get("date")
        venue = request.form.get("venue")
        category = request.form.get("category")
        quantity = request.form.get("quantity")

        # You can save the selected options in session or a temporary storage
        session['selected_options'] = {
            'user_id': user.id,
            'concert_id': concert_id,
            'date': date,
            'venue': venue,
            'category': category,
            'quantity': quantity
        }

        # Render the summary page with the selected options
        return render_template("summary.html", concert=concert, selected_options=session['selected_options'])

    # Handle other cases or errors as needed
    return redirect(url_for("index"))


@purchase_bp.route("/concert/<int:concert_id>/confirm", methods=["POST"])
def confirm(concert_id):
    user = User.query.get(session.get('user_id'))

    if request.method == "POST":
        concert_id = request.form.get("concert_id")
        concert_name = request.form.get("concert_name")
        date = request.form.get("concert_date")
        venue = request.form.get("concert_venue")
        category = request.form.get("ticket_category")
        quantity = request.form.get("ticket_quantity")

        # Create a new purchase and add it to the database
        purchase = Purchase(user_id=user.id, concert_id=concert_id, concert_name=concert_name, date=date, venue=venue, category=category, quantity=quantity)
        db.session.add(purchase)
        db.session.commit()

        # Construct a success message
        message = f"Successful purchase! Your ticket summary: Date: {date}, Venue: {venue}, Category: {category}, Quantity: {quantity}"

        return redirect(url_for("concerts.concerts", message=message))

    # Handle other cases or errors as needed
    return redirect(url_for("index"))
