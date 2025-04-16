from flask import Blueprint, request, render_template, redirect
from app import db
from app.models import Expense, Income
from datetime import datetime
from sqlalchemy import extract
from flask_login import login_required, current_user


# Create a Blueprint for the routes
routes = Blueprint("routes", __name__)

@routes.route("/delete/expense/<int:id>", methods=["POST"])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect("/")

@routes.route("/delete/income/<int:id>", methods=["POST"])
def delete_income(id):
    income = Income.query.get_or_404(id)
    db.session.delete(income)
    db.session.commit()
    return redirect("/")

@routes.route("/", methods=["GET", "POST"])
@login_required
def homepage():
    # receive month and year from the request
    month = request.args.get("month", default=datetime.now().month, type=int)
    year = request.args.get("year", default=datetime.now().year, type=int)

    # Validate month and year
    if month < 1 or month > 12:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

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
            new_expense = Expense(date=date, description = description.capitalize(), amount=amount, user_id=current_user.id)
            db.session.add(new_expense)
            db.session.commit()
        elif form_type == "income":
            new_income = Income(date=date, source=source.capitalize(), amount=amount, user_id=current_user.id)
            db.session.add(new_income)
            db.session.commit()

    month_expenses = Expense.query.filter_by(user_id=current_user.id).filter(
        extract('month', Expense.date) == month,
        extract('year', Expense.date) == year
    ).all()

    month_income = Income.query.filter_by(user_id=current_user.id).filter(
        extract('month', Income.date) == month,
        extract('year', Income.date) == year
    ).all()

    # Calculate the total income for the current month
    total_income = sum(i.amount for i in month_income)
    total_expenses = sum(e.amount for e in month_expenses)
    balance = total_income - total_expenses


    return render_template("index.html",total_income=total_income, total_expenses=total_expenses, balance=balance
                           , month_expenses=month_expenses, month_income=month_income, selected_month=month, selected_year=year, selected_month_name=datetime(year, month, 1).strftime("%B"),
                           current_user=current_user)
