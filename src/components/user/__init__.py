from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
import requests
from src.models import User
from src import db
from src import app
from itsdangerous import URLSafeTimedSerializer
from itsdangerous import Signer

user_blueprint = Blueprint('userblueprint', __name__, template_folder='../../templates')

def send_email(token, email, username):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox4b0232b56d4f44f2bebe89a671ea2498.mailgun.org/messages",
		auth=("api", app.config["EMAIL_API_KEY"]),
		data={"from": "Bailey Nguyen <baileythuong@gmail.com>",
			"to": [email],
			"subject": f"{username}, you have requested to reset your password.",
			"text": f"Someone (hopefully you) has requested a password reset for your TicketBox account. Follow this link to set a new password: http://localhost:5000/user/new_password/{token}"})

@user_blueprint.route('/')
def root():
  return render_template("user/index.html")

@user_blueprint.route('/login', methods=["GET", "POST"])
def login():
    if not current_user.is_anonymous:
        return redirect(url_for("root"))
    elif request.method == "POST":
        user = User.query.filter_by(username = request.form["username"]).first()
        if not user:
            flash("Username and/or Password is incorrect. Try again.", "danger")
        elif user.check_password(request.form["password"]):
            login_user(user)
            flash("Successfully logged in.", "success")
            return redirect(url_for("root"))
    return render_template('user/login.html')

@user_blueprint.route('/signup', methods=["GET", "POST"])
def signup():
  if current_user.is_authenticated:
    flash("You have already signed up.", "success")
  elif request.method == "POST":
    user = User.query.filter_by(email = request.form["email"]).first()
    # print("user", user.email)
    if not user:
        new_user = User(
            email = request.form['email'],
            username = request.form['username']
        )
        new_user.set_password(request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        flash("Successfully signed up.", "success")
        return redirect(url_for("userblueprint.login"))
    else:
        flash("Email has been taken, please choose another email.", "danger")
  return render_template('user/signup.html')

@user_blueprint.route("/forget_password", methods=["GET", "POST"])
def forget_password():
    if request.method == "POST":
        user = User.query.filter_by(email = request.form["email"]).first()
        if not user:
            flash("Email doesn't exist.", "warning")
            return redirect(url_for("userblueprint.forget_password"))
        s = URLSafeTimedSerializer(app.secret_key)
        token = s.dumps(user.email, salt="reset_password")
        print(token)
        s.loads(token, salt="reset_password")
        send_email(token, user.email, user.username)
        flash("We have sent you an email for you to reset your password.", "warning")
    return render_template("user/forget_password.html")

@user_blueprint.route("new_password/<token>", methods=["GET", "POST"])
def new_password(token):
    s = URLSafeTimedSerializer(app.secret_key)
    email_token = s.loads(token, salt="reset_password")
    user = User.query.filter_by(email = email_token).first()
    if not user:
        flash("Invalid token, please try again.", "danger")
        return redirect(url_for("userblueprint.new_password", token=token))
    if request.method == "POST":
        if request.form["password"] != request.form["confirm"]:
            flash("Password does not match.", "warning")
            return redirect(url_for("userblueprint.new_password", token=token))
        user.set_password(request.form["password"])
        flash("Successfully changed password.", "success")
        return redirect(url_for("root"))
    return render_template("user/new_password.html")

@user_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully logged out.", "success")
    return redirect(url_for("root"))