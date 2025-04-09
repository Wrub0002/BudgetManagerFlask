
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def homepage():

    # Add Expenses
    if request.method == "POST":
        form_type = request.form["type"]

        if form_type == "expense":
            date = request.form["date"]
            amount = request.form["amount"]
            description = request.form["description"].capitalize()
            with open("expenses.txt", "a") as file:
                file.write(f"{date} | {description} | {amount}$\n")

        # Add Income
        elif form_type == "income":
            date = request.form["date"]
            source = request.form["source"].capitalize()
            amount = request.form["amount"]
            with open("income.txt", "a") as file:
                file.write(f"{date} | {source} | {amount}$\n")

        # Recent income expenses
        latest_income = []
        try:
            with open("income.txt", "r") as file:
                lines = file.readlines()
                last_three = lines[-3:]

                for line in last_three:
                    parts = line.strip().split(" | ")
                    if len(parts) == 3:
                        date = parts[0]
                        source = parts[1]
                        amount = parts[2].replace("$", "")
                        latest_income.append({
                            "date": date,
                            "source": source,
                            "amount": amount
                        })
        except FileNotFoundError:
            pass

    # Recent Expenses
    latest_expenses = []

    with open("expenses.txt", "r") as file:
        lines = file.readlines()
        last_three = lines[-3:]

        for line in last_three:
            parts = line.strip().split(" | ")
            if len(parts) == 3:
                date = parts[0]
                description = parts[1]
                amount = parts[2].replace("$", "")
                latest_expenses.append({
                    "date": date,
                    "description": description,
                    "amount": amount
                })


    return render_template("index.html", latest_expenses=latest_expenses, latest_income=latest_income)

@app.route("/expenses")
def show_expenses():
    with open("expenses.txt", "r") as file:
        expenses = [line.strip() for line in file.readlines()]
        return render_template("expenses.html", expenses = expenses)


app.run(debug=True)