from flask import Blueprint, render_template
from routes.concert_db import concert_db_bp
import requests

concerts_bp = Blueprint('concerts', __name__)

base_url = 'http://127.0.0.1:5000'


@concerts_bp.route('/concerts')
def concerts():
    concerts_data = requests.get(f'{base_url}/concerts').json()
    print(concerts_data)
    return render_template('concerts.html', concerts=concerts_data)


@concerts_bp.route('/concert/<int:concert_id>')
def concert_detail(concert_id):
    concert = requests.get(f'{base_url}/concerts/{concert_id}').json()
    if concert:
        return render_template('concert_detail.html', concert=concert)
    else:
        return "Concert not found"
