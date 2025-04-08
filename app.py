
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        date = request.form["date"]
        description = request.form["description"].capitalize()
        amount = request.form["amount"]

        with open("expenses.txt", "a") as file:
            file.write(f"{date} | {description} | {amount}$\n")

    latest_expenses = []

    # Read the last three lines from the expenses file
    with open("expenses.txt", "r") as file:
        lines = file.readlines()
        last_three = lines[-3:]

        # Process the last three lines to extract date, description, and amount
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

    return render_template("index.html", latest_expenses=latest_expenses)

@app.route("/expenses")
def show_expenses():
    with open("expenses.txt", "r") as file:
        expenses = [line.strip() for line in file.readlines()]
        return render_template("expenses.html", expenses = expenses)


app.run(debug=True)