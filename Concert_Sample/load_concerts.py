import json
from models import db, Concert
from main import app  # Replace with the actual import path of your Flask app

# Create an application context
with app.app_context():
    # Load data from JSON file
    with open('concerts.json', 'r') as file:
        concerts_data = json.load(file)

    # Iterate through the data and insert it into the database
    for data in concerts_data:

        concert = Concert(
            name=data["name"],
            dates=data["dates"],  # Convert to a JSON string
            venues=data["venues"],  # Convert to a JSON string
            categories=data["categories"],  # Convert to a comma-separated string
            start_ticket_sale=data["start_ticket_sale"],
            end_ticket_sale=data["end_ticket_sale"],
            limit_per_person=data["limit_per_person"],
            total_tickets_for_sale=data["total_tickets_for_sale"],
            waiting_room=data["waiting_room"],  # Convert to a JSON string
            ticket_sales_started=data["ticket_sales_started"] == "True"
        )

        # Add the concert to the session
        db.session.add(concert)

    # Commit the changes
    db.session.commit()
