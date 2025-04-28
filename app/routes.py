from flask import Blueprint, request, render_template, redirect
from app import db
from app.models import Expense, Income
from datetime import datetime
from flask_login import login_required, current_user
from app.services import (
    get_selected_month_year,
    handle_form_submission,
    get_monthly_transactions,
    calculate_summary,
    get_expense_chart_data,
    get_income_chart_data,
    get_total_comparison_data
)

# Create a Blueprint for the routes
routes = Blueprint("routes", __name__)


@routes.route("/delete/expense/<int:id>", methods=["POST"])
def delete_expense(id):
    """Delete an expense by its ID and redirect to homepage."""
    expense = Expense.query.get_or_404(id)  # Fetch the expense or return 404
    db.session.delete(expense)              # Delete from database
    db.session.commit()                     # Commit changes
    return redirect("/")                    # Redirect back to homepage


@routes.route("/delete/income/<int:id>", methods=["POST"])
def delete_income(id):
    """Delete an income by its ID and redirect to homepage."""
    income = Income.query.get_or_404(id)     # Fetch the income or return 404
    db.session.delete(income)                # Delete from database
    db.session.commit()                      # Commit changes
    return redirect("/")                     # Redirect back to homepage


@routes.route("/", methods=["GET", "POST"])
@login_required
def homepage():
    """Render the main dashboard page with user's transactions and summaries."""
    # Get the selected month and year from the request (default to current if none)
    month, year = get_selected_month_year(request)

    if request.method == "POST":
        # Handle form submission for adding income or expenses
        response = handle_form_submission(request.form, current_user.id)
        if response:
            return response

    # Fetch transactions for the selected month
    month_expenses, month_income = get_monthly_transactions(current_user.id, month, year)

    # Calculate total income, expenses, and balance
    total_income, total_expenses, balance = calculate_summary(month_expenses, month_income)

    # Prepare data for expense and income charts
    expense_labels, expense_values = get_expense_chart_data(current_user.id, month, year)
    income_labels, income_values = get_income_chart_data(current_user.id, month, year)
    total_labels, total_values = get_total_comparison_data(current_user.id, month, year)

    # Emojis for categories (used for visual enhancement in the UI)
    category_emojis = {
        "Food": "🍔", "Transport": "🚌", "Housing": "🏠", "Entertainment": "🎮",
        "Healthcare": "💊", "Clothing": "👕", "Education": "🎓", "Subscriptions": "📦",
        "Other": "❓", "Salary": "💼", "Investment": "📈", "Gift": "🎁",
        "Side Job": "🛠️", "Rental": "🏘️", "Interest": "💵", "Dividends": "📊",
        "Bonus": "💰", "Freelance": "🧑‍💻"
    }

    # Render the dashboard template with all necessary data
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
        expense_values=expense_values,
        income_labels=income_labels,
        income_values=income_values,
        total_labels=total_labels,
        total_values=total_values
    )
