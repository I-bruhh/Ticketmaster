from flask import Blueprint, request, redirect, url_for, jsonify, session

# Import your Purchase model and database instance
from models import User, Purchase, db

# Create a Blueprint for purchase-related routes
purchase_bp = Blueprint("purchase", __name__)


@purchase_bp.route("/purchase", methods=["POST"])
def purchase_tickets():
    user = User.query.get(session.get('user_id'))

    if request.method == "POST":
        concert_id = request.form.get("concert_id")
        date = request.form.get("date")
        venue = request.form.get("venue")
        category = request.form.get("category")
        quantity = request.form.get("quantity")

        # Create a new purchase and add it to the database
        purchase = Purchase(user_id=user.id, concert_id=concert_id, date=date, venue=venue, category=category, quantity=quantity)
        db.session.add(purchase)
        db.session.commit()

        # Construct a success message
        message = f"Successful purchase! Your ticket summary: Date: {date}, Venue: {venue}, Category: {category}, Quantity: {quantity}"

        return redirect(url_for("concerts.concerts", message=message))

    # Handle other cases or errors as needed
    return redirect(url_for("index"))
