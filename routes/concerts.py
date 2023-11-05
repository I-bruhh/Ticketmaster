from flask import Blueprint, render_template
from models import Concert  # Assuming you have a Concert model

concerts_bp = Blueprint('concerts', __name__)

@concerts_bp.route('/concerts')
def concerts():
    concerts_data = Concert.query.all()
    return render_template('concerts.html', concerts=concerts_data)

@concerts_bp.route('/concert/<int:concert_id>')
def concert_detail(concert_id):
    concert = Concert.query.get(concert_id)
    if concert:
        return render_template('concert_detail.html', concert=concert)
    else:
        return "Concert not found"
