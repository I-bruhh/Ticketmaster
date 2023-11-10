from flask import Blueprint, render_template
import routes.concert_db as concert_db

concert_bp = Blueprint('concert', __name__)


@concert_bp.route('/concerts')
def concerts():
    concerts_data = concert_db.get_all_concerts().get_json()
    return render_template('concerts.html', concerts=concerts_data)


@concert_bp.route('/concert/<int:concert_id>')
def concert_detail(concert_id):
    concert = concert_db.get_concert_by_id(concert_id)
    if concert:
        return render_template('concert_detail.html', concert=concert)
    else:
        return "Concert not found"
