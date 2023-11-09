from flask import Blueprint, render_template, request, redirect, url_for, session
import boto3
import routes.auth_db as auth_db

profile_bp = Blueprint("profile", __name__)

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='ap-southeast-1', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')

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


@profile_bp.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    user_id = session.get('user_id')

    if user_id:
        try:
            response = dynamodb.get_item(
                TableName=user_table_name,
                Key={'user_id': {'N': user_id}}
            )
            item = response.get('Item')

            if item:
                user = dict((k, v['S']) for k, v in item.items())

                if request.method == "POST":
                    new_username = request.form.get("new_username")
                    new_email = request.form.get("new_email")
                    new_location = request.form.get("new_location")
                    new_phone = request.form.get("new_phone")
                    new_about_me = request.form.get("new_about_me")
                    new_education = request.form.get("new_education")
                    new_work_experience = request.form.get("new_work_experience")

                    user_data = {
                        'user_id': user_id,
                        'username': new_username,
                        'email': new_email,
                        'location': new_location,
                        'phone': new_phone,
                        'about_me': new_about_me,
                        'education': new_education,
                        'work_experience': new_work_experience
                    }

                    response = dynamodb.put_item(
                        TableName=user_table_name,
                        Item={k: {'S': str(v)} for k, v in user_data.items()}
                    )

                    return redirect(url_for("profile.view_profile"))

                return render_template("edit_profile.html", user=user)

        except Exception as e:
            return str(e), 500

    return redirect(url_for("login"))

# Add more profile-related routes
