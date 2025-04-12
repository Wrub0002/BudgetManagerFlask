from app import create_app, db
from app.routes import routes

app = create_app()
app.register_blueprint(routes)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
