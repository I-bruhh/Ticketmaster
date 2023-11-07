from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session

# Import your Purchase model and database instance
from models import User, Concert, Purchase, db

# Create a Blueprint for purchase-related routes
ticket_fairness_bp = Blueprint("ticket_fairness", __name__)


@ticket_fairness_bp.route("/concert/<int:concert_id>/waiting_room")
def waiting_room(concert_id):
    concert = Concert.query.get(concert_id)
    return render_template("waiting_room.html", concert=concert)  # Pass the concert data to the template