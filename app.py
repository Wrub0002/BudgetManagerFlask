from app import create_app, db

# Initialize the Flask app
app = create_app()

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # Run the app in debug mode for development
    app.run(debug=True)
