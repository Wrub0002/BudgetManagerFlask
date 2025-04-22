import re
from dbm import error

from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from app import db
from app.models import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    errors = {}

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user:
            errors["username"] = "Username not found"
        elif not check_password_hash(user.password_hash, password):
            errors["password"] = "Incorrect password"

        if errors:
            return render_template("login.html", errors=errors, username=username)

        login_user(user)
        flash("✅ Login successful!", category="success")
        return redirect(url_for("routes.homepage"))

    return render_template("login.html", errors={})


@auth.route("/logout")
def logout():
    logout_user()
    flash("✅ You have been logged out.", category="success")
    return redirect(url_for("auth.login"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    errors = {}
    username = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Username validation
        if len(username) < 3:
            errors["username"] = "Username must be at least 3 characters long"
        elif not re.match("^[a-zA-Z0-9_]+$", username):
            errors["username"] = "Username can only contain letters, numbers, and underscores"
        elif User.query.filter_by(username=username).first():
            errors["username"] = "Username already exists"

        # Password validation
        if len(password) < 8:
            errors["password"] = "Password must be at least 8 characters long"
        elif not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            errors["password"] = "Password must include both letters and numbers"

        # Confirm password
        if password != confirm_password:
            errors["confirm_password"] = "Passwords do not match"

        # Check if there are any errors
        if errors:
            return render_template("register.html", errors=errors, username=username, form_submitted=True)


        new_user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        flash("✅ Account created! Please log in.", category="success")
        return redirect(url_for("auth.login"))


    return render_template("register.html", errors={}, username="", form_submitted=False)