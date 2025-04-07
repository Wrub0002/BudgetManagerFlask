
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        date = request.form["date"]
        description = request.form["description"]
        amount = request.form["amount"]

        with open("expenses.txt", "a") as file:
            file.write(f"{date} | {description} | {amount}$\n")

        return "✅ Expense added successfully!"

    return render_template("add.html")

@app.route("/expenses")
def show_expenses():
    with open("expenses.txt", "r") as file:
        expenses = [line.strip() for line in file.readlines()]
        return render_template("expenses.html", expenses = expenses)


app.run(debug=True)