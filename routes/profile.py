from flask import Blueprint, render_template, session
import boto3
import routes.auth_db as auth_db

profile_bp = Blueprint("profile", __name__)

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the DynamoDB table name for the User model
user_table_name = 'User'


@profile_bp.route("/profile")
def view_profile():
    username = session.get('username')
    user = auth_db.get_user_by_username(username)

    try:
        if user:
            return render_template("profile.html", user=user)
        else:
            return "User not found"
    except Exception as e:
        return str(e), 500
