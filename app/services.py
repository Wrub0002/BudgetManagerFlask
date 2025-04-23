from app.models import Expense, Income
from sqlalchemy import extract, func
from datetime import datetime
from flask import flash, redirect
from app import db

# Get the selected month and year from the request
def get_selected_month_year(request):
    month = request.args.get("month", default=datetime.now().month, type=int)
    year = request.args.get("year", default=datetime.now().year, type=int)

    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    return month, year

# Handle form submission for both income and expense
def handle_form_submission(form, user_id):
    form_type = form["type"]
    date = datetime.strptime(form["date"], "%Y-%m-%d").date()
    amount = form["amount"]
    description = form.get("description", "")
    source = form.get("source", "")
    category = form.get("category")

    if not date or not amount or (form_type == "expense" and not description) or (
            form_type == "income" and not source):
        flash("❌ All fields are required!", category="warning")
        return redirect("/")

    if form_type == "expense":
        new_expense = Expense(date=date, description=description.capitalize(), amount=amount, category=category,
                              user_id=user_id)
        db.session.add(new_expense)
    elif form_type == "income":
        new_income = Income(date=date, source=source.capitalize(), amount=amount, category=category,
                            user_id=user_id)
        db.session.add(new_income)

    db.session.commit()
    flash("✅ Form submitted successfully!", category="success")

# Check if the form submission was successful
def get_monthly_transactions(user_id, month, year):
    expenses = Expense.query.filter_by(user_id=user_id).filter(
        extract('month', Expense.date) == month,
        extract('year', Expense.date) == year
    ).all()

    income = Income.query.filter_by(user_id=user_id).filter(
        extract('month', Income.date) == month,
        extract('year', Income.date) == year
    ).all()

    return expenses, income

# Calculate total income, expenses, and balance
def calculate_summary(expenses, income):
    total_income = round(sum(i.amount for i in income), 2)
    total_expenses = round(sum(e.amount for e in expenses), 2)
    balance = round(total_income - total_expenses, 2)
    return total_income, total_expenses, balance

# Get expense chart data
def get_expense_chart_data(user_id, month, year):
    expense_data = db.session.query(
        Expense.category,
        func.sum(Expense.amount)
    ).filter_by(user_id=user_id).filter(
        extract('month', Expense.date) == month,
        extract('year', Expense.date) == year
    ).group_by(Expense.category).all()

    labels = [category for category, _ in expense_data]
    values = [float(amount) for _, amount in expense_data]
    return labels, values

# Get income chart data
def get_income_chart_data(user_id, month, year):
    income_data = db.session.query(
        Income.category,
        func.sum(Income.amount)
    ).filter_by(user_id=user_id).filter(
        extract('month', Income.date) == month,
        extract('year', Income.date) == year
    ).group_by(Income.category).all()

    labels = [category for category, _ in income_data]
    values = [float(amount) for _, amount in income_data]
    return labels, values

# Get total comparison data
def get_total_comparison_data(user_id, month, year):
    total_income = db.session.query(
        func.sum(Income.amount)
    ).filter_by(user_id=user_id).filter(
        extract('month', Income.date) == month,
        extract('year', Income.date) == year
    ).scalar() or 0

    total_expense = db.session.query(
        func.sum(Expense.amount)
    ).filter_by(user_id=user_id).filter(
        extract('month', Expense.date) == month,
        extract('year', Expense.date) == year
    ).scalar() or 0

    labels = ["Income", "Expenses"]
    values = [float(total_income), float(total_expense)]
    return labels, values
