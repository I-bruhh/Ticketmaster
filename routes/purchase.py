from flask import Blueprint, request, render_template, redirect, url_for, session
import routes.concert_db as concert_db
import routes.purchase_db as purchase_db

# Create a Blueprint for purchase-related routes
purchase_bp = Blueprint("purchase", __name__)


@purchase_bp.route("/concert/<int:concert_id>/booth", methods=["GET", "POST"])
def booth(concert_id):
    concert = concert_db.get_concert_by_id(concert_id) 

    # Handle GET request to render the booth page
    return render_template("booth.html", concert=concert)


@purchase_bp.route("/concert/<int:concert_id>/summary", methods=["POST"])
def summary(concert_id):
    concert = concert_db.get_concert_by_id(concert_id)

    if request.method == "POST":
        date = request.form.get("date")
        venue = request.form.get("venue")
        category = request.form.get("category")
        quantity = request.form.get("quantity")

        # You can save the selected options in session or a temporary storage
        session['selected_options'] = {
            'concert_id': concert_id,
            'date': date,
            'venue': venue,
            'category': category,
            'quantity': quantity
        }

        # Render the summary page with the selected options
        return render_template("summary.html", concert=concert, selected_options=session['selected_options'])


@purchase_bp.route("/concert/confirm", methods=["GET"])
def confirm():
    purchase_data = session.get('purchase_data', {})

    purchase_db.create_purchase(purchase_data)

    return redirect(url_for("concert.concerts", purchase_data=purchase_data))
