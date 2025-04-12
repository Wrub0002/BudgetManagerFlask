from flask import Blueprint, request, render_template

# Create a Blueprint for the routes
routes = Blueprint("routes", __name__)


@routes.route("/", methods=["GET", "POST"])
def homepage():
    # Add expense
    if request.method == "POST":
        form_type = request.form["type"]
        date = request.form["date"]
        amount = request.form["amount"]
        description = request.form.get("description", "")
        source = request.form.get("source", "")

        if not date or not amount or (form_type == "expense" and not description) or (
                form_type == "income" and not source):
            return "❌ All fields are required!"

        if form_type == "expense":
            with open("expenses.txt", "a") as file:
                file.write(f"{date} | {description.capitalize()} | {amount}$\n")
        elif form_type == "income":
            with open("income.txt", "a") as file:
                file.write(f"{date} | {source.capitalize()} | {amount}$\n")

    # Show latest income
    latest_income = []
    try:
        with open("income.txt", "r") as file:
            lines = file.readlines()
            last_three = lines[-3:]
            for line in last_three:
                parts = line.strip().split(" | ")
                if len(parts) == 3:
                    latest_income.append({
                        "date": parts[0],
                        "source": parts[1],
                        "amount": parts[2].replace("$", "")
                    })
    except FileNotFoundError:
        pass

    # Show latest expenses
    latest_expenses = []
    try:
        with open("expenses.txt", "r") as file:
            lines = file.readlines()
            last_three = lines[-3:]
            for line in last_three:
                parts = line.strip().split(" | ")
                if len(parts) == 3:
                    latest_expenses.append({
                        "date": parts[0],
                        "description": parts[1],
                        "amount": parts[2].replace("$", "")
                    })
    except FileNotFoundError:
        pass

    return render_template("index.html", latest_expenses=latest_expenses, latest_income=latest_income )
