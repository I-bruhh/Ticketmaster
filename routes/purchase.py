from flask import Blueprint, request, render_template, redirect, url_for, session
from routes.auth_db import auth_db_bp
from routes.concert_db import concert_db_bp
from routes.purchase_db import purchase_db_bp

# Create a Blueprint for purchase-related routes
purchase_bp = Blueprint("purchase", __name__)


@purchase_bp.route("/concert/<int:concert_id>/booth", methods=["GET", "POST"])
def booth(concert_id):
    concert = concert_db_bp.get_concert_by_id(concert_id)  # Use concert_db_bp function

    # Handle GET request to render the booth page
    return render_template("booth.html", concert=concert)


@purchase_bp.route("/concert/<int:concert_id>/summary", methods=["POST"])
def summary(concert_id):
    concert = concert_db_bp.get_concert_by_id(concert_id)  # Use concert_db_bp function
    user = auth_db_bp.get_user_by_id(session.get('user_id'))  # Use user_db_bp function

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


@purchase_bp.route("/concert/confirm", methods=["POST"])
def confirm():
    user = auth_db_bp.get_user_by_id(session.get('user_id'))  # Use user_db_bp function

    if request.method == "POST":
        concert_id = request.form.get("concert_id")
        concert_name = request.form.get("concert_name")
        date = request.form.get("concert_date")
        venue = request.form.get("concert_venue")
        category = request.form.get("ticket_category")
        quantity = request.form.get("ticket_quantity")

        # Create a new purchase and add it to the database
        purchase_data = {
            'user_id': user.id,
            'concert_id': concert_id,
            'concert_name': concert_name,
            'date': date,
            'venue': venue,
            'category': category,
            'quantity': quantity
        }

        purchase_db_bp.create_purchase(purchase_data)  # Use purchase_db_bp function

        # Construct a success message
        message = f"Successful purchase! Your ticket summary: Date: {date}," \
                  f" Venue: {venue}, Category: {category}, Quantity: {quantity}"

        return redirect(url_for("concerts.concerts", message=message))

    # Handle other cases or errors as needed
    return redirect(url_for("index"))
