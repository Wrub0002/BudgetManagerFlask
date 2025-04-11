from db import db
from app import app
from models import Expense, Income

with app.app_context():
    db.create_all()
    print("✅ Database and tables created.")