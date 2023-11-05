from flask import Blueprint, render_template, request, redirect, url_for, session
from models import User, db  # Import the specific database instance you need

# Create a Blueprint for profile-related routes
profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile")
def view_profile():
    user = User.query.get(session.get('user_id'))
    return render_template("profile.html", user=user)


@profile_bp.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    user = User.query.get(session.get('user_id'))

    if user:
        if request.method == "POST":
            # Handle user profile updates
            new_username = request.form.get("new_username")
            new_email = request.form.get("new_email")
            new_location = request.form.get("new_location")
            new_phone = request.form.get("new_phone")
            new_about_me = request.form.get("new_about_me")
            new_education = request.form.get("new_education")
            new_work_experience = request.form.get("new_work_experience")

            # Update the user's information in the database and commit the changes
            user.username = new_username
            user.email = new_email
            user.location = new_location
            user.phone = new_phone
            user.about_me = new_about_me
            user.education = new_education
            user.work_experience = new_work_experience

            db.session.commit()

            # Redirect to the user's profile page or display a success message
            return redirect(url_for("profile.view_profile"))

        # Render the profile editing form
        return render_template("edit_profile.html", user=user)

    # Handle the case when no user is logged in
    return redirect(url_for("login"))

# Add more profile-related routes and views as needed
