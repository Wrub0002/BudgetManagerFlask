from flask import Blueprint, request, render_template, redirect, flash
from app import db
from app.models import Expense, Income
from datetime import datetime
from flask_login import login_required, current_user
from app.services import get_selected_month_year, handle_form_submission, get_monthly_transactions, calculate_summary, get_expense_chart_data

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
    month, year = get_selected_month_year(request)

    if request.method == "POST":
        response = handle_form_submission(request.form, current_user.id)
        if response:
            return response

    month_expenses, month_income = get_monthly_transactions(current_user.id, month, year)
    total_income, total_expenses, balance = calculate_summary(month_expenses, month_income)
    expense_labels, expense_values = get_expense_chart_data(current_user.id, month, year)

    category_emojis = {
        "Food": "🍔", "Transport": "🚌", "Housing": "🏠", "Entertainment": "🎮",
        "Healthcare": "💊", "Clothing": "👕", "Education": "🎓", "Subscriptions": "📦",
        "Other": "❓", "Salary": "💼", "Investment": "📈", "Gift": "🎁",
        "Side Job": "🛠️", "Rental": "🏘️", "Interest": "💵", "Dividends": "📊",
        "Bonus": "💰", "Freelance": "🧑‍💻"
    }

    return render_template("index.html",
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        month_expenses=month_expenses,
        month_income=month_income,
        selected_month=month,
        selected_year=year,
        selected_month_name=datetime(year, month, 1).strftime("%B"),
        current_user=current_user,
        category_emojis=category_emojis,
        expense_labels=expense_labels,
        expense_values=expense_values
    )