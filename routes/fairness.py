from flask import Blueprint, render_template
from routes import concert_db

fairness_bp = Blueprint("fairness", __name__)


@fairness_bp.route('/concert/<int:concert_id>/waiting_room/<int:queue_position>')
def waiting_room(concert_id, queue_position):
    # Fetch the concert based on the concert_id
    selected_concert = concert_db.get_concert_by_id(concert_id)

    return render_template('waiting_room.html', concert=selected_concert, queue_position=queue_position)


@fairness_bp.route('/concert/<int:concert_id>/booth')
def booth(concert_id):
    selected_concert = concert_db.get_concert_by_id(concert_id)

    # Handle GET request to render the booth page
    return render_template("booth.html", concert=selected_concert)