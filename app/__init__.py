from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy extension (database object)
db = SQLAlchemy()

# Create a Flask app instance
def create_app():
    """
       Application factory function.

       Creates and configures the Flask application instance.
       """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    return app



