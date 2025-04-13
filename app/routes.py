from flask import Blueprint, request, render_template
from app import db
from app.models import Expense, Income
from datetime import datetime


# Create a Blueprint for the routes
routes = Blueprint("routes", __name__)

@routes.route("/", methods=["GET", "POST"])
def homepage():
    # Add expense
    if request.method == "POST":
        form_type = request.form["type"]
        date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        amount = request.form["amount"]
        description = request.form.get("description", "")
        source = request.form.get("source", "")

        if not date or not amount or (form_type == "expense" and not description) or (
                form_type == "income" and not source):
            return "❌ All fields are required!"

        if form_type == "expense":
            new_expense = Expense(date=date, description = description.capitalize(), amount=amount)
            db.session.add(new_expense)
            db.session.commit()
        elif form_type == "income":
            new_income = Income(date=date, source=source.capitalize(), amount=amount)
            db.session.add(new_income)
            db.session.commit()

    latest_expenses = Expense.query.order_by(Expense.date.desc()).limit(5).all()

    latest_income = Income.query.order_by(Income.date.desc()).limit(5).all()

    return render_template("index.html", latest_expenses=latest_expenses, latest_income=latest_income )
